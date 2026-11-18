"""Year 매출 리포트 클래스

    ReportGenerator에서 호출된다. 

"""

from datetime import date
import pandas as pd 
from config.db_config import get_connection

from sql.sales_queries import (
     CATEGORY_MONTHLY_SALES
    ,CATEGORY_PRODUCT_AVG_PRICE
    ,CATEGORY_TOP2_PRODUCT
)

class YearSalesReport:

    def __init__(self, conn, year:int):
        self.conn = conn
        self.year = int(year)
        self.start_dt = date(self.year, 1, 1)
        self.end_dt = date(self.year+1, 1, 1)

    def get_params(self):
        return {
            "start_date": self.start_dt,
            "end_date": self.end_dt,
        }
    
    def get_category_monthly_sales(self):
        df =  pd.read_sql(CATEGORY_MONTHLY_SALES, self.conn, params=self.get_params())

        # 카테고리별 월별 매출액 피벗
        monthly_sales = pd.pivot_table(df 
                                       ,index="카테고리"
                                       ,columns="월"
                                       ,values="매출금액"
                                       ,aggfunc='sum'
                                       ,fill_value=0)

        # 1월~12월 컬럼을 모두 생성
        monthly_sales = monthly_sales.reindex(
                columns = range(1, 13)
               ,fill_value = 0 
        )

        # 월 컬럼명 변경
        monthly_sales.columns = [f'{month}월' for month in monthly_sales.columns]
            
        # 카테고리별 행 합계 
        monthly_sales['합계'] = monthly_sales.sum(axis=1)

        # 월별합계 열 합계
        monthly_sales.loc['전체 합계'] = monthly_sales.sum(axis=0)

        # 인덱스(카테고리)를 일반 컬럼으로 
        monthly_sales = monthly_sales.reset_index()

        return monthly_sales 

    def get_category_product_avg_price(self):
        return pd.read_sql(CATEGORY_PRODUCT_AVG_PRICE, self.conn)
        
    
    def get_category_top2_products(self):   
        return pd.read_sql(CATEGORY_TOP2_PRODUCT, self.conn, params=self.get_params()) 
# "카테고리별상품수및평균가" : self.get_category_product_avg_price(),

    def get_sheets(self):
        sheets = {
            "카테고리별월별매출": self.get_category_monthly_sales(),
            "카테고리별상품수및평균가" : self.get_category_product_avg_price(),
            "카테고리별Top2상품" : self.get_category_top2_products(),
        }
        return sheets

if __name__ == "__main__":
 with get_connection() as conn:
    report = YearSalesReport(conn, 2025)
    sheets = report.get_sheets()

    for (nm, sheet) in sheets.items():
        print(nm)
        print(sheet) 
    