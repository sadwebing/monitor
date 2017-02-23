#!/bin/bash
source ~/.bash_profile
PATH=/sbin:/bin:/usr/sbin:/usr/bin

basedir=$(cd $(dirname $0); pwd)
md5_now=$(/usr/bin/md5sum ${basedir}/tomcat_info.txt |awk '{print $1}')

if [ -f ${basedir}/md5_1min.txt ];then
    md5_1min=$(cat ${basedir}/md5_1min.txt)
    #echo `date` 1 $md5_now $md5_1min >> /tmp/a.txt
else
    md5_1min=md5_now
    echo ${md5_now} > ${basedir}/md5_1min.txt
    #echo `date` 2 $md5_now $md5_1min >> /tmp/a.txt
fi

if [ "${md5_now}" != "${md5_1min}" ];then
    #echo `date` 3 $md5_now $md5_1min >> /tmp/a.txt
    /usr/local/bin/python ${basedir}/update_tomcat_info.py
    #echo `date` 4 $md5_now $md5_1min >> /tmp/a.txt
    echo ${md5_now} > ${basedir}/md5_1min.txt
    #echo `date` 5 $md5_now $md5_1min >> /tmp/a.txt
fi

