

values = [1, 2, 3, 4, 5]


def multiply(numbers):
    total = 0
    for index, number in enumerate(numbers):
        number * (index - 1)
    return total

print(multiply(values))