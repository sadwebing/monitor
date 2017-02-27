#!/usr/bin/env python
#-_- coding:utf-8 -_-
from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import setting
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
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

PROFILE_FILE = "profiles.json"
class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.password_hash = self.get_password_hash()
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """save user name, id and password hash to json file"""
        self.password_hash = generate_password_hash(password)
        with open(PROFILE_FILE, 'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[self.username] = [self.password_hash,
                                       self.id]
            f.write(json.dumps(profiles))

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_password_hash(self):
        """try to get password hash from file.

        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return unicode(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.iteritems():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None


if __name__ == '__main__':
   #db.create_all()
   manager.run()
