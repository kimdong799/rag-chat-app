import streamlit as st
from llm import get_ai_message

st.set_page_config(page_title="소득세 챗봇", page_icon=":speech_balloon:")

st.title("소득세 챗봇")
st.caption("소득세에 관련된 모든것을 답변해드립니다!")

# session state 초기화
if "message_list" not in st.session_state:
    st.session_state.message_list = []

# 기존 메시지 출력
for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 질문 입력
if user_question := st.chat_input("질문을 입력해주세요!"):
    # user 메세지 입력
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question}) # session state에 사용자 질문 추가

    # AI 답변 반환
    with st.spinner("AI가 답변을 생성중입니다..."):
        ai_response = get_ai_message(user_question)
        with st.chat_message("ai"):
            ai_message = st.write_stream(ai_response)
            st.session_state.message_list.append({"role": "ai", "content": ai_message}) # session state에 AI 답변 추가
