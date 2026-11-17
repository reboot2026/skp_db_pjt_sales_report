"""DB 연결 설정 및 커넥션 관리 모듈.

.env 파일에서 접속 정보를 읽어 MySQL(Market 스키마) 커넥션을 생성한다.

사용 예:
    from config.db_config import get_connection

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
"""

import os
from contextlib import contextmanager

import pymysql
from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일을 환경변수로 로드
load_dotenv()


def get_db_config() -> dict:
    """환경변수에서 DB 접속 정보를 읽어 pymysql.connect()용 딕셔너리로 반환한다."""
    required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(f".env에 다음 값이 없습니다: {', '.join(missing)}")

    return {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,  # 결과를 dict로 받아 pandas 변환이 쉬움
    }


@contextmanager
def get_connection():
    """DB 커넥션을 열고, with 블록이 끝나면 자동으로 닫는다."""
    conn = pymysql.connect(**get_db_config())
    try:
        yield conn
    finally:
        conn.close()


def test_connection() -> bool:
    """접속 테스트: 성공하면 True, 실패하면 오류를 출력하고 False."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION() AS version")
                print(f"DB 연결 성공 (MySQL {cursor.fetchone()['version']})")
        return True
    except (pymysql.MySQLError, RuntimeError) as e:
        print(f"DB 연결 실패: {e}")
        return False


if __name__ == "__main__":
    test_connection()
