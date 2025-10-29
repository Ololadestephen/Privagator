import streamlit as st
import requests
import time
import os

# =========================================
# 🔧 PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Privagator | FHE Demo",
    layout="centered",
    page_icon="🔐"
)

# =========================================
# 🌐 BACKEND CONNECTION
# =========================================
FHE_SERVER_URL = "https://privagator.onrender.com"  # Your Render backend URL
COMPUTE_URL = f"{FHE_SERVER_URL}/compute"
HEALTH_URL = f"{FHE_SERVER_URL}/health"

def check_backend():
    """Check if the FHE backend server is reachable."""
    try:
        res = requests.get(HEALTH_URL, timeout=10)
        return res.status_code == 200
    except Exception:
        return False

# =========================================
# 🧠 APP HEADER
# =========================================
st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=90)
st.title("🔐 Privagator — FHE Demo")
st.markdown("Interact with the encrypted computation engine below 👇")

if check_backend():
    st.success("✅ Connected to FHE backend on Render!")
else:
    st.error("❌ FHE backend not reachable. Please ensure it's running.")
    st.stop()

# =========================================
# ⚙️ SERVER COMMUNICATION
# =========================================
def call_server(op, inputs):
    try:
        r = requests.post(COMPUTE_URL, json={"op": op, "inputs": inputs}, timeout=15)
        if r.status_code == 200 and r.json().get("ok"):
            return r.json()["result"]
        else:
            st.error(r.json().get("error", "Server returned an error"))
    except requests.exceptions.Timeout:
        st.error("⏱️ Connection to backend timed out. Please retry.")
    except Exception as e:
        st.error(f"Connection failed: {e}")
    return None

# =========================================
# 🎛️ DEMO SELECTION
# =========================================
st.markdown("### Choose an FHE demo:")
demo = st.selectbox(
    "",
    [
        "Secure Multiplication",
        "Square Function",
        "Encrypted Addition",
        "Private Comparison",
        "Aggregate Balances"
    ]
)

# =========================================
# 🔢 SECURE MULTIPLICATION
# =========================================
if demo == "Secure Multiplication":
    st.subheader("Multiply two numbers securely 🔢")
    a = st.number_input("Number A", 0, 100, 3)
    b = st.number_input("Number B", 0, 100, 5)
    if st.button("Run FHE Multiplication"):
        with st.spinner("Performing encrypted multiplication..."):
            result = call_server("multiply", [a, b])
        if result is not None:
            st.success(f"Encrypted computation result: {a} × {b} = {result}")

# =========================================
# 🧮 SQUARE FUNCTION
# =========================================
elif demo == "Square Function":
    st.subheader("Compute a number's square securely 🧮")
    x = st.number_input("Enter a number", 0, 100, 6)
    if st.button("Run FHE Square"):
        with st.spinner("Performing encrypted squaring..."):
            result = call_server("square", [x])
        if result is not None:
            st.success(f"Encrypted computation result: {x}² = {result}")

# =========================================
# ➕ ENCRYPTED ADDITION
# =========================================
elif demo == "Encrypted Addition":
    st.subheader("Add two encrypted numbers ➕")
    x = st.number_input("Value X", 0, 100, 3)
    y = st.number_input("Value Y", 0, 100, 7)
    if st.button("Run FHE Addition"):
        with st.spinner("Running encrypted addition..."):
            result = call_server("add", [x, y])
        if result is not None:
            st.success(f"Encrypted result: {x} + {y} = {result}")

# =========================================
# ⚖️ PRIVATE COMPARISON
# =========================================
elif demo == "Private Comparison":
    st.subheader("Compare values privately ⚖️")
    x = st.number_input("Value A", 0, 100, 10)
    y = st.number_input("Value B", 0, 100, 5)
    if st.button("Compare Securely"):
        with st.spinner("Performing secure comparison..."):
            result = call_server("compare", [x, y])
        if result is not None:
            msg = "✅ A is greater than B" if result else "❌ A is not greater than B"
            st.success(msg)

# =========================================
# 💰 AGGREGATE BALANCES
# =========================================
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

# =========================================
# 🧾 FOOTER
# =========================================
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Zama's Concrete FHE library")
st.caption("© 2025 Privagator Project")
