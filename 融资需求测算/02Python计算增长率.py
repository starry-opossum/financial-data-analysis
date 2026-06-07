import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 读取 Excel（基于当前脚本所在目录）
当前目录 = Path(__file__).parent
收入合计 = pd.read_excel(当前目录 / 'SQL调取结果.xlsx')

# 1. 将日期列转换为日期类型
收入合计['日期'] = pd.to_datetime(收入合计['日期'])
收入合计.set_index('日期', inplace=True)

# 2. 按季度、年度进行分组并计算收入合计
季度收入合计 = 收入合计['收入合计'].resample('QE').sum()
年度收入合计 = 收入合计['收入合计'].resample('YE').sum()

# 3. 调整显示效果
pd.options.display.float_format = '{:.2f}'.format
季度收入 = pd.DataFrame(季度收入合计)
年度收入 = pd.DataFrame(年度收入合计)
print("季度收入合计：")
print(季度收入)
print("\n年度收入合计:")
print(年度收入)

# 4. 霍尔特温特模型预测
模型 = ExponentialSmoothing(季度收入['收入合计'], trend='add', seasonal='add', seasonal_periods=4)
训练结果 = 模型.fit()
预测期 = 训练结果.forecast(4)
预测期数年度合计 = 预测期.sum()

print("\n预测期(季度):")
print(预测期)
print(f"预测期年度合计：{预测期数年度合计:.2f}")

# 5. 计算营业收入增长率
基期收入 = 年度收入.at['2023-12-31', '收入合计']
增长率 = round((预测期数年度合计 - 基期收入) / 基期收入, 2)
print(f"营业收入增长率：{增长率}")