import pymysql


def sql(func):
    def wrapper(*args):
        conn = pymysql.connect(host='127.0.0.1', port=3306,
                               user='root', passwd='123456',
                               db='market', charset='utf8')
        cursor = conn.cursor()
        SQL = func(*args)
        cursor.execute(SQL)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return data
    return wrapper


@sql
def insert_into_user(username, password, limit):
    return "insert into user(user_name,user_password,user_limit) value('%s','%s',%s)" % (username, password, limit)


@sql
def select_user_id(username):
    return "select user_id from user where user_name='%s'" % username

@sql
def select_user_name(user_id):
    return "select user_name from user where user_id='%s'" % user_id

@sql
def select_user_password(username):
    return "select user_password from user where user_name='%s'" % username


@sql
def select_user_limit(user_id):
    return "select user_limit from user where user_id='%s'" % user_id

@sql
def update_user_limit(user_id):
    return "update user set user_limit = 3 where user_id = %s"% user_id


@sql
def select_user_all(user_id):
    return "select * from user where user_id = '%s'" % user_id


@sql
def update_user(user_id, what, new):
    return "update user set %s = '%s' where user_id = '%s'" % (what, new, user_id)


@sql
def insert_into_goods(name, info, price, reman_nums, class1, class2, class3, user_id):
    return "insert into goods(goods_name,goods_price,goods_reman_nums,info,goods_class1,goods_class2,goods_class3,user_id) value ('%s',%s,%s,'%s','%s','%s','%s',%s)" % (
        name, price, reman_nums, info, class1, class2, class3, user_id)

@sql
def select_new_good_id():
    return "select max(goods_id) from goods"

@sql
def select_all_goods(user_id):
    return "select * from goods where user_id = '%s'"%user_id

@sql
def select_one_goods(goods_id):
    return "select * from goods where goods_id = '%s'"%goods_id

@sql
def update_goods(goods_id,what,new):
    return "update goods set %s = '%s' where goods_id = '%s'" % (what, new, goods_id)

@sql
def delete_one_goods(goods_id):
    return "delete from goods where goods_id = %s"%goods_id

@sql
def update_user_balance(user_id,money):
    return "update user set user_balance = user_balance + %s where user_id = '%s'"%(money,user_id)

@sql
def select_user_balance(user_id):
    return "select user_balance from user where user_id = %s"%user_id

@sql
def select_goods():
    return "select goods_id,goods_name from goods"

@sql
def select_one_good_info(goods_id):
    return "select goods_name,info,goods_price,goods_reman_nums,goods_sold_num,goods_fra,user_name from goods,user where goods.user_id = user.user_id and goods_id = %s"%goods_id

@sql
def insert_into_shopping_car(user_id,good_id,order_num):
    return "insert into shopping_car(user_id,goods_id,shopping_num) value(%s,%s,%s)"%(user_id,good_id,order_num)

@sql
def show_shopping_car(user_id):
    return "select goods.goods_id,shopping_num,goods_name,goods_price,goods_reman_nums,goods.user_id,put_in_num from goods,shopping_car where shopping_car.user_id = %s and goods.goods_id = shopping_car.goods_id"%user_id


@sql
def update_shopping_num(put_in_num,new):
    return "update shopping_car set shopping_num = %s where put_in_num = %s"%(new,put_in_num)

@sql
def delete_one_shopping_car(put_in_num):
    return "delete from shopping_car where put_in_num = %s"%put_in_num

@sql
def update_goods_nums(goods_id,num):
    return "update goods set goods_reman_nums = goods_reman_nums - %s , goods_sold_num = goods_sold_num + %s where goods_id = '%s'"%(num,num,goods_id)


@sql
def select_goods_reman_nums(goods_id):
    return "select goods_reman_nums from goods where goods_id = %s"%goods_id

@sql
def delete_shopping_car(user_id):
    return "delete from shopping_car where user_id = %s"%user_id

@sql
def insert_into_shopped(user_id,goods_id,name,num,price):
    return "insert into shopped(user_id,goods_id,goods_name,goods_num,goods_price) value(%s,%s,'%s',%s,%s)"%(user_id,goods_id,name,num,price)

@sql
def select_shopped(user_id):
    return "select shopped.goods_id,shopped.goods_name,shopped.goods_num,shopped.goods_price,goods_word,goods_word_answer,goods_grade,orders_num,shopped_time from shopped,goods where shopped.goods_id = goods.goods_id and shopped.user_id = %s order by shopped_time desc"%user_id

@sql
def select_shopped2(orders):
    return "select shopped.goods_id,shopped.goods_name,goods_word,goods_word_answer,goods_grade from shopped,goods where shopped.goods_id = goods.goods_id and orders_num = %s" % orders

@sql
def update_shopped(orders,what,new):
    return "update shopped set %s = '%s' where orders_num = %s"%(what,new,orders)

@sql
def get_goods_fra(goods_id):
    return "select AVG(goods_grade) from shopped where goods_id = %s"%goods_id



@sql
def update_goods_fra(goods_id,goods_fra):
    return "update goods set goods_fra = %s where goods_id = %s"%(goods_fra,goods_id)

@sql
def select_shopped_by_seller(user_id):
    return "select user.user_name,shopped.goods_name,goods_word,goods_word_answer,orders_num,goods_num,shopped.goods_price,goods_grade from user,goods,shopped where goods.goods_id = shopped.goods_id and shopped.user_id = user.user_id and goods.user_id = %s"%user_id

@sql
def select_shopped_by_seller2(orders):
    return "select user.user_name,shopped.goods_name,goods_word,goods_word_answer,goods_num,shopped.goods_price,goods_grade from user,goods,shopped where goods.goods_id = shopped.goods_id and shopped.user_id = user.user_id and shopped.orders_num = %s" % orders

@sql
def select_goods_class(class_name):
    return "select goods_id,goods_name from goods where goods_class1 = '%s' or goods_class2 = '%s' or goods_class3 = '%s'"%(class_name,class_name,class_name)

@sql
def select_goods_by_key_words(key_word):
    return "select goods_id,goods_name from goods where goods_name like '%%%s%%' or goods_class1 like '%%%s%%' or goods_class2 like '%%%s%%' or goods_class3 like '%%%s%%'"%(key_word,key_word,key_word,key_word)

@sql
def select_goods_class1(goods_id):
    return "select goods_class1 from goods where goods_id = %s"%goods_id



@sql
def insert_into_recommend(user_id,goods_id,goods_type):
    return "insert into recommend(user_id,goods_id,goods_type) value(%s,%s,'%s')"%(user_id,goods_id,goods_type)


@sql
def select_recommend(user_id):
    return "select recommend.goods_id,browse_time,goods_name,info,goods_price,user.user_name from recommend,goods,user where recommend.goods_id = goods.goods_id and goods.user_id = user.user_id and recommend.user_id = %s order by browse_num desc"%user_id

@sql
def select_like_class(user_id):
    return "select goods_type from recommend where user_id = %s group by goods_type order by count(*) desc limit 2"%user_id


@sql
def select_goods_name(goods_id):
    return "select goods_name from goods where goods_id = %s"%goods_id

@sql
def select_table_user():
    return "select * from user"

@sql
def select_table_goods():
    return "select * from goods"

@sql
def delete_user(user_id):
    return "delete from user where user_id = %s"%user_id


