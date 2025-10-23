from flask_migrate import Migrate
from models import Email, EmailCategory, EmailPriority, EmailSummary, EmailThread, db

# 마이그레이션 초기화
migrate = Migrate()


def init_db(app):
    """데이터베이스 초기화"""
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # 테이블 생성
        db.create_all()

    return db
