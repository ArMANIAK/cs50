from sys import argv
from cs50 import get_string

if not len(argv) == 2 or not argv[1].isalpha():
    print("Usage: ./caesar key")
    exit(1)

else:
    code = argv[1].lower()

    message = get_string("plaintext: ")
    ciphertext = ""
    j = 0
    for c in range(len(message)):
        key = ord(code[j % len(code)]) - ord('a')
        if message[c] >= 'a' and message[c] <= 'z':
            ciphertext += chr(ord('a') + (ord(message[c]) - ord('a') + key) % 26)
            j += 1
        elif message[c] >= 'A' and message[c] <= 'Z':
            ciphertext += chr(ord('A') + (ord(message[c]) - ord('A') + key) % 26)
            j += 1
        else:
            ciphertext += message[c]
    print("ciphertext:", ciphertext)