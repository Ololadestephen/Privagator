import streamlit as st
from theme_loader import load_theme
load_theme()
from fhe_utils import run_fhe_operation
import time

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Privagator - Encrypted Computation", layout="centered")

st.title("🔐 Privagator: Privacy-Preserving Computations")
st.caption("Powered by Zama’s Fully Homomorphic Encryption (FHE)")

# Sidebar for selecting operations
st.sidebar.header("Demo Options")
operation = st.sidebar.selectbox(
    "Select Operation",
    ["Encrypt & Add", "Encrypt & Subtract", "Encrypt & Multiply"]
)

# -----------------------------
# Input Fields
# -----------------------------
a = st.number_input("Enter first number:", min_value=0, max_value=100, value=3)
b = st.number_input("Enter second number:", min_value=0, max_value=100, value=5)

# -----------------------------
# Run Button
# -----------------------------
if st.button("Run Encrypted Computation", type="primary"):
    with st.spinner("Encrypting your inputs 🔐..."):
        time.sleep(1.2)
    with st.spinner("Performing encrypted computation securely ⚙️..."):
        time.sleep(1.8)
        result = run_fhe_operation(a, b, operation)
    with st.spinner("Decrypting result 🔓..."):
        time.sleep(1.2)

    st.success("✅ Secure computation completed successfully!")
    st.metric(label="Decrypted Result", value=result)
    st.info(f"Operation performed: **{operation}**")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("🧠 Built with ❤️ using ZamaFHE & Streamlit")
