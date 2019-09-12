from flask import request,redirect
import functools

# 判断登录情况
def function(func):
    @functools.wraps(func)
    def wrapper():
        ip_ = request.remote_addr
        get_cookie = request.cookies.get(ip_)
        if get_cookie == None:
            return redirect('/index/')
        else:
            return func()
    return wrapper