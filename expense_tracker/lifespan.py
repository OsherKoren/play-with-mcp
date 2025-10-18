# !/usr/bin/env python

"""Lifespan events for the MCP server."""

from contextlib import asynccontextmanager

from fastmcp import FastMCP

from expense_tracker.logger import log
from expense_tracker.resources import connection


@asynccontextmanager
async def mcp_lifespan(mcp: FastMCP):
    """Lifespan events for the MCP server."""
    log.info("🚀 Starting up the MCP server...")
    await connection.start_database()
    try:
        yield
    finally:
        await connection.shutdown_database()
        log.info("🛑 Shutting down the MCP server...")
