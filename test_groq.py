from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Replace with your actual Groq API key
llm = ChatGroq(groq_api_key="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", model_name="llama3-8b-8192")

try:
    response = llm.invoke([HumanMessage(content="Hello, how are you?")])
    print("✅ Response:", response.content)
except Exception as e:
    print("❌ Error:", str(e))
