import time

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from app.sql_functions import *


# 主页
def index(request):
    ip_ = request.META.get('REMOTE_ADDR')
    get_cookie = request.COOKIES.get(ip_)
    page = request.GET.get('page')

    # 广告位商品
    goods_id1 = 10
    goods_id2 = 35
    goods_name1 = select_goods_name(goods_id1)[0][0]
    goods_name2 = select_goods_name(goods_id2)[0][0]
    goods_rand = select_goods()

    # 未登录
    if get_cookie == None:
        pages = 1 + len(goods_rand) // 15
        goods = dict(goods_rand[0:15])
        page_next = 2
        page_previous = 1

        if page != None:
            page = int(page)
            if page < pages:
                if page != 1:
                    goods = dict(goods_rand[(page - 1) * 15:page * 15])
                    page_next = page + 1
                    page_previous = page - 1
                else:
                    page_next = page + 1
                    page_previous = 1
            else:
                goods = dict(goods_rand[(page - 1) * 15:])
                page_next = page
                page_previous = page - 1
        else:
            page = 1
        return render(request, 'index.html', {'data': 1, 'goods': goods, 'pages': pages, 'page': page,
                                              'page_next': page_next, 'page_previous': page_previous,
                                              'ad_goods1': (goods_id1, goods_name1),
                                              'ad_goods2': (goods_id2, goods_name2)})

    # GET请求
    if request.method == 'GET':
        # 不是搜索
        if request.GET.get('key_word') == None:
            pages = 1 + len(goods_rand) // 15
            goods = dict(goods_rand[0:15])
            page_next = 2
            page_previous = 1

            if page != None:
                page = int(page)
                if page < pages:
                    if page != 1:
                        goods = dict(goods_rand[(page - 1) * 15:page * 15])
                        page_next = page + 1
                        page_previous = page - 1
                    else:
                        page_next = page + 1
                        page_previous = 1
                else:
                    goods = dict(goods_rand[(page - 1) * 15:])
                    page_next = page
                    page_previous = page - 1
            else:
                page = 1
            user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
            username = select_user_name(user_id)[0][0]
            return render(request, 'index.html', {'data': 2, 'username': username, 'goods': goods,
                                                  'pages': pages, 'page': page, 'page_next': page_next,
                                                  'page_previous': page_previous, 'ad_goods1': (goods_id1, goods_name1),
                                                  'ad_goods2': (goods_id2, goods_name2)})
        # 是搜索
        else:
            key_word = request.GET.get('key_word')
            pages = 1 + len(select_goods_by_key_words(key_word)) // 15
            goods = dict(select_goods_by_key_words(key_word)[0:15])
            page_next = 2
            page_previous = 1

            if page != None:
                page = int(page)
                if page < pages:
                    if page != 1:
                        goods = dict(select_goods_by_key_words(key_word)[(page - 1) * 15:page * 15])
                        page_next = page + 1
                        page_previous = page - 1
                    else:
                        page_next = page + 1
                        page_previous = 1
                else:
                    goods = dict(select_goods_by_key_words(key_word)[(page - 1) * 15:])
                    page_next = page
                    if page != 1:
                        page_previous = page - 1
            else:
                page = 1
                if page == pages:
                    page_next = 1
            user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
            username = select_user_name(user_id)[0][0]
            return render(request, 'index.html', {'data': 2, 'username': username, 'goods': goods,
                                                  'pages': pages, 'page': page, 'page_next': page_next,
                                                  'page_previous': page_previous, 'key_word': key_word,
                                                  'ad_goods1': (goods_id1, goods_name1),
                                                  'ad_goods2': (goods_id2, goods_name2)})

    # POST请求
    elif request.method == 'POST':
        key_word = request.POST.get('key_word')
        pages = 1 + len(select_goods_by_key_words(key_word)) // 15
        goods = dict(select_goods_by_key_words(key_word)[0:15])
        page_next = 2
        page_previous = 1

        if page != None:
            page = int(page)
            if page < pages:
                if page != 1:
                    goods = dict(select_goods_by_key_words(key_word)[(page - 1) * 15:page * 15])
                    page_next = page + 1
                    page_previous = page - 1
                else:
                    page_next = page + 1
                    page_previous = 1
            else:
                goods = dict(select_goods_by_key_words(key_word)[(page - 1) * 15:])
                page_next = page
                page_previous = page - 1
        else:
            page = 1
            if page == pages:
                page_next = 1
            user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
            username = select_user_name(user_id)[0][0]
            return render(request, 'index.html', {'data': 2, 'username': username, 'goods': goods,
                                                  'pages': pages, 'page': page, 'page_next': page_next,
                                                  'page_previous': page_previous, 'key_word': key_word,
                                                  'ad_goods1': (goods_id1, goods_name1),
                                                  'ad_goods2': (goods_id2, goods_name2)})

# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('UserName')
        password1 = request.POST.get('PassWord1')
        password2 = request.POST.get('PassWord2')
        limit = request.POST.get('limit')

        if username == '':
            return render(request, 'register.html', {'data': "用户名不能为空"})
        if password1 == '':
            return render(request, 'register.html', {'data': "密码不能为空"})
        if select_user_password(username) != ():
            return render(request, 'register.html', {'data': "用户已存在"})
        else:
            if password1 == password2:
                insert_into_user(username, password1, limit)
                return redirect('/login/')
            else:
                return render(request, 'register.html', {'data': "两次密码不一致"})

#登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('UserName')
        password = request.POST.get('PassWord')

        # 管理员
        if username == 'root' and password == 'root':
            response = redirect('/manage/')
            ip = request.META.get('REMOTE_ADDR')
            response.set_cookie(key=ip, value=('root'))
            return response

        # 判断密码是否正确，加cookie
        if password == select_user_password(username)[0][0]:
            user_id = select_user_id(username)
            response = redirect('/index/')
            ip = request.META.get('REMOTE_ADDR')
            response.set_cookie(key=ip, value=(user_id, password))
            return response
        else:
            return render(request, 'login.html', {'data': "用户名或者密码错误"})

# 装饰器，判断登录情况
def function(func):
    def wrapper(request):
        ip_ = request.META.get('REMOTE_ADDR')
        get_cookie = request.COOKIES.get(ip_)
        if get_cookie == None:
            return redirect('/index/')
        else:
            return func(request)

    return wrapper


@function
# 登出
def logout(request):
    response = redirect('/index/')
    ip = request.META.get('REMOTE_ADDR')
    response.delete_cookie(ip)
    return response


