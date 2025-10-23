from datetime import datetime
from typing import List, Dict, Optional
import logging
from models import db, Email, EmailThread, EmailCategory, EmailPriority, EmailSummary
from services.pop3_client import POP3Client
from config.settings import Config

logger = logging.getLogger(__name__)

class EmailService:
    """이메일 서비스 클래스"""
    
    def __init__(self, config):
        self.config = config
        self.pop3_client = POP3Client(
            host=config.get('POP3_HOST', 'pop.gmail.com'),
            port=config.get('POP3_PORT', 995),
            username=config.get('POP3_USERNAME', ''),
            password=config.get('POP3_PASSWORD', ''),
            use_ssl=config.get('POP3_USE_SSL', True)
        )
    
    def sync_emails(self, delete_from_server: bool = False) -> Dict:
        """POP3 서버에서 이메일 동기화"""
        result = {
            'total_messages': 0,
            'new_messages': 0,
            'updated_messages': 0,
            'errors': []
        }
        
        try:
            with self.pop3_client as client:
                if not client.connection:
                    raise Exception("POP3 서버 연결 실패")
                
                # 메시지 개수 확인
                message_count = client.get_message_count()
                result['total_messages'] = message_count
                
                logger.info(f"서버에서 {message_count}개의 메시지 발견")
                
                # 메시지 목록 가져오기
                messages = client.get_message_list()
                
                for message_info in messages:
                    try:
                        message_number = message_info['number']
                        
                        # 메시지 가져오기
                        message_data = client.fetch_message(message_number)
                        if not message_data:
                            continue
                        
                        # 데이터베이스에 저장
                        email_obj = self._save_email_to_db(message_data)
                        
                        if email_obj:
                            if email_obj.id:  # 새로 생성된 경우
                                result['new_messages'] += 1
                                logger.info(f"새 이메일 저장됨: {email_obj.message_id}")
                            else:  # 업데이트된 경우
                                result['updated_messages'] += 1
                                logger.info(f"이메일 업데이트됨: {email_obj.message_id}")
                        
                        # 서버에서 삭제 (옵션)
                        if delete_from_server:
                            client.delete_message(message_number)
                            logger.info(f"서버에서 메시지 {message_number} 삭제됨")
                    
                    except Exception as e:
                        error_msg = f"메시지 {message_info['number']} 처리 실패: {e}"
                        logger.error(error_msg)
                        result['errors'].append(error_msg)
                        continue
                
                # 트랜잭션 커밋
                db.session.commit()
                logger.info("이메일 동기화 완료")
                
        except Exception as e:
            logger.error(f"이메일 동기화 실패: {e}")
            db.session.rollback()
            result['errors'].append(str(e))
        
        return result
    
    def _save_email_to_db(self, message_data: Dict) -> Optional[Email]:
        """이메일 데이터를 데이터베이스에 저장"""
        try:
            message_id = message_data.get('message_id')
            if not message_id:
                logger.warning("Message-ID가 없는 메시지 건너뜀")
                return None
            
            # 기존 이메일 확인
            existing_email = Email.query.filter_by(message_id=message_id).first()
            
            if existing_email:
                # 기존 이메일 업데이트
                existing_email.subject = message_data.get('subject', existing_email.subject)
                existing_email.sender = message_data.get('sender', existing_email.sender)
                existing_email.recipient = message_data.get('recipient', existing_email.recipient)
                existing_email.body_text = message_data.get('body_text', existing_email.body_text)
                existing_email.body_html = message_data.get('body_html', existing_email.body_html)
                existing_email.attachments = message_data.get('attachments', existing_email.attachments)
                existing_email.headers = message_data.get('headers', existing_email.headers)
                existing_email.size = message_data.get('size', existing_email.size)
                existing_email.updated_at = datetime.utcnow()
                
                db.session.add(existing_email)
                return existing_email
            else:
                # 새 이메일 생성
                new_email = Email(
                    message_id=message_id,
                    subject=message_data.get('subject', ''),
                    sender=message_data.get('sender', ''),
                    recipient=message_data.get('recipient', ''),
                    date_received=message_data.get('date_received', datetime.utcnow()),
                    body_text=message_data.get('body_text', ''),
                    body_html=message_data.get('body_html', ''),
                    attachments=message_data.get('attachments', []),
                    headers=message_data.get('headers', {}),
                    size=message_data.get('size', 0),
                    is_read=False,
                    is_processed=False
                )
                
                db.session.add(new_email)
                return new_email
                
        except Exception as e:
            logger.error(f"이메일 저장 실패: {e}")
            return None
    
    def get_emails(self, limit: int = 50, offset: int = 0, 
                   sender: Optional[str] = None, 
                   date_from: Optional[datetime] = None,
                   date_to: Optional[datetime] = None) -> List[Email]:
        """이메일 목록 조회"""
        try:
            query = Email.query
            
            # 필터 적용
            if sender:
                query = query.filter(Email.sender.ilike(f'%{sender}%'))
            
            if date_from:
                query = query.filter(Email.date_received >= date_from)
            
            if date_to:
                query = query.filter(Email.date_received <= date_to)
            
            # 정렬 및 페이징
            emails = query.order_by(Email.date_received.desc()).offset(offset).limit(limit).all()
            
            return emails
            
        except Exception as e:
            logger.error(f"이메일 목록 조회 실패: {e}")
            return []
    
    def get_email_by_id(self, email_id: int) -> Optional[Email]:
        """ID로 이메일 조회"""
        try:
            return Email.query.get(email_id)
        except Exception as e:
            logger.error(f"이메일 조회 실패: {e}")
            return None
    
    def get_email_by_message_id(self, message_id: str) -> Optional[Email]:
        """Message-ID로 이메일 조회"""
        try:
            return Email.query.filter_by(message_id=message_id).first()
        except Exception as e:
            logger.error(f"이메일 조회 실패: {e}")
            return None
    
    def mark_as_read(self, email_id: int) -> bool:
        """이메일을 읽음으로 표시"""
        try:
            email = Email.query.get(email_id)
            if email:
                email.is_read = True
                email.updated_at = datetime.utcnow()
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"이메일 읽음 표시 실패: {e}")
            db.session.rollback()
            return False
    
    def mark_as_processed(self, email_id: int) -> bool:
        """이메일을 처리됨으로 표시"""
        try:
            email = Email.query.get(email_id)
            if email:
                email.is_processed = True
                email.updated_at = datetime.utcnow()
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"이메일 처리 표시 실패: {e}")
            db.session.rollback()
            return False
    
    def delete_email(self, email_id: int) -> bool:
        """이메일 삭제"""
        try:
            email = Email.query.get(email_id)
            if email:
                db.session.delete(email)
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"이메일 삭제 실패: {e}")
            db.session.rollback()
            return False
    
    def get_email_statistics(self) -> Dict:
        """이메일 통계 조회"""
        try:
            total_emails = Email.query.count()
            unread_emails = Email.query.filter_by(is_read=False).count()
            processed_emails = Email.query.filter_by(is_processed=True).count()
            
            # 최근 7일간의 이메일 수
            from datetime import timedelta
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_emails = Email.query.filter(Email.date_received >= week_ago).count()
            
            return {
                'total_emails': total_emails,
                'unread_emails': unread_emails,
                'processed_emails': processed_emails,
                'recent_emails': recent_emails
            }
        except Exception as e:
            logger.error(f"이메일 통계 조회 실패: {e}")
            return {}
