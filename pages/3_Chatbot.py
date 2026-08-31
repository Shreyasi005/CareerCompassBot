import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # reads the .env file and loads GEMINI_API_KEY into the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Apply purple/indigo aesthetic styling
st.markdown("""
    <style>
        h1 {
            background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        h2 {
            color: #a78bfa;
        }
        .stButton>button {
            background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
            border: none !important;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #7c3aed, #a78bfa) !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Career Chatbot")
st.write(
    "This is a real AI chatbot powered by Google Gemini — it actually "
    "reasons about your question instead of matching keywords."
)

SYSTEM_INSTRUCTION = (
    "You are a career-advice assistant. IMPORTANT: Only answer questions related to careers, jobs, resumes, interviews, "
    "salary negotiation, job searching, professional development, workplace situations, and career growth. "
    "If a question is NOT career-related (e.g., general knowledge, jokes, cooking, sports, politics, etc.), "
    "you MUST politely decline and say: 'Sorry, I can only help with career-related questions. Please ask me about resumes, "
    "interviews, job searching, salary negotiation, or career advice.' "
    "For career questions, give specific, practical advice. Keep answers concise and easy to read. "
    "Do NOT provide answers to non-career topics under any circumstances."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": "user"/"model", "text": ...}

for msg in st.session_state.chat_history:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["text"])

user_input = st.chat_input("Ask me something about your career")

if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if not GEMINI_API_KEY:
            reply = "No Gemini API key found. Add GEMINI_API_KEY to your .env file and restart the app."
            st.markdown(reply)
        else:
            with st.spinner("Thinking..."):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    contents = [
                        types.Content(role=m["role"], parts=[types.Part(text=m["text"])])
                        for m in st.session_state.chat_history
                    ]
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.7,
                        ),
                    )
                    reply = response.text or "Hmm, I got an empty response — try rephrasing."
                except Exception as e:
                    reply = f"⚠️ Couldn't reach Gemini: {e}"
            st.markdown(reply)

    st.session_state.chat_history.append({"role": "model", "text": reply})