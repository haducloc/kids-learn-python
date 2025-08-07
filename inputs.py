# =========================
# Reusable CLI Input Utils (No Advanced Type Hints)
# Author: Loc Ha
# =========================

from datetime import datetime
import re
import parse_util


# --- Core function to get and parse a single input value ---
def __input(var_name, type_converter=None, required=True, validator=None):
    failed = False
    while True:
        if failed:
            print(f"ERROR: Invalid {var_name}.")

        # Prompt user and strip whitespace
        value_str = input(f">>> Enter {var_name}: ").strip()

        # Return None for optional empty input
        if not required and value_str == "":
            return None

        # Attempt conversion using the type_converter
        try:
            parsed_val = value_str if type_converter is None else type_converter(value_str)
        except Exception:
            failed = True
            continue

        # If no validator or it passes, return the result
        if validator is None or validator(parsed_val):
            return parsed_val
        else:
            failed = True


# --- Core function to get and parse a comma-separated list ---
def __input_list(var_name, type_converter=None, required=True, validator=None):
    failed = False
    while True:
        if failed:
            print(f"ERROR: Invalid {var_name}.")
            failed = False

        value_str = input(f">>> Enter {var_name}: ").strip()

        # Split on unescaped commas
        items = re.split(r"(?<!\\),", value_str)

        # Return empty list if optional and no input
        if not required and not value_str:
            return []

        result = []
        for item in items:
            item = item.replace(r"\,", ",").strip()  # Unescape any escaped commas

            try:
                # Allow empty item to become None
                if item == "":
                    result.append(None)
                else:
                    parsed_val = item if type_converter is None else type_converter(item)
                    result.append(parsed_val)
            except Exception:
                failed = True
                break

        if failed:
            continue

        # Validate each item if validator provided
        if validator:
            for parsed_val in result:
                if not validator(parsed_val):
                    failed = True
                    break

            if failed:
                continue

        return result


# === SINGLE VALUE INPUTS ===

def input_int(var_name, required=True, validator=None):
    return __input(var_name, int, required, validator)

def input_float(var_name, required=True, validator=None):
    return __input(var_name, float, required, validator)

def input_string(var_name, required=True, validator=None):
    return __input(var_name, None, required, validator)

def input_bool(var_name):
    return __input(var_name, parse_util.parse_bool, True, None)

def input_date(var_name, required=True, validator=None):
    return __input(var_name, parse_util.parse_date, required, validator)


# === LIST VALUE INPUTS ===

def input_ints(var_name, required=True, validator=None):
    return __input_list(var_name, int, required, validator)

def input_floats(var_name, required=True, validator=None):
    return __input_list(var_name, float, required, validator)

def input_strings(var_name, required=True, validator=None):
    return __input_list(var_name, None, required, validator)

def input_bools(var_name, required=True, validator=None):
    return __input_list(var_name, parse_util.parse_bool, required, validator)

def input_dates(var_name, required=True, validator=None):
    return __input_list(var_name, parse_util.parse_date, required, validator)
