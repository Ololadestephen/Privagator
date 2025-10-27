import requests, time, json, sys
from concrete import fhe

def run_operation(operation, x, y=None):
    try:
        start_total = time.time()

        # Load circuit
        circuit_file = f"circuits/{operation}_circuit.zip"
        circuit = fhe.load(circuit_file)

        # Prepare inputs
        inputs = {"x": int(x)}
        if y is not None:
            inputs["y"] = int(y)

        # Encrypt
        start_enc = time.time()
        enc_inputs = circuit.encrypt(inputs)
        enc_time = time.time() - start_enc

        # Serialize
        payload = {k: v.tolist() if hasattr(v, "tolist") else v for k, v in enc_inputs.items()}

        # Send to FHE server
        start_compute = time.time()
        res = requests.post("http://127.0.0.1:8765/compute", json={"op": operation, "inputs": payload})
        compute_time = time.time() - start_compute

        # Decrypt
        start_dec = time.time()
        decrypted = circuit.decrypt(res.json()["result"])
        dec_time = time.time() - start_dec
        total_time = time.time() - start_total

        # Estimate ciphertext size
        import sys
        payload_size_kb = sys.getsizeof(json.dumps(payload)) / 1024

        metrics = {
            "result": decrypted,
            "encryption_time": round(enc_time, 3),
            "compute_time": round(compute_time, 3),
            "decryption_time": round(dec_time, 3),
            "payload_size_kb": round(payload_size_kb, 2),
            "total_time": round(total_time, 3)
        }
        return metrics

    except Exception as e:
        return {"error": str(e)}
