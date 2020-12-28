import pymysql
from PyQt5 import *
import sys
from PyQt5.QtWidgets import *
from login import *

#链接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='ssh_crud',
    charset='utf8')
cursor = conn.cursor()

#登陆
def sql_login(a, b):
    #定义变量
    value1 = (a,)
    value2 = (b,)
    table = ['admin', 'family_account_number', 'staff_account_number']
    flag = 0
    sql1 = "select id from admin"
    sql2 = "select id from family_account_number"
    sql3 = "select id from staff_account_number"

    #从数据库中查询信息
    cursor.execute(sql1)
    ret1 = cursor.fetchall()
    cursor.execute(sql2)
    ret2 = cursor.fetchall()
    cursor.execute(sql3)
    ret3 = cursor.fetchall()

    #判断登陆的用户的用户类型
    #超级管理员
    for myret1 in ret1:
        if value1 == myret1:
            flag = 1
            user = 0
            break
    #用户
    if flag == 0:
        for myret2 in ret2:
            if value1 == myret2:
                flag = 2
                user = 2
                break
    #普通管理员
    if flag == 0:
        for myret3 in ret3:
            if value1 == myret3:
                flag = 3
                user = 1
                break

    #查询并获取密码
    sql4 = "select password from " + table[flag-1] + " where(id = \'" + a + "\');"
    cursor.execute(sql4)
    ret = cursor.fetchone()

    #判断是否登陆成功
    conn.commit()
    if flag == 0:
        return 0, -1#用户名不存在
    if value2 == ret:
        return 2, user#登陆成功，user为整型值，0，1，2对应超级管理员，普通管理员，用户
    else:
        return 1, -1#密码错误


#修改密码
def sql_change_password(a, b, c, d):
    #定义变量
    cursor = conn.cursor()
    value1 = (a,)
    value2 = (b,)
    value3 = (c,)
    value4 = (d,)
    table_number = 0
    table = ['admin', 'family_account_number', 'staff_account_number']
    sql1 = "select id from admin"
    sql2 = "select id from family_account_number"
    sql3 = "select id from staff_account_number"

    #从数据库读取数据
    cursor.execute(sql1)
    ret1 = cursor.fetchall()
    cursor.execute(sql2)
    ret2 = cursor.fetchall()
    cursor.execute(sql3)
    ret3 = cursor.fetchall()

    #判断尝试登陆的是哪个用户
    for myret1 in ret1:
        if value1 == myret1 :
            table_number = 1
            break
    if table_number == 0:
        for myret2 in ret2:
            if value1 == myret2:
                table_number = 2
                break
    if table_number == 0:
        for myret3 in ret3:
            if value1 == myret3:
                table_number = 3
                break

    #寻找密码的mysql语句
    sql4 = "select password from " + table[table_number-1] + " where(id = \'" + a + "\');"

    #从数据库中寻找密码
    cursor.execute(sql4)
    ret = cursor.fetchone()

    #修改密码语句
    sql5 = "update " + table[table_number - 1] + " set password = \'" + c + "\' where id = \'" + a + "\';"

    #根据不同状态返回值
    if table_number == 0 :
        return 0 #用户名不存在
    if value2 != ret:
        return 1#密码错误
    if value2 == ret :
        if value3 == value4 :
            cursor.execute(sql5)
            conn.commit()
            return 3 #修改成功
        else:
            return 2 #密码不一致

#判断用户与普通管理员所在的小区
def sql_judge_h_e(a):#参数a为用户名
    # 查询用户所在小区,h_e_id为小区编号
    query_id0 = "select staff.h_e_id from staff,staff_account_number where " \
                "staff.id = staff_account_number.staff_id " \
                "and staff_account_number.staff_id = \'" + a + "\';"
    query_id1 = "select family.h_e_id from family,family_account_number where " \
                "family.id = family_account_number.f_id " \
                "and family_account_number.f_id = \'" + a + "\';"
    if a[0] == 's':
        cursor.execute(query_id0)
        h_e_id = cursor.fetchone()
    elif a[0] == 'f':
        cursor.execute(query_id1)
        h_e_id = cursor.fetchone()
    return h_e_id[0]

#查询小区信息
def sql_query_h_e(a, b):# a = 用户名 , b = 返回的身份。0，1，2对应超级管理员，普通管理员，用户
    print(1111)
    print(b)
    print(1111)
    #查询用户所在小区,h_e_id为小区编号
    query_id0 = "select staff.h_e_id from staff,staff_account_number where " \
                "staff.id = staff_account_number.staff_id " \
                "and staff_account_number.staff_id = \'" + a + "\';"
    query_id1 = "select family.h_e_id from family,family_account_number where " \
                "family.id = family_account_number.f_id " \
                "and family_account_number.f_id = \'" + a + "\';"

    if b == 0:
        h_e_id = ('0',)
    elif b == 1:
        cursor.execute(query_id0)
        h_e_id = cursor.fetchone()
    elif b == 2:
        cursor.execute(query_id1)
        h_e_id = cursor.fetchone()
    else:
        return -1, -1
    #定义sql查询语句

    sql0 = "select id, h_e_name, h_e_developer, h_e_area, h_e_staff, h_e_adress, h_e_family, h_e_parking, h_e_pet, h_e_building, h_e_car" \
           "from housing_estate;"
    sql1 = "select id,h_e_name,h_e_developer,h_e_area,h_e_staff,h_e_adress,h_e_family,h_e_parking,h_e_pet,h_e_building,h_e_car" \
           "from housing_estate where id = \'" + h_e_id[0] + "\';"
    sql2 = "select " \
           "h_e_name,h_e_adress,h_e_area,h_e_developer,h_e_staff,h_e_parking " \
           "from housing_estate where id = \'" + h_e_id[0] + "\';"

    #超级管理员
    if b == 0:
        cursor.execute(sql0)
        row = cursor.execute(sql0)
        ret = cursor.fetchall()
    #普通管理员
    elif b == 1:
        cursor.execute(sql1)
        row = cursor.execute(sql1)
        ret = cursor.fetchall()
    #用户
    elif b == 2:
        cursor.execute(sql2)
        row = cursor.execute(sql2)
        ret = cursor.fetchall()
    conn.commit()
    return ret, row

