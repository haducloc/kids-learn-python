def divide(a, b):
    if b == 0:
        raise Exception("Division by zero is not allowed.")
    return a / b

# Example usage
result = divide(10, 0)
print(result)