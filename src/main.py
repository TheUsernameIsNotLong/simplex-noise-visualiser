"""Main module for generating and displaying 2D simplex noise in the terminal."""

from math import floor, ceil
from random import randint
from opensimplex import OpenSimplex
from rich.console import Console
from generic import get_int, get_float
from presets import preset_colours

console = Console()

def generate_random_seed() -> int:
    """Generate a random seed."""
    return randint(0, 1000000)

def determine_gradient_points(num_points: int):
    """Determine key gradient colours for noise mapping."""
    gradient_points = []
    for i in range(num_points):
        r = get_int(f"Enter red value (0-255) of point {i+1}/{num_points}: ", 255)
        g = get_int(f"Enter green value (0-255) of point {i+1}/{num_points}: ", 255)
        b = get_int(f"Enter blue value (0-255) of point {i+1}/{num_points}: ", 255)
        console.print(f"Gradient point {i + 1} set.", style=f"rgb({r},{g},{b})")
        gradient_points.append([r, g, b])
    return gradient_points

def new_colourise_value(value: float, gradient: list) -> str:
    """Convert a noise value to a colored string for terminal output."""
    # Clamp value between -1 and 1
    clamped_value = max(-1, min(1, value))
    # Map value to a range encompassing all gradient points
    mapped_value = (len(gradient)*(clamped_value + 1)) / 2
    # Interpolate colour from custom values
    lower_colour = gradient[floor(mapped_value)-1] #127, 255, 0
    upper_colour = gradient[ceil(mapped_value)-1] #255, 0, 0

    modulo_value = mapped_value % 1
    r = int(lower_colour[0] + (upper_colour[0] - lower_colour[0]) * modulo_value)
    g = int(lower_colour[1] + (upper_colour[1] - lower_colour[1]) * modulo_value)
    b = int(lower_colour[2] + (upper_colour[2] - lower_colour[2]) * modulo_value)
    return f"rgb({r},{g},{b})"

def initialise():
    """Initialise settings by getting user input."""

    # 1: Seed value
    user_seed = get_int("Enter a seed number (leave blank for a random value): ", generate_random_seed())
    ox = OpenSimplex(seed=user_seed)

    # 2: Noise generation settings
    num_rows = get_int("Enter number of rows (default 20): ", 20, upper=1000, lower=1)
    num_cols = get_int("Enter number of columns (default 50): ", 50, upper=1000, lower=1)
    scale = get_float("Enter scale (default 0.1): ", 0.1, upper=10, lower=0)
    # octaves = get_int("Enter number of octaves (default 1): ", 1, upper=10, lower=1)
    # persistence = get_float("Enter persistence (default 0.5): ", 0.5, upper=1, lower=0)
    # lacunarity = get_float("Enter lacunarity (default 2.0): ", 2.0, upper=10, lower=1)
    # 3: Miscellanous display settings
    print("Would you like to use a preset colour gradient or create your own? (default 1)")
    print("1. Preset")
    print("2. Custom")
    choice = get_int("Enter choice (1-2): ", 1)
    if choice == 1:
        print("Available presets:")
        for i, preset_name in enumerate(preset_colours.keys(), start=1):
            console.print(f"{i}. {preset_name}")
        preset_choice = get_int("Select a preset by number (default 1): ", 1)
        preset_names = list(preset_colours.keys())
        selected_preset = preset_names[preset_choice - 1]
        gradient = preset_colours[selected_preset]
    else:
        gradient_points = get_int("Enter number of gradient points (default 2): ", 2)
        gradient = determine_gradient_points(gradient_points)

    try:
        show_value = str(input("Show noise values? (y/N): ")).strip().lower() == "y"
        if not show_value:
            show_value = False
    except ValueError:
        show_value = False

    return ox, num_rows, num_cols, scale, gradient, show_value

def generate(ox: OpenSimplex, num_rows: int, num_cols: int, scale: float, gradient: list, show_value: bool):
    """Generate and display the noise grid."""
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            noise_value = ox.noise2(x=i * scale, y=j * scale)
            colour = new_colourise_value(noise_value, gradient)
            row.append(f"[{noise_value:+.2f}]")
            if not show_value:
                console.print("[]", style=colour, end="")
            else:
                console.print(f"[{noise_value:+.2f}]", style=colour, end=" ")
        console.print()  # New line after each row

if __name__ == "__main__":
    ox, num_rows, num_cols, scale, gradient, show_value = initialise()
    generate(ox, num_rows, num_cols, scale, gradient, show_value)
