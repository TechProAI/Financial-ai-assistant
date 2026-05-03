"""Market data endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.schemas import QuoteResponse
from app.services.market_data import get_market_data_service
from app.core.exceptions import MarketDataError

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/quote/{ticker}", response_model=QuoteResponse)
def quote(ticker: str):
    try:
        return get_market_data_service().get_quote(ticker)
    except MarketDataError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/history/{ticker}")
def history(ticker: str, period: str = Query("1mo"), interval: str = Query("1d")):
    try:
        return {"ticker": ticker.upper(), "data": get_market_data_service().get_history(ticker, period, interval)}
    except MarketDataError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/search")
def search(q: str = Query(..., min_length=1)):
    return {"results": get_market_data_service().search_symbol(q)}