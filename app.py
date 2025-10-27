# app.py
import streamlit as st
import requests
import time
import json

SERVER_URL = "http://127.0.0.1:8765/compute"

st.set_page_config(page_title="🔢 Secure FHE Computation Lab", page_icon="🔐", layout="centered")

st.title("🔢 Secure FHE Computation Demo Lab")
st.caption("Powered by Zama’s Concrete FHE — Privacy-Preserving Computation in Action")

# Sidebar navigation
operation = st.sidebar.selectbox(
    "🧮 Choose Operation",
    ["Square", "Addition", "Comparison"]
)

st.sidebar.markdown("### ⚙️ Settings")
st.sidebar.write("Ensure `fhe_server.py` is running in another terminal window before using this app.")

# Main input form
st.divider()

if operation == "Square":
    st.header("🟩 Encrypted Square Computation")
    st.write("Compute x² securely — input stays private.")
    x = st.number_input("Enter x", value=5, step=1)

    if st.button("Run Secure Computation"):
        payload = {"operation": "square", "x": x}
        try:
            start = time.time()
            response = requests.post(SERVER_URL, json=payload)
            end = time.time()
            data = response.json()

            if "error" in data:
                st.error(f"❌ Error: {data['error']}")
            else:
                st.success(f"✅ Result: {data['result']}")
                st.write("### 📊 Metrics")
                st.json({
                    "Computation time (s)": round(end - start, 4),
                    "Server time (s)": round(data.get("server_time", 0), 4),
                    "Payload size (KB)": round(len(json.dumps(payload)) / 1024, 3),
                })
        except Exception as e:
            st.error(f"Server error: {e}")

elif operation == "Addition":
    st.header("➕ Encrypted Addition Computation")
    st.write("Compute x + y securely — both inputs stay private.")
    x = st.number_input("Enter x", value=3, step=1)
    y = st.number_input("Enter y", value=4, step=1)

    if st.button("Run Secure Computation"):
        payload = {"operation": "add", "x": x, "y": y}
        try:
            start = time.time()
            response = requests.post(SERVER_URL, json=payload)
            end = time.time()
            data = response.json()

            if "error" in data:
                st.error(f"❌ Error: {data['error']}")
            else:
                st.success(f"✅ Result: {data['result']}")
                st.write("### 📊 Metrics")
                st.json({
                    "Computation time (s)": round(end - start, 4),
                    "Server time (s)": round(data.get("server_time", 0), 4),
                    "Payload size (KB)": round(len(json.dumps(payload)) / 1024, 3),
                })
        except Exception as e:
            st.error(f"Server error: {e}")

elif operation == "Comparison":
    st.header("⚖️ Encrypted Comparison Computation")
    st.write("Compare two encrypted numbers (x > y) without revealing them.")
    x = st.number_input("Enter x", value=7, step=1)
    y = st.number_input("Enter y", value=4, step=1)

    if st.button("Run Secure Computation"):
        payload = {"operation": "compare", "x": x, "y": y}
        try:
            start = time.time()
            response = requests.post(SERVER_URL, json=payload)
            end = time.time()
            data = response.json()

            if "error" in data:
                st.error(f"❌ Error: {data['error']}")
            else:
                st.success(f"✅ Result: {data['result']}")
                st.write("### 📊 Metrics")
                st.json({
                    "Computation time (s)": round(end - start, 4),
                    "Server time (s)": round(data.get("server_time", 0), 4),
                    "Payload size (KB)": round(len(json.dumps(payload)) / 1024, 3),
                })
        except Exception as e:
            st.error(f"Server error: {e}")
