from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import String

from app.database.models.base import BaseModel


class SeasonModel(BaseModel):
    __tablename__ = "season"

    description = Column(String, nullable=True)

    games = relationship("GameModel", back_populates="season")