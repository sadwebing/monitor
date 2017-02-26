# coding: utf-8
import logging,os,sys

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(basedir)
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
SECRET_KEY = 'ag866.com'
SQLALCHEMY_DATABASE_URI = 'mysql://check_tomcat:ag866.com@localhost:3306/check_tomcat'
SQLALCHEMY_COMMIT_ON_TEARDOWN  = True
SQLALCHEMY_TRACK_MODIFICATIONS = True


