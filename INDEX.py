# --- Under Construction Pop-up Logic ---
if st.session_state.show_popup:

    st.markdown("""
        <div class="overlay">
            <div class="popup-box">
                <h1 style="color: #EAB308; font-size: 3rem;">🚧</h1>
                <h1 style="color: white;">The Site Is Under Construction</h1>
                <p style="color: #888;">
                    We are currently polishing the portal to ensure you have the best study experience.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Centered OK button (Streamlit-native)
    st.markdown("<br>", unsafe_allow_html=True)
    _, col, _ = st.columns([4, 2, 4])
    with col:
        if st.button("OK", key="popup_ok"):
            st.session_state.show_popup = False
            st.rerun()

    st.stop()

