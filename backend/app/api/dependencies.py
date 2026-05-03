"""Reusable FastAPI dependencies."""
from app.graph.workflow import get_workflow
from app.services.market_data import get_market_data_service
from app.services.news_service import get_news_service


def workflow_dep():
    return get_workflow()


def market_dep():
    return get_market_data_service()


def news_dep():
    return get_news_service()