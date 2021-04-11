from flask import abort
from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import db


class BaseModel(db.Model):
   __abstract__ = True

   id = Column(Integer, primary_key=True, unique=True, nullable=False)
