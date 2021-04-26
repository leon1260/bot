import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase, UserMixin): # Класс добавления таблицы в базу данных
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, # Столбец id, который служит уникальным ключом
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True) # Название книги
    container = sqlalchemy.Column(sqlalchemy.String, nullable=False)
