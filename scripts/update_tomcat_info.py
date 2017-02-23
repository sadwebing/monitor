#!/usr/local/bin/python
#-_- coding:utf-8 -_-
import os,sys
sys.path.append('/opt/monitor/monitor/monitor')
from db import db

#获取当前目录
basedir = os.path.abspath(os.path.dirname(__file__))
#print basedir

tomcat_info_list = []
with open('%s/tomcat_info.txt' %basedir) as f:
    lines = f.readlines()
for line in lines:
    if line == '\n' or '#' in line:
        continue
    else:
        #print line.split('|')
        tomcat_info_list.append(line.split('|'))

url_all = db.tomcat_url.query.all()
for url_info in url_all:
    db.db.session.delete(url_info)
    db.db.session.commit()

for url_info in tomcat_info_list:
    inset = db.tomcat_url(project=url_info[1], url=url_info[0],domain=url_info[2])
    db.db.session.add(inset)
    db.db.session.commit()

#url_all = db.tomcat_url.query.all()
#tomcat_info_db_list = []
#for url_info in url_all:
#    tomcat_info_db_list.append([url_info.url, url_info.project, url_info.domain])




