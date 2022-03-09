import sqlalchemy
from .db_session import SqlAlchemyBase



class Action(SqlAlchemyBase):
    __tablename__ = 'actions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    action = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)
