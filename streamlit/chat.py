import streamlit as st

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
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question}) # session state에 사용자 질문 추가

