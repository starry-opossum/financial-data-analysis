# ------------------------------------前置任务脚本 ------------------------------------
import os
from dotenv import load_dotenv
import pandas as pd 
import numpy as np
# 在连接数据库之前添加
load_dotenv()
收入合计 = pd.read_excel('融资需求测算/SQL调取结果.xlsx')
# 1.将日期列转换为日期类型
收入合计['日期'] = pd.to_datetime(收入合计['日期'] )
收入合计.set_index('日期', inplace=True)  # 设置日期列为索引
# 2.按季度、年度进行分组并计算收入合计
季度收入合计 = 收入合计['收入合计'].resample('QE').sum()
年度收入合计 = 收入合计['收入合计'].resample('YE').sum()
# 3.调整显示效果，打印查看结果
pd.options.display.float_format = '{:.2f}'.format
季度收入 = pd.DataFrame(季度收入合计)
年度收入 = pd.DataFrame(年度收入合计)
# 4. 引入算法工具模块
from statsmodels.tsa.holtwinters import ExponentialSmoothing
# 5. 训练模型
霍尔特温特模型 = ExponentialSmoothing(季度收入['收入合计'], trend='add', seasonal='add', seasonal_periods=4)
训练模型 = 霍尔特温特模型.fit()
# 6. 预测
预测期 = 训练模型.forecast(4)
预测期数年度合计 = 预测期.sum()
# 7. 显示输出预测结果
# 8.计算营业收入增长率
基期收入 = 年度收入.at['2023-12-31', '收入合计']
增长率 = round((预测期数年度合计-基期收入)/基期收入,2) 


# ------------------------------------开始任务----------------------------------------------------------
# -------------------------------------任务8 Python 计算增长率 ------------------------------------

# 1. 读取案例资料中的资产负债表Excel文件。
资产负债表 = pd.read_excel('融资需求测算/案例资源资产负债表.xlsx',sheet_name='资产负债表',index_col=0)
print(资产负债表)


# 2. 将收入数据插入读取表格的第一行中
年度收入=年度收入[['收入合计']].T
年度收入.columns = 资产负债表.columns
资产负债表 = pd.concat([年度收入, 资产负债表])
print(资产负债表)


# 3. 计算相关系数
资产负债表['相关系数']=资产负债表.apply(lambda x:x.corr(年度收入.loc['收入合计']),axis=1)
资产负债表['增长率'] = 增长率
print(资产负债表.head(50))


# 4. 判断是否为敏感项目
def forcast(项目):
    if abs(项目['相关系数'])>0.8:
        项目['是否敏感']= 1
    else:
        项目['是否敏感']= 0
    return 项目
资产负债表=资产负债表.apply(forcast,axis=1)
print(资产负债表)
