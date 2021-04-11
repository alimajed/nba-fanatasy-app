from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer

from app.database.models.base import BaseModel


class PlayerSeasonTeamModel(BaseModel):
    __tablename__ = "seasons"

    season_id = Column(Integer, ForeignKey("season.id"))
    team_id = Column(Integer, ForeignKey("team.id"))
    player_id = Column(Integer, ForeignKey("player.id"))

    __table_args__ = (UniqueConstraint(season_id, team_id, player_id),)

    season = relationship("SeasonModel")
    team = relationship("TeamModel", back_populates="team_seasons")
    player = relationship("PlayerModel", back_populates="player_seasons")