#!/usr/bin/env python3
"""
기존 POP3Client 사용 테스트
"""

from dotenv import load_dotenv
import os
from services.pop3_client import POP3Client

def test_existing_client():
    """기존 POP3Client 사용 테스트"""
    load_dotenv()
    
    print("=== 기존 POP3Client 테스트 ===")
    
    try:
        # 기존 클라이언트 사용
        with POP3Client(
            host=os.getenv('POP3_HOST'),
            port=int(os.getenv('POP3_PORT')),
            username=os.getenv('POP3_USERNAME'),
            password=os.getenv('POP3_PASSWORD'),
            use_ssl=os.getenv('POP3_USE_SSL', 'True').lower() == 'true'
        ) as client:
            
            if client.connection:
                print("✅ 연결 성공!")
                
                # 메시지 개수 확인
                count = client.get_message_count()
                print(f"📧 서버에 {count}개의 메시지가 있습니다.")
                
                # 메시지 목록 확인 (최대 5개)
                if count > 0:
                    messages = client.get_message_list()
                    print(f"\n📋 메시지 목록 (최근 5개):")
                    for msg in messages[-5:]:
                        print(f"  메시지 {msg['number']}: {msg['size']} bytes")
                
            else:
                print("❌ 연결 실패")
                
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_existing_client()
