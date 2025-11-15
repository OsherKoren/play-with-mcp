import asyncio
import runpy
from types import SimpleNamespace

import pytest

from expense_tracker.db import connection
from expense_tracker.lifespan import mcp_lifespan
from expense_tracker.resources.io import read_json_resource
from expense_tracker.tools import queries


class DummyConn:
    def __init__(self):
        self.closed = False

    async def close(self):
        self.closed = True


class AsyncContextConn:
    def __init__(self, total_value=0.0):
        self.total_value = total_value

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    @property
    def row_factory(self):
        return None

    @row_factory.setter
    def row_factory(self, v):
        pass

    async def execute(self, sql, params=None):
        class Cursor:
            def __init__(self, val):
                self._val = val

            async def fetchone(self):
                return {"total": self._val}

        return Cursor(self.total_value)


def test_shutdown_database_noop_and_close(monkeypatch):
    # Ensure shutdown is noop when conn is None
    connection.conn = None
    asyncio.run(connection.shutdown_database())  # should do nothing

    # Now set a dummy conn and ensure shutdown closes it and sets to None
    dummy = DummyConn()
    connection.conn = dummy
    asyncio.run(connection.shutdown_database())
    assert connection.conn is None
    assert dummy.closed


def test_start_and_shutdown_database_monkeypatched(monkeypatch):
    # Monkeypatch aiosqlite.connect to return DummyConn
    async def fake_connect(path):
        return DummyConn()

    import aiosqlite

    monkeypatch.setattr(aiosqlite, "connect", fake_connect)

    # Call start_database and ensure connection.conn is set
    asyncio.run(connection.start_database())
    assert connection.conn is not None
    # Clean up
    asyncio.run(connection.shutdown_database())
    assert connection.conn is None


def test_lifespan_uses_start_and_shutdown(monkeypatch):
    called = SimpleNamespace(start=False, shutdown=False)

    async def fake_start():
        called.start = True

    async def fake_shutdown():
        called.shutdown = True

    monkeypatch.setattr(connection, "start_database", fake_start)
    monkeypatch.setattr(connection, "shutdown_database", fake_shutdown)

    async def run_ctx():
        async with mcp_lifespan(None):
            assert called.start is True

    asyncio.run(run_ctx())
    # after context, shutdown should have been called
    assert called.shutdown is True


def test_queries_fallback_to_fake_conn(monkeypatch):
    # Provide a fake async connection that returns a known total
    fake = AsyncContextConn(total_value=123.45)
    monkeypatch.setattr(connection, "conn", fake)

    total = asyncio.run(queries.select_total_expenses_for_month(8))
    assert float(total) == 123.45

    total_cat = asyncio.run(
        queries.select_total_expenses_for_month_and_category(8, "Food")
    )
    assert float(total_cat) == 123.45


def test_main_executes_run_with_patched_mcp(monkeypatch):
    # Patch the mcp.run function on the server module to avoid starting a server
    import expense_tracker.server as srv

    called = {}

    def fake_run(transport=None, port=None):
        called["ran"] = True
        called["transport"] = transport
        called["port"] = port

    monkeypatch.setattr(srv.mcp, "run", fake_run)

    # run the module as __main__ to execute the guarded block
    runpy.run_module("expense_tracker.main", run_name="__main__")
    assert called.get("ran") is True


def test_read_json_resource_exists():
    # basic sanity check that the report file can be read
    data = read_json_resource("monthly_expenses_report.json")
    assert isinstance(data, dict)
    assert "report_name" in data
