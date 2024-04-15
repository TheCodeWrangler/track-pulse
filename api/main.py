from fastapi import FastAPI
from database.db.connections import create_db_and_tables, get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
import api.routers.image as image_router  # This module should contain your CRUD operations for the Image model.

# set swagger_ui_parameters to collapse sections
swagger_ui_parameters = {"docExpansion": "none"}

tags_metadata = [
    {
        "name": "image",
        "description": "Images CRUD operations",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
app = FastAPI(swagger_ui_parameters=swagger_ui_parameters, openapi_tags=tags_metadata)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Initialize the database and create tables if they don't exist
@app.on_event("startup")
async def startup_event():
    create_db_and_tables(True)  # You can pass local=True if you're running locally


# Including the image router
app.include_router(
    image_router.router, prefix="/image", tags=["image"], dependencies=[Depends(get_db)]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
