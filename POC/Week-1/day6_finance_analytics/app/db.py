from __future__ import annotations

import sqlite3
from datetime import date, datetime

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base


class Database:
    def __init__(self, database_url: str) -> None:
        if database_url.startswith("sqlite"):
            sqlite3.register_adapter(date, lambda value: value.isoformat())
            sqlite3.register_adapter(datetime, lambda value: value.isoformat())
            connect_args = {"check_same_thread": False}
        else:
            connect_args = {}
        self.engine: Engine = create_engine(
            database_url,
            pool_pre_ping=True,
            connect_args=connect_args,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=Session,
            autoflush=False,
            expire_on_commit=False,
        )

    def create_schema(self) -> None:
        Base.metadata.create_all(self.engine)

    def ping(self) -> bool:
        with self.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True

    def dispose(self) -> None:
        self.engine.dispose()
