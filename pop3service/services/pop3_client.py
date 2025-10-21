import poplib
import email
import email.utils
import ssl
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class POP3Client:
    """POP3 클라이언트 클래스"""
    
    def __init__(self, host: str, port: int, username: str, password: str, use_ssl: bool = True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.connection = None
    
    def connect(self) -> bool:
        """POP3 서버에 연결"""
        try:
            if self.use_ssl:
                # SSL 연결
                self.connection = poplib.POP3_SSL(self.host, self.port)
            else:
                # 일반 연결
                self.connection = poplib.POP3(self.host, self.port)
            
            # 인증
            self.connection.user(self.username)
            self.connection.pass_(self.password)
            
            logger.info(f"POP3 서버에 성공적으로 연결됨: {self.host}:{self.port}")
            return True
            
        except Exception as e:
            logger.error(f"POP3 서버 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """POP3 서버 연결 해제"""
        if self.connection:
            try:
                self.connection.quit()
                logger.info("POP3 서버 연결 해제됨")
            except Exception as e:
                logger.error(f"POP3 서버 연결 해제 실패: {e}")
            finally:
                self.connection = None
    
    def get_message_count(self) -> int:
        """서버의 메시지 개수 반환"""
        if not self.connection:
            return 0
        
        try:
            stat = self.connection.stat()
            return stat[0]  # 메시지 개수
        except Exception as e:
            logger.error(f"메시지 개수 조회 실패: {e}")
            return 0
    
    def get_message_list(self) -> List[Dict]:
        """메시지 목록 반환"""
        if not self.connection:
            return []
        
        try:
            messages = []
            stat = self.connection.stat()
            message_count = stat[0]
            
            for i in range(1, message_count + 1):
                try:
                    # 메시지 정보 조회
                    message_info = self.connection.list(i)
                    size = message_info[1].split()[1] if len(message_info[1].split()) > 1 else 0
                    
                    messages.append({
                        'number': i,
                        'size': int(size),
                        'uid': message_info[1].decode('utf-8') if isinstance(message_info[1], bytes) else message_info[1]
                    })
                except Exception as e:
                    logger.warning(f"메시지 {i} 정보 조회 실패: {e}")
                    continue
            
            return messages
            
        except Exception as e:
            logger.error(f"메시지 목록 조회 실패: {e}")
            return []
    
    def fetch_message(self, message_number: int) -> Optional[Dict]:
        """특정 메시지 가져오기"""
        if not self.connection:
            return None
        
        try:
            # 메시지 내용 가져오기
            response, lines, octets = self.connection.retr(message_number)
            
            # 바이트를 문자열로 변환
            message_content = b'\n'.join(lines).decode('utf-8', errors='ignore')
            
            # 이메일 파싱
            email_message = email.message_from_string(message_content)
            
            # 메시지 정보 추출
            message_data = self._parse_email_message(email_message)
            message_data['raw_content'] = message_content
            message_data['size'] = octets
            
            return message_data
            
        except Exception as e:
            logger.error(f"메시지 {message_number} 가져오기 실패: {e}")
            return None
    
    def _parse_email_message(self, email_message) -> Dict:
        """이메일 메시지 파싱"""
        try:
            # 기본 헤더 정보
            subject = email_message.get('Subject', '')
            sender = email_message.get('From', '')
            recipient = email_message.get('To', '')
            date_str = email_message.get('Date', '')
            message_id = email_message.get('Message-ID', '')
            
            # 날짜 파싱
            date_received = None
            if date_str:
                try:
                    date_received = email.utils.parsedate_to_datetime(date_str)
                except Exception:
                    date_received = datetime.utcnow()
            else:
                date_received = datetime.utcnow()
            
            # 본문 추출
            body_text = ""
            body_html = ""
            
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition', ''))
                    
                    if 'attachment' not in content_disposition:
                        if content_type == 'text/plain':
                            body_text = self._decode_content(part)
                        elif content_type == 'text/html':
                            body_html = self._decode_content(part)
            else:
                content_type = email_message.get_content_type()
                if content_type == 'text/plain':
                    body_text = self._decode_content(email_message)
                elif content_type == 'text/html':
                    body_html = self._decode_content(email_message)
            
            # 첨부파일 정보
            attachments = []
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_disposition = str(part.get('Content-Disposition', ''))
                    if 'attachment' in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            attachments.append({
                                'filename': filename,
                                'content_type': part.get_content_type(),
                                'size': len(part.get_payload(decode=True)) if part.get_payload(decode=True) else 0
                            })
            
            # 헤더 정보
            headers = {}
            for header in email_message.keys():
                headers[header] = email_message.get(header)
            
            return {
                'message_id': message_id,
                'subject': subject,
                'sender': sender,
                'recipient': recipient,
                'date_received': date_received,
                'body_text': body_text,
                'body_html': body_html,
                'attachments': attachments,
                'headers': headers
            }
            
        except Exception as e:
            logger.error(f"이메일 메시지 파싱 실패: {e}")
            return {}
    
    def _decode_content(self, part) -> str:
        """이메일 본문 디코딩"""
        try:
            payload = part.get_payload(decode=True)
            if payload:
                charset = part.get_content_charset() or 'utf-8'
                return payload.decode(charset, errors='ignore')
            return ""
        except Exception as e:
            logger.error(f"본문 디코딩 실패: {e}")
            return ""
    
    def delete_message(self, message_number: int) -> bool:
        """메시지 삭제 (서버에서)"""
        if not self.connection:
            return False
        
        try:
            self.connection.dele(message_number)
            logger.info(f"메시지 {message_number} 삭제됨")
            return True
        except Exception as e:
            logger.error(f"메시지 {message_number} 삭제 실패: {e}")
            return False
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.disconnect()
