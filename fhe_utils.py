from concrete import fhe

# -----------------------------
# FHE Functions (Add, Sub, Mul)
# -----------------------------
@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def fhe_add(x, y):
    return x + y

@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def fhe_subtract(x, y):
    return x - y

@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def fhe_multiply(x, y):
    return x * y

# -----------------------------
# Compile the functions
# -----------------------------
inputset = [(a, b) for a in range(0, 16) for b in range(0, 16)]
compiled_add = fhe_add.compile(inputset)
compiled_subtract = fhe_subtract.compile(inputset)
compiled_multiply = fhe_multiply.compile(inputset)

# -----------------------------
# Encryption Routines
# -----------------------------
def run_fhe_operation(a, b, op):
    """
    Run an encrypted computation based on selected operation.
    """
    if op == "Encrypt & Add":
        encrypted = compiled_add.encrypt(a, b)
        result = compiled_add.run(encrypted)
        return compiled_add.decrypt(result)

    elif op == "Encrypt & Subtract":
        encrypted = compiled_subtract.encrypt(a, b)
        result = compiled_subtract.run(encrypted)
        return compiled_subtract.decrypt(result)

    elif op == "Encrypt & Multiply":
        encrypted = compiled_multiply.encrypt(a, b)
        result = compiled_multiply.run(encrypted)
        return compiled_multiply.decrypt(result)

    else:
        return None
