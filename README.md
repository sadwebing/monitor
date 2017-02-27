# monitor
http://www.oschina.net/translate/the-flask-mega-tutorial-part-i-hello-world
pip install flask flask-login flask-openid flask-sqlalchemy sqlalchemy-migrate flask-whooshalchemy flask-wtf flask-babel flup
You are probably using the import style from the older versions:

from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required
The import style changed starting from 0.9.0 version. Be sure to update your imports:

from flask.ext.wtf import Form
from wtforms.fields import TextField, BooleanField
from wtforms.validators import Required
You can find the note about this change in the upgrade section of docs:

https://flask-wtf.readthedocs.org/en/latest/upgrade.html#version-0-9-0
http://www.open-open.com/lib/view/open1481094792784.html
http://blog.csdn.net/geekleee/article/details/52692376
