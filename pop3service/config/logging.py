import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """로깅 설정"""
    if not app.debug and not app.testing:
        # 로그 디렉토리 생성
        if not os.path.exists("logs"):
            os.mkdir("logs")

        # 파일 핸들러 설정
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("ProxyMe Email Service startup")
