import csv

with open("people.csv", mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

for row in data:
    print(row)
