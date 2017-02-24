#!/usr/bin/env python
#-_- coding:utf-8 -_-
from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

#app.config['SECRET_KEY'] = 'ag866.com'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://check_tomcat:ag866.com@localhost:3306/check_tomcat'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app) #实例化

class tomcat_url(db.Model):
    __tablename__ = 'tomcat_url' #定义表名
    id = db.Column(db.Integer,primary_key=True)#定义列对象
    project = db.Column(db.String(64),unique=False)
    domain = db.Column(db.String(128),unique=False)
    url = db.Column(db.String(128),unique=False)
    def __init__(self, project, domain, url):
        self.project = project
        self.domain = domain
        self.url = url

class mail(db.Model):
    __tablename__ = 'mail'
    id = db.Column(db.Integer,primary_key=True)
    mail_address = db.Column(db.String(64),unique=True)
    status = db.Column(db.String(64),unique=False)
    def __init__(self, mail_address, status):
        self.mail_address = mail_address
        self.status = status

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

if __name__ == '__main__':
   db.create_all()

