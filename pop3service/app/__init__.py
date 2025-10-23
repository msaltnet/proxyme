import logging
from datetime import datetime, timedelta
from typing import Optional

from flask import Flask, jsonify, render_template, request
from models.database import init_db

from config.logging import setup_logging
from config.settings import config
from services.email_service import EmailService

logger = logging.getLogger(__name__)


def create_app(config_name="default"):
    """Flask 애플리케이션 팩토리"""
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 로깅 설정
    setup_logging(app)

    # 데이터베이스 초기화
    init_db(app)

    # 이메일 서비스 초기화 (설정 객체 전달)
    email_service = EmailService(app.config)

    @app.route("/")
    def index():
        """메인 페이지"""
        return render_template("index.html")

    @app.route("/api/emails", methods=["GET"])
    def get_emails():
        """이메일 목록 조회 API"""
        try:
            # 쿼리 파라미터
            limit = request.args.get("limit", 50, type=int)
            offset = request.args.get("offset", 0, type=int)
            sender = request.args.get("sender", type=str)
            date_from_str = request.args.get("date_from", type=str)
            date_to_str = request.args.get("date_to", type=str)

            # 날짜 파싱
            date_from = None
            date_to = None

            if date_from_str:
                try:
                    date_from = datetime.fromisoformat(
                        date_from_str.replace("Z", "+00:00")
                    )
                except ValueError:
                    return jsonify({"error": "Invalid date_from format"}), 400

            if date_to_str:
                try:
                    date_to = datetime.fromisoformat(date_to_str.replace("Z", "+00:00"))
                except ValueError:
                    return jsonify({"error": "Invalid date_to format"}), 400

            # 이메일 조회
            emails = email_service.get_emails(
                limit=limit,
                offset=offset,
                sender=sender,
                date_from=date_from,
                date_to=date_to,
            )

            # 응답 데이터 구성
            email_data = [email.to_dict() for email in emails]

            return jsonify(
                {
                    "emails": email_data,
                    "count": len(email_data),
                    "limit": limit,
                    "offset": offset,
                }
            )

        except Exception as e:
            logger.error(f"이메일 목록 조회 API 실패: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/emails/<int:email_id>", methods=["GET"])
    def get_email(email_id):
        """특정 이메일 조회 API"""
        try:
            email = email_service.get_email_by_id(email_id)
            if not email:
                return jsonify({"error": "Email not found"}), 404

            return jsonify(email.to_dict())

        except Exception as e:
            logger.error(f"이메일 조회 API 실패: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/emails/<int:email_id>/read", methods=["POST"])
    def mark_email_read(email_id):
        """이메일 읽음 표시 API"""
        try:
            success = email_service.mark_as_read(email_id)
            if not success:
                return jsonify({"error": "Email not found"}), 404

            return jsonify({"message": "Email marked as read"})

        except Exception as e:
            logger.error(f"이메일 읽음 표시 API 실패: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/emails/<int:email_id>/processed", methods=["POST"])
    def mark_email_processed(email_id):
        """이메일 처리됨 표시 API"""
        try:
            success = email_service.mark_as_processed(email_id)
            if not success:
                return jsonify({"error": "Email not found"}), 404

            return jsonify({"message": "Email marked as processed"})

        except Exception as e:
            logger.error(f"이메일 처리 표시 API 실패: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/emails/<int:email_id>", methods=["DELETE"])
    def delete_email(email_id):
        """이메일 삭제 API"""
        try:
            success = email_service.delete_email(email_id)
            if not success:
                return jsonify({"error": "Email not found"}), 404

            return jsonify({"message": "Email deleted"})

        except Exception as e:
            logger.error(f"이메일 삭제 API 실패: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/sync", methods=["POST"])
    def sync_emails():
        """이메일 동기화 API"""
        try:
            # 요청 데이터
            data = request.get_json() or {}
            delete_from_server = data.get("delete_from_server", False)

            # 동기화 실행
            result = email_service.sync_emails(delete_from_server=delete_from_server)

            return jsonify(result)

        except Exception as e:
            logger.error(f"이메일 동기화 API 실패: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/statistics", methods=["GET"])
    def get_statistics():
        """이메일 통계 API"""
        try:
            stats = email_service.get_email_statistics()
            return jsonify(stats)

        except Exception as e:
            logger.error(f"통계 API 실패: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """헬스 체크 API"""
        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "ProxyMe Email Service",
            }
        )

    # 에러 핸들러
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app
