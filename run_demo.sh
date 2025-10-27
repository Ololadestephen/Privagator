#!/bin/bash
echo ""
echo "🚀 Starting Privagator FHE Demo..."

# Activate venv if not active
source venv310/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null

# Ensure dependencies are installed
pip install -q streamlit flask requests concrete-python

# Step 1: Launch FHE server
echo "🧠 Launching FHE backend server..."
python fhe_server.py > server.log 2>&1 &
SERVER_PID=$!
sleep 3

# Step 2: Launch Streamlit frontend
echo "🌐 Opening Privagator UI..."
streamlit run Home.py --server.port 8501
# (or streamlit run pages/FHE_Demo.py if you want to open that first)

# Step 3: Kill server on exit
trap "echo '🛑 Stopping server...'; kill $SERVER_PID" EXIT
