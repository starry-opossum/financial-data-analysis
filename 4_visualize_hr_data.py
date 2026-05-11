# ------------------------------------前置任务脚本 ------------------------------------
import pandas as pd 
import numpy as np

员工信息 = pd.read_excel('员工信息.xlsx')

# 提取生日月份
生日月份 = []
for i in 员工信息['证件号']:    
    月份 = str(i)[10:12]
    生日月份.append(月份)
员工信息['生日月份'] = pd.DataFrame(生日月份)

# 部门性质映射
部门性质 = pd.DataFrame({
    '所属部门': ['长春销售部', '西安销售部', '南昌销售部', '济南销售部', '北京销售部',
               '行政部', '人力资源部', '法务部', '财务部',
               'ME系统部', 'ATS系统部', '产品运维部', 'PEM系统部'],
    '部门性质': ['销售', '销售', '销售', '销售', '销售',
               '管理', '管理', '管理', '管理',
               '生产', '生产', '生产', '研发']
})
员工信息 = pd.merge(员工信息, 部门性质, on='所属部门', how='left')

# 创建透视表和金额表
透视表 = pd.pivot_table(员工信息, index="生日月份", columns="部门性质", 
                         aggfunc="size", fill_value=0)
金额透视表 = 透视表 * 500
部门合计 = 金额透视表.sum()
总金额 = 部门合计.sum()
金额透视表['合计'] = 金额透视表['管理'] + 金额透视表['销售'] + 金额透视表['生产'] + 金额透视表['研发']


# ------------------------------------开始任务 ------------------------------------
# ------------------------------------任务9 Python人力数据可视化 ------------------------------------
# 1. 导入绘图用的库
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType


# 2. 绘制柱状图
柱状图 = Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))

# 横轴为1-12个月
柱状图.add_xaxis(list(range(1, 13))) 

# 纵轴为金额透视表各部门的金额分布
for i in 金额透视表.columns:      
    柱状图.add_yaxis(
        i, 
        list(金额透视表[i]),
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")])
    )

柱状图.set_global_opts(toolbox_opts=opts.ToolboxOpts(is_show=True))
柱状图.render('柱状图.html')
print("柱状图已生成：柱状图.html")
