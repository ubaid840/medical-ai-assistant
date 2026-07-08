import streamlit as st
from chatbot import ask_medical_ai

st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Medical AI Assistant")

question = st.text_input("Ask your medical question:")

if st.button("Get Answer"):

    if question.strip():

        with st.spinner("Searching medical documents..."):

            result = ask_medical_ai(question)

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")

            for i, doc in enumerate(result["sources"], 1):
                st.write(f"**Source {i}:**")
                st.write(doc.metadata)