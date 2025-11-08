"""expense_tracker.server

FastMCP server module for the expense tracker example.

This module exposes a FastMCP application instance (`mcp`) with two
resource endpoints and per-resource prompts. Each resource keeps its
original behavior and has a matching prompt generator and a small
"analysis" resource that demonstrates how to connect the query result
with a prompt for downstream AI analysis.
"""

# https://www.youtube.com/watch?v=XXh-lrWTMeQ
# https://github.com/XamHans/mcp-course/blob/master/my_server.py

from fastmcp import FastMCP

from expense_tracker.lifespan import mcp_lifespan
from expense_tracker.prompts import templates
from expense_tracker.tools import queries

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
    total = await queries.select_total_expenses_for_month(month)
    return {"month": month, "total": total}


@mcp.tool()
async def get_total_expenses_for_month_and_category(month: int, category: str):
    """Return total expenses for the given month and category from the SQLite database."""
    total = await queries.select_total_expenses_for_month_and_category(month, category)
    return {"month": month, "category": category, "total": total}


# -----------------------------------------------------
# Prompt Builders
# -----------------------------------------------------


@mcp.prompt(
    name="prompt_total_for_month",
    description="Generate a prompt asking the AI to get the total expenses for a month.",
)
async def prompt_total_for_month(month: int) -> str:
    """Generate a prompt asking the AI to get the total expenses for a month."""

    month_str = f"{month:02d}"
    user_prompt = (
        f"You are given the total expenses for month {month_str}. "
        f"Provide an analytical analysis: summarize the total, compare to typical ranges, "
        "highlight possible causes and give 2-3 actionable suggestions."
    )
    return templates.build_prompt(user_prompt=user_prompt)


@mcp.prompt(
    name="prompt_total_for_month_and_category",
    description="Generate a prompt asking the AI to get the total expenses for a month "
    "and category.",
)
async def prompt_total_for_month_and_category(month: int, category: str) -> str:
    """Generate a prompt asking the AI to get the total expenses for a month and category."""
    month_str = f"{month:02d}"
    user_prompt = (
        f"You are given the total expenses for category '{category}' in month {month_str}. "
        f"Provide an analytical analysis: explain whether this spending is expected, "
        "identify trends or anomalies within the category, and suggest ways to optimize."
    )
    return templates.build_prompt(user_prompt=user_prompt)


# -----------------------------------------------------
# Resources
# -----------------------------------------------------

# @mcp.resource(uri="file///resources//latest-report.json", description="Latest expense
# report in JSON format.")
# def get_latest_report():
#     """Get the latest expense report from the packaged resource or the local resources file.
#
#     Returns:
#         A dict parsed from latest_report.json.
#     """
#     res_name = "latest_report.json"
#     try:
#         with open_text("expense_tracker.resources", res_name) as f:
#             return json.load(f)
#     except FileNotFoundError:
#         # Fallback: read from file relative to this module (development mode)
#         base = Path(__file__).resolve().parent / "resources" / res_name
#         with open(base, "r", encoding="utf-8") as f:
#             return json.load(f)
