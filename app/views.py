# coding: utf-8
from flask import render_template, flash, redirect, session, url_for, request, g 
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm
from setting import logging
from flask_wtf.csrf import CSRFProtect as CsrfProtect
#from flask_wtf.csrf import CsrfProtect
from forms import LoginForm, RegistrationForm
from db.db import User
from db import db
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user.username # fake user
    #user = current_user.username # fake user
    posts = [ # fake array of posts
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
    title = 'home',
    user = user,
    posts = posts,
    ip = ip)

# 这个callback函数用于reload User object，根据session中存储的user id
@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    #return User.get(user_id)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)

@app.before_request
def before_request():
    global ip 
    ip = request.remote_addr
    g.user = current_user
    if g.user is not None and current_user.is_authenticated \
            and not current_user.confirmed:
        token = current_user.generate_confirmation_token()
        current_user.confirm(token)
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            logging.info(u'%s 登陆成功' %user.username)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form, ip = ip)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    logging.info('form.validate_on_submit():%s' %form.validate_on_submit())
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is None:
            user = User(username=form.username.data,
                        password=form.password.data)
            logging.info('username:%s' %user.username)
            db.db.session.add(user)
            db.db.session.commit()
            token = user.generate_confirmation_token()
            user.confirm(token)
            #send_email(user.email, 'Confirm Your Account',
            #           'auth/email/confirm', user=user, token=token)
            #flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('login'))
        else:
            logging.info(u'注册IP：%s  账号 %s 已被注册，请更换用户名。' %(ip, form.username.data))
            flash(u'账号 %s 已被注册，请更换用户名。' %form.username.data)
            return redirect(url_for('register'))
    return render_template('register.html', form=form, ip = ip)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
