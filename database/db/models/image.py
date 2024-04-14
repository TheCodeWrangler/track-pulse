from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# from db.models.link_tables import EncounterSetLink


class ImageBase(SQLModel):
    captured_datetime: datetime = datetime.utcnow()
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fp: Optional[str] = None


class Image(ImageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.utcnow()

    # one Image can have many ObjectObservations
    object_observations: List["ObjectObservation"] = Relationship(
        back_populates="image"
    )


class ImageCreate(ImageBase):
    pass


class ImageRead(ImageBase):
    id: int
    created_datetime: datetime


class ImageUpdate(SQLModel):
    pass
