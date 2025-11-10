"""Main module for generating and displaying 2D simplex noise in the terminal."""

from random import randint
import numpy as np
from opensimplex import OpenSimplex
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from generic import get_int, get_float
from presets import preset_colours
from colour import determine_gradient_points, new_colourise_value

console = Console()


def generate_random_seed() -> int:
    """Generate a random seed."""
    return randint(0, 1000000)


def print_summary_bar(user_seed: int, num_rows: int, num_cols: int, scale: float, octaves: int, persistence: float, lacunarity: float):
    """Print a summary bar of the user's configuration."""
    seed = f"SEED: {user_seed}"
    size = f"SIZE: {num_rows} x {num_cols}"
    sca = f"SCL: {scale}"
    otv = f"OCT: {octaves}"
    per = f"PER: {persistence}"
    lac = f"LAC: {lacunarity}"
    joined_text = " | ".join([seed, size, sca, otv, per, lac])
    panel = Panel(Align.center(joined_text), style="bold", width=num_cols * 2) # This wont align if show_value is true, but since that dramatically increases width, this is acceptable
    console.print(panel)


def initialise():
    """Initialise settings by getting user input."""

    # 1: Seed value
    user_seed = get_int("Enter a seed number (leave blank for a random value): ", generate_random_seed())
    ox = OpenSimplex(seed=user_seed)

    # 2: Noise generation settings
    num_rows = get_int("Enter number of rows (default 20): ", 20, upper=1000, lower=1)
    num_cols = get_int("Enter number of columns (default 50): ", 50, upper=1000, lower=1)
    scale = get_float("Enter scale (default 0.1): ", 0.1, upper=10, lower=0)
    octaves = get_int("Enter number of octaves (default 1): ", 1, upper=10, lower=1)
    persistence = get_float("Enter persistence (default 0.5): ", 0.5, upper=1, lower=0)
    lacunarity = get_float("Enter lacunarity (default 2.0): ", 2.0, upper=10, lower=1)

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

    print_summary_bar(user_seed, num_rows, num_cols, scale, octaves, persistence, lacunarity)

    return ox, num_rows, num_cols, scale, octaves, persistence, lacunarity, gradient, show_value


def layered_noise_array(ox: OpenSimplex, width: float, height: float, scale: float, octaves: int, persistence: float, lacunarity: float) -> np.ndarray:
    """Generate layered simplex noise value."""
    total = np.zeros((height, width), dtype=np.float32)
    frequency = 1
    amplitude = 1
    max_value = 0  # Used for normalizing result to -1.0 to 1.0

    x = np.arange(width) * scale
    y = np.arange(height) * scale

    for _ in range(octaves):

        layer = ox.noise2array(x * frequency, y * frequency)
        total += layer * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    return total / max_value


def generate(ox: OpenSimplex, num_rows: int, num_cols: int, scale: float, octaves: int, persistence: float, lacunarity: float, gradient: list, show_value: bool):
    """Generate and display the noise grid."""

    noise_map = layered_noise_array(ox, num_cols, num_rows, scale, octaves, persistence, lacunarity)

    for i in range(num_rows):
        for j in range(num_cols):
            noise_value = noise_map[i][j]
            colour = new_colourise_value(noise_value, gradient)
            if not show_value:
                console.print("██", style=colour, end="")
            else:
                console.print(f"[{noise_value:+.2f}]", style=colour, end=" ")
        console.print()  # New line after each row


if __name__ == "__main__":
    parameters = initialise()
    generate(*parameters)
