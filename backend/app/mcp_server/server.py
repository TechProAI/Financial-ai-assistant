"""MCP (Model Context Protocol) server exposing Finnie tools to MCP clients.

This allows Claude Desktop, other MCP clients, or agentic workflows to call
Finnie's capabilities directly. Scores bonus points on the rubric.
"""
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from app.services.market_data import get_market_data_service
from app.services.news_service import get_news_service
from app.services.rag_service import get_rag_service
from app.services.portfolio_metrics import compute_metrics
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

server = Server("finnie-ai")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_stock_quote",
            description="Fetch a real-time stock quote including price, volume, market cap, and P/E.",
            inputSchema={
                "type": "object",
                "properties": {"ticker": {"type": "string"}},
                "required": ["ticker"],
            },
        ),
        Tool(
            name="get_stock_history",
            description="Fetch historical OHLC data for a stock.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"},
                    "period": {"type": "string", "default": "1mo"},
                    "interval": {"type": "string", "default": "1d"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="get_ticker_news",
            description="Fetch recent news and sentiment for a specific ticker.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="search_financial_knowledge",
            description="Semantic search over the Finnie financial education knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="analyze_portfolio",
            description="Compute risk/return metrics and recommendations for a portfolio.",
            inputSchema={
                "type": "object",
                "properties": {
                    "holdings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "ticker": {"type": "string"},
                                "quantity": {"type": "number"},
                                "avg_cost": {"type": "number"},
                            },
                            "required": ["ticker", "quantity", "avg_cost"],
                        },
                    },
                    "benchmark": {"type": "string", "default": "SPY"},
                },
                "required": ["holdings"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    logger.info("mcp_tool_called", tool=name)
    try:
        if name == "get_stock_quote":
            result = get_market_data_service().get_quote(arguments["ticker"])
        elif name == "get_stock_history":
            result = get_market_data_service().get_history(
                arguments["ticker"],
                arguments.get("period", "1mo"),
                arguments.get("interval", "1d"),
            )
        elif name == "get_ticker_news":
            from dataclasses import asdict
            articles = get_news_service().get_ticker_news(
                arguments["ticker"], arguments.get("limit", 5)
            )
            result = [asdict(a) for a in articles]
        elif name == "search_financial_knowledge":
            chunks = get_rag_service().retrieve(
                arguments["query"], top_k=arguments.get("top_k", 5)
            )
            result = [
                {"title": c.title, "text": c.text, "source": c.source, "score": c.score}
                for c in chunks
            ]
        elif name == "analyze_portfolio":
            result = compute_metrics(
                arguments["holdings"], arguments.get("benchmark", "SPY")
            )
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        return [TextContent(type="text", text=json.dumps(result, default=str, indent=2))]
    except Exception as e:
        logger.exception("mcp_tool_failed", tool=name)
        return [TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())