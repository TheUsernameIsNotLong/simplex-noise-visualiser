"""Utility functions for getting user input with default values."""

def get_int(prompt: str, default: int, upper: int=None, lower: int=None) -> int:
    """Get an integer input from the user, with a default value."""
    while True:
        value = input(prompt)
        if value.strip() == "":
            return default
        try:
            if upper is not None and int(value) > upper:
                print(f"Please enter a value less than or equal to {upper}.")
            elif lower is not None and int(value) < lower:
                print(f"Please enter a value greater than or equal to {lower}.")
            else:
                return int(value)
        except ValueError:
            print(f"Invalid input. Using default value of {default}.")
            return default

def get_float(prompt: str, default: float, upper: float=None, lower: float=None) -> float:
    """Get a float input from the user, with a default value."""
    while True:
        value = input(prompt)
        if value.strip() == "":
            return default
        try:
            if upper is not None and float(value) > upper:
                print(f"Please enter a value less than or equal to {upper}.")
            elif lower is not None and float(value) < lower:
                print(f"Please enter a value greater than or equal to {lower}.")
            else:
                return float(value)
        except ValueError:
            print(f"Invalid input. Using default value of {default}.")
            return default
