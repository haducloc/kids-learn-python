from datetime import date, timedelta
import calendar

def nth_weekday(year, month, weekday, n):
    """
    Returns the date of the nth occurrence of a given weekday in a given month.
    weekday: Monday=0 ... Sunday=6
    n: positive for nth, negative for nth from end (-1 = last)
    """
    if n > 0:
        first_day = date(year, month, 1)
        first_weekday = first_day.weekday()
        day = 1 + (weekday - first_weekday) % 7 + (n - 1) * 7
        return date(year, month, day)
    else:  # e.g., last Friday
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        last_weekday = last_day.weekday()
        day = last_day.day - (last_weekday - weekday) % 7 + (n + 1) * 7
        return date(year, month, day)

def observed(d):
    """
    Adjusts holiday observance if it falls on a weekend:
      - Saturday -> observed Friday before
      - Sunday   -> observed Monday after
    """
    if d.weekday() == 5:  # Saturday
        return d - timedelta(days=1)
    elif d.weekday() == 6:  # Sunday
        return d + timedelta(days=1)
    return d

def nebraska_holidays(year):
    holidays = {
        "New Year’s Day": date(year, 1, 1),
        "Martin Luther King Jr. Day": nth_weekday(year, 1, 0, 3),  # third Monday
        "President’s Day": nth_weekday(year, 2, 0, 3),             # third Monday
        "Arbor Day": nth_weekday(year, 4, 4, -1),                  # last Friday
        "Memorial Day": nth_weekday(year, 5, 0, -1),               # last Monday
        "Juneteenth": date(year, 6, 19),
        "Independence Day": date(year, 7, 4),
        "Labor Day": nth_weekday(year, 9, 0, 1),                   # first Monday
        "Columbus Day": nth_weekday(year, 10, 0, 2),               # second Monday
        "Veterans Day": date(year, 11, 11),
        "Thanksgiving Day": nth_weekday(year, 11, 3, 4),           # fourth Thursday
        "Day after Thanksgiving": nth_weekday(year, 11, 4, 4),     # fourth Friday
        "Christmas Day": date(year, 12, 25),
    }
    # Apply observed date adjustment
    observed_holidays = {name: observed(day) for name, day in holidays.items()}
    return observed_holidays

def weekends(year):
    """
    Returns all Saturdays and Sundays for the given year.
    """
    weekends = {}
    d = date(year, 1, 1)
    while d.year == year:
        if d.weekday() == 5:  # Saturday
            weekends[f"Saturday"] = weekends.get("Saturday", []) + [d]
        elif d.weekday() == 6:  # Sunday
            weekends[f"Sunday"] = weekends.get("Sunday", []) + [d]
        d += timedelta(days=1)
    return weekends

if __name__ == "__main__":
    year = 2025
    holidays = nebraska_holidays(year)
    wknds = weekends(year)

    print("=== Nebraska Holidays ===")
    for name, day in holidays.items():
        print(f"{name}: {day.strftime('%A, %B %d, %Y')}")

    print("\n=== Weekends ===")
    for name, days in wknds.items():
        for d in days:
            print(f"{name}: {d.strftime('%A, %B %d, %Y')}")
