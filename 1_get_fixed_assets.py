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
sql调用语句 = 'select vbill_date,fixed_assets_type,original_cost,accumulated_depreciation,cumulative_impairment,net_book_value from erp_fd_asset where org_name="新兴化肥有限公司" '

# 执行编写好的SQL语句
执行.execute(sql调用语句)

# 获取数据
数据 = 执行.fetchall() 


# 4. 将数据以表格的形式存储在电脑内存中
固定资产台账 = pd.DataFrame(
    数据, 
    columns=['当前期间', '固定资产类别', '原始成本', '累计折旧', '累计减值', '账面净值']
)
固定资产台账[['原始成本', '累计折旧', '累计减值', '账面净值']] = 固定资产台账[['原始成本', '累计折旧', '累计减值', '账面净值']].astype(float)


# 5. 提交请求，关闭数据库连接
登录.commit()
登录.close()
print(固定资产台账)


# 6. 保存为Excel文件
固定资产台账.to_excel('固定资产台账.xlsx')
