# Finnie AI — Backend

Production-grade multi-agent AI finance assistant built with LangGraph, OpenAI, Pinecone, and FastAPI.

## Architecture
6 specialized agents orchestrated by LangGraph:
1. **Supervisor** — intent classification and routing
2. **Education** — RAG-based financial literacy
3. **Market Intelligence** — real-time quotes and fundamentals
4. **Portfolio Analysis** — risk/return metrics
5. **News & Sentiment** — market news with sentiment scoring
6. **Compliance** — disclaimers and risky-language filtering

Plus an MCP server exposing Finnie tools to any MCP client.

## Setup
1. Create and activate a virtual env.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in keys.
4. `python -m scripts.ingest_kb` (once) to populate Pinecone.
5. `uvicorn app.main:app --reload` to run the API.
6. `pytest` to run tests.

## Endpoints
- `GET /health` — health check
- `POST /chat` — main conversational endpoint
- `POST /portfolio/analyze` — portfolio metrics
- `GET /market/quote/{ticker}` — stock quote
- `GET /market/history/{ticker}` — historical data
- `GET /market/search?q=...` — symbol search

Docs available at `http://localhost:8000/docs`.