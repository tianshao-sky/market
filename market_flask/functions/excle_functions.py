import pandas as pd
from io import BytesIO

from functions.sql_functions import select_table_user, select_table_goods


def user_excel():
    # 创建数据流
    output = BytesIO()
    # 创建excel work book
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    # 创建excel sheet
    sheet = workbook.add_worksheet('sheet1')


    sheet.write(0, 0, '用户ID')
    sheet.write(0, 1, '用户名')
    sheet.write(0, 2, '密码')
    sheet.write(0, 3, '身份（1卖家/2普通买家/3VIP买家）')
    sheet.write(0, 4, '余额')

    data_row = 1
    user = select_table_user()
    for i in user:
        sheet.write(data_row, 0, i[0])
        sheet.write(data_row, 1, i[1])
        sheet.write(data_row, 2, i[2])
        sheet.write(data_row, 3, i[3])
        sheet.write(data_row, 4, i[4])
        data_row = data_row + 1


    writer.close()
    output.seek(0)
    return output


def goods_excel():
    # 创建数据流
    output = BytesIO()
    # 创建excel work book
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    # 创建excel sheet
    sheet = workbook.add_worksheet('sheet1')

    sheet.write(0, 0, '商品ID')
    sheet.write(0, 1, '商品名')
    sheet.write(0, 2, '价额')
    sheet.write(0, 3, '库存')
    sheet.write(0, 4, '销量')
    sheet.write(0, 5, '商家ID')
    sheet.write(0, 6, '评分')
    sheet.write(0, 7, '类别1')
    sheet.write(0, 8, '类别2')
    sheet.write(0, 9, '类别3')
    sheet.write(0, 10, '简介')

    data_row = 1
    user = select_table_goods()
    for i in user:
        sheet.write(data_row, 0, i[0])
        sheet.write(data_row, 1, i[1])
        sheet.write(data_row, 2, i[2])
        sheet.write(data_row, 3, i[3])
        sheet.write(data_row, 4, i[4])
        sheet.write(data_row, 5, i[5])
        sheet.write(data_row, 6, i[6])
        sheet.write(data_row, 7, i[7])
        sheet.write(data_row, 8, i[8])
        sheet.write(data_row, 9, i[9])
        sheet.write(data_row, 10, i[10])

        data_row = data_row + 1

    writer.close()
    output.seek(0)
    return output
