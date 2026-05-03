"""FastAPI application entrypoint."""
import os
from dotenv import load_dotenv

# Load .env into actual environment variables FIRST
# LangSmith reads from os.environ, not from Pydantic Settings
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestContextMiddleware
from app.api.routes import health, chat, portfolio, market
from app.api.routes import user_data
from app.graph.workflow import get_workflow

configure_logging()
logger = get_logger(__name__)




@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app_starting", env=settings.APP_ENV)
    get_workflow()
    logger.info("app_ready")
    yield
    logger.info("app_shutting_down")


app = FastAPI(
    title="Finnie AI",
    description="Multi-agent AI finance assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestContextMiddleware)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(portfolio.router)
app.include_router(market.router)
app.include_router(user_data.router)


@app.get("/")
def root():
    return {"name": "Finnie AI", "version": "1.0.0", "docs": "/docs"}