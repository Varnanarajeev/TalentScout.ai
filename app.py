import streamlit as st
from prompts import generate_tech_questions_prompt, generate_follow_up_prompt
from utils import generate_response  # calls Groq LLaMA model with prompt


st.set_page_config(page_title="TalentScout AI", layout="centered")
st.title("🧠 TalentScout – AI Hiring Assistant")


# Initialize session state for flow and user details
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.details = {}


def reset():
    st.session_state.step = 0
    st.session_state.details = {}


def main():
    if st.session_state.step == 0:
        # Collect basic candidate info
        st.write("👋 Hi! I’m TalentScout, your virtual hiring assistant.")

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
        # Get tech stack and generate initial questions
        tech_stack = st.text_input("Enter your Tech Stack (comma-separated)")

        if st.button("Generate Questions"):
            if tech_stack:
                st.session_state.details["tech_stack"] = tech_stack
                prompt = generate_tech_questions_prompt(tech_stack)
                response = generate_response(prompt)

                # Extract clean questions: lines starting with bullet or dash
                questions = [line.strip("-• ").strip() for line in response.split("\n")
                             if line.strip().startswith(("-", "•"))]

                # Initialize session vars
                st.session_state.qa_flow = questions
                st.session_state.current_q = 0
                st.session_state.chat_history = []
                st.session_state.step = 2
            else:
                st.warning("Please enter your tech stack.")

    elif st.session_state.step == 2:
        # Interview in progress: ask questions one by one with context-aware follow-ups

        if st.session_state.current_q < len(st.session_state.qa_flow):
            # Show previous conversation
            for msg in st.session_state.chat_history:
                st.chat_message(msg["role"]).write(msg["content"])

            current_question = st.session_state.qa_flow[st.session_state.current_q]
            question_text = f"Q{st.session_state.current_q + 1}: {current_question}"

            # Show current question
            st.chat_message("assistant").write(question_text)

            # Wait for user's answer
            if user_input := st.chat_input("Your answer"):
                # Append current Q&A to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": question_text})
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.current_q += 1

                # If more questions remain, generate context-aware follow-up question dynamically
                if st.session_state.current_q < len(st.session_state.qa_flow):
                    past_context = "\n".join(
                        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
                    )
                    follow_up_prompt = generate_follow_up_prompt(
                        past_context, st.session_state.details["tech_stack"]
                    )
                    next_question = generate_response(follow_up_prompt)
                    st.session_state.qa_flow[st.session_state.current_q] = next_question.strip()

                st.rerun()

        else:
            # Interview finished
            for msg in st.session_state.chat_history:
                st.chat_message(msg["role"]).write(msg["content"])
            st.success("🎉 That’s the end of your technical interview!")

            if st.button("End Chat"):
                st.session_state.step = 3

    elif st.session_state.step == 3:
        # Thank user and offer restart
        st.balloons()
        st.success(f"Thanks {st.session_state.details['name']}! Your info has been recorded.")
        st.info("Our team will get back to you soon. 👋")

        if st.button("Restart"):
            reset()
            st.rerun()


if __name__ == "__main__":
    main()
