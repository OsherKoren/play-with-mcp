"""expense_tracker.server

FastMCP server module for the expense tracker example.

This module exposes a FastMCP application instance (`mcp`) with two
resource endpoints and a prompt:

- expenses://total_for_month/{month} -> get_total_expenses_for_month
- expenses://total_for_month_and_category/{month}/{category} ->
    get_total_expenses_for_month_and_category
- analyze_expenses_prompt -> general analysis prompt for the AI

Import `mcp` from this module to register the resources with an MCP runner.
"""

# https://github.com/modelcontextprotocol/python-sdk/tree/main


from fastmcp import FastMCP

from expense_tracker.lifespan import mcp_lifespan
from expense_tracker.resources import queries

mcp = FastMCP(
    name="expense_tracker",
    lifespan=mcp_lifespan,
)


@mcp.resource("expenses://total_for_month/{month}")
async def get_total_expenses_for_month(month: int):
    """Return total expenses for the given month from the SQLite database."""
    return await queries.select_total_expenses_for_month(month)


@mcp.resource("expenses://total_for_month_and_category/{month}/{category}")
async def get_total_expenses_for_month_and_category(month: int, category: str):
    """Return total expenses for the given month and category from the SQLite database."""
    return await queries.select_total_expenses_for_month_and_category(month, category)


@mcp.prompt()
def analyze_expenses_prompt() -> str:
    """
    General prompt instructing the AI to analyze total expenses by category.
    """
    return (
        "Please provide an analysis of total expenses by category "
        "for all available months. Highlight which categories have "
        "the highest spending and any patterns."
    )
