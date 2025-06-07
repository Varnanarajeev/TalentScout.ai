import streamlit as st
import re

from prompts import (
    generate_tech_questions_prompt,
    generate_follow_up_prompt,
    generate_supportive_reply_prompt,
)
from utils import generate_response

st.set_page_config(page_title="TalentScout AI", layout="centered")
st.title("🧠 TalentScout – AI Hiring Assistant")

END_KEYWORDS = ["quit", "exit", "stop", "end", "bye", "thanks", "thank you"]

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.details = {}

def reset():
    st.session_state.step = 0
    st.session_state.details = {}

def is_valid_tech_stack(input_text):
    text = input_text.strip()
    if not text:
        return False
    
    if not re.match(r'^[\w\s,.-]+$', text):
        return False
    
    known_techs = [
        'python', 'java', 'c++', 'javascript', 'react', 'node', 'django',
        'flask', 'sql', 'html', 'css', 'aws', 'docker', 'kubernetes', 'go',
        'ruby', 'php', 'angular', 'swift', 'typescript', 'scala', 'rust'
    ]
    text_lower = text.lower()
    
    if not any(tech in text_lower for tech in known_techs):
        return False
    
    return True

def main():
    if st.session_state.step == 0:
        st.write("👋 Welcome to **TalentScout** – your AI-powered hiring assistant.\n\nLet's get started with a few quick details to personalize your interview experience.")


        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        exp = st.text_input("Years of Experience")
        position = st.text_input("Desired Position")
        location = st.text_input("Current Location")

        if st.button("Next"):
            if all([name, email, phone, exp, position, location]):
                st.session_state.details.update(
                    dict(name=name, email=email, phone=phone,
                         experience=exp, position=position, location=location)
                )
                st.session_state.step = 1
            else:
                st.warning("Please fill in all fields.")

    elif st.session_state.step == 1:
        st.caption("🛠️ Let's talk about your technical skills! Tip: Type 'quit' or 'exit' anytime to end the interview.")
        tech_stack = st.text_input("Enter your Tech Stack (comma-separated)")

        if st.button("Generate Questions"):
            if is_valid_tech_stack(tech_stack):
                st.session_state.details["tech_stack"] = tech_stack
                prompt = generate_tech_questions_prompt(tech_stack)
                response = generate_response(prompt)

                questions = [line.strip("-• ").strip()
                             for line in response.split("\n")
                             if line.strip().lower().startswith(("-", "•"))]

                st.session_state.qa_flow = questions
                st.session_state.current_q = 0
                st.session_state.chat_history = []
                st.session_state.step = 2
            else:
                st.warning("Please enter a valid tech stack with recognizable technologies.")

    elif st.session_state.step == 2:
        if st.session_state.current_q < len(st.session_state.qa_flow):
            for msg in st.session_state.chat_history:
                st.chat_message(msg["role"]).write(msg["content"])

            current_question = st.session_state.qa_flow[st.session_state.current_q]
            st.chat_message("assistant").write(f"Q{st.session_state.current_q + 1}: {current_question}")

            if user_input := st.chat_input("Your answer"):
                if any(keyword in user_input.lower() for keyword in END_KEYWORDS):
                    st.session_state.step = 3
                    st.rerun()

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"Q{st.session_state.current_q + 1}: {current_question}"})
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input})

                # Generate supportive professional reply using prompt function
                support_prompt = generate_supportive_reply_prompt(user_input)
                supportive_reply = generate_response(support_prompt)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": supportive_reply}
                )

                st.session_state.current_q += 1

                if st.session_state.current_q < len(st.session_state.qa_flow):
                    past_context = "\n".join(
                        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
                    follow_up_prompt = generate_follow_up_prompt(
                        past_context, st.session_state.details["tech_stack"])
                    next_question = generate_response(follow_up_prompt)
                    st.session_state.qa_flow[st.session_state.current_q] = next_question.strip()

                st.rerun()

        else:
            for msg in st.session_state.chat_history:
                st.chat_message(msg["role"]).write(msg["content"])

            st.success("🎉 That’s the end of your technical interview!")

            if st.button("End Chat"):
                st.session_state.step = 3

    elif st.session_state.step == 3:
        st.balloons()
        st.success(f"Thanks {st.session_state.details['name']}! Your info has been recorded.")
        st.info("Our team will get back to you soon. 👋")

        if st.button("Restart"):
            reset()
            st.rerun()

if __name__ == "__main__":
    main()
