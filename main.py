import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 20
ITERATIONS = 6  # Adjust this for different levels of detail
ROUGHNESS = 0.5

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLUE = (65, 105, 225)

# Function to initialize the height map
def initialize_height_map(size):
    height_map = [[0] * size for _ in range(size)]
    return height_map

# Function to set the corner values
def set_corners(height_map, size):
    height_map[0][0] = random.uniform(0, 1)
    height_map[0][size - 1] = random.uniform(0, 1)
    height_map[size - 1][0] = random.uniform(0, 1)
    height_map[size - 1][size - 1] = random.uniform(0, 1)

# Function to perform the diamond step
def diamond_step(height_map, x, y, size, variation):
    avg = (
        height_map[x - size][y - size]
        + height_map[x + size][y - size]
        + height_map[x - size][y + size]
        + height_map[x + size][y + size]
    ) / 4.0
    height_map[x][y] = avg + random.uniform(-variation, variation)

# Function to perform the square step
def square_step(height_map, x, y, size, variation):
    avg = (
        height_map[(x - size + len(height_map)) % len(height_map)][y]
        + height_map[(x + size) % len(height_map)][y]
        + height_map[x][(y - size + len(height_map[0])) % len(height_map[0])]
        + height_map[x][(y + size) % len(height_map[0])]
    ) / 4.0
    height_map[x][y] = avg + random.uniform(-variation, variation)

# Function to perform the diamond-square algorithm
def diamond_square(height_map, size, variation):
    half = size // 2
    if half < 1:
        return

    for y in range(half, len(height_map) - 1, size):
        for x in range(half, len(height_map) - 1, size):
            diamond_step(height_map, x, y, half, variation)

    for y in range(0, len(height_map), half):
        for x in range((y + half) % size, len(height_map), size):
            square_step(height_map, x, y, half, variation)

    diamond_square(height_map, size // 2, variation * ROUGHNESS)

# Function to render the terrain
def render_terrain(surface, height_map):
    for y in range(len(height_map)):
        for x in range(len(height_map[0])):
            height = height_map[x][y]
            color = GREEN if height < 0.3 else BLUE if height < 0.6 else WHITE
            pygame.draw.rect(
                surface, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

# Main function
def main():
    # Set up display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Diamond Square Terrain")

    # Initialize height map
    size = 2 ** ITERATIONS + 1
    height_map = initialize_height_map(size)
    set_corners(height_map, size)

    # Perform diamond-square algorithm
    diamond_square(height_map, size - 1, 1)

    # Render terrain
    render_terrain(screen, height_map)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
