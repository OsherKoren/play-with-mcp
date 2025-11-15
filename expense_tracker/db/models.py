# !/usr/bin/env python


"""Database tables models"""

from pydantic import BaseModel


class Expense(BaseModel):
    """Expense model."""

    id: int
    date: str
    category: str
    description: str
    amount: float
