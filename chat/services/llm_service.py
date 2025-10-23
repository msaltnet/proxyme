"""
LLM 서비스 모듈 - LiteLLM 기반
"""

from litellm import completion, completion_with_fallbacks, acompletion
import os
from typing import List, Dict, Any, Optional
import json

class LLMService:
    """LLM 서비스 클래스 - LiteLLM 기반"""
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        # LiteLLM 설정
        self.litellm_host = os.getenv("LITELLM_HOST_URL")
        self.litellm_api_key = os.getenv("LITELLM_API_KEY")
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
        if not self.litellm_host:
            raise ValueError("LITELLM_HOST_URL이 설정되지 않았습니다")
        
        # LiteLLM 모델명 설정
        self.model_name = f"openai/{self.model}"
        self.api_base = f"{self.litellm_host.rstrip('/')}/v1"
        self.api_key = self.litellm_api_key or "dummy"
        
        # LiteLLM 환경 변수 설정
        os.environ["OPENAI_API_KEY"] = self.api_key
        os.environ["OPENAI_API_BASE"] = self.api_base
    
    
    def add_message(self, role: str, content: str):
        """대화 기록에 메시지 추가"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_response(self, user_input: str, **kwargs) -> str:
        """사용자 입력에 대한 LLM 응답 생성"""
        try:
            # 사용자 메시지 추가
            self.add_message("user", user_input)
            
            # LiteLLM completion 호출
            response = completion(
                model=self.model_name,
                messages=self.conversation_history,
                max_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7),
                api_base=self.api_base
            )
            
            # 응답 추출
            bot_response = response.choices[0].message.content
            
            # 봇 응답을 대화 기록에 추가
            self.add_message("assistant", bot_response)
            
            return bot_response
            
        except Exception as e:
            error_msg = f"LLM 응답 생성 중 오류 발생: {str(e)}"
            raise RuntimeError(error_msg) from e
    
    def get_response_with_fallback(self, user_input: str, fallback_models: List[str] = None, **kwargs) -> str:
        """폴백 모델을 사용한 LLM 응답 생성"""
        try:
            # 사용자 메시지 추가
            self.add_message("user", user_input)
            
            # 폴백 모델 설정
            if fallback_models is None:
                fallback_models = [self.model_name]
            
            # LiteLLM completion_with_fallbacks 호출
            response = completion_with_fallbacks(
                model=fallback_models,
                messages=self.conversation_history,
                max_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7),
                api_base=self.api_base
            )
            
            # 응답 추출
            bot_response = response.choices[0].message.content
            
            # 봇 응답을 대화 기록에 추가
            self.add_message("assistant", bot_response)
            
            return bot_response
            
        except Exception as e:
            error_msg = f"LLM 응답 생성 중 오류 발생 (폴백 포함): {str(e)}"
            raise RuntimeError(error_msg) from e
    
    def get_multiple_responses(self, user_input: str, models: List[str], **kwargs) -> Dict[str, str]:
        """여러 모델로 동시 응답 생성"""
        responses = {}
        
        for model in models:
            try:
                # 임시로 모델 변경
                original_model = self.model_name
                self.model_name = f"openai/{model}"
                
                response = self.get_response(user_input, **kwargs)
                responses[model] = response
                
                # 원래 모델로 복원
                self.model_name = original_model
                
            except Exception as e:
                responses[model] = f"오류: {str(e)}"
        
        return responses
    
    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """대화 기록 반환"""
        return self.conversation_history.copy()
    
    def set_system_prompt(self, prompt: str):
        """시스템 프롬프트 설정"""
        # 기존 시스템 메시지가 있다면 제거
        self.conversation_history = [
            msg for msg in self.conversation_history 
            if msg["role"] != "system"
        ]
        
        # 새로운 시스템 메시지 추가
        self.conversation_history.insert(0, {
            "role": "system",
            "content": prompt
        })
    
    def export_conversation(self) -> str:
        """대화 기록을 JSON으로 내보내기"""
        return json.dumps(self.conversation_history, ensure_ascii=False, indent=2)
    
    def import_conversation(self, conversation_json: str):
        """JSON에서 대화 기록 가져오기"""
        try:
            self.conversation_history = json.loads(conversation_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"잘못된 JSON 형식: {str(e)}") from e
    
    async def get_streaming_response(self, user_input: str, **kwargs):
        """스트리밍 응답 생성 (비동기)"""
        try:
            # 사용자 메시지 추가
            self.add_message("user", user_input)
            
            # LiteLLM 비동기 스트리밍 호출
            response = await acompletion(
                model=self.model_name,
                messages=self.conversation_history,
                max_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7),
                api_base=self.api_base,
                stream=True
            )
            
            full_response = ""
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # 전체 응답을 대화 기록에 추가
            self.add_message("assistant", full_response)
            
        except Exception as e:
            error_msg = f"스트리밍 응답 생성 중 오류 발생: {str(e)}"
            raise RuntimeError(error_msg) from e
