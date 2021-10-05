from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import Float, Integer, String

from app.database.models.base import BaseModel


class PlayersStatsModel(BaseModel):
    __tablename__ = "players_stats"
    
    start_position = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    minutes = Column(Float, nullable=True)
    fgm = Column(Float, nullable=True)
    fga = Column(Float, nullable=True) 
    fg_pct = Column(Float, nullable=True)
    fg3m = Column(Float, nullable=True)
    fg3a = Column(Float, nullable=True)
    fg3_pct = Column(Float, nullable=True)
    ftm = Column(Float, nullable=True)
    fta = Column(Float, nullable=True)
    ft_pct = Column(Float, nullable=True)
    oreb = Column(Integer, nullable=True)
    dreb = Column(Integer, nullable=True)
    ast = Column(Integer, nullable=True)
    stl = Column(Integer, nullable=True)
    blk = Column(Integer, nullable=True)
    to = Column(Integer, nullable=True)
    pf = Column(Integer, nullable=True)
    pts = Column(Integer, nullable=True)
    plus_minus = Column(Integer, nullable=True)

    game_id = Column(Integer, ForeignKey("game.id"))
    game = relationship("GameModel", backref="players_stats")

    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("TeamModel", backref="players_stats")

    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship("PlayerModel", backref="players_stats")
