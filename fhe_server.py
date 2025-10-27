# fhe_server.py
# Run this in a separate terminal BEFORE running Streamlit.
# It compiles circuits once and exposes a local HTTP API.

from flask import Flask, request, jsonify
from concrete import fhe
import traceback

app = Flask(__name__)

print("🔄 Server: compiling circuits (this runs once, may take a few seconds)...")

# ======================================================
# 🔧 Define FHE functions to compile
# ======================================================

@fhe.compiler({"x": "encrypted"})
def square(x):
    return x * x

@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def multiply(x, y):
    return x * y

@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def add(x, y):
    return x + y

@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def compare(x, y):
    return x > y

# ======================================================
# 🧮 Compile circuits once (sample inputs)
# ======================================================
try:
    square_circuit = square.compile([(i,) for i in range(0, 20)])
    multiply_circuit = multiply.compile([(i, j) for i in range(0, 20) for j in range(0, 20)])
    add_circuit = add.compile([(i, j) for i in range(0, 20) for j in range(0, 20)])
    compare_circuit = compare.compile([(i, j) for i in range(0, 20) for j in range(0, 20)])
    print("✅ Server: circuits compiled and ready")
except Exception as e:
    print("❌ Server: failed to compile circuits")
    traceback.print_exc()
    raise SystemExit(1)


# ======================================================
# 🔐 Helper to run FHE circuit securely
# ======================================================
def run_circuit(circuit, inputs):
    try:
        if len(inputs) == 1:
            enc = circuit.encrypt(inputs[0])
            enc_out = circuit.run(enc)
        else:
            encs = circuit.encrypt(*inputs)
            enc_out = circuit.run(*encs)
        result = circuit.decrypt(enc_out)
        return result
    except Exception as e:
        raise RuntimeError(f"Circuit execution failed: {str(e)}")


# ======================================================
# 🌐 API Endpoint — compute operations securely
# ======================================================
@app.route("/compute", methods=["POST"])
def compute():
    """
    JSON body: { "op": "square" | "add" | "multiply" | "compare" | "aggregate", "inputs": [...] }
    """
    try:
        body = request.get_json(force=True)
        op = body.get("op")
        inputs = body.get("inputs", [])

        if op == "square":
            result = run_circuit(square_circuit, inputs)
            return jsonify({"ok": True, "result": int(result)})

        elif op == "multiply":
            result = run_circuit(multiply_circuit, inputs)
            return jsonify({"ok": True, "result": int(result)})

        elif op == "add":
            result = run_circuit(add_circuit, inputs)
            return jsonify({"ok": True, "result": int(result)})

        elif op == "compare":
            result = run_circuit(compare_circuit, inputs)
            return jsonify({"ok": True, "result": bool(result)})

        elif op == "aggregate":
            balances = [int(v) for v in inputs]
            total = sum(balances)
            average = total // len(balances)
            return jsonify({"ok": True, "result": {"total": total, "average": average}})

        else:
            return jsonify({"ok": False, "error": "Unknown operation"}), 400

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


# ======================================================
# 🩺 Health check endpoint
# ======================================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ======================================================
# 🚀 Run Flask server
# ======================================================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8765, debug=False)
