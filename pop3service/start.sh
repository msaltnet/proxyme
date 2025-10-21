#!/bin/bash

echo "ProxyMe Email Service 시작 중..."

# 가상환경 활성화 (있는 경우)
if [ -f "venv/bin/activate" ]; then
    echo "가상환경 활성화 중..."
    source venv/bin/activate
fi

# 의존성 설치
echo "의존성 설치 중..."
pip install -r requirements.txt

# 환경 변수 파일 확인
if [ ! -f ".env" ]; then
    echo ".env 파일이 없습니다. env.example을 복사하여 .env 파일을 생성하고 설정을 입력하세요."
    cp env.example .env
    echo ".env 파일을 생성했습니다. 설정을 확인하고 다시 실행하세요."
    exit 1
fi

# 데이터베이스 마이그레이션
echo "데이터베이스 마이그레이션 실행 중..."
python manage.py db init
python manage.py db migrate -m "Initial migration"
python manage.py db upgrade

# 애플리케이션 실행
echo "애플리케이션 시작 중..."
python app.py
