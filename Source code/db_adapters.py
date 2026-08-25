from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class DBAdapter(ABC):
    @abstractmethod
    async def connect(self, url: str) -> None: ...

    @abstractmethod
    async def execute(self, command: str) -> Any: ...

    @abstractmethod
    async def close(self) -> None: ...


class SQLAdapter(DBAdapter):
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.conn: Optional[AsyncConnection] = None
    async def connect(self, url: str) -> None:
        self.engine = create_async_engine(url, echo=False)
        self.conn = await self.engine.connect()
    def is_in_transaction(self) -> bool:
        if self.conn is None:
            return False
        if self.conn.in_transaction:
            return True
        return False
    async def execute(self, command: str) -> Any:
        clean_cmd = command.strip().rstrip(";").lower()
        if clean_cmd=="commit":
            await self.conn.commit()
            return {"status": "COMMIT OK"}
        if clean_cmd=="rollback":
            await self.conn.rollback()
            return "Rollback"
        if clean_cmd=="begin":
            if not self.is_in_transaction(self):
                await self.conn.begin()
            if is_in_transaction(self):
                return "[red]Transaction is alredy begin[/red]"
        if self.engine is None:
            raise RuntimeError("No engine")
        if self.conn is None:
            raise RuntimeError("No connection")
        result = await self.conn.execute(text(command))
        return result
    async def close(self) -> None:
        if self.engine:
            await self.engine.dispose()


class MongoAdapter(DBAdapter):
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self, url: str) -> None:
        from motor.motor_asyncio import AsyncIOMotorClient
        self.client = AsyncIOMotorClient(url)
        db_name = url.rsplit("/", 1)[-1].split("?")[0] or "test"
        self.db = self.client[db_name]

    async def execute(self, command: str) -> Any:
        if self.db is None:
            raise RuntimeError("Нет подключения")
        cmd = json.loads(command)
        return await self.db.command(cmd)

    async def close(self) -> None:
        if self.client:
            self.client.close()


ADAPTERS = {
    "postgres": SQLAdapter,
    "mysql": SQLAdapter,
    "mongo": MongoAdapter,
}
