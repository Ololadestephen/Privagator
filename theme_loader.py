import streamlit as st

def load_theme():
    """Loads the global CSS and branding for Privagator"""
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2910/2910791.png", width=60)
    st.sidebar.markdown("<h2 style='color:#e5e5e5;'>Privagator</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='font-size:13px;color:#999;'>Fully Homomorphic Encryption Playground</p>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")
