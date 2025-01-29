import streamlit as st
from src.schemas.all import DocumentType

def title_render():
    st.title("Your AI assistant")

def sidebar_render():
    st.sidebar.title("Upload a document")
    uploaded_file = st.sidebar.file_uploader("Choose a document", type=DocumentType.__members__)
    if uploaded_file:
        return uploaded_file.name
    

def chat_history_render(chat_history):
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def chat_render():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        
    if prompt := st.chat_input("Say something"):
        chat_history_render(st.session_state.messages)
        with st.chat_message("human"):
            st.write(prompt)
            st.session_state.messages.append({"role": "human", "content": prompt})
        with st.spinner("Thinking..."):
            with st.chat_message("ai"):
                st.write(f"Your message is `{prompt}`!")
                st.session_state.messages.append({"role": "ai", "content": prompt})