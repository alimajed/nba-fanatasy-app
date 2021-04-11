from marshmallow.fields import Boolean, Integer, Float, String

from app.schemas.base import BaseModelSchema
from app.database.models.team import TeamModel
from app.database.models.players_stats import PlayersStatsModel


class PlayersStatsSchema(BaseModelSchema):

    class Meta(BaseModelSchema.Meta):
        model = PlayersStatsModel
        load_only = ("id",)
        include_fk = True


players_stats_schema = PlayersStatsSchema(many=True)