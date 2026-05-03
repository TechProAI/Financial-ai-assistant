from unittest.mock import patch, MagicMock
import pandas as pd
from app.services.market_data import MarketDataService


def test_get_quote_caches(monkeypatch):
    svc = MarketDataService()
    fake_hist = pd.DataFrame(
        {"Close": [100, 102], "High": [103, 104], "Low": [99, 101], "Volume": [1000, 1100]},
        index=pd.date_range("2024-01-01", periods=2),
    )
    with patch("app.services.market_data.yf.Ticker") as mock_ticker:
        instance = MagicMock()
        instance.info = {"previousClose": 100, "marketCap": 1e12, "trailingPE": 20.0, "longName": "Test Co"}
        instance.history.return_value = fake_hist
        mock_ticker.return_value = instance

        q1 = svc.get_quote("AAPL")
        q2 = svc.get_quote("AAPL")  # should hit cache
        assert q1 == q2
        assert mock_ticker.call_count == 1