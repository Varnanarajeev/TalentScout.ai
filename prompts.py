def generate_tech_questions_prompt(tech_stack):
    return f"""
You are a technical interviewer for a recruitment agency.

Generate 5 clear, concise technical questions for a candidate skilled in the following technologies:

{tech_stack}

Do not include notes, explanations, or answers.
Format each question as a bullet point.
Only return the list of questions.
"""

def generate_follow_up_prompt(past_context, tech_stack):
    return f"""
You are an AI interviewer.

Here is the interview so far:
{past_context}

Based on the previous questions and answers, generate the next technical question
related to the candidate's skills in {tech_stack}.
Avoid repetition. Return only the question.
"""
