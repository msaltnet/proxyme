"""
입력 처리 및 응답 포맷팅 모듈
"""

from typing import List, Dict, Any
import re

class InputProcessor:
    """사용자 입력 처리 클래스"""
    
    def __init__(self):
        pass
    
    def process_input(self, user_input: str) -> str:
        """사용자 입력 전처리"""
        # 기본적인 텍스트 정리
        processed_input = user_input.strip()
        
        # 연속된 공백 제거
        processed_input = re.sub(r'\s+', ' ', processed_input)
        
        return processed_input
    
    def validate_input(self, user_input: str) -> bool:
        """입력 유효성 검사"""
        if not user_input or not user_input.strip():
            return False
        
        # 너무 긴 입력 체크 (예: 10000자 제한)
        if len(user_input) > 10000:
            return False
        
        return True

class ResponseFormatter:
    """응답 포맷팅 클래스"""
    
    def __init__(self):
        pass
    
    def format_response(self, response: str) -> str:
        """응답 포맷팅"""
        # 기본적인 포맷팅
        formatted_response = response.strip()
        
        # 마크다운 스타일 개선
        formatted_response = self._improve_markdown(formatted_response)
        
        return formatted_response
    
    def _improve_markdown(self, text: str) -> str:
        """마크다운 스타일 개선"""
        # 코드 블록 개선
        text = re.sub(r'```(\w+)?\n(.*?)\n```', r'```\1\n\2\n```', text, flags=re.DOTALL)
        
        return text
    
    def truncate_response(self, response: str, max_length: int = 5000) -> str:
        """응답 길이 제한"""
        if len(response) <= max_length:
            return response
        
        truncated = response[:max_length]
        # 문장이 중간에 잘리지 않도록 조정
        last_period = truncated.rfind('.')
        if last_period > max_length * 0.8:  # 80% 이상이면 문장 끝에서 자르기
            truncated = truncated[:last_period + 1]
        
        return truncated + "\n\n... (응답이 길어서 일부만 표시됩니다)"
