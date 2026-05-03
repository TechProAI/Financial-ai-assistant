"""Quantitative portfolio metrics: returns, volatility, Sharpe, beta, drawdown."""
from typing import List, Dict, Any
import numpy as np
import pandas as pd
import yfinance as yf
from app.core.logging import get_logger
from app.core.exceptions import MarketDataError

logger = get_logger(__name__)

RISK_FREE_RATE_ANNUAL = 0.045  # 4.5%, approximately a 3-month T-bill
TRADING_DAYS = 252


def compute_metrics(
    holdings: List[Dict[str, Any]],
    benchmark: str = "SPY",
    lookback: str = "1y",
) -> Dict[str, Any]:
    """Compute a comprehensive set of portfolio metrics.

    holdings: list of {"ticker": str, "quantity": float, "avg_cost": float}
    Returns dict with total_value, total_cost, metrics, allocations, recommendations.
    """
    if not holdings:
        raise ValueError("Empty holdings")

    tickers = [h["ticker"].upper() for h in holdings]
    all_tickers = list(set(tickers + [benchmark]))

    try:
        from curl_cffi import requests as curl_requests
        session = curl_requests.Session(impersonate="chrome")
    except ImportError:
        session = None

    try:
        data = yf.download(
            all_tickers,
            period=lookback,
            interval="1d",
            progress=False,
            auto_adjust=True,
            group_by="ticker",
            session=session,
        )
    except Exception as e:
        raise MarketDataError(f"Failed to download price history: {e}") from e

    # Build a clean close-price DataFrame across all tickers
    closes = pd.DataFrame()
    for t in all_tickers:
        try:
            closes[t] = data[t]["Close"] if len(all_tickers) > 1 else data["Close"]
        except Exception:
            logger.warning("missing_price_data", ticker=t)

    closes = closes.dropna(how="all").ffill().dropna()
    if closes.empty:
        raise MarketDataError("No usable price data for holdings")

    latest_prices = closes.iloc[-1]

    # --- Position-level values ---
    total_value, total_cost = 0.0, 0.0
    position_values: Dict[str, float] = {}
    for h in holdings:
        t = h["ticker"].upper()
        if t not in latest_prices.index:
            continue
        price = float(latest_prices[t])
        value = price * h["quantity"]
        cost = h["avg_cost"] * h["quantity"]
        total_value += value
        total_cost += cost
        position_values[t] = position_values.get(t, 0.0) + value

    if total_value == 0:
        raise MarketDataError("Portfolio value is zero — check tickers")

    allocations = {t: round(v / total_value * 100, 2) for t, v in position_values.items()}
    total_return_pct = ((total_value - total_cost) / total_cost * 100) if total_cost else 0.0

    # --- Portfolio daily returns (weighted) ---
    weights = pd.Series({t: v / total_value for t, v in position_values.items()})
    portfolio_tickers = [t for t in weights.index if t in closes.columns]
    portfolio_closes = closes[portfolio_tickers]
    daily_returns = portfolio_closes.pct_change().dropna()
    portfolio_returns = (daily_returns * weights[portfolio_tickers]).sum(axis=1)

    mean_daily = float(portfolio_returns.mean())
    std_daily = float(portfolio_returns.std())
    ann_return = mean_daily * TRADING_DAYS
    ann_vol = std_daily * np.sqrt(TRADING_DAYS)
    sharpe = (ann_return - RISK_FREE_RATE_ANNUAL) / ann_vol if ann_vol > 0 else 0.0

    # --- Beta vs benchmark ---
    beta = None
    if benchmark in closes.columns:
        bench_returns = closes[benchmark].pct_change().dropna()
        aligned = pd.concat([portfolio_returns, bench_returns], axis=1, join="inner").dropna()
        if len(aligned) > 10:
            cov = float(np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])[0, 1])
            var = float(np.var(aligned.iloc[:, 1]))
            beta = cov / var if var > 0 else None

    # --- Max drawdown ---
    cumulative = (1 + portfolio_returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = float(drawdown.min()) if not drawdown.empty else 0.0

    metrics = {
        "annualized_return_pct": round(ann_return * 100, 2),
        "annualized_volatility_pct": round(ann_vol * 100, 2),
        "sharpe_ratio": round(sharpe, 2),
        "beta": round(beta, 2) if beta is not None else None,
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "num_positions": len(position_values),
    }

    # --- Recommendations (simple rule-based) ---
    recs: List[str] = []
    if len(position_values) < 5:
        recs.append("Consider diversifying: holding fewer than 5 positions increases concentration risk.")
    top_weight = max(allocations.values()) if allocations else 0
    if top_weight > 40:
        top_ticker = max(allocations, key=allocations.get)
        recs.append(f"{top_ticker} represents {top_weight}% of your portfolio — consider rebalancing.")
    if metrics["annualized_volatility_pct"] > 30:
        recs.append("Portfolio volatility is high; consider adding lower-volatility assets like broad index ETFs.")
    if metrics["sharpe_ratio"] < 0.5:
        recs.append("Risk-adjusted return (Sharpe) is low; review holdings that underperform the benchmark.")
    if not recs:
        recs.append("Portfolio looks reasonably balanced. Continue monitoring and rebalance periodically.")

    return {
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
        "total_return_pct": round(total_return_pct, 2),
        "allocations": allocations,
        "metrics": metrics,
        "recommendations": recs,
    }