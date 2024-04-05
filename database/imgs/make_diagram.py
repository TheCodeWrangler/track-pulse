# Install of eralchemy led to issues with graphviz, and pygraphviz (dependency of eralchemy)
# I was able to get it to work by installing graphviz with homebrew, and then installing pygraphviz with pip
# TODO: Resolve installation and include in pyproject.toml
from eralchemy2 import render_er
from sqlalchemy import create_engine
from database.db import *
from sqlmodel import SQLModel
import os

this_dir = os.path.dirname(__file__)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


create_db_and_tables()

## Draw from database
render_er(sqlite_url, os.path.join(this_dir, "entity_relationships.png"))
