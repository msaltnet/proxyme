# ProxyMe ChatBot

Streamlit을 사용한 웹 GUI 챗봇 애플리케이션입니다.

## 기능

- 텍스트 기반 채팅 인터페이스
- OpenAI GPT 모델을 통한 LLM 응답
- 대화 기록 관리
- 확장 가능한 구조 (향후 버튼, 멀티모달 입력 지원)

## 설치 및 실행

### 방법 1: Docker 사용 (권장)

#### 1. 환경 변수 설정

```bash
cp .env.docker.example .env
# .env 파일을 편집하여 OPENAI_API_KEY 설정
```

#### 2. Docker로 실행

**Windows:**
```bash
docker-start.bat
```

**Linux/Mac:**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

**또는 직접 Docker Compose 사용:**
```bash
docker-compose up --build
```

### 방법 2: 로컬 설치

#### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

#### 2. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
cp .env.example .env
# .env 파일을 편집하여 OPENAI_API_KEY 설정
```

#### 3. 애플리케이션 실행

```bash
streamlit run app.py
```

## 사용법

1. 웹 브라우저에서 `http://localhost:8501` 접속
2. 하단 입력창에 메시지 입력
3. Enter 키 또는 전송 버튼으로 메시지 전송
4. AI가 응답을 생성하여 표시

## Docker 사용법

### Docker 명령어

```bash
# 이미지 빌드
docker build -t proxyme-chatbot .

# 컨테이너 실행
docker run -p 8501:8501 --env-file .env proxyme-chatbot

# Docker Compose로 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build

# 로그 확인
docker-compose logs -f chatbot

# 서비스 중지
docker-compose down
```

### Docker 환경 변수

- `OPENAI_API_KEY`: OpenAI API 키 (필수)
- `LLM_MODEL`: 사용할 LLM 모델 (기본값: gpt-3.5-turbo)
- `LLM_MAX_TOKENS`: 최대 토큰 수 (기본값: 1000)
- `LLM_TEMPERATURE`: 온도 설정 (기본값: 0.7)
- `SYSTEM_PROMPT`: 시스템 프롬프트

## 향후 개발 계획

- 버튼 입력 지원
- 멀티모달 입력 (이미지, 파일 등)
- 음성 입력/출력 기능
- 커스텀 프롬프트 설정
- 대화 내보내기/가져오기
