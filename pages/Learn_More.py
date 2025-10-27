import streamlit as st

st.set_page_config(page_title="Learn More | Privagator", layout="wide")

from theme_loader import load_theme
load_theme()

# -----------------------------
# Header
# -----------------------------
st.title("📘 Learn More About FHE")
st.subheader("Understand how Fully Homomorphic Encryption (FHE) keeps your data private")

st.markdown("""
Fully Homomorphic Encryption (FHE) is a cryptographic breakthrough that allows **computation directly on encrypted data**.  
That means you can send encrypted numbers to a server, and it can perform operations like addition or multiplication **without ever decrypting them**.
""")

st.markdown("---")

# -----------------------------
# Section 1: Core Concepts
# -----------------------------
st.header("🔑 Key FHE Concepts")

with st.expander("1️⃣ Lattices — The Foundation of FHE"):
    st.markdown("""
    FHE relies on **lattice-based cryptography**, which is considered secure even against quantum computers.  
    In simple terms, lattices are grids of points in high-dimensional space.  
    The difficulty of certain lattice problems forms the backbone of FHE’s security.
    """)

with st.expander("2️⃣ Bootstrapping — Refreshing Encrypted Data"):
    st.markdown("""
    Bootstrapping is what allows FHE to perform **unlimited computations**.  
    Each encrypted operation adds noise to the ciphertext.  
    Bootstrapping “cleans” this noise so you can keep computing indefinitely, without losing accuracy.
    """)

with st.expander("3️⃣ Ciphertexts & Keys"):
    st.markdown("""
    - **Public key:** Encrypts your data.  
    - **Private key:** Decrypts results.  
    - **Ciphertext:** The scrambled (encrypted) version of your input.
    """)

st.markdown("---")

# -----------------------------
# Section 2: Code Examples
# -----------------------------
st.header("💻 FHE in Action — with Zama’s Concrete Library")

st.markdown("""
Here’s how FHE operations like **addition** and **multiplication** are implemented using Zama’s `concrete` library:
""")

code = '''
from concrete import fhe

# Compile a secure addition circuit
@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def add(x, y):
    return x + y

# Compile a secure square circuit
@fhe.compiler({"x": "encrypted"})
def square(x):
    return x * x

# Compile the circuits
add_circuit = add.compile([(i, j) for i in range(0, 10) for j in range(0, 10)])
square_circuit = square.compile([(i,) for i in range(0, 10)])

# Encrypt, run, and decrypt
x, y = 5, 7
encrypted_result = add_circuit.encrypt(x, y)
output = add_circuit.run(encrypted_result)
result = add_circuit.decrypt(output)
print(result)  # Result: 12 (computed securely!)
'''
st.code(code, language="python")

st.info("🔒 Notice how the computation happens *entirely on encrypted numbers* — the server never sees the real inputs.")

st.markdown("---")

# -----------------------------
# Section 3: Interactive Sandbox
# -----------------------------
st.header("🧩 Try It Yourself")

st.markdown("Experiment with simple FHE math using Python syntax:")

user_code = st.text_area("Enter Python code using Concrete (safe mode):", 
"""from concrete import fhe

@fhe.compiler({"x": "encrypted"})
def square(x):
    return x * x

square_circuit = square.compile([(i,) for i in range(0, 10)])
print('✅ Circuit compiled successfully!')
""", height=180)

if st.button("💡 Simulate Run"):
    st.success("✅ Code received! (Sandbox execution disabled for safety in demo mode)")
    st.caption("In a real environment, this would compile and run your code securely using Concrete.")

st.markdown("---")

# -----------------------------
# Section 4: Learn More Links
# -----------------------------
st.header("🔗 Explore Further")

st.markdown("""
- 📚 [Zama’s Official Documentation](https://docs.zama.ai/concrete)
- 🧮 [FHE Deep Dive (Zama Blog)](https://www.zama.ai/blog)
- 💬 [Zama Discord Community](https://discord.gg/zama)
- 🧠 [Video: Introduction to Fully Homomorphic Encryption](https://www.youtube.com/watch?v=IJY8D2NR9tE)
""")

st.markdown("---")

st.caption("Built with ❤️ using Streamlit & Zama's Concrete FHE library")
st.caption("© 2025 Privagator Project")
