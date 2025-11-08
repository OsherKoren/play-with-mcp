# !/usr/bin/env python

"""Templates for prompts used in the MCP server."""
from fastmcp.prompts.prompt import FunctionPrompt

SYSTEM_PROMPT = """
You are a helpful personal finance assistant for a bank's customers.
You can answer questions about their monthly expenses, spending by category,
and provide summaries or totals based on the expense records.
Use the available resources (APIs) to fetch accurate numbers.
Be polite, concise, and clear in your explanations.
"""


def build_prompt(user_prompt: str) -> str:
    """Return a combined prompt containing the system prompt followed by the user prompt.

    Args:
        user_prompt: the prompt text describing the specific task or question.

    Returns:
        A single string suitable to send to a model (system context + user prompt).
    """
    return SYSTEM_PROMPT.strip() + "\n\n" + user_prompt.strip()