#用户查看自己的户主信息
def sql_query_f_people(a):#参数a为用户名
    sql = "select pname,psex,page,pphone,id from people where f_id = \'" + a + "\';"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchone()
    return ret, row
#用户查看自己的家庭信息
def sql_query_f_family(a):#参数a为用户名
    sql = "select id,family_number,car,parking,pet from family where id = \'" + a + "\';"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchone()
    return ret, row
#用户查看自己的宠物信息
def sql_query_f_pet(a):#参数a用户名
    #定义数据库查询语句
    sql = "select f_id,pet.id,variety,sex,age from pet,family where pet.f_id = family.id and family.id = \'" + a + "\';"
    cursor.execute(sql)
    ret = cursor.fetchall()
    row = cursor.execute(sql)
    conn.commit()
    #返回元组ret(若用户没有宠物则返回空元组)
    return ret, row
#用户查询车辆信息
def sql_query_f_car(a):#参数a用户名
    #定义数据库查询语句
    sql = "select car.id,color,brand,model from car,family where car.f_id = family.id and family.id = \'" + a + "\';"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row#返回元组ret(若用户没有车辆则返回空元组)
#用户查看自己的小区车位信息
def sql_query_f_parking(a):#参数a为用户名
    #定义数据库语句
    sql = "select housing_estate.h_e_adress,parking.adress from parking,housing_estate,family" \
          " where( housing_estate.id = (select family.h_e_id where family.id = \'" + a + "\') and parking.f_id = \'" + a + "\');"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    return ret, row#返回元组ret(若用户没有车辆则返回空元组)
#用户查看自己小区的员工信息
def sql_query_f_staff(a):#参数a为小区id
    sql = "select staff.id,s_name,staff_position,s_sex,s_age,wages,idcard,telephone " \
          "from staff,housing_estate " \
          "where( staff.h_e_id = housing_estate.id and staff.h_e_id = \'" + a + "\');"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row


