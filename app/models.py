# coding:utf8
# 数据模型 直接和数据库关联起来 面向对象 一个类相当于一个表
from datetime import datetime

from werkzeug.security import generate_password_hash

from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 会员编号
    username = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 用户评论外键关系关联
    moviecollects = db.relationship('MovieCollect', backref='user')  # 用户收藏电影外键关系关联

    def __repr__(self):
        return '<User %r>' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 用户日志
class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)  # 事件编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 会员编号
    ip = db.Column(db.String(100))  # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登陆时间

    def __repr__(self):
        return '<Userlog %r>' % self.id


# 电影标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    movies = db.relationship('Movie', backref='tag')  # 电影外键关系关联

    def __repr__(self):
        return '<Tag %r>' % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 播放地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    play_num = db.Column(db.SmallInteger)  # 播放量
    comment_num = db.Column(db.SmallInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签 外键
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时长
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('Comment', backref='movie')  # 用户评论外键关系关联
    moviecollects = db.relationship('MovieCollect', backref='movie')  # 用户收藏电影外键关系关联

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 用户评论电影
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影，在movie表中创建关联
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户，在user表中创建外键关联
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 用户收藏电影
class MovieCollect(db.Model):
    __tablename__ = 'moviecollect'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影，在movie表中创建关联
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户，在user表中创建外键关联
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<MovieCollect %r>" % self.id


class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 权限地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    auths = db.Column(db.String(600))  # 权限列表
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin', backref='role')  # 管理员外键关系关联，backref互相绑定role表

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否超级管理员 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('AdminLog', backref='admin')  # 管理员日志外键关系关联，backref互相绑定admin表
    operatelogs = db.relationship('OperateLog', backref='operatelog')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, input_pwd):
        """验证密码是否正确，直接将hash密码和输入的密码进行比较，如果相同则，返回True"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, input_pwd)


# 管理员日志
class AdminLog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class OperateLog(db.Model):
    __tablename__ = "operatelog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录ip
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "Operatelog %r" % self.id


# if __name__ == '__main__':
    # db.create_all()
    # role = Role(
    #     name="超级管理员",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()
    # admin = Admin(
    #     name="imoocmovie",
    #     pwd=generate_password_hash('imoocmovie'),
    #     is_super=0,
    #     role_id=1,
    # )
    # db.session.add(admin)
    # db.session.commit()
    # user = User(
    #     username='221801310',
    #     pwd = generate_password_hash('123456'),
    #     email = '2689124501@qq.com',
    #     phone = 13348555521,
    # )
    # db.session.add(user)
    # db.session.commit()