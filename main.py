from opensimplex import OpenSimplex
from rich.console import Console
from random import randint

console = Console()

def get_int(prompt: str, default: int) -> int:
    """Get an integer input from the user, with a default value."""
    value = input(prompt)
    if value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        print(f"Invalid input. Using default value of {default}.")
        return default

def get_float(prompt: str, default: float) -> float:
    """Get a float input from the user, with a default value."""
    value = input(prompt)
    if value.strip() == "":
        return default
    try:
        return float(value)
    except ValueError:
        print(f"Invalid input. Using default value of {default}.")
        return default

def colourise_value(value: float) -> str:
    """Convert a noise value to a colored string for terminal output."""
    # Clamp value between -1 and 1
    clamped_value = max(-1, min(1, value))  
    # Map value to 0 - 1 range
    mapped_value = (clamped_value + 1) / 2
    # Interpolate colour from red, through yellow, to green
    if mapped_value < 0.5:
        r, g, b = 255, int(510 * mapped_value), 0
    else:
        r, g, b = int(510 * (1 - mapped_value)), 255, 0
    return f"rgb({r},{g},{b})"

def generate_random_seed() -> int:
    """Generate a random seed."""
    return randint(0, 1000000)

def initialise():

    # 1: Seed value
    user_seed = get_int("Enter a seed number (leave blank for a random value): ", generate_random_seed())
    ox = OpenSimplex(seed=user_seed)

    # 2: Noise generation settings
    num_rows = get_int("Enter number of rows (default 20): ", 20)
    num_cols = get_int("Enter number of columns (default 50): ", 50)
    scale = get_float("Enter scale (default 0.1): ", 0.1)
    # octaves = get_int("Enter number of octaves (default 1): ", 1)
    # persistence = get_float("Enter persistence (default 0.5): ", 0.5)
    # lacunarity = get_float("Enter lacunarity (default 2.0): ", 2.0)

    # 3: Miscellanous display settings
    try:
        show_value = str(input("Show noise values? (y/N): ")).strip().lower() == "y"
        if not show_value:
            show_value = False
    except ValueError:
        show_value = False
    
    return ox, num_rows, num_cols, scale, show_value

def generate(ox: OpenSimplex, num_rows: int, num_cols: int, scale: float, show_value: bool):
    """Generate and display the noise grid."""
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            noise_value = ox.noise2(x=i * scale, y=j * scale)
            colour = colourise_value(noise_value)
            row.append(f"[{noise_value:+.2f}]")
            if not show_value:
                console.print("[]", style=colour, end="")
            else:
                console.print(f"[{noise_value:+.2f}]", style=colour, end=" ")
        console.print()  # New line after each row

if __name__ == "__main__":
    ox, num_rows, num_cols, scale, show_value = initialise()
    generate(ox, num_rows, num_cols, scale, show_value)