# python_list.py

# Create a list
fruits = ['apple', 'banana', 'cherry']

# Add elements
fruits.append('date')           # Add to end
fruits.insert(1, 'blueberry')   # Insert at index 1

# Remove elements
fruits.remove('banana')         # Remove by value
removed = fruits.pop(2)         # Remove by index (returns removed item)

# Set (update) element
fruits[0] = 'apricot'           # Change first element

# Iterate over list
for fruit in fruits:
    print(fruit)

# Check if element exists
if 'cherry' in fruits:
    print('cherry is in the list')
else:
    print('cherry is not in the list')