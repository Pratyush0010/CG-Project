import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Change Game")

# Colors
COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), 
          (255, 255, 255), (128, 0, 128), (0, 255, 255)]

WHITE = (255, 255, 255)

# Font setup
font = pygame.font.Font(None, 36)

# Function to draw text
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to get a random color
def get_random_color():
    return random.choice(COLORS)

# Function to get a random position for the box
def get_random_position():
    return random.randint(100, WIDTH - 200), random.randint(100, HEIGHT - 200)

# Function to check if the box is touching a corner
def is_touching_corner(x, y):
    return (x <= 0 and y <= 0) or (x + 150 >= WIDTH and y <= 0) or \
           (x <= 0 and y + 150 >= HEIGHT) or (x + 150 >= WIDTH and y + 150 >= HEIGHT)

# Function to wait for Enter key before starting
def wait_for_enter():
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))  # Black background
        draw_text("Press Enter to Start", WIDTH // 2 - 100, HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter key
                waiting = False  # Exit loop when Enter is pressed

# Main loop
def main():
    color = get_random_color()
    x, y = get_random_position()
    score = 0
    last_color_change_time = pygame.time.get_ticks()
    color_change_count = 0  # Count how many times color changes
    game_over = False

    while not game_over:
        screen.fill((0, 0, 0))  # Background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # End game if pressing space when box is touching a corner
                if is_touching_corner(x, y):
                    game_over = True
                else:
                    color = get_random_color()
                    color_change_count += 1
                    score += 1
                    last_color_change_time = pygame.time.get_ticks()
                    
                    # Move box randomly, but place in a corner every 8th change
                    if color_change_count % 8 == 0:
                        corners = [(0, 0), (WIDTH - 150, 0), (0, HEIGHT - 150), (WIDTH - 150, HEIGHT - 150)]
                        x, y = random.choice(corners)
                    else:
                        x, y = get_random_position()

        # Automatically change color every 5 seconds
        if pygame.time.get_ticks() - last_color_change_time > 5000:
            color = get_random_color()
            color_change_count += 1
            last_color_change_time = pygame.time.get_ticks()
            
            # Move box randomly, but place in a corner every 8th change
            if color_change_count % 8 == 0:
                corners = [(0, 0), (WIDTH - 150, 0), (0, HEIGHT - 150), (WIDTH - 150, HEIGHT - 150)]
                x, y = random.choice(corners)
            else:
                x, y = get_random_position()

        # Draw the box with a matching border
        pygame.draw.rect(screen, color, (x, y, 150, 150))
        pygame.draw.rect(screen, color, (x, y, 150, 150), 5)  # Border

        # Display instructions and score
        draw_text("Press Space to change color", 20, 20, WHITE)
        draw_text(f"Score: {score}", WIDTH - 150, 20, WHITE)

        # Update the display
        pygame.display.flip()

    # Show game over screen
    screen.fill((0, 0, 0))
    draw_text("Game Over", WIDTH // 2 - 80, HEIGHT // 2 - 20)
    draw_text(f"Final Score: {score}", WIDTH // 2 - 90, HEIGHT // 2 + 20)
    pygame.display.flip()

    # Wait for player to quit
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    wait_for_enter()
    main()
