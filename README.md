
# 🧠 TalentScout – AI Hiring Assistant

TalentScout is an AI-powered hiring assistant designed to streamline the technical interview process. It gathers candidate details, dynamically generates relevant technical questions based on their tech stack, and conducts a conversational Q&A session with follow-up questions and feedback.

---

## 🚀 Project Overview

TalentScout simulates a professional technical interview using LLM-powered conversations. It takes candidate details, validates the provided tech stack, generates technical questions, allows interactive answering, and even provides polite, concise feedback after each response. The conversation can end gracefully if the user chooses to exit mid-interview.

---

## ⚙️ Installation Instructions

To run the project locally, follow these steps:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/talent-scout-ai.git
   cd talent-scout-ai
   ```

2. **Create a virtual environment (optional but recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your environment variables** (Optional: you can hardcode the API key in `utils.py`)  
   - `GROQ_API_KEY=your_groq_key_here`

5. **Run the Streamlit app**  
   ```bash
   streamlit run app.py
   ```

---

## 🧑‍💻 Usage Guide

1. Launch the app using Streamlit.
2. Fill in your basic details.
3. Enter your tech stack (e.g., Python, Django, JavaScript).
4. Answer each question in the conversational interface.
5. To exit the interview at any time, type keywords like `quit`, `exit`, or `stop`.

---

## 🛠️ Technical Details

- **Frontend**: [Streamlit](https://streamlit.io)
- **LLM Integration**: [Langchain](https://www.langchain.com/) + [Groq](https://groq.com/)
- **Model**: `Llama3-8b-8192` via Groq
- **Prompting**: Custom-designed prompts to generate:
  - Technical questions
  - Follow-up questions
  - Professional one-line feedback responses

---

## 🧠 Prompt Design

The system uses modular prompt functions:

- `generate_tech_questions_prompt()`  
  Generates 5 technical questions based on the candidate's provided tech stack.

- `generate_follow_up_prompt()`  
  Dynamically adapts follow-up questions using context from previous Q&A.

- `generate_supportive_reply_prompt()`  
  Generates short, professional one-liner responses to acknowledge answers.

Prompts are designed with **clarity, conciseness**, and **real-world hiring tone** in mind. The assistant avoids repetition, handles vague answers gracefully, and keeps the flow moving forward.

---

## 🧩 Challenges & Solutions

### ✅ Challenge 1: Handling gibberish or vague tech stack input  
**Solution**: Added a validation layer to detect invalid tech stack entries before continuing.

### ✅ Challenge 2: Allowing users to exit mid-conversation  
**Solution**: Integrated keyword detection (`quit`, `exit`, etc.) that ends the session professionally.

### ✅ Challenge 3: Overly verbose AI responses  
**Solution**: Refined the prompt design to ensure short, professional, and non-emotional responses.

---

## 📂 File Structure

```
├── app.py                # Main Streamlit application
├── prompts.py            # All prompt templates
├── utils.py              # Model calling functions
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 📬 Feedback

For suggestions or improvements, feel free to open an issue or submit a pull request. Happy hiring! 🚀
