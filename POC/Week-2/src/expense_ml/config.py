import json
from pathlib import Path
from typing import Any

from .paths import CONFIG_DIR


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_project_config() -> dict[str, Any]:
    return load_json(CONFIG_DIR / "project_config.json")


def load_contract() -> dict[str, Any]:
    return load_json(CONFIG_DIR / "data_contract.json")
