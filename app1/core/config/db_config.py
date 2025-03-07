import re
from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session, AsyncEngine,
)

from sqlalchemy.exc import IntegrityError

from app1.core.settings import settings


class Utils:
    prefix = settings.db.DB_TABLE_PREFIX

    @staticmethod
    def db_tablename_camel(cls):
        return ''.join(s.capitalize() for s in re.split(r'[ _-]', cls.__name__.lower()))

    @staticmethod
    def camel2snake(name):
        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        return Utils.prefix + '_' + snake.lower()


class DBConfigurerInitializer:
    utils = Utils()

    def __init__(
            self,
            connection_path: str,
            echo: bool,
            pool_size: int,
    ):
        self.connection_path = connection_path
        self.engine: AsyncEngine = create_async_engine(
            url=self.connection_path,
            echo=echo,
            pool_size=pool_size,
        )
        self.Session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.Session() as session:
            yield session

    # def get_scoped_session(self) :
    #     session = async_scoped_session(
    #         session_factory=self.Session,
    #         scopefunc=current_task
    #     )
    #     return session
    #
    # async def session_dependency(self) -> AsyncSession:
    #     async with self.Session() as session:
    #         yield session
    #         await session.close()
    #
    # async def scope_session_dependency(self):
    #     session = self.get_scoped_session()
    #     yield session
    #     await session.close()


DBConfigurer = DBConfigurerInitializer(
    connection_path=settings.db.DB_URL,
    echo=settings.db.DB_ECHO_MODE,
    pool_size=settings.db.DB_POOL_SIZE,
)