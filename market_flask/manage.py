from flask import Flask, request, render_template

from functions.sql_functions import select_user_name
from index import index_blue
from self_center import self_center_blue
from seller_only import seller_only_blue
from shop import shop_blue
from root_user import root_user_blue

import json
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket
from wrappers.login_or_logout import function


app = Flask(__name__)

app.register_blueprint(index_blue)
app.register_blueprint(self_center_blue)
app.register_blueprint(seller_only_blue)
app.register_blueprint(shop_blue)
app.register_blueprint(root_user_blue)

user_dict = {}

# 建立聊天室
@app.route('/ws/<username>')
@function
def ws_chat(username):
    user_socket = request.environ.get('wsgi.websocket') # type:WebSocket
    user_dict[username]=user_socket
    while 1:
        msg = user_socket.receive()  # 等待接收客户端发来的数据
        msg_dict = json.loads(msg)
        msg_dict['from_user'] = username
        to_user = msg_dict.get('to_user')
        if to_user == "":  # 如果用户名是空表示群发
            for uname, uwebsocket in user_dict.items():
                if uname == username:  # 群发时不用给自己发
                    continue
                uwebsocket.send(json.dumps(msg_dict))
            continue
        to_user_socket = user_dict.get(to_user)
        if not to_user_socket:  # 判断用户字典中是否存在用户的websocket连接
            continue
        try:
            msg_dict['from_user'] = msg_dict['from_user'] + '@私聊我'
            to_user_socket.send(json.dumps(msg_dict))
        except:
            user_dict.pop(to_user)

# 聊天
@app.route('/chat/')
@function
def chat():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    user_name = select_user_name(user_id)[0][0]
    print(user_name)
    return render_template('chat.html',contest={'user_name':user_name})

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()


