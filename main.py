from opensimplex import OpenSimplex
from rich.console import Console
from random import randint

console = Console()

try:
    user_seed = int(input("Enter a seed number (leave blank for a random value): "))
except ValueError:
    print("No valid seed provided, using a random seed.")
    user_seed = None

if user_seed is None:
    user_seed = randint(0, 1000000)
    console.print(f"Generated random seed: {user_seed}")

ox = OpenSimplex(seed=user_seed)

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

try:
    num_cols = int(input("Enter number of columns: "))
except ValueError:
    print("Invalid input for columns. Using default value of 10.")
    num_cols = 50

try:
    num_rows = int(input("Enter number of rows: "))
except ValueError:
    print("Invalid input for rows. Using default value of 10.")
    num_rows = 20

try:
    scale = float(input("Enter scale (default 0.1): "))
except ValueError:
    print("Invalid input for scale. Using default value of 0.1.")
    scale = 0.1

# try:
#     octaves = int(input("Enter number of octaves (default 1): "))
# except ValueError:
#     print("Invalid input for octaves. Using default value of 1.")
#     octaves = 1

# try:
#     persistence = float(input("Enter persistence (default 0.5): "))
# except ValueError:
#     print("Invalid input for persistence. Using default value of 0.5.")
#     persistence = 0.5

# try:
#     lacunarity = float(input("Enter lacunarity (default 2.0): "))
# except ValueError:
#     print("Invalid input for lacunarity. Using default value of 2.0.")
#     lacunarity = 2.0

try:
    show_value = str(input("Show noise values? (y/N): ")).strip().lower() == "y"
    if not show_value:
        show_value = False
except ValueError:
    show_value = False

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
