from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)


class Base(DeclarativeBase):
    pass


SQLModel.metadata = Base.metadata
SQLModel._sa_registry = Base.registry


# FastAPI Users does not support SQLModel, so User model must use SQLAlchemy
class User(SQLAlchemyBaseUserTableUUID, Base):
    group_id: Mapped[int] = mapped_column(ForeignKey("usergroup.id"), nullable=True)
    group: Mapped["UserGroup"] = relationship(back_populates="users", lazy="selectin")


# Other models can use SQLModel
# 1) Example of SQLModel model with relationship to User model
class UserGroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    users: list["User"] = Relationship(
        back_populates="group", sa_relationship_kwargs={"lazy": "joined"}
    )


# 2) Example of simple SQLModel model
class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
