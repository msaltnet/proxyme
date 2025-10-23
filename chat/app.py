import datetime
import json
import os
from typing import Dict, List

import streamlit as st
from dotenv import load_dotenv

from config import ChatBotConfig
from core import InputProcessor, ResponseFormatter

# 로컬 모듈 임포트
from services import LLMService
from utils import (
    create_download_button,
    create_upload_widget,
    export_conversation_to_json,
    get_conversation_stats,
    validate_json_import,
)

# 환경 변수 로드
load_dotenv()

# 설정 로드
config = ChatBotConfig()

# 페이지 설정
st.set_page_config(
    page_title=config.get("ui.page_title"),
    page_icon=config.get("ui.page_icon"),
    layout=config.get("ui.layout"),
    initial_sidebar_state=config.get("ui.sidebar_state"),
)


class ChatBot:
    def __init__(self):
        # LLM 설정에서 필요한 값들 가져오기
        llm_config = config.get("llm", {})

        # LiteLLM 서비스 초기화
        self.llm_service = LLMService(model=llm_config.get("model", "gpt-3.5-turbo"))

        self.input_processor = InputProcessor()
        self.response_formatter = ResponseFormatter()

        # 시스템 프롬프트 설정
        system_prompt = config.get("system_prompt")
        if system_prompt:
            self.llm_service.set_system_prompt(system_prompt)

    def get_llm_response(self, user_input: str) -> str:
        """LLM을 통해 사용자 입력에 대한 응답 생성"""
        try:
            # LLM 파라미터 가져오기
            llm_params = config.get("llm", {})

            # LLM 서비스를 통해 응답 생성
            response = self.llm_service.get_response(user_input, **llm_params)
            return response

        except Exception as e:
            st.error(f"LLM 응답 생성 중 오류가 발생했습니다: {str(e)}")
            return f"오류가 발생했습니다: {str(e)}"

    def clear_history(self):
        """대화 기록 초기화"""
        self.llm_service.clear_history()

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """대화 기록 반환"""
        return self.llm_service.get_history()

    def export_conversation(self) -> str:
        """대화 기록 내보내기"""
        return self.llm_service.export_conversation()

    def import_conversation(self, conversation_json: str):
        """대화 기록 가져오기"""
        self.llm_service.import_conversation(conversation_json)


def initialize_session_state():
    """세션 상태 초기화"""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatBot()

    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_chat_interface():
    """채팅 인터페이스 렌더링"""
    st.title("🤖 ProxyMe ChatBot")
    st.markdown("---")

    # 채팅 메시지 표시 영역
    chat_container = st.container()

    # 메시지 표시
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(prompt)

        # 봇 응답 생성 및 표시
        with st.chat_message("assistant"):
            with st.spinner("응답을 생성하고 있습니다..."):
                response = st.session_state.chatbot.get_llm_response(prompt)
                st.markdown(response)

        # 봇 응답을 메시지에 추가
        st.session_state.messages.append({"role": "assistant", "content": response})


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.header("⚙️ 설정")

        # API 키 확인
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ OpenAI API 키가 설정되었습니다")
        else:
            st.error("❌ OpenAI API 키가 설정되지 않았습니다")
            st.info("chat/.env 파일에 OPENAI_API_KEY를 설정해주세요")

        st.markdown("---")

        # 대화 기록 관리
        st.subheader("💬 대화 관리")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 초기화", type="secondary"):
                st.session_state.chatbot.clear_history()
                st.session_state.messages = []
                st.rerun()

        with col2:
            if st.button("📊 통계"):
                stats = get_conversation_stats(st.session_state.messages)
                st.json(stats)

        # 대화 내보내기/가져오기
        st.subheader("📁 대화 파일")

        # 내보내기
        if st.session_state.messages:
            export_data = export_conversation_to_json(st.session_state.messages)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            create_download_button(
                export_data,
                f"conversation_{timestamp}.json",
                "application/json",
            )

        # 가져오기
        uploaded_file = create_upload_widget([".json"], "conversation_upload")
        if uploaded_file is not None:
            try:
                content = uploaded_file.read().decode("utf-8")
                if validate_json_import(content):
                    data = json.loads(content)
                    if "messages" in data:
                        st.session_state.messages = data["messages"]
                        st.session_state.chatbot.import_conversation(content)
                        st.success("대화가 성공적으로 가져와졌습니다!")
                        st.rerun()
                    else:
                        st.error("올바른 대화 파일이 아닙니다.")
                else:
                    st.error("잘못된 JSON 형식입니다.")
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                st.error(f"파일 읽기 오류: {str(e)}")

        st.markdown("---")

        # 대화 기록 정보
        st.subheader("📊 대화 정보")
        stats = get_conversation_stats(st.session_state.messages)
        st.write(f"총 메시지: {stats['total_messages']}")
        st.write(f"사용자: {stats['user_messages']}")
        st.write(f"AI: {stats['assistant_messages']}")

        # LLM 설정 정보
        st.subheader("🤖 LLM 설정")
        llm_config = config.get("llm", {})
        st.write(f"모델: {llm_config.get('model', 'N/A')}")
        st.write(f"최대 토큰: {llm_config.get('max_tokens', 'N/A')}")
        st.write(f"온도: {llm_config.get('temperature', 'N/A')}")

        st.markdown("---")

        # 향후 기능 안내
        st.subheader("🚀 향후 기능")
        features = config.get("features", {})

        enabled_features = []
        disabled_features = []

        for feature, enabled in features.items():
            if enabled:
                enabled_features.append(f"✅ {feature}")
            else:
                disabled_features.append(f"⏳ {feature}")

        if enabled_features:
            st.success("\n".join(enabled_features))

        if disabled_features:
            st.info("\n".join(disabled_features))


def main():
    """메인 함수"""
    initialize_session_state()

    # 사이드바 렌더링
    render_sidebar()

    # 메인 채팅 인터페이스 렌더링
    render_chat_interface()


if __name__ == "__main__":
    main()
