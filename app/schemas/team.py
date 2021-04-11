from app.schemas.base import BaseModelSchema
from app.database.models.team import TeamModel


class TeamSchema(BaseModelSchema):

    class Meta(BaseModelSchema.Meta):
        model = TeamModel


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)