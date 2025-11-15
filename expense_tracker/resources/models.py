from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel


class CategoryExpense(BaseModel):
    category: str
    total: str  # totals are stored as strings like "653.98"


class MonthBlock(BaseModel):
    total: str
    per_category: list[CategoryExpense]


class MonthlyCategoriesReport(BaseModel):
    report_name: str
    last_updated: str
    months: dict[str, MonthBlock]

    @classmethod
    def from_raw_dict(cls, data: dict) -> MonthlyCategoriesReport:
        """Builds the model from the raw JSON structure where month keys are at top-level.

        Expected raw shape:
        {
          "report_name": "monthly_top_categories",
          "last_updated": "2025-11-15",
          "2025-10": { "total": "...", "top_categories": [ ... ] },
          "2025-09": { ... }
        }
        """
        rd = dict(data)
        report_name = rd.pop("report_name")
        last_updated = rd.pop("last_updated")
        months = {}
        for k, v in rd.items():
            months[k] = MonthBlock.model_validate(v)
        return cls(report_name=report_name, last_updated=last_updated, months=months)
