# coding:utf8
# 主路由文件
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/mybilibili"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"]=os.urandom(16)
app.debug = True
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 在app中注册蓝图 将蓝图添加到主app  蓝图就相当于分支的app
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


