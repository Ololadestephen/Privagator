# fhe_server.py
"""
FHE backend server — uses modules/fhe_core.run_circuit.
Run locally (in your venv) with:
    python fhe_server.py
Then run Streamlit UI:
    streamlit run fhe_demo.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

# Import centralized FHE logic (real Concrete if available, otherwise simulated)
from modules.fhe_core import run_circuit, is_concrete_available

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Check availability
available, avail_msg = is_concrete_available()
if available:
    print("✅ Concrete FHE available — server will run real encrypted computations.")
else:
    print("⚠️ Concrete unavailable or failed to compile — server running in simulated mode.")
    print("Details:", avail_msg)


@app.route("/health", methods=["GET"])
def health():
    """Health check for frontends (Streamlit)"""
    return jsonify({
        "ok": True,
        "status": "running",
        "fhe_backend": "concrete" if available else "simulated",
        "message": avail_msg
    }), 200


@app.route("/compute", methods=["POST"])
def compute():
    """
    Expect JSON:
      { "op": "square"|"multiply"|"add"|"compare"|"aggregate", "inputs": [...] }
    Response:
      { "ok": True, "result": ... }  OR  { "ok": False, "error": "...", "trace": "..." }
    """
    try:
        body = request.get_json(force=True)
        op = body.get("op")
        inputs = body.get("inputs", [])

        if not op:
            return jsonify({"ok": False, "error": "Missing 'op' parameter"}), 400

        # run_circuit handles Concrete vs simulation logic
        result = run_circuit(op, inputs)

        return jsonify({"ok": True, "result": result}), 200

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


if __name__ == "__main__":
    print("🚀 Starting FHE server on http://127.0.0.1:8765")
    app.run(host="127.0.0.1", port=8765, debug=False)
