def gcd(a, b):
	 templ = 0
	while a != 0 and b != 0:
        if a > b:
            templ = a % b
            a = templ
        else:
            templ = b % a
            b = templ
    return a + b
print ('Input first number')
a = int(input())
print ('Input second number')
b = int(input())

res = gcd(a, b)
print('GCD = ', str(res))
