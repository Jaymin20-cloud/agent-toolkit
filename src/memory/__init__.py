from contextlib import AbstractAsyncContextManager
from typing import Any

from core.settings import DatabaseType, settings


def initialize_database() -> AbstractAsyncContextManager[Any]:
    """
    Initialize the appropriate database checkpointer based on configuration.
    Returns an initialized AsyncCheckpointer instance.
    """
    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        from memory.postgres import get_postgres_saver

        return get_postgres_saver()
    if settings.DATABASE_TYPE == DatabaseType.MONGO:
        from memory.mongodb import get_mongo_saver

        return get_mongo_saver()
    from memory.sqlite import get_sqlite_saver

    return get_sqlite_saver()


def initialize_store() -> AbstractAsyncContextManager[Any]:
    """
    Initialize the appropriate store based on configuration.
    Returns an async context manager for the initialized store.
    """
    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        from memory.postgres import get_postgres_store

        return get_postgres_store()
    # TODO: Add Mongo store - https://pypi.org/project/langgraph-store-mongodb/
    from memory.sqlite import get_sqlite_store

    return get_sqlite_store()


__all__ = ["initialize_database", "initialize_store"]
