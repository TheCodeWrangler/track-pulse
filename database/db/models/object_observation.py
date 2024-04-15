from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from database.db.models.object_instance import ObjectInstance

from database.db.models.image import Image

class ObjectObservationBase(SQLModel):
    # Pixel Region defines where in the image the object is located
    pixel_region: Optional[str] = None


class ObjectObservation(ObjectObservationBase, table=True):
    __tablename__ = "object_observation"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.utcnow()

    # One object observation is of one object_type
    object_type_id: Optional[int] = Field(foreign_key="object_type.id", default=None)
    object_type: Optional["ObjectType"] = Relationship( # type: ignore
        back_populates="object_observations"
    )

    image_id: Optional[int] = Field(foreign_key="image.id", default=None)
    image: Optional[Image] = Relationship(back_populates="object_observations")

    depth_map_id: Optional[int] = Field(foreign_key="depthmap.id", default=None)
    depth_map: Optional["DepthMap"] = Relationship(back_populates="object_observations") # type: ignore

    object_instance_id: Optional[int] = Field(
        foreign_key="object_instance.id", default=None
    )
    object_instance: Optional["ObjectInstance"] = Relationship(
        back_populates="object_observations"
    )

    segmentation_algorithm_id: Optional[int] = Field(
        foreign_key="segmentation_algorithm.id", default=None
    )
    segmentation_algorithm: Optional["SegmentationAlgorithm"] = Relationship( # type: ignore
        back_populates="object_observations"
    )
