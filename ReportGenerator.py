"""매출 리포트 생성 클래스 모듈.

DB 조회 → DataFrame 가공 → Excel / CSV 저장 흐름을 담당한다.
"""

import pandas as pd

from config.db_config import get_connection


class ReportGenerator:
    """매출 리포트 생성기."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir

    def fetch(self, sql: str) -> pd.DataFrame:
        """SQL을 실행해 결과를 DataFrame으로 반환한다."""
        pass

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """조회 결과를 리포트용 지표로 가공한다."""
        pass

    def save_excel(self, sheets: dict[str, pd.DataFrame], file_name: str) -> str:
        """시트별 DataFrame을 다중 시트 Excel 파일로 저장하고 경로를 반환한다."""
        pass

    def save_csv(self, df: pd.DataFrame, file_name: str) -> str:
        """DataFrame을 CSV 파일로 저장하고 경로를 반환한다."""
        pass
