# coding:utf-8
import os

DEBUG=True

SECRET_KEY=os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@127.0.0.1:3306/test_one?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

