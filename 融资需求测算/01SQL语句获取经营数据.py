# 1. 引入模块
import os
from dotenv import load_dotenv
import pymysql
import pandas as pd
from pathlib import Path

# 加载 .env 文件（位于项目根目录）
load_dotenv()

# 2. 连接数据库
conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8"
)
cursor = conn.cursor()

# 3. 执行 SQL
sql = 'select vbill_date,total_income from erp_fd_fundforecast where org_name="新兴化工材料有限公司"'
cursor.execute(sql)
data = cursor.fetchall()

# 4. 转为 DataFrame
收入合计 = pd.DataFrame(data, columns=['日期', '收入合计'])
收入合计['收入合计'] = 收入合计['收入合计'].astype(float)
收入合计['日期'] = 收入合计['日期'].astype(str)

# 5. 关闭连接
conn.commit()
conn.close()

# 6. 保存到当前脚本所在目录
output_path = Path(__file__).parent / '收入合计.xlsx'
收入合计.to_excel(output_path, index=False)
print(f"收入数据已保存至：{output_path}")
print(收入合计)