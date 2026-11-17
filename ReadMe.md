# 📊 매출 리포트 자동 생성기 (Sales Report Generator)

Market DB의 주문 및 상품 데이터를 조회하여 **카테고리별·월별 매출 지표**를 `pandas`로 집계·가공하고, 실행 날짜가 포함된 **Excel 및 CSV 리포트 파일로 자동 생성**하는 Python 프로젝트입니다.

---

## 🎯 프로젝트 목표
* MySQL 데이터베이스(`Market` 스키마)와 Python 연동 및 SQL 집계 쿼리 실행
* `pandas`를 활용한 데이터프레임(DataFrame) 변환 및 분석 지표 가공
* 시트(Sheet)별로 구분된 다중 시트 Excel(`.xlsx`) 및 백업용 CSV(`.csv`) 리포트 자동 출력

---

## 🛠 기술 스택 및 환경
* **Language:** Python 3.10+
* **Database:** MySQL 8.0 (`Market` Schema)
* **Libraries:**
  * `pymysql` (DB 연결 및 쿼리 실행)
  * `pandas` (데이터 가공 및 리포트 변환)
  * `openpyxl` (다중 시트 Excel 파일 생성 엔진)
  * `python-dotenv` (DB 접속 정보 환경변수 관리)

---

## 📁 디렉토리 구조
```text
sales-report-generator/
├── config/
│   └── db_config.py        # DB 연결 설정 및 커넥션 관리
├── sql/
│   └── sales_queries.py    # 매출 분석용 SQL 쿼리 모음
├── output/                 # 생성된 Excel / CSV 리포트 저장 폴더
├── .env                    # DB 접속 정보 (Git 추적 제외)
├── main.py                 # 리포트 생성 메인 실행 스크립트
├── requirements.txt        # 의존성 패키지 목록
└── README.md               # 프로젝트 설명서