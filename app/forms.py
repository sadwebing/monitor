# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
#from wtforms.fields import TextField, BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from db.db import User

# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField(u'账号', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我', default=False)
    submit = SubmitField(u'登陆')

class RegistrationForm(FlaskForm):
    username = StringField(u'账号', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    #def validate_username(self, field):
    #    if User.query.filter_by(username=field.data).first():
    #        raise ValidationError('Username already in use.')

