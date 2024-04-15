from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.db.models.image import Image, ImageCreate, ImageRead, ImageUpdate
from sqlmodel import select

from database.db.connections import get_db

router = APIRouter()


@router.post("/", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    new_image = Image(**image.dict())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image


@router.get("/{image_id}", response_model=ImageRead)
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.get("/", response_model=List[ImageRead])
def read_images(db: Session = Depends(get_db)):
    images = db.execute(select(Image)).scalars().all()
    return images


@router.put("/{image_id}", response_model=ImageRead)
def update_image(
    image_id: int, image_update: ImageUpdate, db: Session = Depends(get_db)
):
    image = db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    for var, value in image_update.dict(exclude_unset=True).items():
        setattr(image, var, value)
    db.commit()
    db.refresh(image)
    return image


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
    return {"ok": True}
