"""Portfolio analysis endpoint."""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PortfolioAnalyzeRequest, PortfolioAnalyzeResponse
from app.services.portfolio_metrics import compute_metrics
from app.core.exceptions import MarketDataError
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.post("/analyze", response_model=PortfolioAnalyzeResponse)
def analyze(req: PortfolioAnalyzeRequest) -> PortfolioAnalyzeResponse:
    try:
        result = compute_metrics(
            holdings=[h.model_dump() for h in req.holdings],
            benchmark=req.benchmark,
        )
        return PortfolioAnalyzeResponse(**result)
    except MarketDataError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("portfolio_analysis_failed")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")