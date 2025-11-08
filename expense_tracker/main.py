# !/usr/bin/env python

"""Main entry point for the expense tracker MCP server."""

import os

from expense_tracker.server import mcp

if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")

    if transport == "http":
        mcp.run(transport="http", port=8000)
    else:
        mcp.run()
