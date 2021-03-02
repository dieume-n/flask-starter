from datetime import datetime
from sqlalchemy import Column, DateTime
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)
