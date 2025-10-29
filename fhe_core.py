# modules/fhe_core.py


import traceback
import math

# Flags / placeholders
USING_CONCRETE = False
_compile_error = None

# Try to import concrete and compile circuits
try:
    from concrete import fhe

    # ---- define FHE functions ----
    @fhe.compiler({"x": "encrypted"})
    def _square(x):
        return x * x

    @fhe.compiler({"x": "encrypted", "y": "encrypted"})
    def _multiply(x, y):
        return x * y

    @fhe.compiler({"x": "encrypted", "y": "encrypted"})
    def _add(x, y):
        return x + y

    @fhe.compiler({"x": "encrypted", "y": "encrypted"})
    def _compare(x, y):
        return x > y

    # Compile circuits once (small sample ranges)
    print("🔄 modules.fhe_core: compiling Concrete circuits (this can take a few seconds)...")
    try:
        square_circuit = _square.compile([(i,) for i in range(0, 20)])
        multiply_circuit = _multiply.compile([(i, j) for i in range(0, 20) for j in range(0, 20)])
        add_circuit = _add.compile([(i, j) for i in range(0, 20) for j in range(0, 20)])
        compare_circuit = _compare.compile([(i, j) for i in range(0, 20) for j in range(0, 20)])
        USING_CONCRETE = True
        print("✅ modules.fhe_core: Concrete circuits compiled successfully.")
    except Exception as ce:
        _compile_error = traceback.format_exc()
        print("⚠️ modules.fhe_core: Concrete import succeeded but compilation failed.")
        print(_compile_error)
        # leave USING_CONCRETE False so simulation will be used

except Exception as e:
    # Concrete not available (import error, missing native libs, etc.)
    _compile_error = traceback.format_exc()
    print("⚠️ modules.fhe_core: Concrete is not available. Falling back to simulated mode.")
    # USING_CONCRETE stays False


# ---------- Helper wrappers ----------
def _run_concrete_circuit(circuit, inputs):
    """
    Generic helper to run compiled concrete circuits.
    `inputs` is a list or tuple of integers.
    """
    # encryption, run, decrypt using the circuit object API
    if len(inputs) == 1:
        enc = circuit.encrypt(int(inputs[0]))
        out = circuit.run(enc)
        return circuit.decrypt(out)
    else:
        encs = circuit.encrypt(*[int(x) for x in inputs])
        out = circuit.run(*encs)
        return circuit.decrypt(out)


def _simulate(op, inputs):
    """Simple deterministic simulation to show the same semantics as the FHE demos."""
    try:
        if op == "square":
            return int(inputs[0]) ** 2
        if op == "multiply":
            return int(inputs[0]) * int(inputs[1])
        if op == "add":
            return int(inputs[0]) + int(inputs[1])
        if op == "compare":
            return bool(int(inputs[0]) > int(inputs[1]))
        if op == "aggregate":
            vals = [int(v) for v in inputs]
            total = sum(vals)
            avg = total // len(vals) if len(vals) > 0 else 0
            return {"total": total, "average": avg}
    except Exception as e:
        raise RuntimeError(f"Simulation error: {e}")


# ---------- Public API ----------
def run_circuit(op, inputs):
    """
    Run operation `op` with `inputs` (list/tuple).
    Returns an int, bool, or dict depending on operation.
    If Concrete is available and compiled, this will use real FHE circuits.
    Otherwise it falls back to simulation.
    """
    if USING_CONCRETE:
        try:
            if op == "square":
                out = _run_concrete_circuit(square_circuit, inputs)
                return int(out)
            if op == "multiply":
                out = _run_concrete_circuit(multiply_circuit, inputs)
                return int(out)
            if op == "add":
                out = _run_concrete_circuit(add_circuit, inputs)
                return int(out)
            if op == "compare":
                out = _run_concrete_circuit(compare_circuit, inputs)
                return bool(out)
            if op == "aggregate":
                # We didn't compile an aggregate circuit — do local arithmetic (aggregate is safe to do locally)
                vals = [int(v) for v in inputs]
                total = sum(vals)
                avg = total // len(vals) if len(vals) > 0 else 0
                return {"total": total, "average": avg}
            raise ValueError("Unknown operation")
        except Exception as e:
            # Concrete runtime failure -> surface info and fallback
            err = traceback.format_exc()
            raise RuntimeError(f"Concrete runtime error: {e}\n{err}")
    else:
        # Concrete not available — simulation
        return _simulate(op, inputs)


def is_concrete_available():
    """Return (bool, message). If False, message explains why (if known)."""
    if USING_CONCRETE:
        return True, "Concrete is available and circuits compiled."
    else:
        msg = "Concrete not available or compilation failed."
        if _compile_error:
            msg += " Details:\n" + _compile_error.splitlines()[-4:][0] if _compile_error else ""
        return False, msg
