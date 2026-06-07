# ------------------------------------前置任务脚本 ------------------------------------
import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pyecharts.charts import Line
import pyecharts.options as opts
from pyecharts.globals import ThemeType, CurrentConfig

# 设置 CDN（解决图表空白问题）
CurrentConfig.ONLINE_HOST = "https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/"

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

# 4. 敏感项目判断
资产负债表['相关系数'] =资产负债表.apply(lambda x: x.corr(年度收入.loc['收入合计']), axis=1)
资产负债表['是否敏感'] = (abs(资产负债表['相关系数']) > 0.8).astype(int)
资产负债表['增长率'] = 增长率

# 5. 计算预测期金额与变动
资产负债表['预测期'] =资产负债表['2023年'] +资产负债表['2023年'] *资产负债表['是否敏感'] *资产负债表['增长率']
资产负债表['变动'] =资产负债表['预测期'] -资产负债表['2023年']

print("前40行：")
print(资产负债表.head(40))
print("\n后35行：")
print(资产负债表.tail(35))

# 6. 融资需求计算
融资总需求 = (资产负债表.loc['货币资金':'其他非流动资产', '变动'].sum() -
              资产负债表.loc['短期借款':'其他非流动负债', '变动'].sum())
净利润 = 资产负债表.at['收入合计', '预测期'] * 0.05
外部融资需求 = 融资总需求 - 净利润

print(f"\n融资总需求: {融资总需求:,.2f}")
print(f"净利润: {净利润:,.2f}")
print(f"外部融资需求: {外部融资需求:,.2f}")

# 7. 绘图数据准备
时间轴 =资产负债表.columns[:5].tolist()
资产总额 = [round(资产负债表.loc['货币资金':'其他非流动资产', 年份].sum(), 2) for 年份 in 时间轴]
负债总额 = [round(资产负债表.loc['短期借款':'其他非流动负债', 年份].sum(), 2) for 年份 in 时间轴]
营业收入 = 年度收入.values.tolist()[0]

print("\n时间轴:", 时间轴)
print("资产总额:", 资产总额)
print("负债总额:", 负债总额)
print("营业收入:", 营业收入)

# 8. 绘制面积图
面积图 = Line(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
面积图.add_xaxis(时间轴)
面积图.add_yaxis("资产总额", 资产总额, is_smooth=True)
面积图.add_yaxis("负债总额", 负债总额, is_smooth=True)
面积图.add_yaxis("营业收入", 营业收入, is_smooth=True)
面积图.set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
                       label_opts=opts.LabelOpts(is_show=False))
面积图.render('资产负债表面积图.html')