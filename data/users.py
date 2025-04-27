import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import LoginManager, UserMixin
from sqlalchemy_serializer import SerializerMixin

# from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    serialize_only = ('id',
                      'name',
                      "login",
                      'age',
                      'email',
                      'modified_date')

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def check_password(self, p):
        return self.hashed_password == p

    def register(self):
        return all([self.hashed_password, self.name, self.email, self.login])
