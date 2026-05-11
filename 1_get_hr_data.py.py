# 1. 引入sql查询模块和数据处理模块。
import pymysql
import pandas as pd 
import numpy as np


# 2. 向SQL数据库中输入登录账号和密码，连接数据库。
# 注意：密码已脱敏，实际使用时请替换为真实密码或从环境变量读取
登录 = pymysql.connect(
    host="192.168.120.37",    # 输入存储数据的服务器地址
    port=3376,                 # 服务器端口
    user="component",          # 输入用户名
    password="YOUR_PASSWORD",  # 【已脱敏】请替换为真实密码
    database="sql_commonbiz",  # 输入数据库的名字
    charset="utf8"             # 输入表格型号
)
执行 = 登录.cursor() 


# 3. 编写SQL语句'select ... from ...'
# 从基本信息表中调取'证件号'，'所属部门'两列
sql调用语句 = 'select id_number,department from erp_hr_psndoc where org_name="新兴科技有限公司" '

# 执行编写好的SQL语句
执行.execute(sql调用语句)

# 获取数据
数据 = 执行.fetchall() 


# 4. 将数据以表格的形式存储在电脑内存中。
员工信息 = pd.DataFrame(数据, columns=['证件号', '所属部门'])


# 5. 提交请求，关闭数据库连接
登录.commit()
登录.close()
print(员工信息)


# 6. 保存为Excel文件
员工信息.to_excel('员工信息.xlsx')
