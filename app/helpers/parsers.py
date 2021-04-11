from datetime import datetime


def try_parse_int(value, return_none=False):
    try:
        return int(value)
    except:
        return None if return_none else 0

def try_parse_float(value, return_none=False):
    try:
        return float(value)
    except:
        return None if return_none else 0.0

def try_parse_string_to_date(value, format="%Y-%m-%d"):
    try:
        return datetime.strptime(value, format)
    except:
        return None

def try_parse_string_to_time(value, format="%M:%S"):
    try:
        return datetime.strptime(value, format).time()
    except:
        return None