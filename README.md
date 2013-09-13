# Flask TODO

簡易的事件備忘錄，提供新增、更新、刪除、過濾的功能

## Use Steps

### 1. Requirement

需安裝 Python3.3 、 python3-dev 、 Flask 、 Flask-SQLAlchemy 、 pymysql3 、 uwsgi

### 2. Config Setting

Modify flask-todo/todo/config.cfg

    DEBUG = True / False
    SERVER_IP = 'Server IP'
    SERVER_PORT = 80
    LOG_PATH = 'log/sesto.log'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/to_do'
    SQLALCHEMY_ECHO = False
    SECRET_KEY = generate good secret keys : '>>> import os >>> os.urandom(24)'

### 3. Run

python todo_main.py

![image](http://rtd.softstar.com.tw/softstar-web-technique/flask-todo/raw/master/doc/images/todo_login.jpg)

![image](http://rtd.softstar.com.tw/softstar-web-technique/flask-todo/raw/master/doc/images/todo_list.jpg)