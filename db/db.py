#!/usr/bin/env python
#-_- coding:utf-8 -_-
from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import setting

app = Flask(__name__)
app.config.from_object(setting)
#app.config['SECRET_KEY'] = 'ag866.com'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://check_tomcat:ag866.com@localhost:3306/check_tomcat'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app) #实例化
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class tomcat_project(db.Model):
    __tablename__ = 'tomcat_project' #定义表名
    id = db.Column(db.Integer,primary_key=True)#定义列对象
    product = db.Column(db.String(10),unique=False)
    project = db.Column(db.String(32),unique=True)
    tomcat = db.Column(db.String(64),unique=False)
    main_port = db.Column(db.String(10),unique=False)
    jdk = db.Column(db.String(10),unique=False)
    script = db.Column(db.String(64),unique=False)
    def __init__(self,product, project, tomcat, main_port, jdk, script):
        self.product = product
        self.project = project
        self.tomcat = tomcat
        self.main_port = main_port
        self.jdk = jdk
        self.script = script

class tomcat_url(db.Model):
    __tablename__ = 'tomcat_url' #定义表名
    id = db.Column(db.Integer,primary_key=True)#定义列对象
    project = db.Column(db.String(64),unique=False)
    domain = db.Column(db.String(128),unique=False)
    url = db.Column(db.String(128),unique=True)
    
    def __init__(self, project, domain, url):
        self.project = project
        self.domain = domain
        self.url = url

class mail(db.Model):
    __tablename__ = 'mail'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=False)
    mail_address = db.Column(db.String(64),unique=True)
    status = db.Column(db.String(20),unique=False)
    role = db.Column(db.String(10),unique=False)
    def __init__(self, name, mail_address, status, role):
        self.name = name
        self.mail_address = mail_address
        self.status = status
        self.role = role

class check_tomcat(db.Model):
    __tablename__ = 'check_tomcat'
    id = db.Column(db.Integer,primary_key=True)
    access_time = db.Column(db.String(64), unique=False)
    project = db.Column(db.String(64),unique=False)
    domain = db.Column(db.String(128),unique=False)
    url = db.Column(db.String(128),unique=False)
    code = db.Column(db.String(8), unique=False)
    info = db.Column(db.String(1024),unique=False)
    def __init__(self, access_time, project, domain, url, code, info):
        self.access_time = access_time
        self.project = project
        self.domain = domain
        self.url = url
        self.code = code
        self.info = info

class monitor_server(db.Model):
    __tablename__ = 'monitor_server'
    id = db.Column(db.Integer,primary_key=True)
    access_time = db.Column(db.String(64), unique=False)
    url = db.Column(db.String(64), unique=False)
    status = db.Column(db.String(10), unique=False)
    info = db.Column(db.String(1024),unique=False)
    def __init__(self, access_time, url, status, info):
        self.access_time = access_time
        self.url = url
        self.status = status
        self.info = info

if __name__ == '__main__':
   #db.create_all()
   manager.run()
