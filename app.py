import streamlit as st

# Questionnaire structure
questionnaire = [
    {"type": "text", "key": "name", "question": "What's your name?"},
    {"type": "radio", "key": "education", "question": "What is your highest level of education?", "options": ["High School", "Bachelor's", "Master's", "PhD"]},
    {"type": "radio", "key": "experience", "question": "Do you have any prior work or internship experience?", "options": ["No", "Yes - Internship", "Yes - Full-time job"]},
    {"type": "radio", "key": "domain", "question": "Which domain are you targeting?", "options": ["Data Science", "Web Development", "Cybersecurity", "AI/ML", "UI/UX Design", "Cloud Computing"]},
    {"type": "multiselect", "key": "skills", "question": "Which of these skills do you already have?", "options": ["Python", "SQL", "Git", "Machine Learning", "HTML/CSS", "Cloud Basics", "Linux", "Figma","Javascript","Deep Learning","C","ReactJS","NodeJS","Wireshark","AWS", "None"]},
    {"type": "radio", "key": "goal", "question": "What's your primary career goal?", "options": ["Get a job", "Freelance", "Build a startup", "Advance in current role", "Switch career"]},
    {"type": "radio", "key": "learning_style", "question": "How do you prefer to learn?", "options": ["Video courses", "Text articles", "Hands-on projects", "Mentorship"]},
]

st.set_page_config(page_title="STS Career Advisor", layout="centered")
st.title("🎯 Career Advisor - STS")

st.markdown("Please answer a few questions so we can suggest the best learning roadmap for you.")

responses = {}
with st.form("user_form"):
    for q in questionnaire:
        if q["type"] == "text":
            responses[q["key"]] = st.text_input(q["question"])
        elif q["type"] == "radio":
            responses[q["key"]] = st.radio(q["question"], q["options"])
        elif q["type"] == "multiselect":
            responses[q["key"]] = st.multiselect(q["question"], q["options"])

    submitted = st.form_submit_button("Submit")

# Display placeholder for result
if submitted:
    st.success(f"Thanks {responses['name']}! Generating your custom roadmap...")
    st.markdown("_(AI is thinking...)_")

import openai
import os

# Set your OpenAI API key (use environment variable or paste here carefully)
#openai.api_key = os.getenv("OPENAI_API_KEY")  # safer
# OR directly paste for testing only



import requests


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
 # paste your key here
MODEL = "openai/gpt-3.5-turbo"  # or try 'meta-llama/llama-3-8b-instruct'

def generate_recommendation(responses):
    prompt = f"""
You are a helpful career advisor bot.

Based on the following user details, generate a markdown-formatted response with clear sections using headings (##), bullet points, and bold where helpful.

User Name: {responses['name']}
Education: {responses['education']}
Experience: {responses['experience']}
Target Domain: {responses['domain']}
Current Skills: {', '.join(responses['skills']) if responses['skills'] else 'None'}
Career Goal: {responses['goal']}
Learning Style: {responses['learning_style']}

Provide:
1. A **brief summary** of the user's profile.
2. A **rating out of 10** for their readiness in their chosen domain.
3. A list of **3–5 essential skills** they are missing (if any).
4. A **detailed roadmap** from beginner to advanced for their chosen domain (with step-by-step format).
5. Personalize all content using the user's name and learning style.

Use markdown formatting for all output.
"""


    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",  # optional but recommended
        "X-Title": "Career Advisor Bot"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

if submitted:
    st.success(f"Thanks {responses['name']}! Generating your custom roadmap...")
    result = generate_recommendation(responses)
    st.markdown(result)
