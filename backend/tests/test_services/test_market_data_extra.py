from unittest.mock import patch, MagicMock
import pandas as pd
import pytest
from app.services.market_data import MarketDataService
from app.core.exceptions import MarketDataError


def test_get_quote_empty_history_raises():
    svc = MarketDataService()
    with patch("app.services.market_data.yf.Ticker") as mock_ticker:
        instance = MagicMock()
        instance.info = {}
        instance.history.return_value = pd.DataFrame()
        mock_ticker.return_value = instance
        with pytest.raises(MarketDataError):
            svc.get_quote("BADTICK")


def test_get_history_success():
    svc = MarketDataService()
    fake_hist = pd.DataFrame(
        {"Open": [100, 101], "High": [102, 103], "Low": [99, 100],
         "Close": [101, 102], "Volume": [1000, 2000]},
        index=pd.date_range("2024-01-01", periods=2),
    )
    with patch("app.services.market_data.yf.Ticker") as mock_ticker:
        instance = MagicMock()
        instance.history.return_value = fake_hist
        mock_ticker.return_value = instance
        result = svc.get_history("AAPL", period="5d", interval="1d")
        assert len(result) == 2
        assert result[0]["close"] == 101


def test_get_history_empty_raises():
    svc = MarketDataService()
    with patch("app.services.market_data.yf.Ticker") as mock_ticker:
        instance = MagicMock()
        instance.history.return_value = pd.DataFrame()
        mock_ticker.return_value = instance
        with pytest.raises(MarketDataError):
            svc.get_history("BADTICK")


def test_get_multiple_quotes_skips_failures():
    svc = MarketDataService()
    with patch.object(svc, "get_quote") as mock_q:
        mock_q.side_effect = [
            {"ticker": "AAPL", "price": 100},
            MarketDataError("no data"),
        ]
        result = svc.get_multiple_quotes(["AAPL", "BAD"])
        assert "AAPL" in result
        assert "BAD" not in result


def test_search_symbol_handles_failure():
    svc = MarketDataService()
    # yf.Lookup may not exist in all yfinance versions — patch at the yf module level safely
    import yfinance as yf
    with patch.object(yf, "Lookup", create=True, side_effect=RuntimeError("fail")):
        result = svc.search_symbol("apple")
        assert result == []


def test_market_singleton():
    from app.services import market_data
    market_data._market = None
    a = market_data.get_market_data_service()
    b = market_data.get_market_data_service()
    assert a is b