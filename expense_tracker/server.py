"""expense_tracker.server

FastMCP server module for the expense tracker example.

This module exposes a FastMCP application instance (`mcp`) with two
resource endpoints and per-resource prompts. Each resource keeps its
original behavior and has a matching prompt generator and a small
"analysis" resource that demonstrates how to connect the query result
with a prompt for downstream AI analysis.
"""

from fastmcp import FastMCP

from expense_tracker.lifespan import mcp_lifespan
from expense_tracker.prompts.templates import build_prompt
from expense_tracker.resources import queries

mcp = FastMCP(
    name="expense_tracker",
    lifespan=mcp_lifespan,
)


# -----------------------------------------------------
# Query Tools
# -----------------------------------------------------


@mcp.tool()
async def get_total_expenses_for_month(month: int):
    """Return total expenses for the given month from the SQLite database."""
    return await queries.select_total_expenses_for_month(month)


@mcp.tool()
async def get_total_expenses_for_month_and_category(month: int, category: str):
    """Return total expenses for the given month and category from the SQLite database."""
    return await queries.select_total_expenses_for_month_and_category(month, category)


# -----------------------------------------------------
# Prompt Builders
# -----------------------------------------------------


@mcp.prompt()
def prompt_total_for_month(month: int) -> str:
    """Generate a prompt asking the AI to analyze the total expenses for a month."""

    month_str = f"{month:02d}"
    return (
        f"You are given the total expenses for month {month_str}. "
        f"Provide an analytical analysis: summarize the total, compare to typical ranges, "
        "highlight possible causes and give 2-3 actionable suggestions."
    )


@mcp.prompt()
def prompt_total_for_month_and_category(month: int, category: str) -> str:
    """Generate a prompt asking the AI to analyze the total expenses for a month and category."""
    month_str = f"{month:02d}"
    return (
        f"You are given the total expenses for category '{category}' in month {month_str}. "
        f"Provide an analytical analysis: explain whether this spending is expected, "
        "identify trends or anomalies within the category, and suggest ways to optimize."
    )


# -----------------------------------------------------
# Analysis Tools
# -----------------------------------------------------


@mcp.tool()
async def analyze_total_for_month(month: int):
    """Combine database query and prompt generation for a month-wide analysis."""

    total = await queries.select_total_expenses_for_month(month)
    user_prompt = prompt_total_for_month(month)
    full_prompt = build_prompt(user_prompt)
    return f"Month {month:02d} total: {total}"


@mcp.tool()
async def analyze_total_for_month_and_category(month: int, category: str):
    """Combine query and prompt generation for a month+category analysis."""
    total = await queries.select_total_expenses_for_month_and_category(month, category)
    user_prompt = prompt_total_for_month_and_category(month, category)
    full_prompt = build_prompt(user_prompt)
    return f"Month {month:02d}, category: {category}, total: {total}"


# --- Backwards-compatible general prompt (kept for convenience) ---

# @mcp.prompt()
# def analyze_expenses_prompt() -> str:
#     """
#     General prompt instructing the AI to analyze total expenses by category.
#     """
#     return (
#         "Please provide an analysis of total expenses by category "
#         "for all available months. Highlight which categories have "
#         "the highest spending and any patterns."
#     )


# -----------------------------------------------------
# (Optional) Static Resources
# -----------------------------------------------------


@mcp.resource("expenses://metadata")
def get_metadata():
    """Optional example of a static resource."""
    return {
        "name": "Expense Tracker",
        "description": "MCP toolset for analyzing expense data by month and category.",
        "version": "1.0.0",
    }
