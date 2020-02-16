# coding:utf8
# 定义视图
import functools
from . import home
from flask import render_template, url_for, redirect, session, flash, g
from flask import request
from ..models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/mybilibili"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.debug = True
db = SQLAlchemy(app)


# g是一个全局对象
# 这个函数，检查用户id是否已经存储在session中，并从数据库中获取用户数据，然后存储在g.user中
@home.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


# 定义一个装饰器
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('请先登录！')
            return redirect(url_for('home.login'))

        return view(**kwargs)

    return wrapped_view


# 首页
@home.route('/')
def index():
    return render_template("home/index.html")


# 登录
@home.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'Incorrect username.'
        elif not user.check_pwd(password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('home.index'))

        flash(error)
    return render_template("home/login.html")


# 注册
@home.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        email = request.form['email']
        phone = request.form['phone']
        if User.query.filter_by(username=username).first() is not None:
            error = '该账号 {} 已被注册。'.format(username)
        elif User.query.filter_by(email=email).first() is not None:
            error = '该邮箱 {} 已被注册。'.format(email)
        elif User.query.filter_by(phone=phone).first() is not None:
            error = '该手机号码 {} 已被注册。'.format(phone)
        elif (password != repassword):
            error = "两次密码不一致！"

        if error is None:
            # 在数据库中创建新用户
            new_user = User(
                username=username,
                pwd=generate_password_hash(password),
                email=email,
                phone=phone,
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home.login'))
        else:
            flash(error)
            return redirect(url_for('home.register'))

    return render_template('home/register.html')


@home.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for("home.index"))


# 用户中心 修改用户信息
@home.route('/user/', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        error = None
        n_name = request.form['name']
        n_email = request.form['email']
        n_phone = request.form['phone']
        n_face = request.files['face']
        n_info = request.form.get['info']
        my_user = User.query.filter_by(id=g.user['id']).first()
        # 检测是否已被注册
        if User.query.filter_by(username=n_name).first() is not None:
            error = '该账号 {} 已被注册，不可修改为该值。'.format(n_name)
        elif User.query.filter_by(email=n_email).first() is not None:
            error = '该邮箱 {} 已被注册，不可修改为该值。'.format(n_email)
        elif User.query.filter_by(phone=n_phone).first() is not None:
            error = '该手机号码 {} 已被注册，不可修改为该值。'.format(n_phone)
        if error is None:
            my_user.username = n_name
            my_user.email = n_email
            my_user.phone = n_phone
            my_user.face = n_face
            my_user.info = n_info
            db.commit(my_user)
            # 更新一下g中的user
            g.user = User.query.filter_by(id=g.user['id']).first()
            return redirect(url_for('home.user'))
        flash(error)
        return redirect(url_for('home.user'))
    return render_template('home/user.html')


@home.route('/pwd/')
@login_required
def pwd():
    return render_template('home/pwd.html')


@home.route('/comments/')
@login_required
def comments():
    return render_template('home/comments.html')


@home.route('/loginlog/')
@login_required
def loginlog():
    return render_template('home/loginlog.html')


@home.route('/collect/')
@login_required
def collect():
    return render_template('home/collect.html')


@home.route('/search/')
def search():
    return render_template('home/search.html')


@home.route('/play/')
def play():
    return render_template('home/play.html')


@home.route('/video/add/')
def video_add():
    return render_template('home/video_add.html')


@home.route('/movie/list/')
def movie_list():
    return render_template('home/movie_list.html')
