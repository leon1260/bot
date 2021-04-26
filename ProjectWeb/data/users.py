import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin): # Класс добавления таблицы в базу данных
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, # Столбец id, который служит уникальным ключом
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True) # Имя пользователя
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # email = sqlalchemy.Column(sqlalchemy.String,
    #                           index=True, unique=True, nullable=True)
    # hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subscription = sqlalchemy.Column(sqlalchemy.Integer)

    # news = orm.relation("News", back_populates='user')

    def set_password(self, password): # Генерация пароля для пользователей
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password): # Проверка пароля пользователя
        return check_password_hash(self.hashed_password, password)
