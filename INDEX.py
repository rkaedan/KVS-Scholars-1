# ================== IMPORTS (MUST BE AT TOP) ==================
import streamlit as st
import requests
import json
import time

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="KVS Scholars Portal",
    page_icon="✨",
    layout="wide"
)

# ================== API CONFIG ==================
API_KEY = "AIzaSyBMJ9pCw3CqMjlFtP_tVCj1jJNanTfnvdI"
MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# ================== POPUP STATE ==================
if "show_popup" not in st.session_state:
    st.session_state.show_popup = True

# ================== CUSTOM STYLES ==================
st.markdown("""
<style>
.main { background-color: #050505; color: white; }
.stButton>button {
    width: 100%;
    border-radius: 12px;
    font-weight: bold;
    text-transform: uppercase;
}
h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 900 !important;
}
.yellow-text { color: #EAB308; }

/* Popup overlay */
.overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.95);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}
.popup-box {
    background: #111;
    padding: 40px;
    border: 2px solid #EAB308;
    border-radius: 24px;
    text-align: center;
    max-width: 600px;
}
</style>
""", unsafe_allow_html=True)

# ================== POPUP ==================
if st.session_state.show_popup:

    st.markdown("""
    <div class="overlay">
        <div class="popup-box">
            <h1 style="color:#EAB308;">🚧</h1>
            <h1>The Site Is Under Construction</h1>
            <p style="color:#888;">
                We are currently polishing the portal to ensure the best study experience.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([4, 2, 4])
    with col:
        if st.button("OK"):
            st.session_state.show_popup = False
            st.rerun()

    st.stop()

# ================== AI FUNCTION ==================
def call_ai(prompt, system_prompt="You are Scholar Aedan, a helpful mentor for students under 18."):
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{system_prompt}\n\nUser Question: {prompt}"}]
        }]
    }

    for delay in [1, 2, 4]:
        try:
            response = requests.post(MODEL_URL, json=payload, timeout=10)
            data = response.json()
            if "error" in data:
                return f"API Error: {data['error']['message']}"
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            time.sleep(delay)

    return "Connection error."

# ================== SIDEBAR ==================
st.sidebar.title("KVS Scholars")
menu = st.sidebar.radio(
    "Navigation",
    ["📚 Textbook Library", "📝 Paper Gen", "🎥 Video Mentor", "💬 Chat with Aedan"]
)

# ================== TEXTBOOK ==================
if menu == "📚 Textbook Library":
    st.markdown("# The <span class='yellow-text'>Textbook Library</span>", unsafe_allow_html=True)

    grade = st.selectbox("Class", [f"Class {i}" for i in range(6, 13)])
    subject = st.selectbox(
        "Subject",
        ["Mathematics", "Science", "English", "Social Science", "Hindi",
         "Physics", "Chemistry", "Biology"]
    )

    if st.button("GET NCERT PDF"):
        query = f"NCERT {grade} {subject} official textbook PDF"
        st.markdown(
            f"[Click here to search on Google](https://www.google.com/search?q={query.replace(' ', '+')})"
        )

# ================== PAPER GENERATOR ==================
elif menu == "📝 Paper Gen":
    st.markdown("# Paper <span class='yellow-text'>Generator</span>", unsafe_allow_html=True)

    p_grade = st.selectbox("Class", [f"Class {i}" for i in range(6, 13)])
    p_sub = st.selectbox("Subject", ["Mathematics", "Science", "English"])

    chapters = st.text_area("Chapters", "Chapter 1, Chapter 2")

    if st.button("GENERATE"):
        with st.spinner("Generating..."):
            st.write(call_ai(f"Create a question paper for {p_grade} {p_sub} from {chapters}"))

# ================== VIDEO MENTOR ==================
elif menu == "🎥 Video Mentor":
    st.markdown("# Video <span class='yellow-text'>Mentor</span>", unsafe_allow_html=True)

    topic = st.text_input("Topic")
    if topic:
        st.markdown(call_ai(f"Suggest good NCERT-aligned YouTube videos for {topic}"))

# ================== CHAT ==================
elif menu == "💬 Chat with Aedan":
    st.markdown("# Ask <span class='yellow-text'>Aedan</span>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        reply = call_ai(prompt)
        st.chat_message("assistant").write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ================== FOOTER ==================
st.sidebar.markdown("---")
st.sidebar.caption("KVS Scholars Portal v2.0")
