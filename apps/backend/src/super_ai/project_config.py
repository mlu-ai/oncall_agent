"""本地项目 JSON 配置加载，不读取操作系统环境变量。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeAlias, cast

JsonValue: TypeAlias = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


def _read_json_object(path: Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        message = f"配置文件必须是 JSON 对象：{path}"
        raise ValueError(message)
    return cast(JsonObject, value)


def deep_merge(base: JsonObject, override: JsonObject) -> JsonObject:
    """返回不修改输入值的递归深合并结果。"""
    merged = dict(base)
    for key, override_value in override.items():
        base_value = merged.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = deep_merge(base_value, override_value)
        else:
            merged[key] = override_value
    return merged


def _default_config_dir() -> Path:
    return Path(__file__).resolve().parents[4] / "config"


def load_project_config(config_dir: Path | None = None) -> JsonObject:
    """读取 project.json，并在存在时以 user.project.json 深合并覆盖。"""
    directory = config_dir if config_dir is not None else _default_config_dir()
    project_config = _read_json_object(directory / "project.json")
    user_path = directory / "user.project.json"
    if not user_path.exists():
        return project_config
    return deep_merge(project_config, _read_json_object(user_path))
