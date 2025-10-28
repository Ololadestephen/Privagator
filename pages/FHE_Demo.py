import streamlit as st
import requests
import time

import subprocess
import requests
import time
import streamlit as st
import os

# Set up the page
st.set_page_config(page_title="Privagator | FHE Demo", layout="centered")

# Automatically start fhe_server.py if not running
SERVER_URL = "http://127.0.0.1:8765/compute"

def start_fhe_server():
    """Start fhe_server.py if it's not already running."""
    try:
        requests.get(SERVER_URL, timeout=2)
        st.info("✅ FHE backend already running.")
        return
    except Exception:
        st.warning("Starting local FHE server...")

    # Run the FHE server in the background
    subprocess.Popen(
        ["python", "fhe_server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    st.success("🚀 FHE backend started successfully!")

# Run the check/start logic
start_fhe_server()



# PAGE SETUP

st.set_page_config(page_title="Privagator | FHE Demo", layout="centered")

from theme_loader import load_theme
load_theme()

# ------------------------------
# HEADER & THEME
# ------------------------------
st.markdown("<style>img {margin-bottom: 0.5rem;}</style>", unsafe_allow_html=True)
st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=100)
st.title("🔐 Privagator — FHE Demo (client UI)")
st.markdown("Interact with the encrypted computation engine below 👇")

# ------------------------------
# SERVER CONFIG
# ------------------------------
SERVER_URL = "http://127.0.0.1:8765/compute"

def check_server_health():
    """Check if the FHE backend server is reachable."""
    try:
        res = requests.get(SERVER_URL.replace("/compute", "/health"), timeout=5)
        if res.status_code == 200:
            return True
    except Exception:
        return False
    return False

if not check_server_health():
    st.error("❌ FHE backend not reachable. Please run `python fhe_server.py` first.")
    st.stop()

# ------------------------------
# QUERY PARAMS
# ------------------------------
params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
default_feature = params.get("feature", ["multiply"])[0] if isinstance(params.get("feature"), list) else params.get("feature", "multiply")

# ------------------------------
# DEMO OPTIONS
# ------------------------------
feature_map = {
    "multiply": "Secure Multiplication",
    "square": "Square Function",
    "add": "Encrypted Addition",
    "compare": "Private Comparison",
    "aggregate": "Aggregate Balances"
}

feature_keys = list(feature_map.keys())
feature_names = list(feature_map.values())

demo = st.selectbox(
    "Choose an FHE demo:",
    feature_names,
    index=feature_keys.index(default_feature) if default_feature in feature_keys else 0
)

# ------------------------------
# SERVER COMMUNICATION
# ------------------------------
def call_server(op, inputs):
    try:
        r = requests.post(SERVER_URL, json={"op": op, "inputs": inputs}, timeout=15)
        if r.status_code == 200 and r.json().get("ok"):
            return r.json()["result"]
        else:
            st.error(r.json().get("error", "Server error"))
    except Exception as e:
        st.error(f"Connection failed: {e}")
    return None

# ------------------------------
# DEMO: Secure Multiplication
# ------------------------------
if demo == "Secure Multiplication":
    st.subheader("Multiply two numbers securely 🔢")
    a = st.number_input("Number A", 0, 100, 3)
    b = st.number_input("Number B", 0, 100, 5)
    if st.button("Run FHE Multiplication"):
        with st.spinner("Performing encrypted multiplication..."):
            time.sleep(1)
            result = call_server("multiply", [a, b])
        if result is not None:
            st.success(f"Encrypted computation result: {a} × {b} = {result}")

# ------------------------------
# DEMO: Square Function
# ------------------------------
elif demo == "Square Function":
    st.subheader("Compute a number's square securely 🧮")
    x = st.number_input("Enter a number", 0, 100, 6)
    if st.button("Run FHE Square"):
        with st.spinner("Performing encrypted squaring..."):
            time.sleep(1)
            result = call_server("square", [x])
        if result is not None:
            st.success(f"Encrypted computation result: {x}² = {result}")

# ------------------------------
# DEMO: Encrypted Addition
# ------------------------------
elif demo == "Encrypted Addition":
    st.subheader("Add two encrypted numbers ➕")
    x = st.number_input("Value X", 0, 100, 3)
    y = st.number_input("Value Y", 0, 100, 7)
    if st.button("Run FHE Addition"):
        with st.spinner("Running encrypted addition..."):
            time.sleep(1)
            result = call_server("add", [x, y])
        if result is not None:
            st.success(f"Encrypted result: {x} + {y} = {result}")

# ------------------------------
# DEMO: Private Comparison
# ------------------------------
elif demo == "Private Comparison":
    st.subheader("Compare values privately ⚖️")
    x = st.number_input("Value A", 0, 100, 10)
    y = st.number_input("Value B", 0, 100, 5)
    if st.button("Compare Securely"):
        with st.spinner("Performing secure comparison..."):
            time.sleep(1)
            result = call_server("compare", [x, y])
        if result is not None:
            msg = "✅ A is greater than B" if result else "❌ A is not greater than B"
            st.success(msg)

# ------------------------------
# DEMO: Aggregate Balances
# ------------------------------
elif demo == "Aggregate Balances":
    st.subheader("Aggregate Wallet Balances 💰")
    st.caption("Compute total and average balances securely — without revealing individual amounts.")
    
    n = st.slider("Number of wallets", 2, 10, 4)
    balances = [st.number_input(f"Wallet {i+1}", 0, 1000, 100*(i+1)) for i in range(n)]
    
    if st.button("Run Secure Aggregation"):
        with st.spinner("Encrypting and computing securely..."):
            for progress in range(0, 101, 20):
                st.progress(progress)
                time.sleep(0.4)
            result = call_server("aggregate", balances)
        if result is not None:
            total = result["total"]
            avg = result["average"]
            st.success(f"🔢 Total: {total} | ⚖️ Average: {avg}")
            st.balloons()

    with st.expander("🧩 See how FHE protects your data"):
        st.markdown("""
        **Step 1:** Each wallet balance is encrypted — unreadable even to the server.  
        **Step 2:** The server adds them while they remain encrypted.  
        **Step 3:** Only your private key decrypts the final total.  

        > The math happens *without ever seeing your actual numbers*.
        """)
        st.image("https://cdn-icons-png.flaticon.com/512/11496/11496031.png", width=400)

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Zama's Concrete FHE library")
st.caption("© 2025 Privagator Project")
