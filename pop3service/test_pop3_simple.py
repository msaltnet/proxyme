#!/usr/bin/env python3
"""
간단한 POP3 테스트 - poplib 사용
"""

import os
import poplib

from dotenv import load_dotenv


def test_pop3_simple():
    """간단한 POP3 연결 테스트"""
    load_dotenv()

    host = os.getenv("POP3_HOST", "pop.gmail.com")
    port = int(os.getenv("POP3_PORT", "995"))
    username = os.getenv("POP3_USERNAME", "")
    password = os.getenv("POP3_PASSWORD", "")

    print(f"=== 간단한 POP3 테스트 ===")
    print(f"호스트: {host}")
    print(f"포트: {port}")
    print(f"사용자명: {username}")

    try:
        print("\n1. POP3 서버 연결 중...")

        # SSL 연결
        server = poplib.POP3_SSL(host, port)

        print("2. 사용자 인증 중...")
        server.user(username)
        server.pass_(password)

        print("3. 연결 성공! 메시지 정보 확인...")

        # 메시지 개수 확인
        num_messages, total_size = server.stat()
        print(f"📧 총 {num_messages}개의 메시지, {total_size} bytes")

        # 메시지 목록 확인 (최대 5개)
        if num_messages > 0:
            print("\n4. 최근 메시지 목록:")
            messages = server.list()
            for i, msg_info in enumerate(messages[1][-5:]):  # 최근 5개
                msg_num, msg_size = msg_info.decode().split()
                print(f"  메시지 {msg_num}: {msg_size} bytes")

        print("\n5. 연결 종료...")
        server.quit()
        print("✅ 테스트 완료!")

    except poplib.error_proto as e:
        print(f"❌ POP3 프로토콜 오류: {e}")
    except Exception as e:
        print(f"❌ 연결 실패: {e}")


if __name__ == "__main__":
    test_pop3_simple()
