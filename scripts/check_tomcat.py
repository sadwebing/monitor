#!/usr/local/bin/python
#-_- coding:utf-8 -_-
import os,sys,smtplib,requests,datetime
sys.path.append(os.path.dirname(os.getcwd()))
from db import db
from manage import logging,basedir
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf8')

server = 'http://192.168.100.107:9990/tomcat_result'

def send_mail(to_list,sub,content):
    sender = 'monitor@ag866.com'
    msg = MIMEText(str(content),'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要  
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = sender
    msg['To'] = ';'.join(to_list)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('localhost')
        smtp.sendmail(sender, to_list, msg.as_string())
        logging.info('[success]mail from %s, mail to %s, %s' %(sender, to_list, content))
        smtp.quit()
        return True
    except Exception, e:
        logging.error('[failed]mail from %s, mail to %s, %s' %(sender, to_list, content))
        return False

tomcat_error_list = []
mail_list = []
result_list = []
code_list = ['200', '302', '405']
def get_mail_list(list_name):
    url_all = db.mail.query.all()
    for mail_info in url_all:
        if mail_info.status == 'active':
            list_name.append(mail_info.mail_address)
    #return mail_list
def check_tomcat():
    url_all = db.tomcat_url.query.all()
    for tomcat_info in url_all:
        result = {}
        result['time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        result['project'] = tomcat_info.project
        result['domain'] = tomcat_info.domain
        result['url'] = tomcat_info.url
        ret = requests.get(result['url'], headers={'Host': result['domain']})
        result['code'] = ret.status_code
        result['info'] = ''
        #print result['code']
        ret2 = requests.post(server, data=result)
        if result['code'] not in code_list:
            tomcat_error_list.append(result)
        logging.info(result)

if __name__ == '__main__':
    get_mail_list(mail_list)
    check_tomcat()
    #send_mail(mail_list,'tomcat_status',result_list)
