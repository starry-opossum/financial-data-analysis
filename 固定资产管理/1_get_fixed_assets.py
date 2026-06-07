# 1. 引入模块
import os
from dotenv import load_dotenv
import pymysql
import pandas as pd
from pathlib import Path

# 加载 .env 文件（脚本在子文件夹，需要向上一级找到根目录的 .env）
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 2. 连接数据库（使用环境变量）
conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3376)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8"
)
cursor = conn.cursor()

# 3. 执行 SQL
sql = 'select vbill_date,fixed_assets_type,original_cost,accumulated_depreciation,cumulative_impairment,net_book_value from erp_fd_asset where org_name="新兴化肥有限公司"'
cursor.execute(sql)
data = cursor.fetchall()

# 4. 转为 DataFrame
固定资产台账 = pd.DataFrame(
    data,
    columns=['当前期间', '固定资产类别', '原始成本', '累计折旧', '累计减值', '账面净值']
)
固定资产台账[['原始成本', '累计折旧', '累计减值', '账面净值']] = \
    固定资产台账[['原始成本', '累计折旧', '累计减值', '账面净值']].astype(float)

# 5. 关闭连接
conn.commit()
conn.close()

# 6. 保存到当前脚本所在目录
output_path = Path(__file__).parent / '固定资产台账.xlsx'
固定资产台账.to_excel(output_path, index=False)
print(f"固定资产台账已保存至：{output_path}")