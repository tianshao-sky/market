from django.urls import path, re_path

from app import views, excle_functions

urlpatterns = [
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('self_center/',views.self_center,name='self_center'),
    path('change_info/',views.change_info,name='change_info'),
    path('manage_goods/',views.manage_goods,name='manage_goods'),
    path('add_goods/',views.add_goods,name='add_goods'),
    path('change_goods_num/',views.change_goods_num,name='change_goods_num'),
    path('save_money/',views.save_money,name='save_money'),
    path('get_money/',views.get_money,name='get_money'),
    path('goods/',views.goods,name='goods'),
    path('shopping_car/',views.shopping_car,name='shopping_car'),
    path('pay/',views.pay,name='pay'),
    path('change_word/',views.change_word,name='change_word'),
    path('change_word_answer/',views.change_word_answer,name='change_word_answer'),
    path('class/',views.class_,name='class_'),
    path('browse/',views.browse,name='browse'),
    path('guess/',views.guess,name='guess'),
    path('VIP/',views.VIP,name='VIP'),
    path('manage/',views.manage,name='manage'),
    path('user_excel/',excle_functions.user_excel,name='export_excel'),
    path('goods_excel/',excle_functions.goods_excel,name='goods_excel'),
    path('del_user/',views.del_user,name='del_user'),
    path('del_goods/',views.del_goods,name='del_goods'),
    path('chat/', views.room, name='room'),
]