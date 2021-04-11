from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Float, Integer

from app.database.models.base import BaseModel


class TeamsStatsModel(BaseModel):
    __tablename__ = "teams_stats"

    pts = Column(Integer, nullable=True)
    fg_pct = Column(Float, nullable=True)
    ft_pct = Column(Float, nullable=True)
    fg3_pct = Column(Float, nullable=True)
    ast = Column(Integer, nullable=True)
    reb = Column(Integer, nullable=True)
    is_home_team = Column(Boolean, nullable=True)

    game_id = Column(Integer, ForeignKey("game.id"))
    game = relationship("GameModel", backref="teams_stats")

    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("TeamModel", backref="teams_stats")
