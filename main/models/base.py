from main import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def to_dict(self):
        row_as_dict = {
            column: str(getattr(self, column)) for column in self.__table__.c.keys()
        }
        return row_as_dict
