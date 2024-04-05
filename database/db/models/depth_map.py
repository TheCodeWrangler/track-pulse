from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class DepthMapBase(SQLModel):
    captured_datetime: datetime = datetime.utcnow()
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fp: Optional[str] = None

class DepthMap(DepthMapBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.utcnow()

class DepthMapCreate(DepthMapBase):
    pass

class DepthMapRead(DepthMapBase):
    id: int
    created_datetime: datetime


class DepthMapUpdate(SQLModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fp: Optional[str] = None

