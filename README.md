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
python ./setup/01_generate_db.py
```
This creates:
`expense_tracker/db/expenses.db` with sample data in tbl_expenses.

## 3. Generate Demo Report

```py
python ./setup/02_generate_monthly_expenses_report.py
```
This creates:
`expense_tracker/resources/monthely_top_categories.json` report file.


## 4. Run the MCP Server Locally

```bash
  PYTHONPATH=. uv run --with fastmcp fastmcp run expense_tracker/server.py
```
Or using main.py module with http transport:
```bash
  MCP_TRANSPORT=http PYTHONPATH=. uv run expense_tracker/main.py
 ```

Or run main.py file directly from the IDE with the default stdio transport:
```python
if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")

    if transport == "http":
        mcp.run(transport="http", port=8000)
    else:
        mcp.run()
```

You should see logs like:
```
2025-10-12 15:46:13 | INFO     | expense_tracker_mcp_server.lifespan:mcp_lifespan:17 - 🚀 Starting up the MCP server...
```
Or when using http transport:
```
[10/25/25 13:06:35] INFO     Starting MCP server 'expense_tracker' with transport 'http' on http://127.0.0.1:8000/mcp                                                                                                 server.py:1579
INFO:     Started server process [26112]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
2025-10-25 13:11:14 | INFO     | expense_tracker.lifespan:mcp_lifespan:16 - 🚀 Starting up the MCP server...
```

## 5. Connect with Claude Desktop
5.1. Configure Claude Desktop to connect to your local MCP server:
```bash
  fastmcp install claude-desktop ./expense_tracker/server.py
```

You should see logs like:
```
Successfully installed 'server' in Claude Desktop
```

On Windows you can find the generated claude_desktop_config.json here:
```
C:\Users\myuser\AppData\Roaming\Claude
```

5.2. Open **Claude Desktop**.
5.3. Go to **Settings** > **MCP Servers**.
5.3. Add a new server:
5.4. Name: `Expense Tracker` URL: `http://localhost:8000/mcp`


## 6. Connecting via NPX (quick, no-install run)

You can run the official MCP Inspector directly with `npx` (this downloads and runs the Inspector package temporarily). This is the fastest way to open the Inspector UI and launch your MCP server from the same command.

Run in the terminal from your project root:

```bash
PYTHONPATH=. npx @modelcontextprotocol/inspector uv --directory /c/Users/myuser/PycharmProjects/play-with-mcp run expense_tracker/main.py
 ```

Notes:
When prompted "Ok to proceed? (y)" type `y` and press Enter

- `npx` will ask to download `@modelcontextprotocol/inspector` the first time. Answer `y` to proceed if you trust the package.

You should see the Inspector UI open in your default browser, and the MCP server starting up in the terminal.
```
$  PYTHONPATH=. npx @modelcontextprotocol/inspector uv --directory /c/Users/myuser/PycharmProjects/play-with-mcp run expense_tracker/main.py
Starting MCP inspector...
⚙️ Proxy server listening on localhost:6277
🔑 Session token: 0bbbc0439b41784d7284ed09aca5a904f19c1dd060dffa0a11c2268f6dc986db
   Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🚀 MCP Inspector is up and running at:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=0bbbc0439b41784d7284ed09aca5a904f19c1dd060dffa0a11c2268f6dc986db

🌐 Opening browser...
```
