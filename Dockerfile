FROM python:3.13-slim

RUN pip install uv

WORKDIR /app

# Copy only the dependency files to leverage Docker layer caching
COPY pyproject.toml uv.lock* ./

# Freeze dependencies to ensure repeatable builds as the same environment as the local one, without auto upgrades.
RUN uv sync --frozen

COPY expense_tracker ./expense_tracker

ENV PYTHONPATH=.

EXPOSE 8000

#ENV MCP_TRANSPORT=streamable-http
#ENV MCP_HOST=0.0.0.0
#ENV MCP_PORT=8000

CMD ["uv", "run", "expense_tracker/main.py"]
