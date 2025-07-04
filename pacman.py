import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Maze layout (1 is wall, 0 is empty space)
maze_layout = [
    "11111111111111111111111111",
    "10000000000000000000000001",
    "10111011101110111011101101",
    "10101010101010101010101001",
    "10111011101110111011101101",
    "10000000000000000000000001",
    "10111011101110111011101101",
    "10000000000000000000000001",
    "10111011101110111011101101",
    "10000000000000000000000001",
    "11111111111111111111111111",
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Pacman")

# Clock to control frame rate
clock = pygame.time.Clock()

# Pacman class
class Pacman:
    def __init__(self):
        self.x = GRID_SIZE * 1
        self.y = GRID_SIZE * 1
        self.speed = GRID_SIZE
        self.direction = "STOP"

    def move(self):
        # Save the old position to check if the move is valid
        old_x, old_y = self.x, self.y

        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed

        # Check for collision with wall
        if collides_with_wall(self.x, self.y):
            # Revert to old position if there's a collision
            self.x, self.y = old_x, old_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2)

# Pellet class
class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 4)

# Ghost class
class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = GRID_SIZE // 2

    def move(self, target_x, target_y):
        # AI to move the ghost towards Pacman
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        best_direction = None
        min_distance = float('inf')

        # Try each direction and choose the best one
        for direction in directions:
            old_x, old_y = self.x, self.y

            if direction == "UP":
                self.y -= self.speed
            elif direction == "DOWN":
                self.y += self.speed
            elif direction == "LEFT":
                self.x -= self.speed
            elif direction == "RIGHT":
                self.x += self.speed

            # Check if the new position is valid
            if collides_with_wall(self.x, self.y):
                # Revert if the position is invalid
                self.x, self.y = old_x, old_y
                continue

            # Calculate the distance to Pacman
            distance = abs(self.x - target_x) + abs(self.y - target_y)

            # Choose the direction that gets the ghost closest to Pacman
            if distance < min_distance:
                min_distance = distance
                best_direction = direction

            # Revert back to the original position after checking
            self.x, self.y = old_x, old_y

        # Move in the best direction
        if best_direction == "UP":
            self.y -= self.speed
        elif best_direction == "DOWN":
            self.y += self.speed
        elif best_direction == "LEFT":
            self.x -= self.speed
        elif best_direction == "RIGHT":
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, GRID_SIZE, GRID_SIZE))

# Function to draw the maze
def draw_maze(maze_layout):
    for row in range(len(maze_layout)):
        for col in range(len(maze_layout[row])):
            if maze_layout[row][col] == "1":
                pygame.draw.rect(screen, BLUE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Function to check if the position collides with a wall
def collides_with_wall(x, y):
    # Convert the (x, y) position to grid coordinates
    col = x // GRID_SIZE
    row = y // GRID_SIZE

    # Check if the corresponding cell in the maze is a wall
    if maze_layout[row][col] == "1":
        return True
    return False

# Main function
def main():
    pacman = Pacman()
    pellets = [Pellet(x, y) for x in range(0, SCREEN_WIDTH, GRID_SIZE) for y in range(0, SCREEN_HEIGHT, GRID_SIZE)]
    ghost = Ghost(GRID_SIZE * 10, GRID_SIZE * 10)
    score = 0

    # Game loop
    running = True
    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    pacman.direction = "UP"
                elif event.key == K_DOWN:
                    pacman.direction = "DOWN"
                elif event.key == K_LEFT:
                    pacman.direction = "LEFT"
                elif event.key == K_RIGHT:
                    pacman.direction = "RIGHT"

        # Move pacman and ghost
        pacman.move()
        ghost.move(pacman.x, pacman.y)

        # Check for collisions with pellets
        for pellet in pellets[:]:
            if pygame.Rect(pacman.x, pacman.y, GRID_SIZE, GRID_SIZE).colliderect(pygame.Rect(pellet.x, pellet.y, GRID_SIZE, GRID_SIZE)):
                pellets.remove(pellet)  # Remove pellet
                score += 10  # Increase score

        # Check for collision with ghost (Game Over condition)
        if pygame.Rect(pacman.x, pacman.y, GRID_SIZE, GRID_SIZE).colliderect(pygame.Rect(ghost.x, ghost.y, GRID_SIZE, GRID_SIZE)):
            font = pygame.font.Font(None, 48)
            text = font.render("Game Over", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))  # Display "Game Over" message
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            running = False  # End the game

        # Draw maze, pacman, pellets, and ghost
        draw_maze(maze_layout)
        pacman.draw()
        for pellet in pellets:
            pellet.draw()
        ghost.draw()

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Refresh screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(15)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
