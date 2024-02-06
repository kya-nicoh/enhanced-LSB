import numpy as np
from sympy import nextprime, invert, Matrix

class NTRUEncrypt:
    def __init__(self, N=251, p=3, q=128):
        self.N = N
        self.p = p
        self.q = q
        self.generate_keys()

    def generate_keys(self):
        # Generate random polynomials f, g, and invertible polynomial h
        self.f = self.generate_random_poly()
        self.g = self.generate_random_poly()
        while True:
            self.h = self.generate_random_poly()
            if self.is_invertible(self.h):
                break

        # Calculate public and private keys
        self.f_inv = invert(self.f, self.q)
        self.public_key = self.g * self.h % self.q
        self.private_key = self.f_inv * self.public_key % self.q

    def generate_random_poly(self):
        # Generate a random polynomial of degree N with coefficients in {-1, 0, 1}
        return np.random.choice([-1, 0, 1], size=self.N)

    def is_invertible(self, poly):
        # Check if a polynomial is invertible mod q
        return np.gcd(poly, self.q).all() == 1

    def encrypt(self, plaintext, error_stddev=0.5):
        # Encrypt plaintext using public key
        r = self.generate_random_poly() * error_stddev
        e = self.generate_random_poly() * error_stddev
        c = (plaintext * self.public_key + r + e) % self.q
        return c

    def decrypt(self, ciphertext):
        # Decrypt ciphertext using private key
        m = (ciphertext * self.private_key) % self.q
        m_rounded = np.round(m * self.p / self.q)
        return m_rounded.astype(int)

# Example usage:
if __name__ == "__main__":
    ntru = NTRUEncrypt()
    plaintext = np.array([0, 1, 0, 1, 1, 0, 1, 0, 1, 0])  # Example plaintext
    print("Plaintext:", plaintext)
    ciphertext = ntru.encrypt(plaintext)
    print("Ciphertext:", ciphertext)
    decrypted_text = ntru.decrypt(ciphertext)
    print("Decrypted text:", decrypted_text)
