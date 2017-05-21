# Flask TODO

Simple event memo, provides new, update, delete, filter function

[Test site: wes test password: 123456) (test account: wes test password: 123456) (test account: wes test password: 123456)

! [Image] (https://raw.github.com/wesgt/flask_todo/master/doc/images/todo_login.jpg)

[Supervisor status] (http://ec2-54-238-225-130.ap-northeast-1.compute.amazonaws.com:9001/) (test account: user test password: 123)

## Use Steps

### 1. Packages / Dependencies

Make sure you have the correct version of Python

    #install python 3.3
    Sudo apt-get install python3.3
    #check python version
    Python --version
    
Make sure you have virtualenv

    Sudo apt-get install python-virtualenv
    Virtualenv .env3 - python = python3.3
    Source .env3 / bin / activate

Make sure you have the correct version of Flask

    # Install Flask latest version (0.10)
    Pip install Flask
    
Make sure you have the correct version of sqlalchemy

    Pip install sqlalchemy

Install MariaDB

    #install MariaDB
    Sudo apt-get install mariadb
    #create db
    Mysql -u root -p
    Create database to_do

Install Python MySQL Driver

    #install PyMysql3
    Pip install pymysql3
    
Install Redis
    
    Sudo apt-get install redis-server
    
Install the Redis driver

    Pip install redis

Install uwsgi

    #install python-dev
    Sudo apt-get install python-dev

    #install uwsgi
    Pip install uwsgi


### 2. Config Setting

Modify flask-todo / todo / config.cfg

    DEBUG = True / False
    SERVER_IP = 'Server IP'
    SERVER_PORT = 80
    LOG_PATH = 'log / sesto.log'
    SQLALCHEMY_DATABASE_URI = 'mysql + pymysql: // root: 123456 @ localhost / to_do'
    SQLALCHEMY_ECHO = False
    SECRET_KEY = generate good secret keys: '>>> import os >>> os.urandom (24)'

### 3. Run

Python todo_main.py

### 4. Run on uWSGI and use supervisor monitor process

Confirm installation supervisor (python2.7 only)

    # Install python2.7 (ubuntu default installed)
    #install supervisor:
    #With pip> = 1.4
    Pip install supervisor --pre
    #With previous versions of pip
    Pip install supervisor

Creating a Configuration File

    #root under permission
    Echo_supervisord_conf> /etc/supervisord.conf

Config supervisord.cnf

    # Turn on webpage monitoring
    [Inet_http_server]; inet (TCP) server disabled by default
    Port = *: 9001; (ip_address: port specifier, *: port for all iface)
    Username = user; (default is no username (open server))
    Password = 123; (default is no password (open server))

    #Adding a Program
    [Program: todo]
    Command = / home / ubuntu / .env33 / bin / uwsgi -H /home/ubuntu/.env33 -s /home/ubuntu/webapp/flask-todo/uwsgi.sock --module todo_main --callable app --pp / Home / ubuntu / webapp / flask-todo / --chmod-socket
    User = ubuntu
    Directory = / home / ubuntu / webapp / flask-todo /
    Stderr_logfile = /home/ubuntu/webapp/flask-todo/supervisor_todo_err.log
    Stdout_logfile = /home/ubuntu/webapp/flask-todo/supervisor_todo_out.log

Run supervisor & Check status

    #start
    Supervisord
    #restart
    Ps aux | grep supervisord
    Kill -HUP xxxx
    #check status
    Supervisorctl -u user -p 123 status todo

Nginx config

    Location = / todo {rewrite ^ / todo /;}
    Location / todo / {try_files $ uri @todo;}
    Location @todo {
        Include uwsgi_params;
        Uwsgi_param SCRIPT_NAME / todo;
        Uwsgi_modifier1 30;
        Uwsgi_pass unix: /home/ubuntu/webapp/flask-todo/uwsgi.sock;
    }

    Location / static / {
        Alias ​​/ home / ubuntu / webapp / flask-todo / todo / static /;
    }

Nginx restart

    Sudo service nginx restart
