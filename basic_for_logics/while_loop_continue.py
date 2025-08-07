# Example: Using 'continue' in a while loop

count = 0
while count < 10:
    count += 1
    if count % 2 == 0:
        continue  # Skip even numbers
    print("Odd number:", count)