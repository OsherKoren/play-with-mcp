# Expense Tracker MCP Server

This MCP (Model Context Protocol) server lets AI assistants (like **Claude Desktop**) access expense data from your local SQLite database and answer questions like:

- “What were my total expenses in October?”
- “How much did I spend on food last month?”
- “Which category had the highest spending overall?”

---


## 1. Install Dependencies

Make sure you have **Python 3.13+**.

```bash
  poetry add fastmcp loguru
```
# or
```bash
  uv add fastmcp loguru
```

## 2. Create Demo Expenses

Generate a small SQLite database for testing (3 months of sample expenses):

```py
python ./setup_db.py
```
This creates:
expense_tracker/resources/expenses.db


## 3. Run the MCP Server Locally

```bash
  PYTHONPATH=. uv run --with fastmcp fastmcp run expense_tracker/tst_server.py
```

You should see logs like:
```
2025-10-12 15:46:13 | INFO     | expense_tracker_mcp_server.lifespan:mcp_lifespan:17 - 🚀 Starting up the MCP server...
```

## 4. Connect with Claude Desktop
1. Configure Claude Desktop to connect to your local MCP server:
```bash
  fastmcp install claude-desktop ./expense_tracker/tst_server.py
```

You should see logs like:
```
Successfully installed 'server' in Claude Desktop
```

On Windows you can find the generated claude_desktop_config.json here:
```
C:\Users\oshra\AppData\Roaming\Claude
```

1. Open **Claude Desktop**.
2. Go to **Settings** > **MCP Servers**.
3. Add a new server:
4. Name: `Expense Tracker`
   URL: `http://localhost:8000/mcp`
