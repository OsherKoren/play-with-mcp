"""expense_tracker.server

FastMCP server module for the expense tracker example.

This module exposes a FastMCP application instance (`mcp`) with two
resource endpoints and per-resource prompts. Each resource keeps its
original behavior and has a matching prompt generator and a small
"analysis" resource that demonstrates how to connect the query result
with a prompt for downstream AI analysis.
"""

import json
from pathlib import Path

from fastmcp import FastMCP
from pydantic import ValidationError

from expense_tracker.lifespan import mcp_lifespan
from expense_tracker.logger import log
from expense_tracker.prompts import templates
from expense_tracker.resources.io import read_json_resource
from expense_tracker.resources.models import MonthlyCategoriesReport
from expense_tracker.tools import queries

# https://www.youtube.com/watch?v=XXh-lrWTMeQ
# https://github.com/XamHans/mcp-course/blob/master/my_server.py


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


@mcp.prompt(
    name="summarize_top_expenses",
    description="Build a prompt that summarizes the month's expenses using the monthly_expenses_report resource.",
)
async def summarize_top_expenses_prompt() -> str:
    """Build a model prompt using the `monthly_expenses_report` resource.

    Returns:
        A full prompt string (system + user) ready to send to the model.
    """

    raw = read_json_resource("monthly_expenses_report.json")

    user_prompt = f"""Given monthly expenses report in the JSON below:

        === MONTHLY EXPENSES REPORT ===
            {raw}
        ========================

        extract the top three expenses.
        Return them as a numbered list including category and amount.
        Provide a brief insight summary at the end.

        Summarize and analyze the report and include:

        **Top Three Expenses:**
        Month: __________
        1. Category: __________, Amount: __________
        2. Category: __________, Amount: __________
        3. Category: __________, Amount: __________

        **Spending Trends:**
        - Identify any noticeable trends in spending across different months.
        - Highlight categories with significant increases or decreases.

    """
    return templates.build_prompt(user_prompt=user_prompt)


# -----------------------------------------------------
# Resources
# -----------------------------------------------------


@mcp.resource(
    uri="file:///resources//monthly_expenses_report.json",
    name="monthly_expenses_report",
    description="Monthly expenses report (all categories) in JSON format.",
    mime_type="application/json",
)
def get_monthly_expenses_report():
    """Load the monthly expenses report (all categories) from a packaged or local JSON file.

    Behavior:
    - Reads the file `expense_tracker/resources/monthly_expenses_report.json` next to this module.
    - Attempts to parse the loaded JSON into the configured Pydantic model; if parsing
      fails the raw dict is returned for backward compatibility.

    Returns:
        A Pydantic model instance when validation succeeds, otherwise the raw dict.
    """

    raw = read_json_resource("monthly_expenses_report.json")

    try:
        return MonthlyCategoriesReport.from_raw_dict(raw)
    except ValidationError as e:
        log.error(f"{e} . Returning raw data.")
        return raw
