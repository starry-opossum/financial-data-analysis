import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 读取 Excel（基于当前脚本所在目录）
当前目录 = Path(__file__).parent
收入合计 = pd.read_excel(当前目录 / 'SQL调取结果.xlsx')
资产负债表 = pd.read_excel(当前目录 / '案例资源资产负债表.xlsx', sheet_name='资产负债表', index_col=0)

# 1. 收入数据预处理
收入合计['日期'] = pd.to_datetime(收入合计['日期'])
收入合计.set_index('日期', inplace=True)
季度收入合计 = 收入合计['收入合计'].resample('QE').sum()
年度收入合计 = 收入合计['收入合计'].resample('YE').sum()
pd.options.display.float_format = '{:.2f}'.format
季度收入 = pd.DataFrame(季度收入合计)
年度收入 = pd.DataFrame(年度收入合计)

# 2. 预测与增长率
模型 = ExponentialSmoothing(季度收入['收入合计'], trend='add', seasonal='add', seasonal_periods=4)
训练结果 = 模型.fit()
预测期 = 训练结果.forecast(4)
预测期数年度合计 = 预测期.sum()
基期收入 = 年度收入.at['2023-12-31', '收入合计']
增长率 = round((预测期数年度合计 - 基期收入) / 基期收入, 2)

# 3. 将收入数据插入资产负债表第一行
年度收入 = 年度收入[['收入合计']].T
年度收入.columns = 资产负债表.columns
资产负债表 = pd.concat([年度收入, 资产负债表])

# 4. 计算相关系数
资产负债表['相关系数'] =资产负债表.apply(lambda x: x.corr(年度收入.loc['收入合计']), axis=1)
资产负债表['增长率'] = 增长率

# 5. 判断敏感项目
def 判断敏感(项目):
    if abs(项目['相关系数']) > 0.8:
        项目['是否敏感'] = 1
    else:
        项目['是否敏感'] = 0
    return 项目

资产负债表 =资产负债表.apply(判断敏感, axis=1)
print("敏感项目识别结果：")
print(资产负债表)