from unittest.mock import patch
import pandas as pd
import numpy as np
from app.services.portfolio_metrics import compute_metrics


def _fake_price_data(tickers, days=252):
    idx = pd.date_range("2023-01-01", periods=days)
    np.random.seed(42)
    data = {}
    for t in tickers:
        prices = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.015, days))
        df = pd.DataFrame({"Close": prices}, index=idx)
        data[t] = df
    return pd.concat(data, axis=1)


def test_compute_metrics_runs():
    holdings = [
        {"ticker": "AAPL", "quantity": 10, "avg_cost": 150},
        {"ticker": "MSFT", "quantity": 5, "avg_cost": 300},
    ]
    with patch("app.services.portfolio_metrics.yf.download") as mock_dl:
        mock_dl.return_value = _fake_price_data(["AAPL", "MSFT", "SPY"])
        result = compute_metrics(holdings)
        assert "total_value" in result
        assert "metrics" in result
        assert "sharpe_ratio" in result["metrics"]
        assert len(result["recommendations"]) > 0