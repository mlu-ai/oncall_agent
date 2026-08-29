from __future__ import annotations

import json
from pathlib import Path
from subprocess import run

ROOT = Path(__file__).resolve().parents[3]


def test_required_foundation_directories_and_ignore_rules_exist() -> None:
    for path in (
        "apps/backend",
        "apps/frontend",
        "packages/api-contracts",
        "config",
        "infra",
        "scripts",
        "openspec",
        "docs",
    ):
        assert (ROOT / path).is_dir()

    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for entry in (
        "config/project.json",
        "config/user.project.json",
        ".env*",
        ".idea/",
        ".venv/",
        "node_modules/",
        "dist/",
        "coverage/",
        "docs/.vitepress/cache/",
        "docs/.vitepress/dist/",
        "apps/backend/var/",
        "*.sqlite",
        "*.log",
    ):
        assert entry in ignored


def test_no_application_compose_or_image_files_exist() -> None:
    assert not (ROOT / "project.compose.json").exists()
    assert not list(ROOT.rglob("app.Dockerfile"))


def test_workspace_scripts_and_local_configuration_boundary_exist() -> None:
    root_package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    for script_name in (
        "contracts:typecheck",
        "contracts:test",
        "frontend:dev",
        "frontend:typecheck",
        "frontend:test",
        "frontend:build",
        "docs:build",
    ):
        assert script_name in root_package["scripts"]

    result = run(
        ["git", "check-ignore", "config/project.json", "config/user.project.json"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_project_guides_record_host_and_compose_boundaries() -> None:
    guidance = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    infrastructure = (ROOT / "infra/README.md").read_text(encoding="utf-8")
    for service in ("etcd", "MinIO", "Milvus", "Attu", "Alertmanager"):
        assert service in guidance
        assert service in infrastructure
    assert "主机运行" in guidance
