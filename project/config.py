#encoding:utf8
import os
from datetime import timedelta

DEBUG=True
SEND_FILE_MAX_AGE_DEFAULT=timedelta(seconds=1)

SECRET_KEY='joiafidnoianiofjo'
PERMANENT_SESSION_LIFETIME=timedelta(hours=2)
DIALECT='mysql'
DRIVER='mysqldb'
USERNAME='root'
PASSWORD=''
HOST='127.0.0.1'
PORT='3306'
DATABASE='zhihu'

SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS=True
