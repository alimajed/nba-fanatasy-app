from app.database.models.team import TeamModel
from app.daos.base import BaseDAO


class TeamDAO(BaseDAO):
    def __init__(self, model):
        super().__init__(model)


team_doa = TeamDAO(TeamModel)