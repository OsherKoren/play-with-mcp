# !/usr/bin/env python

"""Main entry point for the expense tracker MCP server."""

import os

from expense_tracker.server import mcp

if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))

    if transport == "http":
        mcp.run(transport="http", host=host, port=port, path="/mcp")
    else:
        mcp.run()
