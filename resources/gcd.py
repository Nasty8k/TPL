a = 90
b = 50
while a != 0 and b != 0:
    if a > b:
        a = a % b
    else:
        b = b % a
gcd = a + b

print(gcd)
