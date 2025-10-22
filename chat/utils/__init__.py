"""
유틸리티 함수들
"""

import streamlit as st
from typing import Any, Dict, List
import json
import datetime

def display_message(message: Dict[str, Any], container=None):
    """메시지를 표시하는 유틸리티 함수"""
    if container is None:
        container = st
    
    with container.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # 메시지 타입에 따른 추가 처리
        if message.get("type") == "error":
            st.error("오류가 발생했습니다")
        elif message.get("type") == "warning":
            st.warning("경고가 발생했습니다")

def create_button_row(buttons: List[Dict[str, str]], key_prefix: str = "btn"):
    """버튼 행을 생성하는 유틸리티 함수"""
    cols = st.columns(len(buttons))
    
    for i, button in enumerate(buttons):
        with cols[i]:
            if st.button(
                button["label"], 
                key=f"{key_prefix}_{i}",
                help=button.get("help", "")
            ):
                return button["value"]
    
    return None

def format_timestamp(timestamp: datetime.datetime = None) -> str:
    """타임스탬프를 포맷팅"""
    if timestamp is None:
        timestamp = datetime.datetime.now()
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def export_conversation_to_json(messages: List[Dict[str, Any]]) -> str:
    """대화를 JSON으로 내보내기"""
    export_data = {
        "exported_at": format_timestamp(),
        "total_messages": len(messages),
        "messages": messages
    }
    
    return json.dumps(export_data, ensure_ascii=False, indent=2)

def validate_json_import(json_string: str) -> bool:
    """JSON 가져오기 유효성 검사"""
    try:
        data = json.loads(json_string)
        
        # 필수 필드 확인
        if "messages" not in data:
            return False
        
        # 메시지 형식 확인
        for message in data["messages"]:
            if not isinstance(message, dict):
                return False
            if "role" not in message or "content" not in message:
                return False
            if message["role"] not in ["user", "assistant", "system"]:
                return False
        
        return True
        
    except (json.JSONDecodeError, TypeError):
        return False

def get_conversation_stats(messages: List[Dict[str, Any]]) -> Dict[str, int]:
    """대화 통계 계산"""
    stats = {
        "total": len(messages),
        "user": 0,
        "assistant": 0,
        "system": 0
    }
    
    for message in messages:
        role = message.get("role", "unknown")
        if role in stats:
            stats[role] += 1
    
    return stats

def create_download_button(data: str, filename: str, mime_type: str = "application/json"):
    """다운로드 버튼 생성"""
    return st.download_button(
        label="📥 다운로드",
        data=data,
        file_name=filename,
        mime=mime_type
    )

def create_upload_widget(accept_types: List[str] = None, key: str = "upload"):
    """업로드 위젯 생성"""
    if accept_types is None:
        accept_types = [".json"]
    
    return st.file_uploader(
        "파일 업로드",
        type=accept_types,
        key=key,
        help=f"지원되는 파일 형식: {', '.join(accept_types)}"
    )
