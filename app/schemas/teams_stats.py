from marshmallow.fields import Boolean, Integer, Float, String

from app.schemas.base import BaseModelSchema
from app.database.models.team import TeamModel
from app.database.models.teams_stats import TeamsStatsModel


class TeamsStatsSchema(BaseModelSchema):

    class Meta(BaseModelSchema.Meta):
        model = TeamsStatsModel
        load_only = ("id",)
        include_fk = True


teams_stats_schema = TeamsStatsSchema(many=True)