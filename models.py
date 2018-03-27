from exts import db
from datetime import  datetime

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    phone=db.Column(db.String(13),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)


class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    #now()写入程序第一次运行时间
    #now每次创建模型时间
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #反转,反向查找
    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #负号是代表倒序,
    question = db.relationship('Question',backref=db.backref('answers',order_by=('-create_time')))
    author = db.relationship('User',backref=db.backref('answers'))

