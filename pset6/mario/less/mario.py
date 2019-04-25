from cs50 import get_int

# getting a number

while True:
    print("Give a positive integer not greater then 8")
    n = get_int()
    if n > 0 and n < 9:
        break

# printing bloxx
for i in range(n):
    for j in range(n - i - 1):
        print(" ", end="")

    for k in range(i + 1):
        print("#", end="")

    print()