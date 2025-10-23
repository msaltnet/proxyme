# Chat 모듈 개발 환경 설정

## 린트 및 포매터 설정

이 프로젝트는 다음과 같은 코드 품질 도구들을 사용합니다:

- **Black**: 코드 포매터 (88자 줄 길이)
- **isort**: import 정렬 도구
- **flake8**: 린터 (88자 줄 길이, E203, W503, E501 무시)
- **pre-commit**: Git 커밋 전 자동 검사

## 설치 및 설정

### 1. 의존성 설치

```bash
cd chat
pip install -r requirements.txt
```

### 2. Pre-commit 설치

```bash
cd chat
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
