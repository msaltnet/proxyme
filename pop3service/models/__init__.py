import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Email(db.Model):
    """이메일 모델"""

    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    subject = db.Column(db.Text)
    sender = db.Column(db.String(255), nullable=False, index=True)
    recipient = db.Column(db.String(255), nullable=False, index=True)
    date_received = db.Column(db.DateTime, nullable=False, index=True)
    date_sent = db.Column(db.DateTime)

    # 이메일 내용
    body_text = db.Column(db.Text)
    body_html = db.Column(db.Text)

    # 첨부파일 정보
    attachments = db.Column(db.Text)  # JSON을 Text로 변경

    # 메타데이터
    headers = db.Column(db.Text)  # JSON을 Text로 변경
    size = db.Column(db.Integer)

    # 처리 상태
    is_read = db.Column(db.Boolean, default=False)
    is_processed = db.Column(db.Boolean, default=False)

    # 생성/수정 시간
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Email {self.message_id}: {self.subject}>"

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "message_id": self.message_id,
            "subject": self.subject,
            "sender": self.sender,
            "recipient": self.recipient,
            "date_received": self.date_received.isoformat()
            if self.date_received
            else None,
            "date_sent": self.date_sent.isoformat() if self.date_sent else None,
            "body_text": self.body_text,
            "body_html": self.body_html,
            "attachments": json.loads(self.attachments) if self.attachments else None,
            "headers": json.loads(self.headers) if self.headers else None,
            "size": self.size,
            "is_read": self.is_read,
            "is_processed": self.is_processed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class EmailThread(db.Model):
    """이메일 스레드 모델"""

    __tablename__ = "email_threads"

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    subject = db.Column(db.Text)
    participants = db.Column(db.Text)  # 참여자 목록 (JSON을 Text로 변경)
    email_count = db.Column(db.Integer, default=0)

    # 생성/수정 시간
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<EmailThread {self.thread_id}: {self.subject}>"


class EmailCategory(db.Model):
    """이메일 카테고리 모델"""

    __tablename__ = "email_categories"

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    confidence = db.Column(db.Float)  # 분류 신뢰도

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailCategory {self.email_id}: {self.category}>"


class EmailPriority(db.Model):
    """이메일 우선순위 모델"""

    __tablename__ = "email_priorities"

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False)
    priority_level = db.Column(db.Integer, nullable=False)  # 1-5 (1: 높음, 5: 낮음)
    requires_response = db.Column(db.Boolean, default=False)
    confidence = db.Column(db.Float)  # 우선순위 판단 신뢰도

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailPriority {self.email_id}: {self.priority_level}>"


class EmailSummary(db.Model):
    """이메일 요약 모델"""

    __tablename__ = "email_summaries"

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False)
    summary = db.Column(db.Text)
    keywords = db.Column(db.Text)  # 키워드 목록 (JSON을 Text로 변경)
    sentiment = db.Column(db.String(50))  # 감정 분석 결과

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailSummary {self.email_id}>"
