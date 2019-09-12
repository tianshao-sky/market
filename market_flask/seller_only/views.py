from flask import request, render_template, redirect
from wrappers.login_or_logout import function
from functions.sql_functions import *
from seller_only import seller_only_blue


# 商品管理
@seller_only_blue.route('/manage_goods/',methods=['GET','POST'])
@function
def manage_goods():
    ip_ = request.remote_addr
    user_id = request.cookies.get(ip_)
    goods = select_all_goods(user_id)
    data = {}
    for i in goods:
        data[i[0]] = {'name': i[1], 'price': i[2], 'reman_num': i[3], 'sold_num': i[4], 'fra': i[6],
                      'class': i[7] + '/' + i[8] + '/' + i[9], 'info': i[10]}
    return render_template('manage_goods.html', contest={'data': data})

# 增加商品
@seller_only_blue.route('/add_goods/',methods=['GET','POST'])
@function
def add_goods():
    if request.method == 'GET':
        return render_template('add_goods.html',contest={})
    elif request.method == 'POST':
        ip_ = request.remote_addr
        user_id = request.cookies.get(ip_)
        goods_img = request.form.get('img')
        goods_name = request.form.get('goods_name')
        info = request.form.get('info')
        goods_price = request.form.get('goods_price')
        goods_reman_nums = request.form.get('goods_reman_nums')
        goods_class1 = request.form.get('goods_class1')
        goods_class2 = request.form.get('goods_class2')
        goods_class3 = request.form.get('goods_class3')
        insert_into_goods(goods_name, info, goods_price, goods_reman_nums, goods_class1, goods_class2, goods_class3,
                          user_id)
        good_id = select_new_good_id()[0][0]
        # 保存卖家上传的商品图片
        if goods_img != None:
            with open('static/goods/' + str(good_id) + '.jpg', 'wb') as f:
                for line in goods_img:
                    f.write(line)

        return render_template('add_goods.html', contest={'data': '增加成功'})


# 更改商品信息
@seller_only_blue.route('/change_goods_num/',methods=['GET','POST'])
@function
def change_goods_num():
    goods_id = request.args.get('id')
    if request.method == 'GET':
        goods_info = select_one_goods(int(goods_id))[0]
        return render_template('change_goods_num.html', contest={'name': goods_info[1], 'price': goods_info[2],
                                                         'reman_num': goods_info[3], 'sold_num': goods_info[4],
                                                         'class': goods_info[7] + '/' + goods_info[8] + '/' +
                                                                  goods_info[9],
                                                         'info': goods_info[10], 'goods_id': goods_id})
    elif request.method == 'POST':
        name = request.form.get('newName')
        info = request.form.get('newInfo')
        price = request.form.get('newPrice')
        remen_nums = request.form.get('newRemen_nums')

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
        return render_template('change_goods_num.html', contest={'name': goods_info[1], 'price': goods_info[2],
                                                         'reman_num': goods_info[3], 'sold_num': goods_info[4],
                                                         'class': goods_info[7] + '/' + goods_info[8] + '/' +
                                                                  goods_info[9], 'info': goods_info[10],
                                                         'goods_id': goods_id})



# 商家回复
@seller_only_blue.route('/change_word_answer/',methods=['GET','POST'])
@function
def change_word_answer():
    orders_num = request.args.get('orders')
    shopped_info = select_shopped_by_seller2(orders_num)[0]

    if request.method == 'POST':
        word_answer = request.form.get('word_answer')
        if word_answer != '' and word_answer != None:
            update_shopped(orders_num, 'goods_word_answer', word_answer)
        shopped_info = select_shopped_by_seller2(orders_num)[0]
    return render_template('change_word_answer.html', contest={'orders': orders_num, 'shopped_info': shopped_info})

