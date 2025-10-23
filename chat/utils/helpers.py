"""
유틸리티 함수들
"""

import datetime
import json
from typing import Any, Dict, List

import streamlit as st


def create_download_button(data: str, filename: str, label: str = "다운로드"):
    """다운로드 버튼 생성"""
    # label이 문자열이 아닌 경우 기본값 사용
    if not isinstance(label, str):
        label = "다운로드"

    return st.download_button(
        label=label, data=data, file_name=filename, mime="application/json"
    )


def create_upload_widget(label: str = "파일 업로드", accept_multiple_files: bool = False):
    """파일 업로드 위젯 생성"""
    # label이 문자열이 아닌 경우 기본값 사용
    if not isinstance(label, str):
        label = "파일 업로드"

    return st.file_uploader(
        label=label, type=["json"], accept_multiple_files=accept_multiple_files
    )


def export_conversation_to_json(conversation_history: List[Dict[str, str]]) -> str:
    """대화 기록을 JSON으로 내보내기"""
    export_data = {
        "export_date": datetime.datetime.now().isoformat(),
        "conversation_count": len(conversation_history),
        "conversation_history": conversation_history,
    }

    return json.dumps(export_data, ensure_ascii=False, indent=2)


def validate_json_import(json_data: str) -> tuple[bool, str, List[Dict[str, str]]]:
    """JSON 가져오기 유효성 검사"""
    try:
        data = json.loads(json_data)

        # 기본 구조 검사
        if not isinstance(data, dict):
            return False, "JSON 데이터가 올바른 형식이 아닙니다.", []

        # 대화 기록 추출
        if "conversation_history" in data:
            conversation = data["conversation_history"]
        elif isinstance(data, list):
            conversation = data
        else:
            return False, "대화 기록을 찾을 수 없습니다.", []

        # 대화 기록 유효성 검사
        if not isinstance(conversation, list):
            return False, "대화 기록이 리스트 형식이 아닙니다.", []

        for i, message in enumerate(conversation):
            if not isinstance(message, dict):
                return False, f"메시지 {i+1}이 올바른 형식이 아닙니다.", []

            if "role" not in message or "content" not in message:
                return False, f"메시지 {i+1}에 role 또는 content가 없습니다.", []

            if message["role"] not in ["user", "assistant", "system"]:
                return False, f"메시지 {i+1}의 role이 올바르지 않습니다.", []

        return True, "유효한 대화 기록입니다.", conversation

    except json.JSONDecodeError as e:
        return False, f"JSON 파싱 오류: {str(e)}", []
    except Exception as e:
        return False, f"오류 발생: {str(e)}", []


def get_conversation_stats(
    conversation_history: List[Dict[str, str]],
) -> Dict[str, Any]:
    """대화 통계 정보 생성"""
    if not conversation_history:
        return {
            "total_messages": 0,
            "user_messages": 0,
            "assistant_messages": 0,
            "system_messages": 0,
            "total_characters": 0,
            "average_message_length": 0,
        }

    user_messages = sum(1 for msg in conversation_history if msg["role"] == "user")
    assistant_messages = sum(
        1 for msg in conversation_history if msg["role"] == "assistant"
    )
    system_messages = sum(1 for msg in conversation_history if msg["role"] == "system")

    total_characters = sum(len(msg["content"]) for msg in conversation_history)
    average_length = (
        total_characters / len(conversation_history) if conversation_history else 0
    )

    return {
        "total_messages": len(conversation_history),
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "system_messages": system_messages,
        "total_characters": total_characters,
        "average_message_length": round(average_length, 2),
    }


def format_timestamp(timestamp: datetime.datetime = None) -> str:
    """타임스탬프 포맷팅"""
    if timestamp is None:
        timestamp = datetime.datetime.now()

    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_filename(filename: str) -> str:
    """파일명 정리"""
    import re

    # 특수문자 제거 및 공백을 언더스코어로 변경
    sanitized = re.sub(r"[^\w\-_\.]", "_", filename)
    # 연속된 언더스코어 제거
    sanitized = re.sub(r"_+", "_", sanitized)
    return sanitized.strip("_")
