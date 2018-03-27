from functools import wraps
from flask import redirect,url_for,session
#登录限制装饰器
def login_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #切记这里不能用 session['user_id'],当值为空就报错。
        #if session['user_id']:
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper