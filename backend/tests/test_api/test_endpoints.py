from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import MarketDataError

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["name"] == "Finnie AI"


def test_market_quote_success():
    with patch("app.api.routes.market.get_market_data_service") as mock_svc:
        instance = MagicMock()
        instance.get_quote.return_value = {
            "ticker": "AAPL", "price": 190.0, "change": 1.0, "change_percent": 0.5,
            "volume": 1000000, "market_cap": 3e12, "pe_ratio": 28.0,
            "day_high": 191.0, "day_low": 189.0,
            "timestamp": "2024-01-01T00:00:00",
        }
        mock_svc.return_value = instance
        r = client.get("/market/quote/AAPL")
        assert r.status_code == 200


def test_market_quote_error():
    with patch("app.api.routes.market.get_market_data_service") as mock_svc:
        instance = MagicMock()
        instance.get_quote.side_effect = MarketDataError("bad ticker")
        mock_svc.return_value = instance
        r = client.get("/market/quote/BAD")
        assert r.status_code == 502


def test_market_history():
    with patch("app.api.routes.market.get_market_data_service") as mock_svc:
        instance = MagicMock()
        instance.get_history.return_value = [{"date": "2024-01-01", "close": 100}]
        mock_svc.return_value = instance
        r = client.get("/market/history/AAPL?period=1mo&interval=1d")
        assert r.status_code == 200
        assert r.json()["ticker"] == "AAPL"


def test_market_history_error():
    with patch("app.api.routes.market.get_market_data_service") as mock_svc:
        instance = MagicMock()
        instance.get_history.side_effect = MarketDataError("fail")
        mock_svc.return_value = instance
        r = client.get("/market/history/BAD")
        assert r.status_code == 502


def test_market_search():
    with patch("app.api.routes.market.get_market_data_service") as mock_svc:
        instance = MagicMock()
        instance.search_symbol.return_value = [{"symbol": "AAPL", "name": "Apple"}]
        mock_svc.return_value = instance
        r = client.get("/market/search?q=apple")
        assert r.status_code == 200
        assert len(r.json()["results"]) == 1


def test_portfolio_analyze_success():
    with patch("app.api.routes.portfolio.compute_metrics") as mock_cm:
        mock_cm.return_value = {
            "total_value": 10000.0, "total_cost": 9000.0, "total_return_pct": 11.11,
            "allocations": {"AAPL": 100.0},
            "metrics": {"sharpe_ratio": 1.2, "annualized_return_pct": 12.0},
            "recommendations": ["Diversify more"],
        }
        r = client.post("/portfolio/analyze", json={
            "holdings": [{"ticker": "AAPL", "quantity": 10, "avg_cost": 150}],
        })
        assert r.status_code == 200
        assert r.json()["total_value"] == 10000.0


def test_portfolio_analyze_market_error():
    with patch("app.api.routes.portfolio.compute_metrics", side_effect=MarketDataError("no data")):
        r = client.post("/portfolio/analyze", json={
            "holdings": [{"ticker": "BAD", "quantity": 1, "avg_cost": 10}],
        })
        assert r.status_code == 502


def test_portfolio_analyze_value_error():
    with patch("app.api.routes.portfolio.compute_metrics", side_effect=ValueError("empty")):
        r = client.post("/portfolio/analyze", json={
            "holdings": [{"ticker": "AAPL", "quantity": 1, "avg_cost": 10}],
        })
        assert r.status_code == 400