"""Test expense_tracker MCP server resources and prompts."""

import asyncio
import inspect
import json

import pytest

from expense_tracker.resources.io import read_json_resource
from expense_tracker.resources.models import MonthlyCategoriesReport
from expense_tracker.server import build_summarize_prompt


def test_get_monthly_expenses_report_type():
    """Load the JSON report and verify it parses into the Pydantic model."""
    raw = read_json_resource("monthly_expenses_report.json")
    assert isinstance(raw, dict)
    assert "report_name" in raw and "last_updated" in raw

    model = MonthlyCategoriesReport.from_raw_dict(raw)
    assert isinstance(model, MonthlyCategoriesReport)


def test_summarize_prompt_returns_string():
    """The prompt builder should return a non-empty string prompt."""
    # Call the synchronous helper that builds the prompt to avoid wrapper indirection
    prompt = build_summarize_prompt()

    assert isinstance(prompt, str)
    assert prompt.strip()
    # sanity check: should contain task instructions we add
    assert "Task:" in prompt or "Top" in prompt


def test_report_contains_months_and_top_categories():
    """The generated JSON report should include month blocks with top_categories lists."""
    report = read_json_resource("monthly_expenses_report.json")
    assert isinstance(report, dict)
    # ensure metadata present
    assert "report_name" in report
    assert "last_updated" in report

    months = [k for k in report.keys() if k not in ("report_name", "last_updated")]
    assert months, "No months found in report"

    for m in months:
        block = report[m]
        assert "total" in block
        assert "per_category" in block or "top_categories" in block
        top = block.get("top_categories") or block.get("per_category")
        assert isinstance(top, list)
        for entry in top:
            assert "category" in entry
            assert "total" in entry
            float(entry["total"])  # will raise if invalid


def test_top_categories_sum_not_exceed_total():
    """For the latest month, the sum of top_categories totals should not exceed the reported total."""
    report = read_json_resource("monthly_expenses_report.json")
    months = [k for k in report.keys() if k not in ("report_name", "last_updated")]
    assert months
    latest = months[0]
    block = report[latest]
    total = float(block["total"])
    top_list = block.get("top_categories") or block.get("per_category") or []
    top_sum = sum(float(e["total"]) for e in top_list)
    assert top_sum <= total + 1e-6
