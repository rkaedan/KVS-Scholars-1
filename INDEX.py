# ================== IMPORTS ==================
import streamlit as st
import requests
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
if "popup_state" not in st.session_state:
    st.session_state.popup_state = "open"  
    # states: open | minimized | closed

# ================== STYLES ==================
st.markdown("""
<style>
.main { background-color: #050505; color: white; }
.yellow-text { color: #EAB308; }

/* Popup overlay */
.overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.85);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Popup box */
.popup-box {
    background: #111;
    padding: 40px;
    border: 2px solid #EAB308;
    border-radius: 24px;
    text-align: center;
    max-width: 600px;
}

/* Popup controls */
.popup-controls {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

/* Minimized bar */
.minimized-bar {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #111;
    border: 2px solid #EAB308;
    padding: 10px 16px;
    border-radius: 16px;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# ================== POPUP OPEN ==================
if st.session_state.popup_state == "open":

    st.markdown("""
    <div class="overlay">
        <div class="popup-box">
            <div class="popup-controls">
                <span style="color:#888;">_</span>
            </div>
            <h1 style="color:#EAB308;">🚧</h1>
            <h2>This Site Is Under Construction</h2>
            <p style="color:#888;">
                We are currently polishing the portal.
                You can continue exploring the site.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        if st.button("➖ Minimize"):
            st.session_state.popup_state = "minimized"
            st.rerun()

    with col3:
        if st.button("❌ Close"):
            st.session_state.popup_state = "closed"
            st.rerun()

# ================== POPUP MINIMIZED ==================
elif st.session_state.popup_state == "minimized":

    st.markdown("""
    <div class="minimized-bar">
        🚧 Site Under Construction
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔼 Restore"):
        st.session_state.popup_state = "open"
        st.rerun()

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
                return data["error"]["message"]
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

# ================== TEXTBOOK LIBRARY ==================
if menu == "📚 Textbook Library":
    st.markdown("# The <span class='yellow-text'>Textbook Library</span>", unsafe_allow_html=True)

    grade = st.selectbox("Class", [f"Class {i}" for i in range(6, 13)])
    subject = st.selectbox(
        "Subject",
        ["Mathematics", "Science", "English", "Social Science", "Hindi",
         "Physics", "Chemistry", "Biology"]
    )

    if st.button("GET NCERT PDF"):
        query = f"NCERT {grade} {subject} PDF"
        st.markdown(
            f"[Search on Google](https://www.google.com/search?q={query.replace(' ', '+')})"
        )

# ================== PAPER GENERATOR ==================
elif menu == "📝 Paper Gen":
    st.markdown("# Paper <span class='yellow-text'>Generator</span>", unsafe_allow_html=True)

    p_grade = st.selectbox("Class", [f"Class {i}" for i in range(6, 13)])
    p_sub = st.selectbox("Subject", ["Mathematics", "Science", "English"])
    chapters = st.text_area("Chapters", "Chapter 1, Chapter 2")

    if st.button("Generate"):
        with st.spinner("Generating..."):
            st.write(call_ai(f"Create a paper for {p_grade} {p_sub} from {chapters}"))

# ================== VIDEO MENTOR ==================
elif menu == "🎥 Video Mentor":
    st.markdown("# Video <span class='yellow-text'>Mentor</span>", unsafe_allow_html=True)

    topic = st.text_input("Topic")
    if topic:
        st.write(call_ai(f"Suggest NCERT-aligned videos for {topic}"))

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
st.sidebar.caption("KVS Scholars Portal v2.1")
