from sys import argv
import crypt
from cs50 import get_string


def CharIncrement(char, depth):

    # how to change a letter?

    if (char[depth] >= 'A' and char[depth] < 'Z') or (char[depth] >= 'a' and char[depth] < 'z'):
        char = char[:depth] + chr(ord(char[depth]) + 1) + char[depth + 1:]
    elif char[depth] == 'Z':
        char = char[:depth] + 'a' + char[depth + 1:]
    else:
        char = char[:depth] + 'A' + char[depth + 1:]
        if depth + 1 == len(char):
            char += 'A'
        char = CharIncrement(char, depth + 1)
    return char


if not len(argv) == 2:
    print("Usage: ./crack key")
    exit(1)

else:
    pass_hash = argv[1]
    salt = pass_hash[0] + pass_hash[1]

    pass_code = "A"
    while True:
        if crypt.crypt(pass_code, salt) == pass_hash:
            break
        else:
            pass_code = CharIncrement(pass_code, 0)

    print(pass_code)