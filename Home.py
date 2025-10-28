import streamlit as st

# Must come first
st.set_page_config(page_title="Privagator | FHE Demo", layout="centered")

from theme_loader import load_theme
load_theme()

# Header section

st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=100)
st.title("🔐 Welcome to Privagator")
st.subheader("Your interactive Fully Homomorphic Encryption (FHE) demo lab")

st.markdown("""
**Privagator** is an educational platform that shows how **privacy-preserving computation** works using  
**Fully Homomorphic Encryption (FHE)** — a breakthrough that allows operations on encrypted data **without decrypting it**.
""")

st.markdown("---")


# Features section 

st.header("✨ Explore the Demos")

col1, col2, col3, col4 = st.columns(4)

# Helper to navigate to demo page
def goto_demo(feature_key):
    # Set the query param dynamically
    st.query_params["feature"] = feature_key
    try:
        st.switch_page("pages/FHE_Demo.py")
    except Exception:
        st.rerun()

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3649/3649461.png", width=80)
    st.markdown("### 🔢 Secure Multiplication")
    st.caption("Run encrypted arithmetic using FHE — your data stays private.")
    if st.button("Try Secure Multiplication"):
        goto_demo("multiply")

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/1006/1006555.png", width=80)
    st.markdown("### ➕ Encrypted Addition")
    st.caption("Compute sums on encrypted inputs.")
    if st.button("Try Encrypted Addition"):
        goto_demo("add")

with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/3867/3867605.png", width=80)
    st.markdown("### ⚖️ Private Comparison")
    st.caption("Compare two encrypted numbers without revealing them.")
    if st.button("Try Private Comparison"):
        goto_demo("compare")

with col4:
    st.image("https://cdn-icons-png.flaticon.com/512/3416/3416076.png", width=80)
    st.markdown("### 💰 Aggregate Balances")
    st.caption("Compute total & average of balances privately.")
    if st.button("Try Aggregate Balances"):
        goto_demo("aggregate")

st.markdown("---")

# How it works

st.header("🧠 How It Works")

st.markdown("""
1. **Encrypt your data:** Your input is converted into ciphertext — unreadable to anyone.  
2. **Compute securely:** Operations like addition or multiplication happen on encrypted values.  
3. **Decrypt result:** Only you (with the private key) can decrypt and see the real outcome.  
""")

st.info("🔒 With FHE, privacy isn’t an option, it’s built into the math.")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Zama's Concrete FHE library")
st.caption("© 2025 Privagator Project")

