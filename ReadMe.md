# 📊 매출 리포트 자동 생성기 (Sales Report Generator)

Market DB의 주문 및 상품 데이터를 조회하여 **카테고리별·월별 매출 지표**를 `pandas`로 집계·가공하고, 실행 일시별 폴더에 **그래프가 포함된 Excel 리포트와 CSV 파일을 연도별로 자동 생성**하는 Python 프로젝트입니다.

> 📐 클래스 구조·처리 흐름·시스템 구조도는 **[설계서](docs/설계서.md)** 를 참고하세요.

---

## 🎯 프로젝트 목표
* MySQL 데이터베이스(`Market` 스키마)와 Python 연동 및 SQL 집계 쿼리 실행
* `pandas`를 활용한 데이터프레임(DataFrame) 변환 및 분석 지표 가공 (피벗, 합계)
* `matplotlib` 그래프를 이미지로 생성해 Excel 시트에 삽입
* 시트(Sheet)별로 구분된 다중 시트 Excel(`.xlsx`) 및 백업용 CSV(`.csv`) 리포트 자동 출력

---

## 📑 리포트 구성

주문 데이터가 있는 **연도마다** Excel 파일 1개가 생성되며, 각 파일에는 아래 3개 시트가 들어갑니다.

| 시트 | 내용 | 그래프 |
|---|---|---|
| 카테고리별월별매출 | 카테고리 × 1~12월 매출금액 (`수량 × 상품단가`), 카테고리별 합계 열 / 전체 합계 행 | 꺾은선 |
| 카테고리별상품수및평균가 | 카테고리별 상품 수, 평균 상품가격 (상품 마스터 기준) | 세로 막대 |
| 카테고리별Top2상품 | 카테고리별 판매수량 상위 2개 상품 | 가로 막대 |

---

## 🛠 기술 스택 및 환경
* **Language:** Python 3.13 (3.13.18에서 검증)
* **Database:** MySQL 8.4 (`Market` Schema)
* **Libraries:**
  * `pymysql` (DB 연결 및 쿼리 실행)
  * `pandas` (데이터 가공 및 리포트 변환)
  * `openpyxl` (다중 시트 Excel 파일 생성, 그래프 이미지 삽입)
  * `matplotlib` (그래프 이미지 생성)
  * `python-dotenv` (DB 접속 정보 환경변수 관리)

---

## 📁 디렉토리 구조
```text
skp_db_pjt_sales_report/
├── config/
│   └── db_config.py        # DB 연결 설정 및 커넥션 관리
├── sql/
│   └── sales_queries.py    # 매출 분석용 SQL 쿼리 모음
├── chart/
│   └── sales_charts.py     # 시트별 그래프 함수 모음 (CHARTS 등록표)
├── docs/
│   ├── 설계서.md            # 시스템·클래스·흐름 구조, ERD 설계서
│   └── images/erd.png      # DB ERD (MySQL Workbench)
├── output/                 # 생성된 리포트 저장 폴더 (실행 일시별 하위 폴더, Git 제외)
├── .env                    # DB 접속 정보 (Git 추적 제외)
├── main.py                 # 리포트 생성 메인 실행 스크립트
├── report_generator.py     # ReportGenerator: 연도별 반복, Excel/CSV/그래프 저장
├── year_sales_report.py    # YearSalesReport: 한 연도의 시트 데이터 생성
├── requirements.txt        # 의존성 패키지 목록
└── ReadMe.md               # 프로젝트 설명서
```

```text
main.py ──▶ ReportGenerator ──▶ YearSalesReport ──▶ sql/sales_queries.py ──▶ MySQL
                  │
                  ├──▶ chart/sales_charts.py (그래프)
                  └──▶ output/실행일시/ (.xlsx · .csv · .png)
```

---

## 📦 Python 라이브러리