@function
# 个人中心
def self_center(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    limit = select_user_limit(user_id)[0][0]

    shopped_info = select_shopped(user_id)

    if limit == '1':  # 卖家
        goods_word = select_shopped_by_seller(user_id)
        all_money = 0
        for i in goods_word: # 销售金额的计算
            all_money += int(i[5]) * float(i[6])
        return render(request, 'self_center.html',
                      {'limit': 1, 'shopped_info': shopped_info, 'goods_word': goods_word, 'all_money': all_money})
    else:  # 买家
        return render(request, 'self_center.html', {'limit': int(limit), 'shopped_info': shopped_info})


@function
# 修改个人信息
def change_info(request):
    # GET 请求 不修改 返回数据库的内容
    if request.method == 'GET':
        ip_ = request.META.get('REMOTE_ADDR')
        user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
        user_info = select_user_all(user_id)[0]
        limit = select_user_limit(user_id)[0][0]

        return render(request, 'change_info.html', {'limit': int(limit),
                                                    'data': {'user_id': user_info[0], 'user_name': user_info[1],
                                                             'user_password': user_info[2],
                                                             'user_balance': user_info[4]}})
    # POST 请求 根据传入的值进行修改
    elif request.method == 'POST':
        ip_ = request.META.get('REMOTE_ADDR')
        user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
        new_username = request.POST.get('newUsername')
        new_password = request.POST.get('newPassword')
        limit = select_user_limit(user_id)[0][0]

        if new_password != None and new_password != '': # 密码
            update_user(user_id, 'user_password', new_password)
        if new_username != None and new_username != '': # 用户名
            update_user(user_id, 'user_name', new_username)
        # 修改完后 读取数据库
        user_info = select_user_all(user_id)[0]
        return render(request, 'change_info.html', {'limit': int(limit),
                                                    'data': {'user_id': user_info[0], 'user_name': user_info[1],
                                                             'user_password': user_info[2],
                                                             'user_balance': user_info[4]}})


@function
# 商品管理
def manage_goods(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    goods = select_all_goods(user_id)
    data = {}
    for i in goods:
        data[i[0]] = {'name': i[1], 'price': i[2], 'reman_num': i[3], 'sold_num': i[4], 'fra': i[6],
                      'class': i[7] + '/' + i[8] + '/' + i[9], 'info': i[10]}
    return render(request, 'manage_goods.html', {'data': data})


@function
# 增加商品
def add_goods(request):
    if request.method == 'GET':
        return render(request, 'add_goods.html')
    elif request.method == 'POST':
        ip_ = request.META.get('REMOTE_ADDR')
        user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
        goods_img = request.FILES.get('img')
        goods_name = request.POST.get('goods_name')
        info = request.POST.get('info')
        goods_price = request.POST.get('goods_price')
        goods_reman_nums = request.POST.get('goods_reman_nums')
        goods_class1 = request.POST.get('goods_class1')
        goods_class2 = request.POST.get('goods_class2')
        goods_class3 = request.POST.get('goods_class3')
        insert_into_goods(goods_name, info, goods_price, goods_reman_nums, goods_class1, goods_class2, goods_class3,
                          user_id)
        good_id = select_new_good_id()[0][0]
        # 保存卖家上传的商品图片
        if goods_img != None:
            with open('static/goods/' + str(good_id) + '.jpg', 'wb') as f:
                for line in goods_img:
                    f.write(line)

        return render(request, 'add_goods.html', {'data': '增加成功'})


@function
# 更改商品信息
def change_goods_num(request):
    goods_id = request.GET.get('id')
    if request.method == 'GET':
        goods_info = select_one_goods(int(goods_id))[0]
        return render(request, 'change_goods_num.html', {'name': goods_info[1], 'price': goods_info[2],
                                                         'reman_num': goods_info[3], 'sold_num': goods_info[4],
                                                         'class': goods_info[7] + '/' + goods_info[8] + '/' +
                                                                  goods_info[9],
                                                         'info': goods_info[10], 'goods_id': goods_id})
    elif request.method == 'POST':
        name = request.POST.get('newName')
        info = request.POST.get('newInfo')
        price = request.POST.get('newPrice')
        remen_nums = request.POST.get('newRemen_nums')

        # 根据传入的值进行更改
        if name != None and name != '': # 商品名
            update_goods(goods_id, 'goods_name', name)
        if info != None and info != '': # 简介
            update_goods(goods_id, 'info', info)
        if price != None and price != '': # 价格
            update_goods(goods_id, 'goods_price', price)
        if remen_nums != None and remen_nums != '': # 库存
            # 库存为0 即下架 删库
            if remen_nums == '0':
                delete_one_goods(goods_id)
                return redirect('/manage_goods/')
            else:
                update_goods(goods_id, 'goods_remen_nums', remen_nums)

        goods_info = select_one_goods(int(goods_id))[0]
        return render(request, 'change_goods_num.html', {'name': goods_info[1], 'price': goods_info[2],
                                                         'reman_num': goods_info[3], 'sold_num': goods_info[4],
                                                         'class': goods_info[7] + '/' + goods_info[8] + '/' +
                                                                  goods_info[9], 'info': goods_info[10],
                                                         'goods_id': goods_id})


@function
# 充值
def save_money(request):
    if request.method == 'GET':
        return render(request, 'save_money.html')
    elif request.method == 'POST':
        money = request.POST.get('money')
        if money.isdigit():
            ip_ = request.META.get('REMOTE_ADDR')
            user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]

            update_user_balance(user_id, money)
            return render(request, 'save_money.html', {'data': '充值成功'})
        else:
            return render(request, 'save_money.html', {'data': '输入内容不正确，请输入正整数金额！'})


@function
# 提现
def get_money(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    balance = select_user_balance(user_id)[0][0]

    if request.method == 'GET':
        return render(request, 'get_money.html', {'balance': balance})
    elif request.method == 'POST':
        money = request.POST.get('money')

        if money.isdigit(): # 限定提现金额只能为正整数
            if balance - int(money) >= 0:
                money = -int(money)
                update_user_balance(user_id, money)
                balance = select_user_balance(user_id)[0][0]
                return render(request, 'get_money.html', {'data': '提现成功', 'balance': balance})
            else:
                return render(request, 'get_money.html', {'data': '余额不足！', 'balance': balance})
        else:
            return render(request, 'get_money.html', {'data': '输入内容不正确，请输入正整数金额！', 'balance': balance})


@function
# 商品详情
def goods(request):
    goods_id = request.GET.get("id")
    goods_info = select_one_good_info(goods_id)[0]

    # 根据传入的商品ID进行展示商品

    if request.method == 'GET':
        # 浏览记录 写入数据库
        ip_ = request.META.get('REMOTE_ADDR')
        user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
        goods_class = select_goods_class1(goods_id)[0][0]
        insert_into_recommend(user_id, goods_id, goods_class)
        return render(request, 'goods.html', {"goods_id": goods_id, "goods_info": goods_info})
    elif request.method == 'POST':
        order_nums = request.POST.get('order_nums')
        if order_nums.isdigit(): # 限定数量为正整数
            if int(order_nums) <= goods_info[3]: # 判断库存量
                ip_ = request.META.get('REMOTE_ADDR')
                user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
                insert_into_shopping_car(user_id, goods_id, order_nums)
                data = '成功加入购物车'
            else:
                data = '商品库存不足'
        else:
            data = '输入格式有误，请输入正整数'
        return render(request, 'goods.html', {"goods_id": goods_id, "goods_info": goods_info, 'data': data})


@function
# 购物车
def shopping_car(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    goods_info = show_shopping_car(user_id)
    sum_money = 0

    if request.method == 'POST':
        dict_test = dict(request.POST)
        dict_test.pop('csrfmiddlewaretoken')
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
    return render(request, 'shopping_car.html', {'goods_info': goods_info, 'sum_money': sum_money, 'limit': limit})


@function
# 总金额的计算
def pay(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
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
        return render(request, 'pay.html', {'pay': money, 'balance': balance})
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
        return render(request, 'pay.html', {'pay': money, 'balance': balance, 'data': data})


@function
# 评价
def change_word(request):
    orders = request.GET.get('orders')
    shopped_info = select_shopped2(orders)[0]

    if request.method == 'POST':
        words = request.POST.get('words')
        grade = request.POST.get('grade')

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
    return render(request, 'change_word.html', {'orders': orders, 'shopped_info': shopped_info})


@function
# 商家回复
def change_word_answer(request):
    orders_num = request.GET.get('orders')
    shopped_info = select_shopped_by_seller2(orders_num)[0]

    if request.method == 'POST':
        word_answer = request.POST.get('word_answer')
        if word_answer != '' and word_answer != None:
            update_shopped(orders_num, 'goods_word_answer', word_answer)
        shopped_info = select_shopped_by_seller2(orders_num)[0]
    return render(request, 'change_word_answer.html', {'orders': orders_num, 'shopped_info': shopped_info})


@function
# 按类查询
def class_(request):
    if request.method == 'GET':
        class_name = request.GET.get('class_name')
        page = request.GET.get('page')
        pages = 1 + len(select_goods_class(class_name)) // 15

        goods = dict(select_goods_class(class_name)[0:15])
        page_next = 2
        page_previous = 1

        # GET 请求 展示 全部
        if page != None and page != '':
            page = int(page)
            if page < pages:
                if page != 1:
                    goods = dict(select_goods_class(class_name)[(page - 1) * 15:page * 15])
                    page_next = page + 1
                    page_previous = page - 1
                else:
                    page_next = page + 1
                    page_previous = 1
            else:
                goods = dict(select_goods_class(class_name)[(page - 1) * 15:])
                page_next = page
                page_previous = page - 1
        else:
            page = 1
        return render(request, 'class.html', {'class_name': class_name, 'goods': goods, 'page': page,
                                              'pages': pages, 'page_previous': page_previous, 'page_next': page_next})
    # POST 按类查找
    elif request.method == 'POST':
        class_name = request.POST.get('class_name')
        page = 1
        pages = 1 + len(select_goods_class(class_name)) // 15

        goods = dict(select_goods_class(class_name)[0:15])
        page_next = 2
        if page == pages:
            page_next = 1
        page_previous = 1
        return render(request, 'class.html', {'class_name': class_name, 'goods': goods, 'page': page,
                                              'pages': pages, 'page_previous': page_previous, 'page_next': page_next})


@function
# 浏览记录
def browse(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    browse_info = select_recommend(user_id)
    return render(request, 'browse.html', {'browse_info': browse_info})


@function
# 猜你喜欢
def guess(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    likes = select_like_class(user_id) # 根据浏览记录获取最高两类

    if len(likes) == 0: # 无浏览记录 默认推荐
        like_first = '手机'
        like_second = '电脑'
    elif len(likes) == 1: # 浏览记录只有一类 默认推荐
        like_first = likes[0][0]
        like_second = '手机'
    else:
        like_first = likes[0][0]
        like_second = likes[1][0]
    # 查最高两类的商品
    like_first_goods = select_goods_class(like_first)
    like_second_goods = select_goods_class(like_second)
    # 两类相加去重
    like_goods = tuple(set(like_first_goods + like_second_goods))

    page = request.GET.get('page')
    pages = 1 + len(like_goods) // 15

    goods = dict(like_goods[0:15])
    page_next = 2
    page_previous = 1
    # 分页
    if page != None and page != '':
        page = int(page)
        if page < pages:
            if page != 1:
                goods = dict(like_goods[(page - 1) * 15:page * 15])
                page_next = page + 1
                page_previous = page - 1
            else:
                page_next = page + 1
                page_previous = 1
                if pages == 1:
                    page_next = page
        else:
            goods = dict(like_goods[(page - 1) * 15:])
            page_next = page
            page_previous = page - 1
    else:
        page = 1
        if pages == 1:
            page_next = page
    return render(request, 'guess.html', {'goods': goods, 'page': page, 'pages': pages, 'page_previous': page_previous,
                                          'page_next': page_next})


@function
# 成为VIP
def VIP(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    balance = select_user_balance(user_id)[0][0]
    if request.method == 'GET':
        return render(request, 'VIP.html', {'balance': balance})
    elif request.method == 'POST':
        if float(balance) >= 998:
            update_user_balance(user_id, -998)
            update_user_limit(user_id)
            balance = select_user_balance(user_id)[0][0]
            data = '恭喜成为VIP'
        else:
            data = '余额不足'
        return render(request, 'VIP.html', {'balance': balance, 'data': data})


# 管理员页面
def manage(request):
    ip_ = request.META.get('REMOTE_ADDR')
    get_cookie = request.COOKIES.get(ip_)
    if get_cookie == 'root':
        user = select_table_user()
        goods = select_table_goods()
        return render(request, 'manage.html', {'user': user, 'goods': goods})

    else:
        return HttpResponse('404 Not Found')

# 删除用户
def del_user(request):
    if request.method == 'POST':
        dict_id = dict(request.POST)
        dict_id.pop('csrfmiddlewaretoken')
        for key in dict_id:
            delete_user(key)
        user = select_table_user()
        goods = select_table_goods()
        response = redirect('/manage/', {'user': user, 'goods': goods})
        return response
    else:
        return HttpResponse('404 Not Found')

# 删除商品
def del_goods(request):
    if request.method == 'POST':
        dict_id = dict(request.POST)
        dict_id.pop('csrfmiddlewaretoken')
        for key in dict_id:
            delete_one_goods(key)
        user = select_table_user()
        goods = select_table_goods()
        response = redirect('/manage/', {'user': user, 'goods': goods})
        return response
    else:
        return HttpResponse('404 Not Found')

@function
# 聊天室
def room(request):
    ip_ = request.META.get('REMOTE_ADDR')
    user_id = request.COOKIES.get(ip_).split("(")[3].split(',')[0]
    user_name = select_user_name(user_id)[0][0]
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return render(request, 'room.html', {'user_name':user_name,'data':times})
