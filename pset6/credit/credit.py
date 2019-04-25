from cs50 import get_int

card_num = get_int("Number: ")
card_digits = str(card_num)
total_digits = len(card_digits)

sum = 0
start_num = card_num // (10**(total_digits - 2))

# calculating hash sum

is_other = False
while card_num > 0:
    if not is_other:
        sum += card_num % 10
        card_num //= 10
        is_other = True
    else:
        digit = card_num % 10 * 2
        if digit > 9:
            sum += digit % 10 + digit // 10
        else:
            sum += digit
        is_other = False
        card_num //= 10
if sum % 10 == 0:
    if total_digits == 15 and (start_num == 34 or start_num == 37):
        print("AMEX")
    elif total_digits == 16 and (start_num > 50 and start_num < 56):
        print("MASTERCARD")
    elif (total_digits == 13 or total_digits == 16) and (start_num > 39 and start_num < 50):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")