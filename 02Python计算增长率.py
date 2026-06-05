import os
from dotenv import load_dotenv
import pandas as pd 
import numpy as np
# 加载环境变量
load_dotenv()

收入合计 = pd.read_excel('融资需求测算/SQL调取结果.xlsx')
# ------------------------------------开始任务 ------------------------------------

# ------------------------------------数据透视 ------------------------------------
# 1.将日期列转换为日期类型
收入合计['日期'] = pd.to_datetime(收入合计['日期'] )
收入合计.set_index('日期', inplace=True)  # 设置日期列为索引

# 2.按季度、年度进行分组并计算收入合计
# 按季度进行分组并计算收入合计
季度收入合计 = 收入合计['收入合计'].resample('QE').sum()
年度收入合计 = 收入合计['收入合计'].resample('YE').sum()

# 3.调整显示效果，打印查看结果
# 完整显示金额
pd.options.display.float_format = '{:.2f}'.format
季度收入 = pd.DataFrame(季度收入合计)
年度收入 = pd.DataFrame(年度收入合计)
print(季度收入)
print(年度收入)



# ------------------------------------霍尔特温特模型预测------------------------------------
# 4. 引入算法工具模块
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 5. 训练模型
霍尔特温特模型 = ExponentialSmoothing(季度收入['收入合计'], trend='add', seasonal='add', seasonal_periods=4)
训练模型 = 霍尔特温特模型.fit()


# 6. 预测
预测期 = 训练模型.forecast(4)
预测期数年度合计 = 预测期.sum()


# 7. 显示输出预测结果
print('预测期:',预测期)
print('预测期数年度合计:',预测期数年度合计)


# ------------------------------------计算营业收入增长率-----------------------------------
# 8.计算营业收入增长率
基期收入 = 年度收入.at['2023-12-31', '收入合计']
增长率 = round((预测期数年度合计-基期收入)/基期收入,2) 
print('增长率:',增长率)


