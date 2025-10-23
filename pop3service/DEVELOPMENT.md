# POP3Service 모듈 개발 환경 설정

## 린트 및 포매터 설정

이 프로젝트는 다음과 같은 코드 품질 도구들을 사용합니다:

- **Black**: 코드 포매터 (88자 줄 길이)
- **isort**: import 정렬 도구
- **flake8**: 린터 (88자 줄 길이, E203, W503, E501 무시)
- **pre-commit**: Git 커밋 전 자동 검사

## 설치 및 설정

### 1. 의존성 설치

```bash
cd pop3service
pip install -r requirements.txt
```

### 2. Pre-commit 설치

```bash
cd pop3service
python -m pre_commit install
```

## 사용법

### 수동 실행

```bash
# Black 포매터 적용
python -m black .

# isort로 import 정렬
python -m isort .

# flake8으로 린트 검사
python -m flake8 .
```

### Pre-commit 실행

```bash
# 모든 파일에 대해 pre-commit 실행
python -m pre_commit run --all-files

# 특정 파일에 대해 pre-commit 실행
python -m pre_commit run --files app.py
```

## 설정 파일

- `pyproject.toml`: Black, isort, flake8 설정
- `.flake8`: flake8 설정 (88자 줄 길이)
- `.pre-commit-config.yaml`: pre-commit 훅 설정

## Git 커밋 시 자동 실행

pre-commit이 설치되면 Git 커밋 시 자동으로 다음 검사들이 실행됩니다:

1. trailing whitespace 제거
2. 파일 끝 개행 문자 추가
3. YAML 파일 검증
4. 큰 파일 검사
5. merge conflict 검사
6. debug statements 검사
7. Black 포매터 적용
8. isort로 import 정렬

모든 검사를 통과해야 커밋이 완료됩니다.

## 프로젝트 구조

```
pop3service/
├── app/                 # Flask 애플리케이션 팩토리
├── config/              # 설정 관리
├── models/              # 데이터베이스 모델
├── services/            # 비즈니스 로직
├── migrations/          # 데이터베이스 마이그레이션
├── static/              # 정적 파일
├── templates/           # HTML 템플릿
├── instance/            # 데이터베이스 파일
└── tests/               # 테스트 파일
```

## 주요 기능

- POP3 서버에서 이메일 동기화
- 이메일 데이터베이스 저장 및 관리
- Flask 웹 인터페이스
- 이메일 통계 및 검색 기능
