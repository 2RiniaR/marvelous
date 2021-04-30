def clamp(value, min_value, max_value):
    if min_value > max_value:
        raise ValueError(f"max_value({max_value}) must be larger than min_value({min_value}).")
    return max(min_value, min(max_value, value))
