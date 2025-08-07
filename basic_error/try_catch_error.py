def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return None

# Example usage
x = 10
y = 0
output = divide_numbers(x, y)
print(f"Result: {output}")