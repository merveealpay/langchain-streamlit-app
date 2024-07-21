import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


st.set_page_config(page_title="Merve's Bot", page_icon=":robot_face:")
st.title("Merve's Bot")

def get_response(query, chat_history):
    template = f"""
    You are a helpful assistant that provides responses to user queries.
    Chat history: {chat_history}
    User query: {user_query}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"chat_history": chat_history, "user_question": query})


for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, [msg.content for msg in st.session_state.chat_history]))

    st.session_state.chat_history.append(AIMessage(ai_response))

