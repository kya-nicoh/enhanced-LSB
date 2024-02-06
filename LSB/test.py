import numpy as np

from NTRU.NTRUencrypt import NTRUencrypt
from NTRU.NTRUdecrypt import NTRUdecrypt
from NTRU.NTRUutil import *

# Testing

# Initialise the private and public keys, write them out (and test reading)
NTRUdecrypt = NTRUdecrypt()
NTRUdecrypt.setNpq(N=107,p=3,q=64,df=15,dg=12,d=5)
NTRUdecrypt.genPubPriv()

# Encrypt a test mesage array
NTRUencrypt = NTRUencrypt()
NTRUencrypt.readPub()
NTRUencrypt.setM([1,-1,0,0,0,0,0,1,-1])
NTRUencrypt.encrypt()

# Test the decryption
print("d : ",NTRUdecrypt.decrypt(NTRUencrypt.e))

# Now try encrypting a string
MSG = "hello World"
print("String to Bit: ",str2bit(MSG)) # String to bit
NTRUencrypt.encryptString(MSG)
print("Encrypted Message: ",NTRUencrypt.Me)

# And then decrypt the string and print for a check
NTRUdecrypt.decryptString(NTRUencrypt.Me)
print("Message: ",NTRUdecrypt.M)
