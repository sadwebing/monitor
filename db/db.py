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

if __name__ == '__main__':
   db.create_all()

