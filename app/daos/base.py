# from app.database.db import session
from app.database.db import db

class BaseDAO:
    def __init__(self, model):
        self.model = model
        self.session = db.session

    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, _id):
        return self.session.query(self.model).filter_by(id=_id).first()
    