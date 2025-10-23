# ProxyMe Email Service

이메일을 POP3로 받아서 PostgreSQL 데이터베이스에 저장하는 서비스입니다.

## 기능
- POP3 서버에서 이메일 수신
- 이메일을 데이터베이스에 저장
- 웹 API를 통한 이메일 조회
- 이메일 메타데이터 관리
- 웹 인터페이스를 통한 이메일 관리

## 설치 및 실행

### 방법 1: Docker Compose 사용 (권장)

1. Docker와 Docker Compose 설치
2. 환경 변수 설정
```bash
cp env.example .env
# .env 파일을 편집하여 POP3 서버 설정 입력
```

3. 서비스 실행
```bash
docker-compose up -d
```

4. 웹 인터페이스 접속: http://localhost:5000

### 방법 2: 로컬 설치

1. Python 3.9+ 설치 (권장: Python 3.11+)
2. PostgreSQL 설치 및 데이터베이스 생성
```bash
createdb proxyme_email
```

또는 도커로 실행
```bash
# PostgreSQL 컨테이너 직접 실행
docker run -d \
  --name proxyme-postgres \
  -e POSTGRES_DB=proxyme_email \
  -e POSTGRES_USER=proxyme_user \
  -e POSTGRES_PASSWORD=proxyme_password \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:13
```

3. 프로젝트 설정
```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt

# 주요 패키지 버전:
# Flask==3.1.2
# Flask-Migrate==4.0.5
# Flask-SQLAlchemy==3.0.5
# psycopg2-binary==2.9.11
```

4. 환경 변수 설정
```bash
cp env.example .env
# .env 파일을 편집하여 설정값 입력
```

5. 데이터베이스 마이그레이션
```bash
# Flask CLI 방식 (권장)
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade
```

6. 서비스 실행
```bash
python app.py
```

## 설정

### 환경 변수 (.env 파일)

```env
# 데이터베이스 설정
DATABASE_URL=postgresql://username:password@localhost:5432/proxyme_email

# POP3 서버 설정
POP3_HOST=pop.gmail.com
POP3_PORT=995
POP3_USERNAME=your_email@gmail.com
POP3_PASSWORD=your_app_password
POP3_USE_SSL=True

# Flask 설정
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Gmail 설정 (예시)

Gmail을 사용하는 경우:
1. 2단계 인증 활성화
2. 앱 비밀번호 생성
3. POP3 설정에서 앱 비밀번호 사용

## API 엔드포인트

- `GET /` - 웹 인터페이스
- `GET /api/emails` - 이메일 목록 조회
- `GET /api/emails/{id}` - 특정 이메일 조회
- `POST /api/emails/{id}/read` - 이메일 읽음 표시
- `POST /api/emails/{id}/processed` - 이메일 처리됨 표시
- `DELETE /api/emails/{id}` - 이메일 삭제
- `POST /api/sync` - POP3에서 이메일 동기화
- `GET /api/statistics` - 이메일 통계
- `GET /api/health` - 헬스 체크

## 데이터베이스 스키마

### 주요 테이블
- `emails`: 이메일 기본 정보
- `email_threads`: 이메일 스레드 정보
- `email_categories`: 이메일 카테고리 분류
- `email_priorities`: 이메일 우선순위
- `email_summaries`: 이메일 요약 정보

## 개발

### Flask-Migrate 사용법

**Flask-Migrate 4.0.5에서는 Flask CLI 방식을 사용합니다:**

```bash
# 마이그레이션 초기화 (최초 1회만)
python -m flask db init

# 새 마이그레이션 생성
python -m flask db migrate -m "마이그레이션 설명"

# 마이그레이션 적용
python -m flask db upgrade

# 마이그레이션 히스토리 확인
python -m flask db history

# 특정 버전으로 되돌리기
python -m flask db downgrade <revision>
```

**주의사항:**
- `python manage.py db` 명령어는 Flask-Migrate 4.0.5에서 더 이상 지원되지 않습니다
- `manage.py`는 Flask 앱 실행용으로만 사용됩니다

### 프로젝트 구조
```
pop3service/
├── app/                 # Flask 애플리케이션
├── models/              # 데이터베이스 모델
├── services/            # 비즈니스 로직
├── config/              # 설정 파일
├── templates/           # HTML 템플릿
├── static/              # 정적 파일
├── migrations/          # 데이터베이스 마이그레이션
├── logs/                # 로그 파일
├── app.py               # 애플리케이션 진입점
├── manage.py            # 관리 스크립트
├── requirements.txt     # Python 의존성
├── Dockerfile           # Docker 이미지
├── docker-compose.yml   # Docker Compose 설정
└── README.md           # 프로젝트 문서
```

### 로그
애플리케이션 로그는 `logs/app.log`에 저장됩니다.

## 문제 해결

### 일반적인 문제들

1. **데이터베이스 연결 실패**
   - PostgreSQL 서비스가 실행 중인지 확인
   - DATABASE_URL 설정 확인

   netstat -an | findstr :5432
   ```

   **Python으로 연결 테스트:**
   ```python
   import psycopg2
   conn = psycopg2.connect(host='localhost', port=5432, user='proxyme_user', password='proxyme_password', database='proxyme_email')
   ```

   **Flask 앱 실행 테스트:**
   ```bash
   python manage.py
   # 또는
   python app.py
   ```

2. **POP3 연결 실패**
   - POP3 서버 설정 확인
   - 방화벽 설정 확인
   - 인증 정보 확인

3. **포트 충돌**
   - 다른 애플리케이션이 5000 포트를 사용 중인지 확인
   - 포트 변경: `export PORT=8080`

## 라이선스

MIT License
