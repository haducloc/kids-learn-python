from datetime import datetime
from typing import Optional

# --- Date Parsing ---

def parse_date(value):
    """
    Parses a string into a datetime object.
    Supports ISO format (YYYY-MM-DD) and US format (MM/DD/YYYY).
    Raises ValueError on failure.
    """
    if not value:
        return None

    value = value.strip()
    date_formats = [
        "%Y-%m-%d",  # ISO format
        "%m/%d/%Y"   # US format
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise ValueError("Could not parse the given date. Expected format: YYYY-MM-DD or MM/DD/YYYY")


def date_or_none(s: str) -> Optional[datetime]:
    """
    Returns parsed datetime object or None if invalid or empty.
    """
    try:
        return parse_date(s.strip()) if s else None
    except ValueError:
        return None

# --- Boolean Parsing ---

def parse_bool(value):
    """
    Parses a string into a boolean value.
    Accepts true/false, yes/no, y/n, 1/0, on/off.
    Raises ValueError on failure.
    """
    if not value:
        return None

    value = value.strip().lower()
    if value in ("true", "yes", "y", "1", "on"):
        return True
    if value in ("false", "no", "n", "0", "off"):
        return False

    raise ValueError("Could not convert the string to a boolean. Expected: true|false|yes|no|y|n|1|0|on|off")


def bool_or_none(s: str) -> Optional[bool]:
    """
    Returns parsed boolean or None if invalid or empty.
    """
    try:
        return parse_bool(s.strip()) if s else None
    except ValueError:
        return None

# --- Integer Parsing ---

def parse_int(value):
    """
    Parses a string into an integer.
    Raises ValueError on failure.
    """
    if not value:
        return None
    try:
        return int(value.strip())
    except Exception:
        raise ValueError("Could not convert the string to an integer.")


def int_or_none(s: str) -> Optional[int]:
    """
    Returns parsed integer or None if invalid or empty.
    """
    try:
        return parse_int(s.strip()) if s else None
    except ValueError:
        return None

# --- Float Parsing ---

def parse_float(value):
    """
    Parses a string into a float.
    Raises ValueError on failure.
    """
    if not value:
        return None
    try:
        return float(value.strip())
    except Exception:
        raise ValueError("Could not convert the string to a float.")


def float_or_none(s: str) -> Optional[float]:
    """
    Returns parsed float or None if invalid or empty.
    """
    try:
        return parse_float(s.strip()) if s else None
    except ValueError:
        return None

# --- String Parsing ---

def parse_str(s):
    """
    Returns a stripped string or None if empty or not a string.
    """
    if isinstance(s, str):
        s = s.strip()
        return s if s else None
    return None


def parse_code(s):
    """
    Returns an uppercase, stripped string (used for codes), or None if invalid or empty.
    """
    if isinstance(s, str):
        s = s.strip().upper()
        return s if s else None
    return None
