# Example 1: Skip even numbers using continue
for i in range(10):
    if i % 2 == 0:
        continue
    print(f"Odd number: {i}")

# Example 2: Skip words shorter than 5 letters
words = ["apple", "cat", "banana", "dog", "elephant"]
for word in words:
    if len(word) < 5:
        continue
    print(f"Long word: {word}")