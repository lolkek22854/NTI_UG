import sqlalchemy
from .db_session import SqlAlchemyBase


class Tank(SqlAlchemyBase):
    __tablename__ = 'tanks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    resources = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    is_servo = sqlalchemy.Column(sqlalchemy.Integer)
    is_rgb = sqlalchemy.Column(sqlalchemy.Integer)
    is_near = sqlalchemy.Column(sqlalchemy.Integer)
