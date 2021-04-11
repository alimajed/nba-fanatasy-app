from app.schemas.base import BaseModelSchema
from app.database.models.player import PlayerModel


class PlayerSchema(BaseModelSchema):

    class Meta(BaseModelSchema.Meta):
        model = PlayerModel


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)