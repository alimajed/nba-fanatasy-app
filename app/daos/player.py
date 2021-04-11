from app.database.models.player import PlayerModel
from app.daos.base import BaseDAO


class PlayerDAO(BaseDAO):
    def __init__(self, model):
        super().__init__(model)


player_doa = PlayerDAO(PlayerModel)

    