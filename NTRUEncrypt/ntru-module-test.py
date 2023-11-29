import pq_ntru

pq_ntru.generate_keys("key_filename", mode="moderate")

enc = pq_ntru.encrypt("key_filename", "message")
print(enc)