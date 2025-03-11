from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from app1.core.config.db_config import DBConfigurer
from app1.core.settings import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.NAMING_CONVENTION
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return DBConfigurer.utils.camel2snake(cls.__name__)
        # return '_'.join([settings.db.DB_TABLE_PREFIX, cls.__name__.lower()])

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            result[column.name] = getattr(self, column.name)
        return result
