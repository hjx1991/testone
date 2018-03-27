from flask import Flask,render_template,redirect,url_for,request,session,g
from flask_bootstrap import  Bootstrap
from flask_moment   import  Moment
from datetime import datetime
from flask_wtf import FlaskForm,CSRFProtect
#如果输入的是字符串那么就用StringField,如果是整数那么就用IntegerField
from wtforms import StringField,IntegerField
#验证方式
from wtforms.validators import Length,EqualTo,InputRequired
from decorators import login_request
from models import *
from exts import  db
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
#表单验证
# CSRFProtect(app)
# class RegistForm(FlaskForm):
#     username = StringField(validators=[Length(min=3,max=10,message=u"用户名长度有问题")])
#     password = StringField(validators=[Length(min=6,max=20)])
#     age = IntegerField(validators=[InputRequired()])


@app.route('/')
def index():
    try:
        print('aaaaaa')
        context = {
        'questions': Question.query.order_by('-create_time').all()}
    except:
        context ={'name':'error'}
    print(context,type(context))
    if session.get('user_id') == None:
        return render_template('index.html',one = u'登录',two = u'注册',**context)
    else:
        return render_template('index.html',two =u'退出',**context)


@app.route('/user',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('user.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 设置session在31天都有效
            # session.permanent = True
            # return  render_template('indexed.html',user_name=user.username)
            return redirect(url_for('index'))
        else:
            return u'手机号码或密码错误!'


@app.route('/regist',methods=['POST','GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(phone,username,password,password2)
        try:
            user = User.query.filter(User.phone == phone).first()
        except:
            user =None
        print(user,'11111')
        if  user != None:
            return u'手机号码已注册,请重新输出新的号码！'
        elif password != password2:
            return u'两次密码不相同,请重新输入!'
        else:
            user = User(phone=phone, username=username, password=password2)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/send',methods=['POST','GET'])
@login_request
def send():
    if request.method == 'GET':
        return render_template('send.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        print(title,content)
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        print(type(user),user)
        question.author = user
        print(type(question.author),question.author)
        db.session.add(question)
        db.session.commit()
        return  redirect(url_for('index'))

@app.route('/add_answer/',methods=['POST'])
@login_request
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session['user_id']
    print(content,question_id,answer,user_id)
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id = question_id))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=question)

#错误页面
@app.errorhandler(404)
def  page_not_found(e):
    return render_template('404.html'),404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
