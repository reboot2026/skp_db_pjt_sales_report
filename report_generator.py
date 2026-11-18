"""매출 리포트 생성 클래스 모듈.

DB 조회 → DataFrame 가공 → Excel / CSV 저장 흐름을 담당한다.
"""
import os
import pandas as pd

from datetime           import datetime 
from sql.sales_queries  import GET_YEARS
from year_sales_report  import YearSalesReport

from openpyxl.drawing.image import Image
from openpyxl.utils         import get_column_letter
from chart.sales_charts     import CHARTS, plt 

class ReportGenerator:
    """매출 리포트 생성기."""

    def __init__(self, conn, base_dir: str = "output"):
        self.conn = conn
        self.base_dir = base_dir
        self.create_folder()

    # 폴더 생성 
    def create_folder(self):
        folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.folder_path = os.path.join(self.base_dir, folder_name) 
        os.makedirs(self.folder_path, exist_ok=True) 

    # 연도 목록 조회
    def get_years(self):
        df = pd.read_sql(GET_YEARS, self.conn)
        return df["ORDER_YEAR"].dropna().astype(int).tolist()

    # Excel 저장
    def to_excel(self, year, sheets):
        file_path = os.path.join(self.folder_path, f"매출리포트_{year}년도.xlsx") 

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            for (sheetname, df) in sheets.items():
                df.to_excel(writer,
                            sheet_name = sheetname,
                            index=False
                            )
                
                # 그래프가 등록된 시트만 이미지 삽입 
                if sheetname in CHARTS:
                    ax = CHARTS[sheetname](df)
                    self.add_image(writer.sheets[sheetname], ax, f"{year}_{sheetname}")
                    

    # CSV 저장
    def to_csv(self, year, sheets):
        for (sheetname, sheet) in sheets.items():
            csv_path = os.path.join(self.folder_path, f"매출리포트_{year}년도_{sheetname}.csv")
            sheet.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # 그래프를 PNG로 저장 후 시트의 표 오른쪽에 삽입
    def add_image(self, ws, ax, file_name):
        img_path = os.path.join(self.folder_path, f"{file_name}.png")
        ax.figure.savefig(img_path, dpi=100, bbox_inches="tight")
        plt.close(ax.figure)
        ws.add_image(Image(img_path), f"{get_column_letter(ws.max_column + 2)}2")


    # 전체 보고서 생성
    def generate(self):
        years = self.get_years()

        for year in years:
            print(f"==== {year}년도 보고서 생성 시작====")
            report = YearSalesReport(self.conn, year)
            sheets = report.get_sheets()
            # 엑셀 저장 
            self.to_excel(year, sheets) 
            # CSV 저장 
            self.to_csv(year, sheets)
            print(f"==== {year}년도 보고서 생성 완료====")
                        
