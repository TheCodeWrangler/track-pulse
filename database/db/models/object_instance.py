from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class ObjectInstanceBase(SQLModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ObjectInstance(ObjectInstanceBase, table=True):
    __tablename__ = "object_instance"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.utcnow()

    # One object instance can have many object observations
    object_observations: List["ObjectObservation"] = Relationship(
        back_populates="object_instance"
    )
    # One object instance has one object type
    object_type_id: Optional[int] = Field(foreign_key="object_type.id", default=None)
    object_type: Optional["ObjectType"] = Relationship(
        back_populates="object_instances"
    )

    # one instance is from on
