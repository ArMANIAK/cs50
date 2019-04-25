from cs50 import get_float

while True:
    print("Change owed: ", end="")
    change = get_float()
    if change > 0:
        print("accepted")
        break

coins = [0.25, 0.1, 0.05, 0.01]
rest = 0

# print(change, coins[1])
while not change < 0:
    print("first loop")
    for i in range(4):
        print("second loop")
        if not change < coins[i]:
            print(f"third loop {change}, {coins[i]}")
            rest += 1
            change -= coins[i]
            print(change, rest, coins[i])
print(rest)
