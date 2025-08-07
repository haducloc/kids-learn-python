import pandas as pd

# Create a sample DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [30, 25, 35],
    "city": ["New York", "Los Angeles", "Chicago"]
})

# Write to CSV with UTF-8 BOM
df.to_csv("people.csv", index=False, encoding="utf-8-sig")

print("CSV written successfully with UTF-8 BOM.")
