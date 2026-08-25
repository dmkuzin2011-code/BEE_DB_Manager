from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine


class DBAdapter(ABC):
    @abstractmethod
    async def connect(self, url: str) -> None: ...

    @abstractmethod
    async def execute(self, command: str) -> Any: ...

    @abstractmethod
    async def close(self) -> None: ...


class SQLAdapter(DBAdapter):
    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.conn: Optional[AsyncConnection] = None

    async def connect(self, url: str) -> None:
        self.engine = create_async_engine(url, echo=False)
        self.conn = await self.engine.connect()

    def is_in_transaction(self) -> bool:
        if self.conn is None:
            return False
        # in_transaction is a method in SQLAlchemy 2.x
        in_tx = self.conn.in_transaction
        return bool(in_tx() if callable(in_tx) else in_tx)

    async def execute(self, command: str) -> Any:
        if self.engine is None or self.conn is None:
            raise RuntimeError("No connection")

        clean_cmd = command.strip().rstrip(";").lower()

        if clean_cmd == "commit":
            await self.conn.commit()
            return {"status": "COMMIT OK"}

        if clean_cmd == "rollback":
            await self.conn.rollback()
            return {"status": "ROLLBACK OK"}

        if clean_cmd == "begin":
            if self.is_in_transaction():
                return {"status": "Transaction already started"}
            await self.conn.begin()
            return {"status": "BEGIN OK"}

        result = await self.conn.execute(text(command))

        # SELECT / RETURNING → rows as list of dicts (for Rich table)
        if result.returns_rows:
            return [dict(row) for row in result.mappings().all()]

        # INSERT / UPDATE / DELETE
        return {"status": "OK", "rowcount": result.rowcount}


    async def close(self) -> None:
        if self.conn is not None:
            await self.conn.close()
            self.conn = None
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None


class MongoAdapter(DBAdapter):
    def __init__(self) -> None:
        self.client = None
        self.db = None

    async def connect(self, url: str) -> None:
        from motor.motor_asyncio import AsyncIOMotorClient

        self.client = AsyncIOMotorClient(url)
        db_name = url.rsplit("/", 1)[-1].split("?")[0] or "test"
        self.db = self.client[db_name]

    async def execute(self, command: str) -> Any:
        if self.db is None:
            raise RuntimeError("No connection")
        cmd = json.loads(command)
        return await self.db.command(cmd)

    async def close(self) -> None:
        if self.client is not None:
            self.client.close()
            self.client = None
            self.db = None


ADAPTERS = {
    "postgres": SQLAdapter,
    "mysql": SQLAdapter,
    "mongo": MongoAdapter,
}
