import tkinter as tk
from functools import reduce

# Use case 1: Sorting a list of tuples by the second element
pairs = [(1, 3), (2, 2), (4, 1)]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print(sorted_pairs)  # [(4, 1), (2, 2), (1, 3)]

# Use case 2: Filtering a list for even numbers
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6]

# Use case 3: Mapping values to their squares
squares = list(map(lambda x: x ** 2, numbers))
print(squares)  # [1, 4, 9, 16, 25, 36]

# Use case 4: Using lambda in GUI callbacks (e.g., Tkinter)
root = tk.Tk()
button = tk.Button(root, text="Click me", command=lambda: print("Button clicked!"))
button.pack()
# root.mainloop()  # Uncomment to run the GUI

# Use case 5: Reducing a list to a single value (sum)
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 21