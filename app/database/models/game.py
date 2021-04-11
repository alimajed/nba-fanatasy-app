from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, Integer, String

from app.database.models.base import BaseModel


class GameModel(BaseModel):
    __tablename__ = "game"

    game_date_est = Column(DateTime, nullable=True)
    game_status_text = Column(String, nullable=True)
    home_team = Column(String, nullable=True)
    home_score = Column(Integer, nullable=True)
    away_team = Column(String, nullable=True)
    away_score = Column(Integer, nullable=True)
    home_team_wins = Column(Boolean, nullable=True)
    is_playoff = Column(Boolean, nullable=True)
    playoff_seried_id = Column(Integer, nullable=True)

    season_id = Column(Integer, ForeignKey("season.id"))
    season = relationship("SeasonModel", back_populates="games")

    teams = association_proxy("teams_stats", "team")
    players = association_proxy("players_stats", "player")