from datetime import datetime
from typing import Optional

# --- Date Parsing ---

def parse_date(value):
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
    try:
        return parse_date(s.strip()) if s else None
    except ValueError:
        return None

# --- Boolean Parsing ---

def parse_bool(value):
    if not value:
        return None

    value = value.strip().lower()
    if value in ("true", "yes", "y", "1", "on"):
        return True
    if value in ("false", "no", "n", "0", "off"):
        return False

    raise ValueError("Could not convert the string to a boolean. Expected: true|false|yes|no|y|n|1|0|on|off")

def bool_or_none(s: str) -> Optional[bool]:
    try:
        return parse_bool(s.strip()) if s else None
    except ValueError:
        return None

# --- Integer Parsing ---

def parse_int(value):
    if not value:
        return None
    try:
        return int(value.strip())
    except Exception:
        raise ValueError("Could not convert the string to an integer.")

def int_or_none(s: str) -> Optional[int]:
    try:
        return parse_int(s.strip()) if s else None
    except ValueError:
        return None

# --- Float Parsing ---

def parse_float(value):
    if not value:
        return None
    try:
        return float(value.strip())
    except Exception:
        raise ValueError("Could not convert the string to a float.")

def float_or_none(s: str) -> Optional[float]:
    try:
        return parse_float(s.strip()) if s else None
    except ValueError:
        return None
