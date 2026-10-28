import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "survey.db"

with sqlite3.connect(DB_PATH) as connection:
    existing = {
        row[1]
        for row in connection.execute("PRAGMA table_info(research_projects)")
    }

    if "research_plan" not in existing:
        connection.execute(
            "ALTER TABLE research_projects ADD COLUMN research_plan JSON"
        )

print("Research plan migration completed.")
