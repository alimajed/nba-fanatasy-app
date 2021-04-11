from app.database.models.season import SeasonModel
from app.daos.base import BaseDAO


class SeasonDAO(BaseDAO):
    def __init__(self, model):
        super().__init__(model)


season_doa = SeasonDAO(SeasonModel)
 
    