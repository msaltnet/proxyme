"""
챗봇 설정 관리
"""

import os
from typing import Dict, Any
import json

class ChatBotConfig:
    """챗봇 설정 클래스"""
    
    def __init__(self):
        self.config = self._load_default_config()
        self._load_env_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """기본 설정 로드"""
        return {
            "llm": {
                "model": "gpt-3.5-turbo",
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            },
            "ui": {
                "page_title": "ProxyMe ChatBot",
                "page_icon": "🤖",
                "layout": "wide",
                "sidebar_state": "expanded"
            },
            "features": {
                "text_input": True,
                "button_input": False,  # 향후 구현
                "multimodal_input": False,  # 향후 구현
                "voice_input": False,  # 향후 구현
                "file_upload": False,  # 향후 구현
                "export_conversation": True,
                "import_conversation": True
            },
            "system_prompt": "당신은 ProxyMe라는 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 정확하고 유용한 답변을 제공해주세요."
        }
    
    def _load_env_config(self):
        """환경 변수에서 설정 로드"""
        # LLM 설정
        if os.getenv("LLM_MODEL"):
            self.config["llm"]["model"] = os.getenv("LLM_MODEL")
        
        if os.getenv("LLM_MAX_TOKENS"):
            self.config["llm"]["max_tokens"] = int(os.getenv("LLM_MAX_TOKENS"))
        
        if os.getenv("LLM_TEMPERATURE"):
            self.config["llm"]["temperature"] = float(os.getenv("LLM_TEMPERATURE"))
        
        # 시스템 프롬프트
        if os.getenv("SYSTEM_PROMPT"):
            self.config["system_prompt"] = os.getenv("SYSTEM_PROMPT")
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정 값 가져오기"""
        keys = key.split(".")
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """설정 값 설정"""
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """설정을 딕셔너리로 반환"""
        return self.config.copy()
    
    def save_to_file(self, filepath: str):
        """설정을 파일로 저장"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """파일에서 설정 로드"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
