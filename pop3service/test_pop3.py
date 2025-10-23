#!/usr/bin/env python3
"""
POP3 연결 테스트 스크립트
"""

import socket
import ssl
from dotenv import load_dotenv
import os

def test_pop3_connection():
    """POP3 연결 테스트"""
    load_dotenv()
    
    host = os.getenv('POP3_HOST', 'pop.gmail.com')
    port = int(os.getenv('POP3_PORT', '995'))
    username = os.getenv('POP3_USERNAME', '')
    password = os.getenv('POP3_PASSWORD', '')
    
    print(f"=== POP3 연결 테스트 ===")
    print(f"호스트: {host}")
    print(f"포트: {port}")
    print(f"사용자명: {username}")
    print(f"비밀번호 길이: {len(password)}")
    
    try:
        # SSL 소켓 생성
        print("\n1. SSL 소켓 생성 중...")
        context = ssl.create_default_context()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        
        print("2. 서버 연결 시도 중...")
        ssl_sock.connect((host, port))
        print("연결 성공!")
        
        # 서버 응답 확인
        print("3. 서버 응답 확인...")
        response = ssl_sock.recv(1024).decode('utf-8')
        print(f"서버 응답: {response.strip()}")
        
        # USER 명령
        print("4. 사용자 인증 시도...")
        ssl_sock.send(f"USER {username}\r\n".encode('utf-8'))
        response = ssl_sock.recv(1024).decode('utf-8')
        print(f"USER 응답: {response.strip()}")
        
        if "+OK" in response:
            # PASS 명령
            ssl_sock.send(f"PASS {password}\r\n".encode('utf-8'))
            response = ssl_sock.recv(1024).decode('utf-8')
            print(f"PASS 응답: {response.strip()}")
            
            if "+OK" in response:
                print("인증 성공!")
                
                # STAT 명령 (메시지 개수 확인)
                ssl_sock.send("STAT\r\n".encode('utf-8'))
                response = ssl_sock.recv(1024).decode('utf-8')
                print(f"STAT 응답: {response.strip()}")
                
                # QUIT 명령
                ssl_sock.send("QUIT\r\n".encode('utf-8'))
                response = ssl_sock.recv(1024).decode('utf-8')
                print(f"QUIT 응답: {response.strip()}")
                
            else:
                print("인증 실패!")
        else:
            print("사용자명 오류!")
            
    except socket.timeout:
        print("연결 시간 초과")
    except ConnectionRefusedError:
        print("연결 거부됨")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        try:
            ssl_sock.close()
            print("연결 종료")
        except:
            pass

if __name__ == "__main__":
    test_pop3_connection()
