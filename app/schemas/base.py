from marshmallow import post_dump, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class BaseModelSchema(SQLAlchemyAutoSchema):

    class Meta:
        load_instance = True
