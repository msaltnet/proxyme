# ProxyMe ChatBot

Streamlit을 사용한 웹 GUI 챗봇 애플리케이션입니다.

## 기능

- 텍스트 기반 채팅 인터페이스
- **LiteLLM 기반 멀티 LLM 지원** (OpenAI, Anthropic, Google, Cohere 등)
- **폴백 모델 지원** (장애 시 자동 대체)
- **멀티 모델 동시 응답** (여러 모델로 같은 질문에 답변)
- **스트리밍 응답 지원** (실시간 답변 생성)
- 대화 기록 관리
- 확장 가능한 구조 (향후 버튼, 멀티모달 입력 지원)

## 설치 및 실행

공통으로 우선 환경 변수 설정 필요. `env.example` 를 `.env` 로 복사해서 작성.

### 방법 1: Docker 사용

Docker로 실행 또는 직접 Docker Compose 사용:

```bash
docker-compose up --build
```

### 방법 2: 로컬 설치

의존성 설치
```bash
pip install -r requirements.txt
```

애플리케이션 실행
```bash
streamlit run app.py
```

## 사용법

1. 웹 브라우저에서 `http://localhost:8501` 접속
2. 하단 입력창에 메시지 입력
3. Enter 키 또는 전송 버튼으로 메시지 전송
4. AI가 응답을 생성하여 표시

### 환경 변수

- `LITELLM_HOST_URL`: LiteLLM 서버 URL (예: http://localhost:4000)
- `LITELLM_API_KEY`: LiteLLM API 키 (예: dummy)
- `LLM_MODEL`: 사용할 LLM 모델 (예: llama-2, mistral-7b, gpt-3.5-turbo)
- `LLM_MAX_TOKENS`: 최대 토큰 수 (기본값: 1000)
- `LLM_TEMPERATURE`: 온도 설정 (기본값: 0.7)
- `SYSTEM_PROMPT`: 시스템 프롬프트
- `FALLBACK_MODELS`: 폴백 모델 목록 (쉼표로 구분, 예: gpt-3.5-turbo,llama-2)

## 고급 기능

### 멀티 모델 지원
여러 LLM을 동시에 사용하여 같은 질문에 답변을 받을 수 있습니다.

```python
# 여러 모델로 동시 응답
responses = llm_service.get_multiple_responses(
    "안녕하세요!",
    models=["gpt-3.5-turbo", "llama-2", "mistral-7b"]
)
```

### 폴백 모델 지원
주 모델이 실패할 경우 자동으로 다른 모델로 전환합니다.

```python
# 폴백 모델과 함께 응답
response = llm_service.get_response_with_fallback(
    "안녕하세요!",
    fallback_models=["gpt-3.5-turbo", "llama-2"]
)
```

### 스트리밍 응답
실시간으로 응답을 받아볼 수 있습니다.

```python
# 스트리밍 응답 (비동기)
async for chunk in llm_service.get_streaming_response("안녕하세요!"):
    print(chunk, end="", flush=True)
```

## 오프레미스 호스트 사용

### LiteLLM 사용

LiteLLM을 사용하여 로컬 LLM 모델을 OpenAI 호환 API로 제공할 수 있습니다.

1. **LiteLLM 서버 시작**:
```bash
# 예: Llama 2 모델 사용
litellm --model llama-2 --port 4000
```

2. **환경 변수 설정**:
```bash
# .env 파일
OPENAI_BASE_URL=http://localhost:4000/v1
OPENAI_API_KEY=dummy  # LiteLLM은 API 키가 필요하지 않지만 빈 값이 아닌 값이 필요
LLM_MODEL=llama-2
```

### 기타 호환 호스트

- **Ollama**: `http://localhost:11434/v1`
- **LocalAI**: `http://localhost:8080/v1`
- **vLLM**: `http://localhost:8000/v1`

### 설정 예시

```bash
# Ollama 사용
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
LLM_MODEL=llama2

# LocalAI 사용
OPENAI_BASE_URL=http://localhost:8080/v1
OPENAI_API_KEY=your_localai_key
LLM_MODEL=gpt-3.5-turbo
```
