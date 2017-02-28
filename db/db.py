#!/usr/bin/env python
#-_- coding:utf-8 -_-
from flask import Flask, current_app
#from flask.ext.sqlalchemy import SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import setting
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
import json
import uuid

app = Flask(__name__)
app.config.from_object(setting)
db = SQLAlchemy(app) #实例化
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class tomcat_project(db.Model):
    __tablename__ = 'tomcat_project' #定义表名
    id = db.Column(db.Integer,primary_key=True)#定义列对象
    product = db.Column(db.String(10),unique=False)
    project = db.Column(db.String(32),unique=True)
    code_dir = db.Column(db.String(32),unique=False)
    tomcat = db.Column(db.String(64),unique=False)
    main_port = db.Column(db.String(10),unique=False)
    jdk = db.Column(db.String(10),unique=False)
    script = db.Column(db.String(64),unique=False)
    def __init__(self,product, project, code_dir, tomcat, main_port, jdk, script):
        self.product = product
        self.project = project
        self.code_dir = code_dir
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

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
###########################################################
    def generate_reset_token(self, expiration=3600):
    #增加generate_reset_token方法，用来生成用户的id的加密签名
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        #先产生个Serializer类的实例，里面设置好密钥和过期时间
        return s.dumps({'reset': self.id}) 
        #返回一个加密签名

    def reset_password(self, token, new_password):
    #增加更改密码的方法，接受token加密签名，新密码
        s = Serializer(current_app.config['SECRET_KEY'])
        #产生实例s
        try:
            data = s.loads(token)
        except:
            return False
        #试着解析加密签名，得到字典data，否则返回False
        if data.get('reset') != self.id:
            return False
        #如果data字典中的reset的值不等于用户的id，返回False
        self.password = new_password
        #否则，更新用户密码
        db.session.add(self)
        #提交到数据库
        return True
        #返回True

    def __repr__(self):
        return '<User %r>' % self.username
#########################################################

if __name__ == '__main__':
   #db.create_all()
   manager.run()
