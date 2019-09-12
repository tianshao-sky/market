from flask import request, render_template, redirect, send_file, url_for
from functions.sql_functions import *
from functions.excle_functions import *
from root_user import root_user_blue

# 管理员页面
@root_user_blue.route('/manage/',methods=['GET','POST'])
def manage():
    ip_ = request.remote_addr
    if request.cookies.get(ip_) == 'root':
        user = select_table_user()
        goods = select_table_goods()
        return render_template('manage.html', contest={'user': user, 'goods': goods})

    else:
        return '404 Not Found'

# 删除用户
@root_user_blue.route('/del_user/',methods=['GET','POST'])
def del_user():
    if request.method == 'POST':
        dict_id = dict(request.form)
        for key in dict_id:
            delete_user(key)
        return '删除成功'
    else:
        return '404 Not Found'

# 删除商品
@root_user_blue.route('/del_goods/',methods=['GET','POST'])
def del_goods():
    if request.method == 'POST':
        dict_id = dict(request.form)
        for key in dict_id:
            delete_one_goods(key)
        return '删除成功'
    else:
        return '404 Not Found'

@root_user_blue.route('/user_excel/',methods=['GET','POST'])
def user_excel_():
    output = user_excel()
    return send_file(output, attachment_filename="user.xlsx",
                     as_attachment=True)

@root_user_blue.route('/goods_excel/',methods=['GET','POST'])
def goods_excel_():
    output = goods_excel()
    return send_file(output, attachment_filename="goods.xlsx",
                     as_attachment=True)