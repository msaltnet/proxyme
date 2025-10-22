"""
챗봇의 핵심 기능을 담당하는 모듈들
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json

class InputHandler(ABC):
    """입력 처리기 추상 클래스"""
    
    @abstractmethod
    def can_handle(self, input_type: str) -> bool:
        """해당 입력 타입을 처리할 수 있는지 확인"""
        pass
    
    @abstractmethod
    def process(self, input_data: Any) -> str:
        """입력을 처리하여 텍스트로 변환"""
        pass

class TextInputHandler(InputHandler):
    """텍스트 입력 처리기"""
    
    def can_handle(self, input_type: str) -> bool:
        return input_type == "text"
    
    def process(self, input_data: str) -> str:
        return input_data.strip()

class ButtonInputHandler(InputHandler):
    """버튼 입력 처리기 (향후 구현)"""
    
    def can_handle(self, input_type: str) -> bool:
        return input_type == "button"
    
    def process(self, input_data: Dict[str, Any]) -> str:
        # 향후 버튼 입력 처리 로직 구현
        return f"버튼 클릭: {input_data.get('value', '')}"

class MultimodalInputHandler(InputHandler):
    """멀티모달 입력 처리기 (향후 구현)"""
    
    def can_handle(self, input_type: str) -> bool:
        return input_type in ["image", "file", "audio"]
    
    def process(self, input_data: Dict[str, Any]) -> str:
        # 향후 멀티모달 입력 처리 로직 구현
        input_type = input_data.get("type", "")
        return f"멀티모달 입력 ({input_type}): {input_data.get('description', '')}"

class InputProcessor:
    """입력 처리 관리자"""
    
    def __init__(self):
        self.handlers: List[InputHandler] = [
            TextInputHandler(),
            ButtonInputHandler(),
            MultimodalInputHandler()
        ]
    
    def process_input(self, input_type: str, input_data: Any) -> str:
        """입력 타입에 따라 적절한 처리기로 처리"""
        for handler in self.handlers:
            if handler.can_handle(input_type):
                return handler.process(input_data)
        
        raise ValueError(f"지원하지 않는 입력 타입: {input_type}")

class ResponseFormatter:
    """응답 포맷터"""
    
    @staticmethod
    def format_response(response: str, response_type: str = "text") -> Dict[str, Any]:
        """응답을 포맷팅"""
        return {
            "type": response_type,
            "content": response,
            "timestamp": None  # 향후 타임스탬프 추가
        }
    
    @staticmethod
    def format_error(error_message: str) -> Dict[str, Any]:
        """에러 응답 포맷팅"""
        return {
            "type": "error",
            "content": f"오류: {error_message}",
            "timestamp": None
        }
