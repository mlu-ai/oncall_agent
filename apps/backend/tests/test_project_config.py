from __future__ import annotations

import json
from pathlib import Path

import pytest

from super_ai.project_config import load_project_config


def test_load_project_config_recursively_merges_user_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "project.json").write_text(
        json.dumps(
            {
                "frontend": {"title": "基础", "analytics": {"publicKey": "a"}},
                "llm": {"apiKey": "x"},
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "user.project.json").write_text(
        json.dumps({"frontend": {"title": "本机"}}), encoding="utf-8"
    )
    monkeypatch.setenv("PROJECT_CONFIG", "must-not-be-read")

    config = load_project_config(tmp_path)

    assert config["frontend"] == {"title": "本机", "analytics": {"publicKey": "a"}}
    assert config["llm"] == {"apiKey": "x"}
