from cs50 import get_string
from sys import argv


def main():
    if not len(argv) == 2:
        print("Usage: python bleep.py dictionary")
        exit(1)
    else:
        swear_words = set()
        file = open(argv[1], "r")
        for word in file:
            swear_words.add(word[:len(word) - 1].lower())
        file.close()

        phrase = get_string("What message would you like to censor?\n")
        phrase_split = phrase.split()
        for word in phrase_split:
            if word.lower() in swear_words:
                for i in range(len(word)):
                    print("*", end="")
                print(" ", end="")
            else:
                print(f"{word} ", end="")
        print()


if __name__ == "__main__":
    main()
