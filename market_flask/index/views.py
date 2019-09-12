from flask import request, render_template, redirect
from wrappers.login_or_logout import function
from functions.sql_functions import *
from index import index_blue

# 主页
@index_blue.route('/',methods=['GET','POST'])
@index_blue.route('/index/',methods=['GET','POST'])
def index():
    ip_ = request.remote_addr
    get_cookie = request.cookies.get(ip_)
    page = request.args.get('page')

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
        return render_template('index.html', contest={'data': 1, 'goods': goods, 'pages': pages, 'page': page,
                                              'page_next': page_next, 'page_previous': page_previous,
                                              'ad_goods1': (goods_id1, goods_name1),
                                              'ad_goods2': (goods_id2, goods_name2)})

    # GET请求
    if request.method == 'GET':
        # 不是搜索
        if request.args.get('key_word') == None:
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

            user_id = request.cookies.get(ip_)
            username = select_user_name(user_id)[0][0]
            return render_template('index.html', contest={'data': 2, 'username': username, 'goods': goods,
                                                  'pages': pages, 'page': page, 'page_next': page_next,
                                                  'page_previous': page_previous, 'ad_goods1': (goods_id1, goods_name1),
                                                  'ad_goods2': (goods_id2, goods_name2)})
        # 是搜索
        else:
            key_word = request.args.get('key_word')
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
            user_id = request.cookies.get(ip_)
            username = select_user_name(user_id)[0][0]
            return render_template('index.html', contest={'data': 2, 'username': username, 'goods': goods,
                                                  'pages': pages, 'page': page, 'page_next': page_next,
                                                  'page_previous': page_previous, 'key_word': key_word,
                                                  'ad_goods1': (goods_id1, goods_name1),
                                                  'ad_goods2': (goods_id2, goods_name2)})

    # POST请求
    elif request.method == 'POST':
        key_word = request.form.get('key_word')
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
            user_id = request.cookies.get(ip_)
            username = select_user_name(user_id)[0][0]
            return render_template('index.html', contest={'data': 2, 'username': username, 'goods': goods,
                                                  'pages': pages, 'page': page, 'page_next': page_next,
                                                  'page_previous': page_previous, 'key_word': key_word,
                                                  'ad_goods1': (goods_id1, goods_name1),
                                                  'ad_goods2': (goods_id2, goods_name2)})

# 注册
@index_blue.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html',contest={})
    elif request.method == 'POST':
        username = request.form.get('UserName')
        password1 = request.form.get('PassWord1')
        password2 = request.form.get('PassWord2')
        limit = request.form.get('limit')

        if username == '':
            return render_template('register.html', contest={'data': "用户名不能为空"})
        if password1 == '':
            return render_template('register.html', contest={'data': "密码不能为空"})
        if select_user_password(username) != ():
            return render_template('register.html', contest={'data': "用户已存在"})
        else:
            if password1 == password2:
                insert_into_user(username, password1, limit)
                return redirect('/login/')
            else:
                return render_template('register.html', contest={'data': "两次密码不一致"})

# 登录
@index_blue.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',contest={})
    elif request.method == 'POST':
        username = request.form.get('UserName')
        password = request.form.get('PassWord')

        # 管理员
        if username == 'root' and password == 'root':
            response = redirect('/manage/')
            ip = request.remote_addr
            response.set_cookie(key=ip, value=('root'))
            return response

        # 判断密码是否正确，加cookie
        if password == select_user_password(username)[0][0]:
            user_id = select_user_id(username)[0][0]
            response = redirect('/index/')
            ip = request.remote_addr
            response.set_cookie(ip, str(user_id))
            return response
        else:
            return render_template('login.html', contest={'data': "用户名或者密码错误"})



# 登出
@index_blue.route('/logout/',methods=['GET','POST'])
@function
def logout():
    response = redirect('/index/')
    ip = request.remote_addr
    response.delete_cookie(ip)
    return response


# 按类查询
@index_blue.route('/class/',methods=['GET','POST'])
@function
def class_():
    if request.method == 'GET':
        class_name = request.args.get('class_name')
        page = request.args.get('page')
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
        return render_template('class.html', contest={'class_name': class_name, 'goods': goods, 'page': page,
                                              'pages': pages, 'page_previous': page_previous, 'page_next': page_next})
    # POST 按类查找
    elif request.method == 'POST':
        class_name = request.form.get('class_name')
        page = 1
        pages = 1 + len(select_goods_class(class_name)) // 15

        goods = dict(select_goods_class(class_name)[0:15])
        page_next = 2
        if page == pages:
            page_next = 1
        page_previous = 1
        return render_template( 'class.html', contest={'class_name': class_name, 'goods': goods, 'page': page,
                                              'pages': pages, 'page_previous': page_previous, 'page_next': page_next})


# 猜你喜欢
@index_blue.route('/guess/',methods=['GET','POST'])
@function
def guess():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)

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

    page = request.args.get('page')
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
    return render_template( 'guess.html', contest={'goods': goods, 'page': page, 'pages': pages, 'page_previous': page_previous,
                                          'page_next': page_next})