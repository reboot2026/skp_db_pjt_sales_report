from config.db_config import get_connection
from report_generator import ReportGenerator

import warnings
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

# DB 연결 (with 블록이 끝나면 커넥션 자동 close)
with get_connection() as conn:
    # 보고서 생성
    generator = ReportGenerator(conn)
    generator.generate()
