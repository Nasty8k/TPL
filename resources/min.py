arr = [5, 3, 10, 7, 8, 9]
size = 6
start = 0
x = arr[start]

it = start
end = size - 1
while it != end:
	if x > arr[it]:
		x = arr[it]
	it = it + 1

print(x)
