from datetime import date, timedelta
import calendar
import csv
from collections import defaultdict


def nth_weekday(year, month, weekday, n):
    """Return the date of the nth occurrence of a given weekday in a month."""
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
    """Adjusts holiday observance if it falls on a weekend."""
    if d.weekday() == 5:  # Saturday
        return d - timedelta(days=1)
    elif d.weekday() == 6:  # Sunday
        return d + timedelta(days=1)
    return d


def nebraska_holidays(year):
    """Returns Nebraska state holidays (with observed dates)."""
    holidays = {
        "New Year's Day": date(year, 1, 1),
        "Martin Luther King Jr. Day": nth_weekday(year, 1, 0, 3),
        "President's Day": nth_weekday(year, 2, 0, 3),
        "Arbor Day": nth_weekday(year, 4, 4, -1),
        "Memorial Day": nth_weekday(year, 5, 0, -1),
        "Juneteenth": date(year, 6, 19),
        "Independence Day": date(year, 7, 4),
        "Labor Day": nth_weekday(year, 9, 0, 1),
        "Columbus Day": nth_weekday(year, 10, 0, 2),
        "Veterans Day": date(year, 11, 11),
        "Thanksgiving Day": nth_weekday(year, 11, 3, 4),
        "Day after Thanksgiving": nth_weekday(year, 11, 4, 4),
        "Christmas Day": date(year, 12, 25),
    }

    observed_holidays = defaultdict(list)
    for name, day in holidays.items():
        observed_day = observed(day)
        observed_holidays[observed_day].append(name)
    return observed_holidays


def weekends(year):
    """Returns all Saturdays and Sundays for the given year."""
    weekends = defaultdict(list)
    d = date(year, 1, 1)
    while d.year == year:
        if d.weekday() == 5:
            weekends[d].append("Saturday")
        elif d.weekday() == 6:
            weekends[d].append("Sunday")
        d += timedelta(days=1)
    return weekends


def generate_csv(year, filename):
    """Generates a CSV with all holidays and weekends for a given year."""
    holidays = nebraska_holidays(year)
    wknds = weekends(year)

    # Combine into one dictionary
    combined = defaultdict(list)
    for day, names in holidays.items():
        for name in names:
            combined[day].append((name, "holiday"))
    for day, names in wknds.items():
        for name in names:
            combined[day].append((name, "weekend"))

    # Write CSV
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["holiday_date", "holiday_name", "type"])
        for day in sorted(combined):
            for name, kind in combined[day]:
                writer.writerow([day.strftime("%Y-%m-%d"), name, kind])


def generate_for_years(start_year, end_year):
    """Generate CSV files for multiple years in the given range."""
    for year in range(start_year, end_year + 1):
        filename = f"nebraska_days_{year}.csv"
        generate_csv(year, filename)
        print(f"CSV file generated: {filename}")


if __name__ == "__main__":
    # Example: Generate CSVs for 2025 through 2030
    generate_for_years(2025, 2030)
