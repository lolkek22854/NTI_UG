from flask_login.mixins import *
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import *


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    points = sqlalchemy.Column(sqlalchemy.Integer)
    card_id = sqlalchemy.Column(sqlalchemy.Integer)
    role = sqlalchemy.Column(sqlalchemy.Integer)


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
