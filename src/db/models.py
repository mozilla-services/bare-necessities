from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from typing import Dict

db: SQLAlchemy = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(1000), unique=True, nullable=False)
    email = Column(String(1000), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


def get_user_details(user_name: str) -> Dict[str, str]:
    user_details = db.session.query(User.name, User.email,).filter_by(name=user_name)
    return dict(user_details)
