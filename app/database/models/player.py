from sqlalchemy import Column
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Integer, String

from app.database.models.base import BaseModel


class PlayerModel(BaseModel):
    __tablename__ = "player"

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    from_year = Column(Integer, nullable=True)
    to_year = Column(Integer, nullable=True)
    still_playing = Column(Boolean, nullable=True)

    player_seasons = relationship("PlayerSeasonTeamModel", back_populates="player")
    games = association_proxy("players_stats", "game")