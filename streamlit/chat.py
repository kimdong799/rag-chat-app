import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA

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

def get_ai_message(user_message):
    load_dotenv()

    index_name = 'tax-markdown-table-index'

    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI()
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    database = PineconeVectorStore.from_existing_index(embedding=embedding, index_name=index_name)

    retriever = database.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
    )

    dictionary = ["사람을 나타내는 표현 -> 거주자"]

    custom_prompt = ChatPromptTemplate.from_template(f"""
        사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요.
        만약 변경할 필요가 없다고 판단된다면, 사용자의 질문을 변경하지 않아도 됩니다.
        사전: {dictionary}

        질문: {{question}}
    """)

    dictionary_chain = custom_prompt | llm | StrOutputParser()

    tax_chain = {"query": dictionary_chain} | qa_chain
    ai_response = tax_chain.invoke({"question": user_message})
    return ai_response


# 사용자 질문 입력
if user_question := st.chat_input("질문을 입력해주세요!"):
    # user 메세지 입력
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question}) # session state에 사용자 질문 추가

    # AI 답변 반환
    with st.spinner("AI가 답변을 생성중입니다..."):
        ai_message = get_ai_message(user_question)
        with st.chat_message("ai"):
            st.write(ai_message["result"])
    st.session_state.message_list.append({"role": "ai", "content": ai_message["result"]}) # session state에 AI 답변 추가
