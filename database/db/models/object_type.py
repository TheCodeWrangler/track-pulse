from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from typing import Optional, List
from datetime import datetime


class ObjectTypeBase(SQLModel):
    name: str = Field(sa_column=Column(String, unique=True))
    description: Optional[str] = None


class ObjectType(ObjectTypeBase, table=True):
    __tablename__ = "object_type"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.utcnow()

    # An object type can have many object observations
    object_observations: List["ObjectObservation"] = Relationship(
        back_populates="object_type"
    )
    object_instances: List["ObjectInstance"] = Relationship(
        back_populates="object_type"
    )


class ObjectTypeCreate(ObjectTypeBase):
    pass


class ObjectTypeRead(ObjectTypeBase):
    id: int
    created_datetime: datetime


class ObjectTypeUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
