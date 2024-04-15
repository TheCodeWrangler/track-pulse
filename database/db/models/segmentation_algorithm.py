from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class SegmentationAlgorithmBase(SQLModel):
    released_datetime: Optional[datetime] = None
    version: str
    description: Optional[str] = None

class SegmentationAlgorithm(SegmentationAlgorithmBase, table=True):
    __tablename__ = "segmentation_algorithm"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.utcnow()

    # one SegmentationAlgorithm can have many ObjectObservations
    object_observations: List["ObjectObservation"] = Relationship( # type: ignore
        back_populates="segmentation_algorithm"
    )

class SegmentationAlgorithmCreate(SegmentationAlgorithmBase):
    pass

class SegmentationAlgorithmRead(SegmentationAlgorithmBase):
    id: int
    created_datetime: datetime

class SegmentationAlgorithmUpdate(SQLModel):
    description: Optional[str] = None
    version: Optional[str] = None