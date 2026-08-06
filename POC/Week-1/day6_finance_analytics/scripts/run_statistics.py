from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import Settings  # noqa: E402
from app.db import Database  # noqa: E402
from app.services.statistics import approval_amount_welch_test  # noqa: E402


def main() -> None:
    settings = Settings.from_env()
    database = Database(settings.database_url)
    with database.session_factory() as session:
        result = approval_amount_welch_test(session)
    database.dispose()
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
