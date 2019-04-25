from cs50 import get_float

while True:
    print("Change owed: ", end="")
    change = get_float()
    if change > 0:
        break

change = (int)(change * 100)
coins = [25, 10, 5, 1]
rest = 0

while change > 0:
    for i in range(4):
        if not change < coins[i]:
            rest += change // coins[i]
            change %= coins[i]
print(rest)
