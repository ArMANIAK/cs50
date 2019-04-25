from sys import argv
from cs50 import get_string

if not len(argv) == 2:
    print("Usage: ./caesar key")
    exit(1)

else:
    key = int(argv[1])

    message = get_string("plaintext: ")
    cyphertext = ""
    for c in range(len(message)):
        if message[c] >= 'a' and message[c] <= 'z':
            cyphertext += chr(ord('a') + (ord(message[c]) - ord('a') + key) % 26)
        elif message[c] >= 'A' and message[c] <= 'Z':
            cyphertext += chr(ord('A') + (ord(message[c]) - ord('A') + key) % 26)
        else:
            cyphertext += message[c]
    cyphertext.strip()
    print("ciphertext:", cyphertext)
