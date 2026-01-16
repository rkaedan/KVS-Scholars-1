import streamlit as st
import requests
import json
import time

# --- Configuration ---
API_KEY = "AIzaSyBMJ9pCw3CqMjlFtP_tVCj1jJNanTfnvdI"
MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="KVS Scholars Portal", page_icon="✨", layout="wide")

# --- Pop-up State Management ---
if "show_popup" not in st.session_state:
    st.session_state.show_popup = True

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: bold; text-transform: uppercase; }
    .stSelectbox, .stTextArea, .stTextInput { background-color: #111 !important; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 900 !important; }
    .yellow-text { color: #EAB308; }
    
    /* Overlay styling for the pop-up */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.95);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .popup-box {
        background-color: #111;
        padding: 50px;
        border: 2px solid #EAB308;
        border-radius: 24px;
        box-shadow: 0 0 30px rgba(234, 179, 8, 0.2);
        max-width: 600px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Under Construction Pop-up Logic ---
if st.session_state.show_popup:
    # We wrap the HTML and the button in a container to ensure the button is clickable
    st.markdown("""
        <div class="overlay">
            <div class="popup-box">
                <h1 style="color: #EAB308; font-size: 3rem; margin-bottom: 10px;">🚧</h1>
                <h1 style="color: white; margin-bottom: 20px;">The Site Is Under Construction</h1>
                <p style="color: #888; margin-bottom: 30px;">We are currently polishing the portal to ensure you have the best study experience. Feel free to explore the preview!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Place the Streamlit button within a centered column layout
    # This button sits "above" the fixed overlay due to Streamlit's rendering order
    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        st.markdown('<div style="position: relative; z-index: 10000;">', unsafe_allow_html=True)
        if st.button("OK"):
            st.session_state.show_popup = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.stop() # Prevents the rest of the app from loading until "OK" is clicked

# --- AI Integration Logic ---
def call_ai(prompt, system_prompt="You are Scholar Aedan, a helpful mentor for students under 18. Provide safe, encouraging, clean, and educational content strictly following NCERT standards."):
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
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            time.sleep(delay)
    return "Connection error. Please check your internet."

# --- Sidebar / Navigation ---
st.sidebar.title("KVS Scholars")
menu = st.sidebar.radio("Navigation", ["📚 Textbook Library", "📝 Paper Gen", "🎥 Video Mentor", "💬 Chat with Aedan"])

# --- App Logic ---

if menu == "📚 Textbook Library":
    st.markdown("# The <span class='yellow-text'>Textbook Library.</span>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        grade = st.selectbox("Grade Level", [f"Class {i}" for i in range(6, 13)])
        subject = st.selectbox("Subject Area", ["Mathematics", "Science", "English", "Social Science", "Hindi", "Physics", "Chemistry", "Biology"])
        if st.button("GET NCERT PDF"):
            query = f"NCERT {grade} {subject} official textbook PDF download"
            st.info(f"Redirecting to search for: {query}")
            st.markdown(f"[Click here to search on Google](https://www.google.com/search?q={query.replace(' ', '+')})")
            
    with col2:
        st.info("Access official NCERT books updated for the current session. Select your grade and subject to find the latest study materials.")

elif menu == "📝 Paper Gen":
    st.markdown("# Paper <span class='yellow-text'>Generator.</span>", unsafe_allow_html=True)
    
    col_set, col_prev = st.columns([1, 2])
    
    with col_set:
        st.subheader("Settings")
        p_grade = st.selectbox("Target Class", [f"Class {i}" for i in range(6, 13)], key="p_grade")
        p_sub = st.selectbox("Subject", ["Mathematics", "Science", "English", "Social Science", "Physics", "Chemistry", "Biology"], key="p_sub")
        chapters = st.text_area("Included Chapters", "Chapter 1, Chapter 2, Chapter 3")
        
        if st.button("GENERATE BLUEPRINT"):
            with st.spinner("Designing..."):
                prompt = f"Generate a detailed NCERT-based exam blueprint for {p_grade} {p_sub}. Chapters: {chapters}. Include marks for MCQs, Short, and Long answers."
                st.session_state.blueprint = call_ai(prompt)

    with col_prev:
        if "blueprint" in st.session_state:
            st.subheader("Draft Blueprint")
            editable_bp = st.text_area("Refine Blueprint", st.session_state.blueprint, height=300)
            
            if st.button("CREATE FINAL PAPER"):
                with st.spinner("Writing Paper..."):
                    paper_prompt = f"Create a full sample practice paper for {p_grade} {p_sub} based on this blueprint:\n\n{editable_bp}"
                    st.session_state.final_paper = call_ai(paper_prompt)
        
        if "final_paper" in st.session_state:
            st.success("Paper Generated Successfully!")
            st.text_area("Final Question Paper", st.session_state.final_paper, height=400)
            st.download_button("Download Paper", st.session_state.final_paper, file_name=f"Practice_Paper_{p_sub}.txt")

elif menu == "🎥 Video Mentor":
    st.markdown("# Video <span class='yellow-text'>Mentor.</span>", unsafe_allow_html=True)
    v_topic = st.text_input("Enter a topic to find quality study videos", placeholder="e.g. Photosynthesis")
    
    if v_topic:
        with st.spinner("Searching for top lessons..."):
            v_prompt = f"Suggest 4-6 educational YouTube video topics for: '{v_topic}'. Return strictly as a list of titles and why they are good."
            recommendations = call_ai(v_prompt)
            st.markdown(recommendations)
            st.link_button("Search on YouTube", f"https://www.youtube.com/results?search_query={v_topic}+NCERT")

elif menu == "💬 Chat with Aedan":
    st.markdown("# Ask <span class='yellow-text'>Aedan.</span>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Namaste! I am Scholar Aedan. How can I assist your schoolwork today?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if chat_input := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": chat_input})
        st.chat_message("user").write(chat_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = call_ai(chat_input)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("KVS Scholars Portal v2.0 (Python Edition)")
