# coding:utf8
from flask import Blueprint
# 创建蓝图，然后通过注册的方法，将蓝图添加到主app中
home = Blueprint("home", __name__)

import app.home.views