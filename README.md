# 企业财务数据分析工具集

## 📊 项目概述

本仓库是基于新道 DBE5cloud 平台开发的 Python 财务分析工具集，包含两个核心模块：

1. **融资需求测算**  
   基于历史日收入数据与资产负债表，采用霍尔特‑温特时间序列模型预测未来收入增长率，通过销售百分比法计算外部融资需求，并生成交互式可视化面积图。

2. **固定资产更新成本测算**  
   从 ERP 数据库提取资产台账，筛选折旧率 > 70% 的待退役设备，自动测算出售可回收金额及重新购置预算，为企业设备更新决策提供量化依据。

> 所有项目均使用**模拟数据**，可公开作为作品集展示，不涉及真实企业机密。

**技术栈**：Python / Pandas / NumPy / statsmodels / Pyecharts / pymysql / SQL / Excel / python-dotenv

---

## 📁 项目结构

```
financial-data-analysis/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example               # 环境变量模板
├── requirements.txt           # Python 依赖清单
│
├── 融资需求测算/
│   ├── 01SQL语句获取经营数据.py
│   ├── 02Python计算增长率.py
│   ├── 03Python计算资产负债表中销售敏感项目.py
│   ├── 04Python融资需求可视化分析.py
│   ├── SQL调取结果.xlsx        # 示例日收入数据（模拟）
│   └── 案例资源资产负债表.xlsx  # 示例资产负债表（模拟）
│
└── 固定资产/
    ├── 1_get_fixed_assets.py
    ├── 2_filter_assets.py
    ├── 3_calculate_update_cost.py
    └── (运行时生成：固定资产台账.xlsx)
```

---

## 🔧 模块一：融资需求测算

### 业务背景
企业需预测未来一年营业收入增长率，并据此估算外部融资额。传统手工处理耗时长且难以识别敏感项目。

### 核心流程
1. **数据预处理**：将日收入重采样为季度/年度合计。
2. **时间序列预测**：使用霍尔特‑温特加法模型（趋势 + 季节）预测未来 4 个季度收入，计算年度增长率。
3. **敏感项目识别**：计算资产负债表各科目与收入的相关系数，筛选 |r|>0.8 的敏感资产与负债。
4. **融资需求计算**：
   - 融资总需求 = 敏感资产变动额 – 敏感负债变动额
   - 净利润 = 预测期收入 × 5%（假设净利率）
   - 外部融资需求 = 融资总需求 – 净利润
5. **可视化**：生成资产总额、负债总额、营业收入随年份变化的交互式面积图（HTML 格式）。

### 关键代码示例

```python
# 霍尔特‑温特模型预测
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(季度收入, trend='add', seasonal='add', seasonal_periods=4)
fitted = model.fit()
forecast = fitted.forecast(4)
growth_rate = (forecast.sum() - 基期收入) / 基期收入

# 敏感项目判断
资产负债表['相关系数'] =资产负债表.apply(
    lambda x: x.corr(年度收入.loc['收入合计']), axis=1)
资产负债表['是否敏感'] = (abs(资产负债表['相关系数']) > 0.8).astype(int)
```

### 运行方式

```bash
cd 融资需求测算
python3 04Python融资需求可视化分析.py
```

运行后控制台输出融资总需求、净利润、外部融资需求，并在当前目录生成 `资产负债表面积图.html`。

---

## 🔧 模块二：固定资产更新成本测算

### 业务背景
企业需定期评估固定资产状态，识别高折旧率设备以制定更新计划。原手工处理容易遗漏且缺乏量化成本测算。

### 核心流程
1. **SQL 取数**：从 ERP 数据库 `erp_fd_asset` 表提取资产期间、类别、原始成本、累计折旧等字段。
2. **数据筛选**：仅保留目标期间（如 2023‑03）及指定类别（“计算机及电子设备”）。
3. **计算折旧率**：折旧率 = 累计折旧 / 原始成本，筛选折旧率 > 70% 的待出售资产。
4. **成本测算**：
   - 待出售资产原值、累计折旧、减值、账面净值合计
   - 预计可回收金额 = 原始成本 × 10%
   - 重新购置预算 = 原始成本 × 1.1
5. **输出报告**：打印格式化测算结果。

### 关键代码示例

```python
# 筛选待出售资产
固定资产台账['折旧率'] = 固定资产台账['累计折旧'] / 固定资产台账['原始成本']
待出售资产 = 固定资产台账[固定资产台账['折旧率'] > 0.7]

# 测算更新成本
回收价合计 = (待出售资产['原始成本'] * 0.1).sum()
新购预算合计 = (待出售资产['原始成本'] * 1.1).sum()
```

### 运行方式

```bash
cd 固定资产
python3 1_get_fixed_assets.py     # 从数据库提取数据（需配置 .env）
python3 2_filter_assets.py        # 筛选并显示待出售资产
python3 3_calculate_update_cost.py # 输出更新成本测算报告
```

> 注：数据库密码已脱敏，请按下方“快速开始”配置 `.env` 文件。

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/starry-opossum/financial-data-analysis.git
cd financial-data-analysis
```

### 2. 创建虚拟环境并安装依赖
```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 3. 配置数据库连接（仅用于 SQL 取数模块）
```bash
cp .env.example .env
# 编辑 .env 文件，填入真实的数据库信息
```

`.env` 文件格式示例：
```
DB_HOST=your_host
DB_PORT=3376
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```

> **注意**：`.env` 已加入 `.gitignore`，不会上传到 GitHub。

### 4. 运行融资需求测算模块
```bash
cd 融资需求测算
python3 04Python融资需求可视化分析.py
```

### 5. 运行固定资产模块
```bash
cd ../固定资产
python3 1_get_fixed_assets.py    # 需要 .env 数据库配置
python3 2_filter_assets.py
python3 3_calculate_update_cost.py
```

---

## 📌 扩展计划

后续计划添加：
- **人力成本分摊分析**（部门福利费用自动化计算与看板）
- **销售业绩评价系统**（基于订单数据的绩效可视化）
- **现金流预测模型**（结合收款周期预测现金缺口）

欢迎通过 Issue 或 Pull Request 贡献新模块。

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 👤 作者

**starry-opossum** · [GitHub 主页](https://github.com/starry-opossum)

> 项目基于新道 DBE5cloud 平台开发，所有数据均为模拟，仅用于学习与作品集展示。
