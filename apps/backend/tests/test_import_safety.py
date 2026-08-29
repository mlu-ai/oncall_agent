from __future__ import annotations

import importlib
import socket
import sqlite3
import sys
from typing import NoReturn

import pytest


def test_importing_application_does_not_connect_to_external_services(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_connection(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("模块导入期间不得连接 SQLite")

    monkeypatch.setattr(sqlite3, "connect", unexpected_connection)
    monkeypatch.setattr(socket, "create_connection", unexpected_connection)
    for module_name in list(sys.modules):
        if module_name == "super_ai" or module_name.startswith("super_ai."):
            del sys.modules[module_name]

    importlib.import_module("super_ai.app")
