#1. 引入sql查询模块和数据处理模块。
import os
from dotenv import load_dotenv
import pymysql
import pandas as pd 
import numpy as np

# 在连接数据库之前添加
load_dotenv()

# 2. 向SQL数据库中输入登录账号和密码，连接数据库。
登录 = pymysql.connect(
    host=os.getenv("DB_HOST"),    # 输入存储数据的服务器地址
    port=int(os.getenv("DB_PORT")),  #服务器端口
    user=os.getenv("DB_USER"),         # 输入用户名
    password=os.getenv("DB_PASSWORD"),  # 输入密码
    database=os.getenv("DB_NAME"),   # 输入数据库的名字
    charset="utf8")       # 输入表格型号
执行 = 登录.cursor() 

# 用登录信息连接数据库
执行 = 登录.cursor() 

# 3. 编写SQL语句’select ... from ...‘
sql调用语句 ='select vbill_date,total_income from erp_fd_fundforecast where org_name="新兴化工材料有限公司" '
# 执行编写好的SQL语句
执行.execute(sql调用语句)
# 获取数据
数据=执行.fetchall() 

# 4.将数据以表格的形式存储在电脑内存中。
收入合计 = pd.DataFrame(数据,columns=['日期','收入合计'])
收入合计[['收入合计']] = 收入合计[['收入合计']].astype(float)
收入合计[['日期']] =收入合计[['日期']].astype(str)

# 5. 提交请求，关闭数据库连接，打印查看取得的数据明细。
登录.commit()
登录.close()
print(收入合计)

# 6. 保存为Excel文件
收入合计.to_excel('收入合计.xlsx')
