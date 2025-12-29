from pathlib import Path
from sqlmodel import SQLModel, create_engine

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Single, fixed SQLite DB file
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")

# SQLite engine
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=True,
    connect_args={"check_same_thread": False},  # required for FastAPI
)

def create_tables() -> None:
    SQLModel.metadata.create_all(engine)