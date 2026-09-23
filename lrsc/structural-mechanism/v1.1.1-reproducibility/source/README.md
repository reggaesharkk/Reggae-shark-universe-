# Source and reproduction

Run `python3 audit_k1_to_k10.py` with Python 3, NumPy, and a C++17 compiler (`g++` default). The Python program builds the channel vectors, constructs the real Gram objective, calls the recursive exhaustive C++ enumerator for K=1,...,10, checks every expected combination count, and directly recomputes best and runner-up residuals from the original complex arrays. It directly verifies the K=11 witness.

`VERIFICATION_OUTPUT.txt` is the full recorded output. Floating-point values can differ in low-order digits on other platforms. See the PDF for operator definitions and claim scope.
