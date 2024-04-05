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

    # # Link to other tables (many to many) through link tables
    # encounter_sets: list["EncounterSet"] = Relationship(  # noqa: F821
    #     back_populates="encounters", link_model=EncounterSetLink
    # )  # type: ignore

    # transcripts: Optional[List["Transcript"]] = Relationship(  # noqa: F821
    #     back_populates="encounter"
    # )  # noqa: F821


class ImageCreate(ImageBase):
    pass


class ImageRead(ImageBase):
    id: int
    created_datetime: datetime


class ImageUpdate(SQLModel):
    pass