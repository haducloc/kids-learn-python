# Python dictionary basic operations

# Create a dictionary (put)
my_dict = {}
my_dict['apple'] = 1
my_dict['banana'] = 2

# Check if a key exists (contains)
if 'apple' in my_dict:
    print("'apple' is in the dictionary")

# Remove a key
removed_value = my_dict.pop('banana', None)
print(f"Removed value: {removed_value}")

# Iterate over keys
for key in my_dict.keys():
    print(f"Key: {key}")

# Iterate over entries (key-value pairs)
for key, value in my_dict.items():
    print(f"{key}: {value}")