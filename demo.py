from concrete import fhe

# Step 1: Define computation (e.g., sum)
@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def add(x, y):
    return x + y

# Step 2: Compile
inputset = [(1, 2), (5, 10), (12, 23)]
compiled = add.compile(inputset)

# Step 3: Encrypt inputs & run computation
x, y = 5, 10
enc_x, enc_y = compiled.encrypt(x, y)
enc_result = compiled.run(enc_x, enc_y)
result = compiled.decrypt(enc_result)

print("Encrypted computation result:", result)
