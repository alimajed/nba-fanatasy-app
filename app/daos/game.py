from app.database.models.game import GameModel
from app.daos.base import BaseDAO


class GameDAO(BaseDAO):
    def __init__(self, model):
        super().__init__(model)


game_doa = GameDAO(GameModel)

    