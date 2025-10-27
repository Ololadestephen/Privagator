import streamlit as st
import time
import random
from theme_loader import load_theme
load_theme()

st.set_page_config(page_title="Privagator - Encryption Demo", layout="centered")

st.title("🧩 Encryption Visualization Demo")
st.caption("See how your data transforms securely using Fully Homomorphic Encryption (FHE)")

st.markdown("---")

# -----------------------------
# Step 1: User Input
# -----------------------------
st.subheader("Step 1️⃣: Enter your data")

data = st.text_input("Enter a number or text:", "42")

if st.button("Encrypt My Data 🔐", type="primary"):
    st.write("🔄 Initializing encryption process...")
    progress = st.progress(0)

    # Fake encryption animation
    for percent_complete in range(0, 101, 5):
        time.sleep(0.05)
        progress.progress(percent_complete)

    st.success("✅ Data successfully encrypted!")

    # Generate fake ciphertext (looks random)
    ciphertext = "".join(
        random.choice("01ABCDEF") for _ in range(32)
    )
    st.code(ciphertext, language="text")

    st.caption("Above is your encrypted ciphertext. It looks random and reveals nothing about your data!")

    st.markdown("---")
    st.subheader("Step 2️⃣: Perform computation (while encrypted)")
    st.info("The system can compute directly on this ciphertext — without ever decrypting it.")
    with st.spinner("Simulating secure computation..."):
        time.sleep(1.8)
    st.success("💡 Computation done securely inside the encrypted space!")

    st.markdown("---")
    st.subheader("Step 3️⃣: Decrypt and recover original result 🔓")
    with st.spinner("Decrypting..."):
        time.sleep(1.2)
    st.success("Decryption complete!")

    st.metric("Recovered Result", data)
    st.balloons()

st.markdown("---")
st.caption("🔐 Fully Homomorphic Encryption allows computation without exposing your data — true privacy in action.")
