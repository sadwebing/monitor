# coding: utf-8
import logging,os,sys

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
SECRET_KEY = 'you-guess'
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='%s/logs/monitor.log' %basedir,
    filemode='a'
)

HOST='192.168.100.107'
PORT=9990
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://check_tomcat:ag866.com@localhost:3306/check_tomcat'
SQLALCHEMY_COMMIT_ON_TEARDOWN  = True
SQLALCHEMY_TRACK_MODIFICATIONS = True


