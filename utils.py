from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

groq_api_key = "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"

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

def generate_response(prompt):
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
