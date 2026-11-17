import pandas as pd
import numpy as np 
from config.db_config import get_connection
from sql.sales_queries import CATEGORY_SALES_SQL 

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(CATEGORY_SALES_SQL)
        df = pd.DataFrame(cursor.fetchall())
    
print(df) 

df.to_csv("output/test_result.csv")
df.to_excel("output/test_result.xlsx")

