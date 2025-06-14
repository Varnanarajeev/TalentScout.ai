import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os


llm = ChatGroq(groq_api_key=st.secrets["groq_api_key"], model_name="Llama3-8b-8192")

def generate_response(prompt):
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
