import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    """애플리케이션 설정 클래스"""
    
    # 데이터베이스 설정
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/proxyme_email')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # POP3 서버 설정
    POP3_HOST = os.getenv('POP3_HOST', 'pop.gmail.com')
    POP3_PORT = int(os.getenv('POP3_PORT', '995'))
    POP3_USERNAME = os.getenv('POP3_USERNAME', '')
    POP3_PASSWORD = os.getenv('POP3_PASSWORD', '')
    POP3_USE_SSL = os.getenv('POP3_USE_SSL', 'True').lower() == 'true'
    
    # Flask 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # 로그 설정
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    @staticmethod
    def init_app(app):
        """애플리케이션 초기화"""
        pass

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True

class ProductionConfig(Config):
    """프로덕션 환경 설정"""
    DEBUG = False

# 설정 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
