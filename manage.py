#!/usr/bin/env python
from flask import Flask,request
import requests,logging
import os,sys
from db import db
app = db.app

@app.route('/curl_result', methods=['GET','POST'])
def curl_result():
    if request.method == 'POST':
        wr_to_db()
        return "success!"
    elif request.method == 'GET':
        return 'You get nothing!'
@app.route('/tomcat_result', methods=['GET','POST'])
def tomcat_result():
    if request.method == 'POST':
        update_check_tomcat()
        #wr_to_db()
        return "success!"
    elif request.method == 'GET':
        return 'You get nothing!'

def wr_to_db():
    data = request.get_data().decode('utf-8').split('&')
    data2 = request.form
    #data = request.form
    #info = eval(data)
    info="name is " + str(data2.get('name') + data2.get('age'))
    logging.info(info)
def update_check_tomcat():
    data = request.form 
    result = db.check_tomcat(
        access_time = "".join(data.getlist('time')),
        project     = "".join(data.getlist('project')),
        domain      = "".join(data.getlist('domain')),
        url         = "".join(data.getlist('url')),
        code        = "".join(data.getlist('code')),
        info        = "".join(data.getlist('info'))
    )
    db.db.session.add(result)
    db.db.session.commit()

if __name__ == '__main__':
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'), debug=app.debug)

