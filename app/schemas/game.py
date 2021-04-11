from app.schemas.base import BaseModelSchema
from app.database.models.game import GameModel


class GameSchema(BaseModelSchema):

    class Meta(BaseModelSchema.Meta):
        model = GameModel


game_schema = GameSchema()
games_schema = GameSchema(many=True)