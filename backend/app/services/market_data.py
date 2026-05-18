"""Market data service using yfinance with in-memory TTL caching."""
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import yfinance as yf
import pandas as pd
from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import MarketDataError

logger = get_logger(__name__)


def _make_session():
    """Create a browser-impersonating session that bypasses Yahoo's scraping defenses."""
    try:
        from curl_cffi import requests as curl_requests
        session = curl_requests.Session(impersonate="chrome")
        session.timeout = 10  # 10 second timeout instead of default 30+
        return session
    except ImportError:
        logger.warning("curl_cffi not installed; yfinance may be rate-limited")
        return None


class _TTLCache:
    def __init__(self, ttl: int):
        self.ttl = ttl
        self._store: Dict[str, tuple] = {}

    def get(self, key: str):
        v = self._store.get(key)
        if not v:
            return None
        value, ts = v
        if time.time() - ts > self.ttl:
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value):
        self._store[key] = (value, time.time())


class MarketDataService:
    """yfinance wrapper with caching and error handling."""

    def __init__(self):
        self._cache = _TTLCache(settings.MARKET_CACHE_TTL_SECONDS)
        self._session = _make_session()

    def _ticker(self, symbol: str) -> yf.Ticker:
        return yf.Ticker(symbol, session=self._session) if self._session else yf.Ticker(symbol)

    def get_quote(self, ticker: str) -> Dict[str, Any]:
        """Fetch current quote snapshot for a ticker. Auto-resolves Indian company names."""
        ticker = ticker.upper().strip()
        cached = self._cache.get(f"quote:{ticker}")
        if cached:
            return cached

        # Try the ticker as-is first, then with .NS suffix for Indian stocks
        tickers_to_try = [ticker]
        if "." not in ticker and not ticker.startswith("^"):
            tickers_to_try.append(f"{ticker}.NS")

        last_error = None
        for try_ticker in tickers_to_try:
            try:
                quote = self._fetch_quote(try_ticker)
                self._cache.set(f"quote:{ticker}", quote)
                # Also cache under the resolved ticker
                if try_ticker != ticker:
                    self._cache.set(f"quote:{try_ticker}", quote)
                return quote
            except MarketDataError as e:
                last_error = e
                continue

        raise last_error or MarketDataError(f"No data for ticker {ticker}")

    def _fetch_quote(self, ticker: str) -> Dict[str, Any]:
        """Fetch one quote variant. Primary data from t.history() (works even when
        Yahoo rate-limits t.info). Optional enrichment from t.info — wrapped in
        try/except so a blocked info call doesn't kill the whole quote."""
        try:
            t = self._ticker(ticker)

            # PRIMARY: history endpoint — not crumb-protected, works on cloud IPs
            hist = t.history(period="5d")
            if hist is None or (isinstance(hist, pd.DataFrame) and hist.empty):
                raise MarketDataError(f"No historical data available for {ticker}")

            latest = hist.iloc[-1]
            prev_close = float(hist.iloc[-2]["Close"]) if len(hist) > 1 else float(latest["Close"])
            price = float(latest["Close"])
            change = price - prev_close
            change_pct = (change / prev_close * 100) if prev_close else 0.0

            currency = "INR" if ticker.endswith((".NS", ".BO")) else "USD"

            # OPTIONAL: info enrichment — try, but never fail because of it
            company_name = ticker
            market_cap = None
            pe_ratio = None
            sector = None
            try:
                info = t.info or {}
                company_name = info.get("longName") or info.get("shortName") or ticker
                market_cap = info.get("marketCap")
                pe_ratio = info.get("trailingPE")
                sector = info.get("sector")
                currency = info.get("currency", currency)
            except Exception as e:
                logger.info("info_enrichment_skipped", ticker=ticker, reason=str(e))

            return {
                "ticker": ticker,
                "price": round(price, 2),
                "change": round(change, 2),
                "change_percent": round(change_pct, 2),
                "volume": int(latest.get("Volume", 0)),
                "market_cap": market_cap,
                "pe_ratio": pe_ratio,
                "day_high": round(float(latest.get("High", price)), 2),
                "day_low": round(float(latest.get("Low", price)), 2),
                "company_name": company_name,
                "sector": sector,
                "currency": currency,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except MarketDataError:
            raise
        except Exception as e:
            logger.error("quote_fetch_error", ticker=ticker, error=str(e), exc_info=True)
            raise MarketDataError(f"Failed to fetch quote for {ticker}: {e}") from e

    def get_history(self, ticker: str, period: str = "1mo", interval: str = "1d") -> List[Dict[str, Any]]:
        """Fetch historical OHLC data. Auto-resolves Indian tickers."""
        ticker = ticker.upper().strip()
        cache_key = f"hist:{ticker}:{period}:{interval}"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        tickers_to_try = [ticker]
        if "." not in ticker and not ticker.startswith("^"):
            tickers_to_try.append(f"{ticker}.NS")

        last_error = None
        for try_ticker in tickers_to_try:
            try:
                hist = self._ticker(try_ticker).history(period=period, interval=interval)
                if hist.empty:
                    raise MarketDataError(f"No historical data for {try_ticker}")

                records = [
                    {
                        "date": idx.isoformat(),
                        "open": round(float(row["Open"]), 2),
                        "high": round(float(row["High"]), 2),
                        "low": round(float(row["Low"]), 2),
                        "close": round(float(row["Close"]), 2),
                        "volume": int(row["Volume"]),
                    }
                    for idx, row in hist.iterrows()
                ]
                self._cache.set(cache_key, records)
                return records
            except MarketDataError as e:
                last_error = e
                continue

        raise last_error or MarketDataError(f"No historical data for {ticker}")

    def get_multiple_quotes(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        out: Dict[str, Dict[str, Any]] = {}
        for t in tickers:
            try:
                out[t.upper()] = self.get_quote(t)
            except MarketDataError as e:
                logger.warning("skipping_ticker", ticker=t, error=str(e))
        return out

    def search_symbol(self, query: str) -> List[Dict[str, str]]:
        try:
            result = yf.Lookup(query).get_stock(count=5)
            if result is None or result.empty:
                return []
            return [{"symbol": idx, "name": row.get("shortName", "")} for idx, row in result.iterrows()]
        except Exception as e:
            logger.warning("symbol_search_failed", query=query, error=str(e))
            return []


_market: Optional[MarketDataService] = None


def get_market_data_service() -> MarketDataService:
    global _market
    if _market is None:
        _market = MarketDataService()
    return _market