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
季度收入合计 = 收入合计['收入合计'].resample('QE').sum()   # 'Q' -> 'QE'
年度收入合计 = 收入合计['收入合计'].resample('YE').sum()   # 'Y' -> 'YE'
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
# 8.计算营业收入增长率
基期收入 = 年度收入.at['2023-12-31', '收入合计']
增长率 = round((预测期数年度合计-基期收入)/基期收入,2) 
# 1. 读取案例资料中的资产负债表Excel文件。
资产负债表 = pd.read_excel('融资需求测算/案例资源资产负债表.xlsx',sheet_name='资产负债表',index_col=0)
# 2. 将收入数据插入读取表格的第一行中
年度收入=年度收入[['收入合计']].T
年度收入.columns = 资产负债表.columns
资产负债表 = pd.concat([年度收入, 资产负债表])
# 3. 计算相关系数
资产负债表['相关系数']=资产负债表.apply(lambda x:x.corr(年度收入.loc['收入合计']),axis=1)
资产负债表['增长率'] = 增长率
# 4. 判断是否为敏感项目
def forcast(项目):
    if abs(项目['相关系数'])>0.8:
        项目['是否敏感']= 1
    else:
        项目['是否敏感']= 0
    return 项目
资产负债表=资产负债表.apply(forcast,axis=1)


# ------------------------------------开始任务 ----------------------------------------------------------------------
# ------------------------------------任务9 Python 融资需求可视化分析 ------------------------------------

# 1. 计算资产负债表项目预测期金额
# 预测期
资产负债表['预测期']=资产负债表['2023年']+资产负债表['2023年']*资产负债表['是否敏感']*资产负债表['增长率']
资产负债表['变动']=资产负债表['预测期']-资产负债表['2023年']
print(资产负债表.head(40))
print(资产负债表.tail(35))


# 2. 计算融资总需求
融资总需求 = 资产负债表.loc['货币资金':'其他非流动资产','变动'].sum()-资产负债表.loc['短期借款':'其他非流动负债','变动'].sum()
print('融资总需求:',融资总需求)



# 3. 计算内部融资额
净利润 = 资产负债表.at['收入合计', '预测期']*0.05
print('净利润:',净利润)



# 4.计算外部融资额
外部融资需求 = 融资总需求-净利润
print('外部融资需求:',外部融资需求 )



# 5. 绘制资产负债表面积图
# 5.1 将数据转换为绘图可用格式的数据。
时间轴 = 资产负债表.columns[0:5].tolist()
print(时间轴)

# 选择'货币资金'到'其他非流动资产'的行范围，计算每年的合计数
资产总额 = []
for 年份 in 时间轴:
    本年合计 = round(资产负债表.loc['货币资金':'其他非流动资产', 年份].sum(),2)
    资产总额.append(本年合计)
print(资产总额)

# 选择'短期借款'到'其他非流动负债'的行范围，计算每年的合计数
负债总额 = []
for 年份 in 时间轴:
    本年合计 = round(资产负债表.loc['短期借款':'其他非流动负债', 年份].sum(),2)
    负债总额.append(本年合计)
print(负债总额)

营业收入 = 年度收入.values.tolist()[0]
print(营业收入)

# 5.2 引入在线echarts模块，设置在线echarts模块的CDN地址。
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/"

      
# 5.3 使用pyecharts绘图模块进行面积图的绘制。
from pyecharts.charts import  Line
import pyecharts.options as opts
from pyecharts.globals import ThemeType
面积图 =  Line(init_opts = opts.InitOpts(theme=ThemeType.VINTAGE)) # 复古主题配色
面积图.add_xaxis(时间轴)
面积图.add_yaxis("资产总额", 资产总额, is_smooth=True)
面积图.add_yaxis("负债总额", 负债总额, is_smooth=True)
面积图.add_yaxis("营业收入", 营业收入, is_smooth=True)
面积图.set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.2),# 透明度选择0.2，可以根据喜好调整
                      label_opts=opts.LabelOpts(is_show=False)) # 不直接显示数据，删除此行则会显示具体数据                    
面积图.render('资产负债表面积图.html')