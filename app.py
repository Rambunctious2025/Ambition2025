import streamlit as st
import PyPDF2
import google.generativeai as genai

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        except:
            continue
    return text

def ask_gemini(user_question, context_text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([context_text, user_question])
    return response.text

st.title("Gemini AI PDF Book Chatbot")

api_key = st.text_input("Enter your Gemini API key:", type="password")
pdf_file = st.file_uploader("Upload your PDF book", type=["pdf"])

if api_key and pdf_file:
    if "book_text" not in st.session_state:
        st.session_state.book_text = extract_text_from_pdf(pdf_file)
    user_input = st.text_input("Describe your symptom or ask your question:")
    if user_input:
        context_text = st.session_state.book_text[:2000] # limit for Gemini
        answer = ask_gemini(user_input, context_text, api_key)
        st.write(answer)
