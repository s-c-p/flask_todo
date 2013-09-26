# Flask TODO

簡易的事件備忘錄，提供新增、更新、刪除、過濾的功能

[測試網站](http://172.18.101.16/todo/) (測試帳號 : wes 測試密碼 : 123456)

![image](http://rtd.softstar.com.tw/softstar-web-technique/flask-todo/raw/master/doc/images/todo_login.jpg)

![image](http://rtd.softstar.com.tw/softstar-web-technique/flask-todo/raw/master/doc/images/todo_list.jpg)

[supervisor status](http://172.18.101.16:9001/)(測試帳號 : user 測試密碼 : 123)

## Use Steps

### 1. Packages / Dependencies

確認您有 Python 的正確版本

    #install python 3.3
    sudo apt-get install python3.3
    #check python version
    python --version

確認您有 Flask 的正確版本

    #install Flask latest version (0.10)
    pip install Flask

安裝 MariaDB

    #install MariaDB
    sudo apt-get install mariadb
    #create db
    mysql -u root -p
    create database to_do

安裝 Python MySQL Driver

    #install PyMysql3
    pip install pymysql3

安裝 uwsgi

    #install python-dev
    apt-get install python-dev

    #install uwsgi
    pip install uwsgi


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

### 4. Run on uWSGI and use supervisor monitor process

確認安裝 supervisor(只支援python2.7)

    #install python2.7(ubuntu 預設就有裝)
    #install supervisor :
    #With pip >= 1.4
    pip install supervisor --pre
    #With previous versions of pip
    pip install supervisor

Creating a Configuration File

    #root 的權限下
    echo_supervisord_conf > /etc/supervisord.conf

Config supervisord.cnf

    #開啟網頁監控
    [inet_http_server]         ; inet (TCP) server disabled by default
    port=*:9001        ; (ip_address:port specifier, *:port for all iface)
    username=user              ; (default is no username (open server))
    password=123               ; (default is no password (open server))

    #Adding a Program
    [program:todo]
    command=/home/rdadmmin/py33ENV/bin/uwsgi -H /home/rdadmmin/py33ENV -s /home/rdadmmin/tmp/uwsgi.sock --module todo_main --callable app --pp /home/rdadmmin/py33ENV/test/ --chmod-socket
    user=rdadmin
    directory=/home/rdadmmin/py33ENV/flask-todo/
    stderr_logfile = /home/rdadmmin/tmp/supervisor_todo_err.log
    stdout_logfile = /home/rdadmmin/tmp/supervisor_todo_out.log

Run supervisor

    run $BINDIR/supervisord

Nginx config

    upstream gunicorn_flask_server {
        server unix:/home/rdadmmin/py33ENV/flask-todo/gunicorn_flask.sock fail_timeout=0;
    }

    location = /todo { rewrite ^ /todo/; }
    location /todo/ { try_files $uri @todo; }
    location @todo {
       include uwsgi_params;
       uwsgi_param SCRIPT_NAME /todo;
       uwsgi_modifier1 30;
       uwsgi_pass unix:/home/rdadmmin/tmp/uwsgi.sock;
    }

Nginx restart

    sudo service nginx restart


