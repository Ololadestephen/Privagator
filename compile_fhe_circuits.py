from concrete import fhe
import os
import json
import base64
import pickle

print("🔄 Compiling FHE circuits...")

os.makedirs("compiled_circuits", exist_ok=True)


# ----------------------
# Define circuits
# ----------------------
def square(x):
    return x * x


def add(x, y):
    return x + y


def compare(x, y):
    return x > y


# ----------------------
# Helper function to save safely
# ----------------------
def compile_and_save(func, name, sample_inputs, encrypted_params):
    path = f"compiled_circuits/{name}.json"
    try:
        compiler = fhe.Compiler(func, parameter_encryption_statuses=encrypted_params)
        circuit = compiler.compile(sample_inputs)

        # ✅ Use __getstate__() to serialize safely
        state = circuit.__getstate__()
        encoded = base64.b64encode(pickle.dumps(state)).decode("utf-8")

        with open(path, "w") as f:
            json.dump({"name": name, "data": encoded}, f, indent=2)

        print(f"✅ Saved {name} successfully at {path}")

    except Exception as e:
        print(f"❌ Failed to save {name}: {e}")


# ----------------------
# Compile all circuits
# ----------------------
compile_and_save(square, "square_circuit", [i for i in range(10)], {"x": "encrypted"})
compile_and_save(add, "add_circuit", [(x, y) for x in range(10) for y in range(10)],
                 {"x": "encrypted", "y": "encrypted"})
compile_and_save(compare, "compare_circuit", [(x, y) for x in range(10) for y in range(10)],
                 {"x": "encrypted", "y": "encrypted"})

print("🎯 Compilation finished successfully!")
