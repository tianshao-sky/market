from flask import request, render_template
from wrappers.login_or_logout import function
from functions.sql_functions import *
from shop import shop_blue


# 商品详情
@shop_blue.route('/goods/',methods=['GET','POST'])
@function
def goods():
    goods_id = request.args.get("id")
    goods_info = select_one_good_info(goods_id)[0]

    # 根据传入的商品ID进行展示商品

    if request.method == 'GET':
        # 浏览记录 写入数据库
        ip_ = request.remote_addr
        user_id = request.cookies.get(ip_)
        goods_class = select_goods_class1(goods_id)[0][0]
        insert_into_recommend(user_id, goods_id, goods_class)
        return render_template('goods.html', contest={"goods_id": goods_id, "goods_info": goods_info})
    elif request.method == 'POST':
        order_nums = request.form.get('order_nums')
        if order_nums.isdigit(): # 限定数量为正整数
            if int(order_nums) <= goods_info[3]: # 判断库存量
                ip_ = request.remote_addr
                user_id = request.cookies.get(ip_)
                insert_into_shopping_car(user_id, goods_id, order_nums)
                data = '成功加入购物车'
            else:
                data = '商品库存不足'
        else:
            data = '输入格式有误，请输入正整数'
        return render_template('goods.html', contest={"goods_id": goods_id, "goods_info": goods_info, 'data': data})


# 购物车
@shop_blue.route('/shopping_car/',methods=['GET','POST'])
@function
def shopping_car():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    goods_info = show_shopping_car(user_id)
    sum_money = 0

    if request.method == 'POST':
        dict_test = dict(request.form)
        # 调整购买数量
        for key, value in dict_test.items():
            if value[0] == '0': # 数量为0 即放弃购买 移除购物车
                delete_one_shopping_car(key)
            else:
                update_shopping_num(key, value[0])
        # 重新读取数据库
        goods_info = show_shopping_car(user_id)

    for i in goods_info: # 商品总金额的计算
        sum_money += i[1] * i[3]
    # VIP用户的判断
    limit = select_user_limit(user_id)[0][0]
    if limit == '3':
        sum_money = round(0.98 * sum_money, 2)
    return render_template('shopping_car.html', contest={'goods_info': goods_info, 'sum_money': sum_money, 'limit': limit})


# 总金额的计算
@shop_blue.route('/pay/',methods=['GET','POST'])
@function
def pay():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    balance = select_user_balance(user_id)[0][0]
    limit = select_user_limit(user_id)[0][0]

    goods_info = show_shopping_car(user_id)
    money = 0
    # 总金额的计算
    for i in goods_info:
        money += i[1] * i[3]
    # VIP的判断
    if limit == '3':
        money = round(0.98 * money, 2)

    if request.method == 'GET':
        return render_template( 'pay.html', contest={'pay': money, 'balance': balance})
    elif request.method == 'POST':
        if float(balance) >= float(money):
            goods_info = show_shopping_car(user_id)
            dict_pay = {} # 根据卖家的ID 计算支付金额
            dict_goods = {} # 根据商品ID 计算数量
            dict_price = {} # 商品的单价
            dict_name = {} # 商品的名称
            flag = 1 # 库存判断flag
            for i in goods_info:
                if select_goods_reman_nums(i[0])[0][0] >= i[1]: #库存判断，不足flag变为0
                    if dict_pay.get(str(i[5])):
                        dict_pay[str(i[5])] += i[3] * i[1]
                    else:
                        dict_pay[str(i[5])] = i[3] * i[1]

                    if dict_pay.get(str(i[0])):
                        dict_goods[str(i[0])] += i[1]
                    else:
                        dict_goods[str(i[0])] = i[1]
                        dict_price[str(i[0])] = i[3]
                        dict_name[str(i[0])] = i[2]

                else:
                    flag = 0
                    break

            if flag == 1: # 库存充足
                # 更改卖家余额
                for key, value in dict_pay.items():
                    update_user_balance(key, value)
                # 更改商品的库存
                for key, value in dict_goods.items():
                    update_goods_nums(key, value)
                    insert_into_shopped(user_id, key, dict_name[key], value, dict_price[key])

                # 更改买家余额
                update_user_balance(user_id, -1 * float(money))
                balance = select_user_balance(user_id)[0][0]
                money = 0
                delete_shopping_car(user_id)
                data = '支付成功'
            else:
                data = '库存不足'
        else:
            data = '余额不足，请充值'
        return render_template('pay.html', contest={'pay': money, 'balance': balance, 'data': data})


