"""Small utilities to read packaged/local resource files under expense_tracker/resources."""

import json
from pathlib import Path


def read_json_resource(filename: str):
    """Read a JSON file from the `expense_tracker/resources` directory.

    Args:
        filename: the filename under the resources directory, e.g. "monthly_expenses_report.json".

    Returns:
        The parsed JSON object (usually a dict).

    Raises:
        FileNotFoundError if the file doesn't exist.
        json.JSONDecodeError if the file isn't valid JSON.
    """
    base = Path(__file__).resolve().parent
    file_path = base / filename
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)
