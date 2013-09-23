from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from todo.model.user import User
from todo.model.memo import TodoMemo