#超级管理员选择小区
def sql_select_super_root_h_e(a):#参数a为用户输入的值
    sql1 = "select id from housing_estate where id = \'" + a[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone();
    if not x:
        return 0 #未找到对应的小区
    return x[0] #返回小区编号

#超级管理员查看所有小区
def sql_query_super_root_h_e():
    sql = "select h_e_name,id,h_e_adress from housing_estate;"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    return ret, row

#超级管理员添加小区查看所有小区信息
def sql_query_super_root_add_community():
    sql = "select id,h_e_name,h_e_developer,h_e_area,h_e_staff,h_e_adress," \
          "h_e_family,h_e_parking,h_e_pet,h_e_building,h_e_car " \
          "from housing_estate;"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    return ret, row

#超级管理员增加小区
def sql_add_super_root_h_e(a):#参数a为用户输入的值, 小区编号，小区地址，小区开发商，小区名，小区面积不能为空值，小区员工数量，
    #小区家庭数量，小区停车场数量，小区宠物数量，小区楼栋数量，小区车辆数量均默认为零且增加时不支持赋值
    column = ("id","h_e_name","h_e_developer","h_e_area","h_e_staff","h_e_adress",
              "h_e_family","h_e_parking","h_e_pet","h_e_building","h_e_car")
    temp = (a[0],a[5],a[2],a[3],a[8],a[6],a[10],a[4],a[9],a[7],a[1])
    sql2 = "select id from housing_estate where id = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    x = cursor.fetchone()
    conn.commit()
    if x:
        return 0  # 该小区已经存在
    sql1 = "insert into housing_estate values("
    for i in temp:
        if temp.index(i) == 3:
            if i != -1:
                sql1 = sql1 + str(i) + "0,"
            else:
                sql1 = sql1 + "0,"
        elif temp.index(i) == 5:
            if i != -1:
                sql1 = sql1 + str(i) + "0,"
            else:
                sql1 = sql1 + "0,"
        elif temp.index(i) == 6:
            sql1 = sql1 + "0,"
        elif temp.index(i) == 7:
            sql1 = sql1 + "0,"
        elif temp.index(i) == 8:
            sql1 = sql1 + "0,"
        elif temp.index(i) == 9:
            sql1 = sql1 + "0,"
        elif temp.index(i) == 4:
            sql1 = sql1 + "0,"
        elif temp.index(i) == 9:
            sql1 = sql1 + "0,"
        else :
            sql1 = sql1 + "\'" + i + "\',"
    sql1 = sql1[:-1] + ");"
    cursor.execute(sql1)
    conn.commit()
    return 1  # 成功插入


#超级管理员删除小区
def sql_del_super_root_h_e(a):#参数a为用户输入的值,其中小区编号不能为空
    sql1 = "select id from housing_estate where id = \'" + a[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 不存在该用户
    sql2 = "delete from housing_estate where id = \'" + a[0] + "\';"
    cursor.execute(sql2)
    conn.commit()
    return 1  # 删除成功




#管理员查看当前小区所有户主信息
def sql_query_root_people_owner(a):#参数a为小区id
    sql = "select people.f_id,people.pname,people.psex,people.page,people.id,people.pphone " \
          "from people,family where people.f_id = family.id and  family.h_e_id = \'" + a + "\';"
    print(sql)
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret ,row
#管理员根据检索值查看户主信息
def sql_query_root_p_search(a,b):#参数a为用户输入的索引值，参数b为小区id
    sql = "select f_id,pname,psex,page,people.id,pphone from " \
          "people,family where(people.f_id = family.id and family.h_e_id = \'" + b + "\' and "
    column = ("people.f_id","people.pname","people.psex","people.page","people.id","people.pphone")
    for i in a :
        if i != -1:
            if a.index(i) != 3 :
                x = a.index(i)
                sql = sql + column[x] + " = \'" + i + "\' and "
            elif a.index(i) == 3:
                x = a.index(i)
                sql = sql + column[x] + " = " + str(i) + " and "
    sql = sql[:-5]
    sql = sql + ' );'
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret ,row

#管理员查看当前小区所有楼栋信息
def sql_query_root_building(a):#参数a为小区id
    sql = "select building.id,building.b_adress,building.b_family,building.unit,building.floor,building.room " \
          "from building,housing_estate where building.h_e_id = housing_estate.id and housing_estate.id = \'" + a + "\';"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row
#管理员根据检索值查看当前小区的楼栋信息
def sql_query_root_b_search(a,b):#参数a为用户输入的索引值，参数b为小区id
    sql = "select building.id,b_adress,b_family,unit,floor,room " \
          "from building,housing_estate where(building.h_e_id = housing_estate.id " \
          "and housing_estate.id = \'" + b + "\' and "
    column = ("building.id", "building.b_adress", "building.b_family", "building.unit", "building.floor", "building.room")
    for i in a:
        if i != -1:
            if a.index(i) == 0 or a.index(i) == 1 :
                x = a.index(i)
                sql = sql + column[x] + " = \'" + i + "\' and "
            else :
                x = a.index(i)
                sql = sql + column[x] + " = " + str(i) + " and "
    sql = sql[:-5]
    sql = sql + ' );'
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row

#管理员查看当前小区停车位信息
def sql_query_root_parking(a):#参数a为小区编号
    sql = "select f_id,adress from parking where h_e_id = \'" + a + "\';"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row
#管理员根据检索值查看当前小区停车位信息
def sql_query_root_parking_search(a,b):#参数a为用户输入的索引值，参数b为小区id
    sql = "select f_id,adress from parking where( h_e_id = \'" + b + "\' and "
    column = ("f_id", "adress")
    for i in a:
        if i != -1:
            x = a.index(i)
            sql = sql + column[x] + " = \'" + i + "\' and "
    sql = sql[:-5]
    sql = sql + ' );'
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret,row

#管理员查看当前小区车辆信息
def sql_query_root_car(a):#参数a为小区id
    sql = "select car.id,f_id,color,brand,model from car,family " \
          "where( car.f_id = family.id and family.h_e_id = \'" + a + "\');"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row
#管理员根据检索值查看当前小区车辆信息
def sql_query_root_car_search(a,b):#参数a为用户输入的索引值，参数b为小区id
    sql = "select car.id,f_id,color,brand,model from car,family " \
          "where( car.f_id = family.id and family.h_e_id = \'" + b + "\' and "
    column = ("car.id", "f_id","color","brand","model")
    for i in a :
        if i != -1:
            x = a.index(i)
            sql = sql + column[x] + " = \'" + i + "\' and "
    sql = sql[:-5]
    sql = sql + ' );'
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row

#管理员查看当前小区所有的宠物信息
def sql_query_root_pet(a):#参数a为小区id
    sql = "select f_id,pet.id,variety,sex,age from pet,family " \
          "where( pet.f_id = family.id and family.h_e_id = \'" + a + "\');"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row
#管理员根据检索值查看当前小区的宠物信息
def sql_query_root_pet_search(a,b):#参数a为用户输入的索引值，参数b为小区id
    sql = "select f_id,pet.id,variety,sex,age from pet,family " \
          "where( pet.f_id = family.id and family.h_e_id = \'" + b + "\' and "
    column = ("f_id", "pet.id", "variety", "sex", "age")
    for i in a :
        if i != -1:
            if a.index(i) != 4:
                x = a.index(i)
                sql = sql + column[x] + " = \'" + i + "\' and "
            else :
                x = a.index(i)
                sql = sql + column[x] + " = " + str(i) + " and "
    sql = sql[:-5]
    sql = sql + ' );'
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row

#管理员查看当前小区的所有员工信息
def sql_query_root_staff(a):#参数a为小区id
    sql = "select staff.id,s_name,staff_position,s_sex,s_age,wages,idcard,telephone " \
          "from staff,housing_estate " \
          "where( staff.h_e_id = housing_estate.id and staff.h_e_id = \'" + a + "\');"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row
#管理员根据检索值查看当前小区的员工信息
def sql_query_root_staff_search(a,b):#参数a为用户输入的索引值，参数b为小区id
    sql = "select staff.id,s_name,staff_position,s_sex,s_age,wages,idcard,telephone " \
          "from staff,housing_estate " \
          "where( staff.h_e_id = housing_estate.id and staff.h_e_id = \'" + b + "\' and "
    column = ("staff.id", "s_name", "staff_position", "s_sex", "s_age","wages","idcard","telephone")
    for i in a :
        if i != -1:
            if a.index(i) == 4 or a.index(i) == 5:
                x = a.index(i)
                sql = sql + column[x] + " = " + str(i) + " and "
            else :
                x = a.index(i)
                sql = sql + column[x] + " = \'" + i + "\' and "
    sql = sql[:-5]
    sql = sql + ' );'
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row

#管理员查看当前小区的所有家庭信息
def sql_query_root_family(a):#参数a为小区id
    sql = "select family.id,family_number,car,parking,people,pet " \
          "from family,housing_estate " \
          "where(family.h_e_id = housing_estate.id and family.h_e_id = \'" + a + "\');"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row
#管理员根据检索值查看当前小区的家庭信息
def sql_query_root_family_search(a,b):#参数a为用户输入的索引值，参数b为小区id
    sql = "select family.id,family_number,car,parking,people,pet " \
          "from family,housing_estate " \
          "where(family.h_e_id = housing_estate.id and family.h_e_id = \'" + b + "\' and "
    column = ("family.id", "family_number", "car", "parking", "people", "pet")
    for i in a :
        if i != -1:
            if a.index(i) == 0 or a.index(i) == 1:
                x = a.index(i)
                sql = sql + column[x] + " = \'" + i + "\' and "
            else :
                x = a.index(i)
                sql = sql + column[x] + " = " + str(i) + " and "
    sql = sql[:-5]
    sql = sql + ' );'
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    conn.commit()
    return ret, row

#管理员查看小区信息
def sql_query_root_h_e_infor(a):#参数a为小区编号
    sql = "select id,h_e_name,h_e_developer,h_e_area,h_e_staff,h_e_adress," \
          "h_e_family,h_e_parking,h_e_pet,h_e_building,h_e_car " \
          "from housing_estate where id = \'" + a + "\';"
    cursor.execute(sql)
    row = cursor.execute(sql)
    ret = cursor.fetchall()
    return ret, row

#管理员根据用户输入的信息修改小区信息，只支持修改小区名，小区开发商，小区面积，小区地址
def sql_change_housing_estate(a): #参数a为用户输入的值 , 其中小区编号不能为空
    column = ("id", "h_e_name", "h_e_developer", "h_e_area", "h_e_staff", "h_e_adress",
              "h_e_family", "h_e_parking", "h_e_pet", "h_e_building", "h_e_car")
    temp = (a[0],a[5],a[2],a[3],a[8],a[6],a[10],a[4],a[9],a[7],a[1])
    column1 = (column[0],column[5],column[2],column[3],column[8],column[6],column[10]
               ,column[4],column[9],column[7],column[1])
    sql1 = "select id from housing_estate where id = \'" + a[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 不存在该小区
    sql2 = "update housing_estate set "
    for i in temp:
        if i != -1:
            if temp.index(i) != 0:
                if temp.index(i) == 1:
                    sql2 = sql2 + column1[temp.index(i)] + "= \'" + i + "\', "
                elif temp.index(i) == 2:
                    sql2 = sql2 + column1[temp.index(i)] + "= \'" + i + "\', "
                elif temp.index(i) == 10:
                    sql2 = sql2 + column1[temp.index(i)] + "= \'" + i + "\', "
                else:
                    sql2 = sql2 + column1[temp.index(i)] + " = " + str(i) + ", "
    sql2 = sql2[:-2] + " where id = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    conn.commit()
    return 1  # 修改成功



#管理员增加户主信息
def sql_add_people(a):#参数a为用户输入的值，a中，除年龄与电话外，其余均不能为空值，空值用-1表示
    column = ("people.f_id", "people.pname", "people.psex", "people.page", "people.id", "people.pphone")
    temp = (a[4], a[0], a[1], a[2], a[3], a[5])
    sql2 = "select family.id from family,people where people.f_id = family.id and people.f_id = \'" + temp[1] + "\';"
    cursor.execute(sql2)
    x = cursor.fetchone()
    if not x:
        return 0#找不到对应的家庭
    sql4 = "select people.id from people,family where people.f_id = family.id and people.f_id = \'" + temp[1] + "\';"
    cursor.execute(sql4)
    x = cursor.fetchone()
    if x :
        return 1#该家庭已经存在户主
    sql3 = "select id from people where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    x = cursor.fetchone()
    conn.commit()
    if x:
        return 2#该用户已经存在
    sql1 = "insert into people values("
    for i in temp:
        if temp.index(i) == 4:
            if i != -1:
                sql1 = sql1 + str(i) + ","
            else:
                sql1 = sql1 + "null,"
        elif temp.index(i) == 5:
            if i != -1:
                sql1 = sql1 + "\'" + i + "\',"
            else:
                sql1 = sql1 + "null,"
        else:
            sql1 = sql1 + "\'" + i + "\',"
    sql1 = sql1[:-1] + ");"
    cursor.execute(sql1)
    conn.commit()
    return 3#成功插入
#管理员删除户主信息
def sql_del_people(a):#参数a为用户输入的信息,其中身份证号不能为空
    print(a)
    column = ("people.f_id", "people.pname", "people.psex", "people.page", "people.id", "people.pphone")
    sql1 = "select id from people where id = \'" + a[4] + "\';"
    print(sql1)
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0#不存在该用户
    sql2 = "delete from people where id = \'" + a[4] + "\';"
    print(sql2)
    cursor.execute(sql2)
    conn.commit()
    return 1 #删除成功
#管理员根据输入的值修改户主信息
def sql_change_people(a):#参数a为用户输入的值,其中身份证号不能为空
    column = ("people.f_id", "people.pname", "people.psex", "people.page", "people.id", "people.pphone")
    temp = (a[4], a[0], a[1], a[2], a[3], a[5])
    sql1 = "select id from people where id = \'" + a[4] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  #不存在该用户
    if temp[1] != -1:
        sql2 = "select f_id from people where id = \'" + temp[0] + "\';"
        cursor.execute(sql2)
        x = cursor.fetchone()
        if x[0] != temp[1]:
            return 1  #不能修改家庭
    column1 = (column[4],column[0],column[1],column[2],column[3],column[5])
    sql3 = "update people set "
    for i in temp:
        if i != -1:
            if temp.index(i) != 0:
                if temp.index(i) == 4:
                    sql3 = sql3 + column1[temp.index(i)] + " = " + str(i) + ", "
                else:
                    sql3 = sql3 + column1[temp.index(i)] + "= \'" + i + "\', "
    sql3 = sql3[:-2] + " where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    conn.commit()
    return 2 #修改成功

#管理员增加车辆
def sql_add_car(a):#参数a为用户输入的值,其中除车型外均不能为空
    column = ("car.id", "f_id", "color", "brand", "model")
    sql1 = "select id from family where id = \'" + a[1] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    conn.commit()
    if not x:
        return 0  # 找不到对应的家庭
    sql2 = "select id from car where id = \'" + a[0] + "\';"
    cursor.execute(sql2)
    x = cursor.fetchone()
    if x:
        return 1  # 该车辆已经存在
    sql3 = "insert into car values("
    for i in a:
        if a.index(i) == 4:
            if i == -1:
                sql3 = sql3 + "null,"
            else :
                sql3 = sql3 + "\'" + i + "\',"
        else:
            sql3 = sql3 + "\'" + i + "\',"
    sql3 = sql3[:-1] + ");"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_car = h_e_car + 1 where id = " \
           "(select h_e_id from family,car where car.f_id = family.id and car.id = \'" + a[0] + "\');"
    cursor.execute(sql4)
    sql5 = "update family set car  = car + 1 where id = \'" + a[1] + "\';"
    cursor.execute(sql5)
    conn.commit()
    return 2  # 成功插入
#管理员删除车辆
def sql_del_car(a):#参数a为用户输入的值，其中车牌号不能为空
    sql1 = "select id from car where id = \'" + a[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0#该车辆不存在
    sql3 = "select f_id from car where id = \'" + a[0] + "\';"
    cursor.execute(sql3)
    y = cursor.fetchone()
    sql2 = "delete from car where id = \'" + a[0] + "\';"
    cursor.execute(sql2)
    sql4 = "update housing_estate set h_e_car = h_e_car - 1 where id = " \
           "(select h_e_id from family,car where car.f_id = family.id and car.id = \'"+ a[0] +"\');"
    cursor.execute(sql4)
    sql5 = "update family set car  = car - 1 where id = \'" + y[0] + "\';"
    cursor.execute(sql5)
    conn.commit()
    return 1#删除成功
#管理员根据用户输入的值修改车辆信息
def sql_change_car(a):#参数a为用户输入的值，其中车辆编号不能为空
    column = ("car.id", "f_id", "color", "brand", "model")
    sql1 = "select id from car where id = \'" + a[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    conn.commit()
    if not x:
        return 0  # 不存在该车辆
    if a[1] != -1:
        sql2 = "select f_id from car where id = \'" + a[0] + "\';"
        cursor.execute(sql2)
        x = cursor.fetchone()
        if x[0] != a[1]:
            return 1  # 不能修改家庭
    sql3 = "update car set "
    for i in a:
        if i != -1:
            if a.index(i) != 0:
                sql3 = sql3 + column[a.index(i)] + "= \'" + i + "\', "
    sql3 = sql3[:-2] + " where id = \'" + a[0] + "\';"
    cursor.execute(sql3)
    conn.commit()
    return 2  # 修改成功


#管理员增加宠物
def sql_add_pet(a):#参数a为用户输入的值,其中除年龄外均不能为空
    column = ("f_id","id","variety","sex","age")
    temp = (a[1],a[0],a[2],a[3],a[4])
    sql1 = "select id from pet where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    print(x)
    if x:
        return 0 #该宠物已经存在
    sql2 = "select id from family where id = \'" + temp[1] + "\';"
    cursor.execute(sql2)
    x = cursor.fetchone()
    if not x:
        return 1 #找不到对应的家庭
    sql3 = "insert into pet values("
    for i in temp:
        if temp.index(i) == 4:
            if i == -1:
                sql3 = sql3 + "null,"
            else :
                sql3 = sql3 + str(i) + ","
        else:
            sql3 = sql3 + "\'" + i + "\',"
    sql3 = sql3[:-1] + ");"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_pet = h_e_pet + 1 where id = " \
           "(select h_e_id from family,pet where pet.f_id = family.id and pet.id = \'" + temp[0] + "\');"
    cursor.execute(sql4)
    sql5 = "update family set pet = pet + 1 where id = \'" + temp[1] + "\';"
    cursor.execute(sql5)
    conn.commit()
    return 2  # 插入成功
#管理员删除宠物
def sql_del_pet(a):#参数a为用户输入的值，其中宠物编号不能为空
    column = ("f_id", "id", "variety", "sex", "age")
    temp = (a[1], a[0], a[2], a[3], a[4])
    sql1 = "select id from pet where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 该宠物不存在
    sql2 = "select f_id from pet where id = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    y = cursor.fetchone()
    sql3 = "delete from pet where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_pet = h_e_pet - 1 where id = " \
           "(select h_e_id from family,pet where pet.f_id = family.id and pet.id = \'"+ temp[0] +"\');"
    cursor.execute(sql4)
    sql5 = "update family set pet  = pet - 1 where id = \'" + y[0] + "\';"
    cursor.execute(sql5)
    conn.commit()
    return 1  # 删除成功
#管理员根据用户输入的值修改宠物信息
def sql_change_pet(a):#参数a为用户输入的值,其中宠物编号不能为空
    print('aaa')
    column = ("f_id", "id", "variety", "sex", "age")
    column1 = (column[1],column[0],column[2],column[3],column[4])
    temp = (a[1],a[0],a[2],a[3],a[4])
    sql1 = "select id from pet where id = \'" + a[1] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    conn.commit()
    if not x:
        return 0  # 不存在该宠物
    if a[0] != -1:
        sql2 = "select f_id from pet where id = \'" + a[1] + "\';"
        cursor.execute(sql2)
        x = cursor.fetchone()
        if x[0] != a[0]:
            return 1  # 不能修改家庭
    sql3 = "update pet set "
    for i in temp:
        if i != -1:
            if temp.index(i) != 0:
                if temp.index(i) != 4:
                    sql3 = sql3 + column1[temp.index(i)] + "= \'" + i + "\', "
                else:
                    sql3 = sql3 + column1[temp.index(i)] + "= " + str(i) + ", "
    sql3 = sql3[:-2] + " where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    conn.commit()
    return 2  # 修改成功


#管理员增加员工
def sql_add_staff(a,b):#参数a为用户输入的值，其中员工编号，姓名，性别不能为空，参数b为小区id
    column = ("id", "s_name","staff_position","s_sex","s_age","wages","idcard","telephone")
    column1 = (column[0],column[1],column[3],column[4],column[7],column[6],column[2],column[5])
    temp = (a[0],a[1],a[3],a[4],a[7],a[6],a[2],a[5])
    sql1 = "select id from staff where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if x:
        return 0  # 该员工已经存在
    sql3 = "insert into staff values("
    for i in temp:
        if temp.index(i) == 0:
            sql3 = sql3 + "\'" + i + "\',"
            sql3 = sql3 + "\'" + b + "\',"
        elif temp.index(i) == 1:
            sql3 = sql3 + "\'" + i + "\',"
        elif temp.index(i) == 2:
            sql3 = sql3 + "\'" + i + "\',"
        else :
            sql3 = sql3 + str(i) + ","
    sql3 = sql3[:-1] + ");"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_staff = h_e_staff + 1 where id = \'" + b + "\';"
    cursor.execute(sql4)
    conn.commit()
    return 1#插入成功
#管理员删除员工
def sql_del_staff(a):#参数a为用户输入的信息，其中员工编号不能为空
    column = ("id", "s_name", "staff_position", "s_sex", "s_age", "wages", "idcard", "telephone")
    column1 = (column[0], column[1], column[3], column[4], column[7], column[6], column[2], column[5])
    temp = (a[0], a[1], a[3], a[4], a[7], a[6], a[2], a[5])
    sql1 = "select id from staff where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 该员工不存在
    sql2 = "select h_e_id from staff where id = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    h_e_id = cursor.fetchone()
    sql3 = "delete from staff where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_staff = h_e_staff - 1 where id = \'" + h_e_id[0] + "\';"
    cursor.execute(sql4)
    conn.commit()
    return 1#修改成功
#管理员根据用户输入的值修改员工信息
def sql_change_staff(a):#参数a为用户输入的值，其中员工编号不能为空
    column = ("id", "s_name", "staff_position", "s_sex", "s_age", "wages", "idcard", "telephone")
    column1 = (column[0], column[1], column[3], column[4], column[7], column[6], column[2], column[5])
    temp = (a[0], a[1], a[3], a[4], a[7], a[6], a[2], a[5])
    sql1 = "select id from staff where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 该员工不存在
    sql3 = "update staff set "
    for i in temp:
        if i != -1:
            if temp.index(i) != 0:
                if temp.index(i) != 3:
                    sql3 = sql3 + column1[temp.index(i)] + "= \'" + i + "\', "
                elif temp.index(i) != 7:
                    sql3 = sql3 + column1[temp.index(i)] + "= \'" + i + "\', "
                else:
                    sql3 = sql3 + column1[temp.index(i)] + "= " + str(i) + ", "
    sql3 = sql3[:-2] + " where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    conn.commit()
    return 2  # 修改成功


#管理员增加停车位
def sql_add_parking(a, b):#参数a为用户输入的值，其中地址不能为空，参数b为小区编号
    print(a, b)
    column = ("f_id", "adress")
    temp = (a[1], a[0])
    sql1 = "select adress from parking where adress = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if x:
        return 0  # 该停车位已经存在
    print(1)
    sql3 = "insert into parking values("
    for i in temp:
        if temp.index(i) == 0:
            sql3 = sql3 + "\'" + i + "\',"
            sql3 = sql3 + "\'" + b + "\',"
        elif temp.index(i) == 1:
            if i != -1:
                sql3 = sql3 + "\'" + i + "\',"
            else:
                sql3 = sql3 + "null,"
    sql3 = sql3[:-1] + ");"
    print(sql3)
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_parking = h_e_parking + 1 where id = \'" + b + "\';"
    cursor.execute(sql4)
    if temp[1] != -1:
        sql5 = "update family set parking = parking + 1 where id = \'" + temp[1] + "\';"
        cursor.execute(sql5)
    conn.commit()
    return 1  # 插入成功
#管理员删除停车位
def sql_del_parking(a):#参数a为用户输入的值，其中地址不能为空
    column = ("f_id", "adress")
    temp = (a[1], a[0])
    sql1 = "select adress from parking where adress = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 该停车位不存在
    sql2 = "select h_e_id from parking where adress = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    x = cursor.fetchone()
    sql5 = "select f_id from parking where adress = \'" + temp[0] + "\';"
    cursor.execute(sql5)
    y = cursor.fetchone()
    sql3 = "delete from parking where adress = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_parking = h_e_parking - 1 where id = \'" + x[0] + "\'"
    cursor.execute(sql4)
    sql6 = "update family set parking = parking - 1 where id = \'" + y[0] + "\'"
    cursor.execute(sql6)
    conn.commit()
    return 1  # 删除成功
#管理员修改停车位信息
def sql_change_parking(a):#参数a为用户输入的值，其中地址不能为空
    column = ("f_id", "adress")
    column1 = (column[1],column[0])
    temp = (a[1], a[0])
    sql = "select adress from parking where adress = \'" + temp[0] + "\';"
    cursor.execute(sql)
    x = cursor.fetchone()
    if not x:
        return 0#未找到该停车位
    sql1 = "update parking set f_id = \'" + temp[1] + "\' where adress = \'" + temp[0] + "\';"
    sql2 = "select f_id from parking where adress = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    old_f_id = cursor.fetchone()
    cursor.execute(sql1)
    cursor.execute(sql2)
    new_f_id = cursor.fetchone()
    print(old_f_id,new_f_id)
    if old_f_id[0] !=None:
        sql3 = "update family set parking = parking - 1 where id = \'" + old_f_id[0] + "\';"
        cursor.execute(sql3)
    if new_f_id[0] != None:
        sql3 = "update family set parking = parking + 1 where id = \'" + new_f_id[0] + "\';"
        cursor.execute(sql3)
    conn.commit()
    return 1#修改成功



#管理员增加楼栋
def sql_add_building(a,b):#参数a为用户输入的值其中房产编号和房产地址不能为空，参数b为小区编号
    column = ("id", "b_adress", "b_family", "unit", "floor","room")
    temp = (a[0], a[1], a[2], a[4], a[3],a[5])
    sql1 = "select id from building where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if x:
        return 0  # 该楼栋已经存在
    sql3 = "insert into building values("
    for i in temp:
        if temp.index(i) == 0:
            sql3 = sql3 + "\'" + i + "\',"
            sql3 = sql3 + "\'" + b + "\',"
        elif temp.index(i) == 1:
            sql3 = sql3 + "\'" + i + "\',"
        else:
            if i == -1:
                sql3 = sql3 + "null,"
            else:
                sql3 = sql3 + str(i) + ","
    sql3 = sql3[:-1] + ");"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_building = h_e_building + 1 where id = \'" + b + "\';"
    cursor.execute(sql4)
    conn.commit()
    return 1 #插入成功
#管理员删除楼栋
def sql_del_building(a):#参数a为用户输入的值，其中房产编号不能为空
    column = ("id", "b_adress", "b_family", "unit", "floor", "room")
    temp = (a[0], a[1], a[2], a[4], a[3], a[5])
    sql1 = "select id from building where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 该楼栋不存在
    sql2 = "select h_e_id from building where id = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    x = cursor.fetchone()
    sql3 = "delete from building where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_building = h_e_building - 1 where id = \'" + x[0] + "\'"
    cursor.execute(sql4)
    conn.commit()
    return 1  # 删除成功
#管理员根据用户输入的值修改楼栋信息
def sql_change_building(a):#参数a为用户输入的值，其中房产编号不能为空且住户数量不支持修改
    column = ("id", "b_adress", "b_family", "unit", "floor", "room")
    column1 = (column[0],column[1],column[2],column[4],column[3],column[5])
    temp = (a[0], a[1], a[2], a[4], a[3], a[5])
    sql = "select id from building where id = \'" + temp[0] + "\';"
    cursor.execute(sql)
    x = cursor.fetchone()
    if not x:
        return 0  # 未找到该楼栋
    sql3 = "update building set "
    for i in temp:
        if i != -1:
            if temp.index(i) != 0:
                if temp.index(i) == 1:
                    sql3 = sql3 + column1[temp.index(i)] + "= \'" + i + "\', "
                else:
                    sql3 = sql3 + column1[temp.index(i)] + "= " + str(i) + ", "
    sql3 = sql3[:-2] + " where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    conn.commit()
    return 2  # 修改成功



#管理员增加家庭
def sql_add_family(a,b):#参数a为用户输入的值，其中家庭编号，门牌号不能为空，参数b为字符串类型的小区编号
    column = ("id", "family_number", "car","parking", "people", "pet")
    temp = (a[0],a[1],a[3],a[5],a[4],a[2])
    sql1 = "select id from family where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if x:
        return 0  # 该小区已经存在
    sql3 = "insert into family values("
    for i in temp:
        if temp.index(i) == 2:
            if i == -1:
                sql3 = sql3 + "null,"
            else :
                sql3 = sql3 + str(i) + ","
        elif temp.index(i) == 3:
            if i == -1:
                sql3 = sql3 + "null,"
            else :
                sql3 = sql3 + str(i) + ","
        elif temp.index(i) == 4:
            if i == -1:
                sql3 = sql3 + "null,"
            else :
                sql3 = sql3 + str(i) + ","
        elif temp.index(i) == 5:
            if i == -1:
                sql3 = sql3 + "null,"
            else :
                sql3 = sql3 + str(i) + ","
        elif temp.index(i) == 0:
            sql3 = sql3 + "\'" + i + "\',"
            sql3 = sql3 + "\'" + b + "\',"
        else:
            sql3 = sql3 + "\'" + i + "\',"
    sql3 = sql3[:-1] + ");"
    cursor.execute(sql3)
    sql4 = "update housing_estate set h_e_family = h_e_family + 1 where id = \'" + b + "\';"
    cursor.execute(sql4)
    conn.commit()
    return 1  # 插入成功
#管理员删除家庭
def sql_del_family(a):#参数a为用户输入的值，其中家庭编号不能为空,当前仅当该家庭除门牌号外的值为空时可以删除
    column = ("id", "family_number", "car", "parking", "people", "pet")
    column1 = (column[0], column[1], column[3], column[5], column[4], column[2])
    temp = (a[0], a[1], a[3], a[5], a[4], a[2])
    sql1 = "select id from family where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 该家庭不存在
    sql2 = "select car from family where id = \'" + temp[0] + "\';"
    sql3 = "select parking from family where id = \'" + temp[0] + "\';"
    sql4 = "select people from family where id = \'" + temp[0] + "\';"
    sql5 = "select pet from family where id = \'" + temp[0] + "\';"
    sql8 = "select h_e_id from family where id = \'" + temp[0] + "\';"
    cursor.execute(sql2)
    car = cursor.fetchone()
    cursor.execute(sql3)
    parking = cursor.fetchone()
    cursor.execute(sql4)
    people = cursor.fetchone()
    cursor.execute(sql5)
    pet = cursor.fetchone()
    cursor.execute(sql8)
    h_e_id = cursor.fetchone()
    if car[0] == 0:
        if parking[0] == 0:
            if people[0] == 0:
                if pet[0] == 0:
                    sql6 = "delete from family where id = \'" + temp[0] + "\';"
                    cursor.execute(sql6)
                    sql7 = "update housing_estate set h_e_family = family - 1 where id = \'" + h_e_id + "\';"
                    cursor.execute(sql7)
                    conn.commit()
                    return 2#删除成功
                else:
                    return 1 #不合法删除
            else:
                return 1  # 不合法删除
        else:
            return 1  # 不合法删除
    else:
        return 1  # 不合法删除
#管理员根据用户输入的值修改家庭信息
def sql_change_family(a):#参数a为用户输入的值，其中家庭编号不能为空且仅支持修改门牌号与家庭成员数量
    print('aaaaaa')
    print(a)
    column = ("id", "family_number", "car", "parking", "people", "pet")
    column1 = (column[0],column[1],column[3],column[5],column[4],column[2])
    temp = (a[0], a[1], a[3], a[5], a[4], a[2])
    sql1 = "select id from family where id = \'" + temp[0] + "\';"
    cursor.execute(sql1)
    x = cursor.fetchone()
    if not x:
        return 0  # 该家庭不存在
    for i in temp:
        if i != -1:
            if temp.index(i) != 0:
                if temp.index(i) == 1:
                    sql3 = sql3 + column1[temp.index(i)] + "= \'" + i + "\', "
                elif temp.index(i) == 4:
                    sql3 = sql3 + column1[temp.index(i)] + "= " + str(i) + ", "
    sql3 = sql3[:-2] + " where id = \'" + temp[0] + "\';"
    cursor.execute(sql3)
    conn.commit()
    return 2  # 修改成功