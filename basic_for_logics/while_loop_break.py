# Example: while loop with break for counting

count = 0
while True:
    print("Count:", count)
    count += 1
    if count >= 5:
        print("Reached 5, breaking the loop.")
        break

print("Loop ended.")
