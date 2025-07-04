import openai
import streamlit as st
from PyPDF2 import PdfReader

# Set your OpenAI API key
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
  # Replace with your OpenAI API key

st.set_page_config(page_title="AI Job Recommender", page_icon="🤖", layout="centered")
st.title("🤖 AI Job Recommendation Assistant")
st.markdown("Upload your resume or type your skills & qualification to get job suggestions!")

if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":
                 "You are a helpful job assistant. Extract user's skills and qualifications and recommend 2-3 relevant job roles with reasons."},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

uploaded_resume = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])

if uploaded_resume is not None:
    with st.spinner("📄 Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.success("✅ Resume processed successfully!")
        st.text_area("Extracted Resume Text", resume_text, height=150)
        st.session_state.messages.append({"role": "user", "content": resume_text})
        with st.spinner("🤖 Finding job recommendations..."):
            reply = ask_openai(resume_text)
        st.session_state.messages.append({"role": "assistant", "content": reply})

user_input = st.chat_input("Or type your qualification and skills here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("🤖 Thinking..."):
        reply = ask_openai(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
