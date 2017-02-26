#!/usr//bin/env python
#-_- coding:utf-8 -_-
import os,sys,logging
#sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
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
tomcat_project_list = []
mail_list = []
def get_list(filename, list_name):
    with open('%s/%s' %(current_dir,filename)) as f:
        lines = f.readlines()
    for line in lines:
        if line == '\n' or '#' in line:
            continue
        else:
            #print line.split('|')
            list_name.append(line.replace('\n', '').split('|'))

def update_tomcat_project():
    get_list('tomcat_project.txt', tomcat_project_list)
    info_list = db.tomcat_project.query.all()
    for info in info_list:
        db.db.session.delete(info)
    db.db.session.commit()
    db.db.engine.execute('alter table tomcat_project AUTO_INCREMENT=1; ')
    for tomcat_info in tomcat_project_list:
        if len(tomcat_info) != 6:
            continue
        else:
            inset = db.tomcat_project(product=tomcat_info[0], project=tomcat_info[1], tomcat=tomcat_info[2], main_port=tomcat_info[3], script=tomcat_info[4], jdk=tomcat_info[5])
            db.db.session.add(inset)
    db.db.session.commit()

def update_tomcat_url():
    get_list('tomcat_info.txt', tomcat_info_list)
    info_list = db.tomcat_url.query.all()
    for info in info_list:
        db.db.session.delete(info)
    db.db.session.commit()
    db.db.engine.execute('alter table tomcat_url AUTO_INCREMENT=1; ')
    for url_info in tomcat_info_list:
        if len(url_info) != 3:
            continue
        else:
            inset = db.tomcat_url(project=url_info[1], url=url_info[0],domain=url_info[2])
            db.db.session.add(inset)
    db.db.session.commit()

def update_mail():
    get_list('mail.txt', mail_list)
    info_list = db.mail.query.all()
    for info in info_list:
        db.db.session.delete(info)
    db.db.session.commit()
    db.db.engine.execute('alter table mail AUTO_INCREMENT=1; ')
    for mail_info in mail_list:
        if len(mail_info) != 4:
            continue
        else:
            inset = db.mail(name=mail_info[0], mail_address=mail_info[1], status=mail_info[2], role=mail_info[3])
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
    elif sys.argv[1] == 'tomcat_project':
        logging.info('update table tomcat_project.')
        update_tomcat_project()
    else:
        logging.error('talbe %s doesn\'t exit.' %sys.argv[0])
