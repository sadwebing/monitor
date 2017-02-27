import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from setting import basedir

app = Flask(__name__)
app.config.from_object('setting')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'
lm.session_protection = 'strong'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
from app import views
