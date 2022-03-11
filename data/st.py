import sqlalchemy
from .db_session import SqlAlchemyBase


class Status(SqlAlchemyBase):
    __tablename__ = 'status'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.Integer)