| 라이브러리 | 용도 |
|---|---|
| `pymysql` | MySQL DB 연결 및 SQL 쿼리 실행 |
| `pandas` | 조회 결과를 DataFrame으로 변환, 매출 지표 집계·가공 |
| `openpyxl` | pandas가 다중 시트 Excel(`.xlsx`) 파일을 쓸 때 사용하는 엔진, 그래프 이미지 삽입 |
| `matplotlib` | 시트 데이터로 그래프를 그려 PNG 이미지로 저장 (설치 시 `pillow`도 함께 설치됨) |
| `python-dotenv` | `.env` 파일의 DB 접속 정보를 환경변수로 로드 |
| `numpy` | pandas 의존성. 스마트 앱 컨트롤 차단 문제로 `numpy<2.4` 고정 ([문제 해결](#-문제-해결) 참고) |

패키지 목록은 `requirements.txt`에서 관리합니다.

---

## ⚙️ 가상환경 생성 및 실행 (Windows / Git Bash)

> 명령어는 **Git Bash** 기준이며, PowerShell에서 다른 부분은 각 단계에 함께 적었습니다.
> 모든 명령어는 **프로젝트 루트**에서 실행합니다.

### 1. 가상환경 생성 (Python 3.13)
PC에 여러 버전의 Python이 설치되어 있으면 `python` 명령이 다른 버전을 가리킬 수 있으므로,
Windows의 `py` 런처로 버전을 직접 지정합니다. 먼저 설치된 Python 목록을 확인합니다.
```bash
py --list
```

**목록에 `-V:3.13`이 있는 경우** (python.org 공식 설치본)
```bash
py -3.13 -m venv .venv
```

**목록에 `-V:Astral\CPython3.13.18`처럼 표시되는 경우** (uv로 설치한 Python)
`py -3.13`으로는 찾지 못하므로 목록에 표시된 이름을 그대로 지정합니다.
Git Bash에서는 역슬래시(`\`) 때문에 **따옴표로 감싸야** 합니다.
```bash
py '-V:Astral\CPython3.13.18' -m venv .venv
```

**목록에 3.13이 없는 경우** 먼저 설치한 뒤 `py -3.13 -m venv .venv`를 실행합니다.
```bash
# 설치 가능한 3.13 버전 확인
py list --online 3.13

# 설치 (버전 번호 없이 3.13으로 지정 → 설치 가능한 최신 3.13 버전이 설치됨)
py install 3.13
```
> ⚠️ `py install 3.13.18`처럼 **세부 버전을 지정하면 실패할 수 있습니다.**
> ```
> [ERROR] Failed to find a suitable install for '3.13.18'.
> ```
> Python 3.13은 보안 패치만 나오는 단계라, python.org에서 Windows용 설치 파일을 제공하지 않는 버전이 있습니다.
> (2026-11 기준 python.org에서 설치 가능한 최신 버전은 **3.13.17**이고, 3.13.18은 uv로만 설치 가능)
> 3.13.17과 3.13.18은 보안 패치 차이뿐이라 이 프로젝트 실행에는 영향이 없습니다.
>
> 3.13.18이 꼭 필요하면 uv로 설치한 뒤 위의 `-V:Astral\CPython3.13.18` 방법으로 가상환경을 만듭니다.
> ```bash
> uv python install 3.13.18
> ```

### 2. 가상환경 활성화
```bash
# Git Bash
source .venv/Scripts/activate

# PowerShell
.\.venv\Scripts\Activate.ps1
```
활성화되면 프롬프트 앞에 `(.venv)`가 표시됩니다. `python --version`으로 3.13인지 확인합니다.

> PowerShell에서 "스크립트를 실행할 수 없습니다" 오류가 나면 아래 명령을 한 번 실행한 뒤 다시 활성화합니다.
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

### 3. 라이브러리 설치
```bash
python -m pip install -r requirements.txt

# 설치 확인
python -c "import numpy, pandas, matplotlib; print('numpy', numpy.__version__, '/ pandas', pandas.__version__, '/ matplotlib', matplotlib.__version__)"
```
> `pip` 대신 `python -m pip`을 쓰면 가상환경의 pip이 확실히 실행됩니다. ([권한 오류](#pip-install-시-권한-오류-access-denied) 참고)

### 4. DB 접속 정보 설정
프로젝트 루트에 `.env` 파일을 만들고 접속 정보를 입력합니다. (`.env`는 Git에 커밋되지 않으므로 직접 작성해야 합니다.)
```
DB_HOST=DB_서버_주소
DB_PORT=3306
DB_USER=사용자명
DB_PASSWORD=비밀번호
DB_NAME=dt_pjt
```
> 테이블 이름은 대문자입니다(`PRODUCT`, `ORDER`, `ORDER_DESC` 등). 이 DB는 대소문자를 구분하므로 쿼리에서도 대문자로 씁니다.
> `ORDER`는 SQL 예약어이므로 항상 `` `ORDER` ``처럼 백틱으로 감쌉니다.

### 5. DB 연결 테스트 및 실행
```bash
python -m config.db_config   # DB 연결 테스트 → "DB 연결 성공 (MySQL 8.4.x)" 출력
python main.py               # 리포트 생성
```
> 다른 폴더(`config/`, `sql/`)로 이동해서 실행하면 `ModuleNotFoundError`가 날 수 있으니 항상 프로젝트 루트에서 실행합니다.

**실행 결과**
```text
==== 2025년도 보고서 생성 시작====
==== 2025년도 보고서 생성 완료====
==== 2026년도 보고서 생성 시작====
==== 2026년도 보고서 생성 완료====
```
```text
output/
└── 20261118_130824/                              ← 실행할 때마다 새 폴더
    ├── 매출리포트_2025년도.xlsx                    ← 시트 3개, 각 시트 표 오른쪽에 그래프
    ├── 매출리포트_2025년도_카테고리별월별매출.csv   ← 시트마다 CSV 1개
    ├── …
    ├── 2025_카테고리별월별매출.png                 ← Excel에 삽입된 그래프 원본
    └── … (연도별 동일 구성)
```

### 6. 가상환경 비활성화
```bash
deactivate
```

---

## 🧯 문제 해결

### "애플리케이션 제어 정책에서 이 파일을 차단했습니다" (numpy / pandas import 오류)
```
ImportError: DLL load failed while importing _multiarray_umath: 애플리케이션 제어 정책에서 이 파일을 차단했습니다.
```
* **원인:** Windows 11의 **스마트 앱 컨트롤**이 아직 평판이 쌓이지 않은 numpy의 DLL(`.pyd`) 파일을 차단합니다. 코드 문제가 아닙니다.
* **이 프로젝트의 조치:**
  * Python 3.15 대신 **3.13**을 사용합니다.
  * `requirements.txt`에서 **numpy를 2.4 미만(`numpy<2.4`)으로 고정**합니다. (numpy 2.3.5에서 정상 동작 확인)
* **그래도 차단되면:** Windows 보안 → 앱 및 브라우저 컨트롤 → 스마트 앱 컨트롤 설정에서 끌 수 있습니다.
  보안 수준이 낮아지고 다시 켜려면 Windows 초기화가 필요할 수 있으므로, 회사·학교 PC는 관리자에게 먼저 확인합니다.
* matplotlib 등 다른 패키지에서 같은 오류가 나도 원인은 같습니다.

### pip install 시 권한 오류 (Access denied)
* **원인:** 가상환경이 활성화되지 않은 터미널에서 `pip`을 실행하면, PC에 설치된 **전역 Python의 pip**이 실행되어 전역 폴더에 설치하려다 거부됩니다.
* **해결:** 가상환경의 python으로 pip을 실행합니다. 활성화 여부와 관계없이 `.venv`에 설치됩니다.
  ```bash
  .venv/Scripts/python -m pip install -r requirements.txt      # Git Bash
  .\.venv\Scripts\python -m pip install -r requirements.txt    # PowerShell
  ```
* `pip --version`으로 출력되는 경로가 `.venv` 안인지 확인할 수 있습니다.

### `ValueError: unsupported format character 'Y'` (SQL 실행 오류)
* **원인:** `params`를 넘겨 실행하는 쿼리는 pymysql이 쿼리 전체를 `query % params`로 치환합니다. SQL 안의 `%`(주석 포함)도 치환 문자로 해석됩니다.
* **해결:** `params`를 쓰는 쿼리에서는 `%`를 `%%`로 씁니다. 예: `date_format(dt, '%%Y-%%m')`, `LIKE '%%abc%%'`

### `IndexError: At least one sheet must be visible` (Excel 저장 오류)
* **원인:** `pd.ExcelWriter`의 `with` 블록 안에서 먼저 다른 오류가 나서, 시트가 없는 상태로 저장을 시도한 것입니다. **2차 오류**입니다.
* **해결:** 트레이스백 위쪽(`During handling of the above exception…` 앞)에서 내 소스 파일(`chart/`, `year_sales_report.py` 등) 경로가 나오는 첫 오류를 찾아 수정합니다.

### `UserWarning: pandas only supports SQLAlchemy connectable…`
* pymysql 커넥션을 `pd.read_sql`에 직접 넘겨서 나오는 **경고**이며, 결과는 정상입니다. `main.py`에서 숨김 처리되어 있습니다.

### 그래프의 한글이 □□□로 표시됨
* `chart/sales_charts.py`의 `plt.rcParams["font.family"] = "Malgun Gothic"` 설정을 확인합니다. (Windows 기본 폰트 '맑은 고딕')
