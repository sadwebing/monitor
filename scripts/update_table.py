#!/usr/local/bin/python
#-_- coding:utf-8 -_-
import os,sys,logging
sys.path.append(os.path.dirname(os.getcwd()))
from db import db
from flask import request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='%s/logs/monitor.log' %os.path.dirname(os.getcwd()),
    filemode='a'
)

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))
#print basedir

tomcat_info_list = []
mail_list = []
def get_list(filename, list_name):
    with open('%s/%s' %(current_dir,filename)) as f:
        lines = f.readlines()
    for line in lines:
        if line == '\n' or '#' in line:
            continue
        else:
            #print line.split('|')
            list_name.append(line.split('|'))

def update_tomcat_url():
    get_list('tomcat_info.txt', tomcat_info_list)
    url_all = db.tomcat_url.query.all()
    for url_info in url_all:
        db.db.session.delete(url_info)
        db.db.session.commit()
    for url_info in tomcat_info_list:
        inset = db.tomcat_url(project=url_info[1], url=url_info[0],domain=url_info[2])
        db.db.session.add(inset)
        db.db.session.commit()
def update_mail():
    get_list('mail.txt', mail_list)
    url_all = db.mail.query.all()
    for mail_info in url_all:
        db.db.session.delete(mail_info)
        db.db.session.commit()
    for mail_info in mail_list:
        inset = db.mail(mail_address=mail_info[0], status=mail_info[1])
        db.db.session.add(inset)
        db.db.session.commit()
def update_check_tomcat():
    data = request.form 
    result = db.check_tomcat(
        time = data.get('time'),
        project = data.get('project'),
        domain = data.get('domain'),
        url = data.get('url'),
        code = data.get('code')
    )
    db.db.session.add(result)
    db.db.session.commit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        logging.error('No table specified.')
    elif sys.argv[1] == 'tomcat_url':
        logging.info('update table tomcat_url.')
        update_tomcat_url()
    elif sys.argv[1] == 'mail':
        logging.info('update table mail.')
        update_mail()
    else:
        logging.error('talbe %s doesn\'t exit.' %sys.argv[0])
