# Demonstrating basic set operations in Python

# Create a set
my_set = set()

# Add elements
my_set.add(1)
my_set.add(2)
my_set.add(3)

# Remove an element
my_set.remove(2)  # Raises KeyError if 2 not present

# Check if an element exists
contains_one = 1 in my_set  # True
contains_two = 2 in my_set  # False

# Iterate over the set
for item in my_set:
    print(item)

# Output:
# 1
# 3