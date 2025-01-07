from dotenv import load_dotenv
from langchain import hub
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA

def get_retriever():
    index_name = 'tax-markdown-table-index'
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    database = PineconeVectorStore.from_existing_index(embedding=embedding, index_name=index_name)
    retriever = database.as_retriever()
    return retriever

def get_llm():
    llm = ChatOpenAI()
    return llm

def get_dictionary_chain():
    dictionary = ["사람을 나타내는 표현 -> 거주자"]

    custom_prompt = ChatPromptTemplate.from_template(f"""
        사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요.
        만약 변경할 필요가 없다고 판단된다면, 사용자의 질문을 변경하지 않아도 됩니다.
        사전: {dictionary}

        질문: {{question}}
    """)

    llm = get_llm()

    dictionary_chain = custom_prompt | llm | StrOutputParser()
    return dictionary_chain

def get_qa_chain():
    llm = get_llm()
    retriever = get_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

def get_ai_message(user_message):
    load_dotenv()
    qa_chain = get_qa_chain()
    dictionary_chain = get_dictionary_chain()
    tax_chain = {"query": dictionary_chain} | qa_chain
    ai_response = tax_chain.invoke({"question": user_message})
    return ai_response