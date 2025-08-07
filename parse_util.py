from datetime import datetime, date

# ============================================================
# DATE PARSING
# ============================================================

def parse_date(s: str) -> datetime:
    """
    Parses a string into a datetime object.
    Supports ISO format (YYYY-MM-DD) and US format (MM/DD/YYYY).
    Raises ValueError on failure.
    """
    if not s:
        return None

    s = s.strip()
    date_formats = [
        "%Y-%m-%d",  # ISO format
        "%m/%d/%Y"   # US format
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    raise ValueError("Could not parse the given date. Expected format: YYYY-MM-DD or MM/DD/YYYY")


def date_or_none(s: str) -> datetime | None:
    """
    Returns parsed datetime object or None if invalid or empty.
    """
    try:
        return parse_date(s.strip()) if s else None
    except ValueError:
        return None


def try_parse_date(s: str) -> tuple[date | None, bool]:
    """
    Tries to parse a date string and returns (value, success).
    """
    if not s:
        return None, True
    try:
        return parse_date(s), True
    except Exception:
        return None, False

# ============================================================
# BOOLEAN PARSING
# ============================================================

def parse_bool(s: str) -> bool:
    """
    Parses a string into a boolean.
    Accepts true/false, yes/no, y/n, 1/0, on/off.
    Raises ValueError on failure.
    """
    if not s:
        return None

    s = s.strip().lower()
    if s in ("true", "yes", "y", "1", "on"):
        return True
    if s in ("false", "no", "n", "0", "off"):
        return False

    raise ValueError("Could not convert the string to a boolean. Expected: true|false|yes|no|y|n|1|0|on|off")


def bool_or_none(s: str) -> bool | None:
    """
    Returns parsed boolean or None if invalid or empty.
    """
    try:
        return parse_bool(s.strip()) if s else None
    except ValueError:
        return None


def try_parse_bool(s: str) -> tuple[bool | None, bool]:
    """
    Tries to parse a boolean string and returns (value, success).
    """
    if not s:
        return None, True
    try:
        return parse_bool(s), True
    except Exception:
        return None, False

# ============================================================
# INTEGER PARSING
# ============================================================

def parse_int(s: str) -> int:
    """
    Parses a string into an integer.
    Raises ValueError on failure.
    """
    if not s:
        return None
    try:
        return int(s.strip())
    except Exception:
        raise ValueError("Could not convert the string to an integer.")


def int_or_none(s: str) -> int | None:
    """
    Returns parsed integer or None if invalid or empty.
    """
    try:
        return parse_int(s.strip()) if s else None
    except ValueError:
        return None


def try_parse_int(s: str) -> tuple[int | None, bool]:
    """
    Tries to parse an integer string and returns (value, success).
    """
    if not s:
        return None, True
    try:
        return parse_int(s), True
    except Exception:
        return None, False

# ============================================================
# FLOAT PARSING
# ============================================================

def parse_float(s: str) -> float:
    """
    Parses a string into a float.
    Raises ValueError on failure.
    """
    if not s:
        return None
    try:
        return float(s.strip())
    except Exception:
        raise ValueError("Could not convert the string to a float.")


def float_or_none(s: str) -> float | None:
    """
    Returns parsed float or None if invalid or empty.
    """
    try:
        return parse_float(s.strip()) if s else None
    except ValueError:
        return None


def try_parse_float(s: str) -> tuple[float | None, bool]:
    """
    Tries to parse a float string and returns (value, success).
    """
    if not s:
        return None, True
    try:
        return parse_float(s), True
    except Exception:
        return None, False

# ============================================================
# STRING PARSING
# ============================================================

def str_or_none(s: str) -> str | None:
    """
    Returns a stripped string or None if empty or not a string.
    """
    if not s:
        return None
    s = s.strip()
    return s if s else None


def code_or_none(s: str) -> str | None:
    """
    Returns a stripped uppercase string or None if empty or not a string.
    """
    if not s:
        return None
    s = s.strip().upper()
    return s if s else None
