from datetime import date, time, datetime, timedelta

# Current date
today = date.today()
print("Today's date:", today)

# Specific date
d = date(2024, 6, 1)
print("Specific date:", d)

# Current date and time
now = datetime.now()
print("Current date and time:", now)

# Specific date and time
dt = datetime(2024, 6, 1, 14, 30, 0)
print("Specific date and time:", dt)

# Time only
t = time(14, 30, 0)
print("Specific time:", t)

# Formatting dates
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted datetime:", formatted)

# Parsing string to datetime
parsed = datetime.strptime("2024-06-01 14:30:00", "%Y-%m-%d %H:%M:%S")
print("Parsed datetime:", parsed)

# Date arithmetic
tomorrow = today + timedelta(days=1)
print("Tomorrow's date:", tomorrow)

# Difference between dates
delta = tomorrow - today
print("Difference in days:", delta.days)