"""
LLM 서비스 모듈
"""

import openai
import os
from typing import List, Dict, Any, Optional
import json

class LLMService:
    """LLM 서비스 클래스"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
        if not self.api_key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다")
        
        openai.api_key = self.api_key
    
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
            
            # 기본 파라미터 설정
            params = {
                "model": self.model,
                "messages": self.conversation_history,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 1.0),
                "frequency_penalty": kwargs.get("frequency_penalty", 0.0),
                "presence_penalty": kwargs.get("presence_penalty", 0.0)
            }
            
            # OpenAI API 호출
            response = openai.ChatCompletion.create(**params)
            
            # 응답 추출
            bot_response = response.choices[0].message.content
            
            # 봇 응답을 대화 기록에 추가
            self.add_message("assistant", bot_response)
            
            return bot_response
            
        except Exception as e:
            raise Exception(f"LLM 응답 생성 중 오류 발생: {str(e)}") from e
    
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
