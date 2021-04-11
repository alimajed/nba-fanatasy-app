from sqlalchemy import ForeignKey, Column
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from app.database.models.base import BaseModel


class TeamModel(BaseModel):
    __tablename__ = "team"

    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    team_code = Column(String, nullable=True)
    nick_name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    year_founded = Column(Integer, nullable=True)
    arena = Column(String, nullable=True)

    team_seasons = relationship("PlayerSeasonTeamModel", back_populates="team")
    games = association_proxy("teams_stats", "game")