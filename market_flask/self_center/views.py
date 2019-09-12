from flask import request, render_template
from wrappers.login_or_logout import function
from functions.sql_functions import *
from self_center import self_center_blue

# 个人中心
@self_center_blue.route('/self_center/',methods=['GET','POST'])
@function
def self_center():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    limit = select_user_limit(user_id)[0][0]

    shopped_info = select_shopped(user_id)

    if limit == '1':  # 卖家
        goods_word = select_shopped_by_seller(user_id)
        all_money = 0
        for i in goods_word: # 销售金额的计算
            all_money += int(i[5]) * float(i[6])
        return render_template('self_center.html',contest=
                      {'limit': 1, 'shopped_info': shopped_info, 'goods_word': goods_word, 'all_money': all_money})
    else:  # 买家
        return render_template('self_center.html', contest={'limit': int(limit), 'shopped_info': shopped_info})


# 修改个人信息
@self_center_blue.route('/change_info/',methods=['GET','POST'])
@function
def change_info():
    # GET 请求 不修改 返回数据库的内容
    if request.method == 'GET':
        ip_ = request.remote_addr
        user_id = request.cookies.get(ip_)
        user_info = select_user_all(user_id)[0]
        limit = select_user_limit(user_id)[0][0]

        return render_template('change_info.html', contest={'limit': int(limit),
                                                    'data': {'user_id': user_info[0], 'user_name': user_info[1],
                                                             'user_password': user_info[2],
                                                             'user_balance': user_info[4]}})
    # POST 请求 根据传入的值进行修改
    elif request.method == 'POST':
        ip_ = request.remote_addr
        user_id = request.cookies.get(ip_)
        new_username = request.form.get('newUsername')
        new_password = request.form.get('newPassword')
        limit = select_user_limit(user_id)[0][0]

        if new_password != None and new_password != '': # 密码
            update_user(user_id, 'user_password', new_password)
        if new_username != None and new_username != '': # 用户名
            update_user(user_id, 'user_name', new_username)
        # 修改完后 读取数据库
        user_info = select_user_all(user_id)[0]
        return render_template('change_info.html', contest={'limit': int(limit),
                                                    'data': {'user_id': user_info[0], 'user_name': user_info[1],
                                                             'user_password': user_info[2],
                                                             'user_balance': user_info[4]}})


# 充值
@self_center_blue.route('/save_money/',methods=['GET','POST'])
@function
def save_money():
    if request.method == 'GET':
        return render_template('save_money.html',contest={})
    elif request.method == 'POST':
        money = request.form.get('money')
        if money.isdigit():
            ip_ = request.remote_addr
            user_id = request.cookies.get(ip_)

            update_user_balance(user_id, money)
            return render_template('save_money.html', contest={'data': '充值成功'})
        else:
            return render_template('save_money.html', contest={'data': '输入内容不正确，请输入正整数金额！'})

# 提现
@self_center_blue.route('/get_money/',methods=['GET','POST'])
@function
def get_money():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    balance = select_user_balance(user_id)[0][0]

    if request.method == 'GET':
        return render_template('get_money.html', contest={'balance': balance})
    elif request.method == 'POST':
        money = request.form.get('money')

        if money.isdigit(): # 限定提现金额只能为正整数
            if balance - int(money) >= 0:
                money = -int(money)
                update_user_balance(user_id, money)
                balance = select_user_balance(user_id)[0][0]
                return render_template('get_money.html', contest={'data': '提现成功', 'balance': balance})
            else:
                return render_template('get_money.html', contest={'data': '余额不足！', 'balance': balance})
        else:
            return render_template('get_money.html', contest={'data': '输入内容不正确，请输入正整数金额！', 'balance': balance})

# 评价
@self_center_blue.route('/change_word/',methods=['GET','POST'])
@function
def change_word():
    orders = request.args.get('orders')
    shopped_info = select_shopped2(orders)[0]

    if request.method == 'POST':
        words = request.form.get('words')
        grade = request.form.get('grade')

        # 评价
        if words != None and words != '':
            update_shopped(orders, 'goods_word', words)

        # 评分
        if grade != None and grade != '':
            goods_id = shopped_info[0]
            update_shopped(orders, 'goods_grade', grade)
            goods_fra = round(get_goods_fra(goods_id)[0][0], 2)
            update_goods_fra(goods_id, goods_fra)
        shopped_info = select_shopped2(orders)[0]
    return render_template('change_word.html', contest={'orders': orders, 'shopped_info': shopped_info})

# 浏览记录
@self_center_blue.route('/browse/',methods=['GET','POST'])
@function
def browse():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    browse_info = select_recommend(user_id)
    return render_template('browse.html', contest={'browse_info': browse_info})


# 成为VIP
@self_center_blue.route('/VIP/',methods=['GET','POST'])
@function
def VIP():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    balance = select_user_balance(user_id)[0][0]
    if request.method == 'GET':
        return render_template('VIP.html', contest={'balance': balance})
    elif request.method == 'POST':
        if float(balance) >= 998:
            update_user_balance(user_id, -998)
            update_user_limit(user_id)
            balance = select_user_balance(user_id)[0][0]
            data = '恭喜成为VIP'
        else:
            data = '余额不足'
        return render_template('VIP.html', contest={'balance': balance, 'data': data})

