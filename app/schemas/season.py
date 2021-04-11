from app.schemas.base import BaseModelSchema
from app.database.models.season import SeasonModel


class SeasonSchema(BaseModelSchema):

    class Meta(BaseModelSchema.Meta):
        model = SeasonModel


season_schema = SeasonSchema()
seasons_schema = SeasonSchema(many=True)