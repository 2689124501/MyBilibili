#coding:utf8
from .import admin
from flask import render_template, url_for, redirect, session, flash
from flask import request
from app import db
from ..models import User, Admin
from werkzeug.security import generate_password_hash, check_password_hash

@admin.route('/')
def index():
    return render_template('admin/index.html')


# 登录
@admin.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error=None
        username = request.form['user']
        password = request.form['password']
        admin = Admin.query.filter_by(name=username).first()
        if admin is None:
            error = 'Incorrect username.'
        elif not admin.check_pwd(password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['admin_id'] = admin.id
            return redirect(url_for('admin.index'))

        flash(error)
    return render_template('admin/login.html')


@admin.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


@admin.route('/pwd/')
def pwd():
    return render_template('admin/pwd.html')


@admin.route('/tag/add/')
def tag_add():
    return render_template('admin/tag_add.html')

@admin.route('/tag/list/')
def tag_list():
    return render_template('admin/tag_list.html')

@admin.route('/movie/add/')
def movie_add():
    return render_template('admin/movie_add.html')


@admin.route('/movie/list/')
def movie_list():
    return render_template('admin/movie_list.html')



@admin.route('/user/list/')
def user_list():
    return render_template('admin/user_list.html')


@admin.route('/user/view/')
def user_view():
    return render_template('admin/user_view.html')

@admin.route('/comment/comment_list')
def comment_list():
    return render_template('admin/comment_list.html')


@admin.route('/collect/')
def collect():
    return render_template('admin/collect.html')


@admin.route('/oplog/list/')
def oplog_list():
    return render_template('admin/oplog_list.html')


@admin.route('/adminloginlog/list/')
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


@admin.route('/userlogin/list/')
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')
