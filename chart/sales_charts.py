"""시트별 그래프 정의.

그래프 추가 방법:
  1) DataFrame을 받아 ax를 반환하는 함수 작성
  2) 아래 CHARTS에 "시트명": 함수 한 줄 등록
"""
import matplotlib
matplotlib.use("Agg")   # 창 없이 파일로만 저장 
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

plt.rcParams["font.family"] = "Malgun Gothic"   # 한글 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False

# 카테고리별 월별 매출 (꺾은선)
def monthly_sales_chart(df):
    data = df.set_index("카테고리").drop(index="전체 합계", columns="합계")
    ax =  data.T.plot(kind="line", 
                      marker="o", 
                      figsize=(10,5), 
                      title="카테고리별 월별 매출") 
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _:f"{x/1000:,.0f}"))
    ax.set_ylabel("매출금액(천원)")
    ax.set_xticks(range(len(data.columns)), data.columns) # 추가 : 1월~12월
    return ax

# 카테고리별 평균가 (세로 막대)
def avg_price_chart(df):
    ax =  df.plot( kind="bar",
                   x="카테고리",
                   y="평균가",
                   legend=False,
                   figsize=(8,4),
                   title="카테고리별 평균가",
                   rot=0
                   )
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_ylabel("평균가(원)")
    return ax 

# 카테고리별 Top2 상품 판매수량 (가로 막대)
def top2_product_chart(df):
    data = df.set_index(df["카테고리"]+" - "+df["상품명"])
    ax = data.plot(kind="barh",
                   y="판매수량",
                   legend=False,
                   figsize=(8,5),
                   title="카테고리별 Top2 상품 판매수량")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("판매수량(개)")
    return ax 

# 시트명 - 그래프 함수(get_sheets()의 시트명과 똑같이)
CHARTS = {
    "카테고리별월별매출" : monthly_sales_chart,
    "카테고리별상품수및평균가" : avg_price_chart,
    "카테고리별Top2상품" : top2_product_chart
}
