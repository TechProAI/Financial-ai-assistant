"""Run the Finnie MCP server over stdio:
    python -m scripts.run_mcp
"""
import asyncio
from app.mcp_server.server import main

if __name__ == "__main__":
    asyncio.run(main())