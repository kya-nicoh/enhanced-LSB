from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate RSA key pair
key = RSA.generate(2048)

# Get public and private keys
public_key = key.publickey()
private_key = key

# Message to be encrypted
message = b"-9 -29 -31 -18 -31 6 -29 -6 -6 -21 -26 3 15 18 30 -10 1 -12 -26 29 25 32 3 32 -9 1 -26 -2 -24 22 9 12 14 -22 -5 19 24 -26 29 9 -18 -21 16 3 30 1 -27 5 21 16 18 -27 25 27 -7 24 24 -26 16 -26 27 13 26 -13 -21 -29 -20 9 -27 -17 21 -25 -1 -14 27 28 -6 -25 -8 3 -12 -23 14 24 7 -12 -27 22 6 16 -9 12 -29 -12 15 -21 -22 -6 21 12 -17 19 -14 10 -8 -30 15"

# Encrypt message with public key
cipher_rsa = PKCS1_OAEP.new(public_key)
cipher_text = cipher_rsa.encrypt(message)

# Decrypt message with private key
cipher_rsa = PKCS1_OAEP.new(private_key)
decrypted_message = cipher_rsa.decrypt(cipher_text)

print("Cipher_text Message:", cipher_text)
print("Decrypted Message:", decrypted_message)
