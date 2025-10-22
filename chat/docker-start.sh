#!/bin/bash

echo "ProxyMe ChatBot Docker 컨테이너를 시작합니다..."
echo

# 환경 변수 파일 확인
if [ ! -f ".env" ]; then
    echo ".env 파일이 없습니다. .env.docker.example을 복사하여 설정하세요."
    cp .env.docker.example .env
    echo
    echo ".env 파일을 편집하여 OPENAI_API_KEY를 설정한 후 다시 실행하세요."
    exit 1
fi

# Docker Compose로 서비스 시작
echo "Docker Compose로 서비스를 시작합니다..."
docker-compose up --build
