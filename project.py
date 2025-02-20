import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Ball Game")

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (10, 10, 40)  # Dark blue night sky
GREEN = (34, 139, 34)  # Green color for ground
ORANGE = (255, 165, 0)  # Orange for the ball
GREY = (169, 169, 169)  # Grey for obstacles

# Generate random stars
NUM_STARS = 100
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2)) for _ in range(NUM_STARS)]

# Font setup
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_dda_line(x1, y1, x2, y2, color):
    """Draws a line using the DDA algorithm."""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        screen.set_at((int(x), int(y)), color)
        x += x_increment
        y += y_increment

def draw_ground():
    """Draws the ground using DDA lines."""
    ground_height = HEIGHT // 4  # Adjusted ground height
    for y in range(HEIGHT - ground_height, HEIGHT):
        draw_dda_line(0, y, WIDTH, y, GREEN)

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

def main():
    clock = pygame.time.Clock()
    ball_x, ball_y = 100, HEIGHT - HEIGHT // 4 - 30
    ball_radius = 20
    ball_velocity_y = 0
    gravity = 2  # Increased initial gravity
    jump_strength = -15
    obstacles = []
    obstacle_width = 40
    obstacle_height = 60
    obstacle_speed = 8  # Increased initial speed
    spawn_timer = 0
    score = 0
    game_over = False

    start_ticks = pygame.time.get_ticks()  # Start time tracking

    while not game_over:
        screen.fill(BACKGROUND)  # Clear the screen with the night sky color

        # Update score based on time survived
        score = (pygame.time.get_ticks() - start_ticks) // 1000  

        # Increase obstacle speed and gravity over time
        obstacle_speed = 8 + (score // 5)  
        gravity = 2 + (score // 10)  

        # Draw stars (twinkling effect)
        for star in stars:
            brightness = random.randint(150, 255)  # Make stars flicker
            screen.set_at(star, (brightness, brightness, brightness))
        
        # Draw the moon (filled with white color)
        pygame.draw.circle(screen, WHITE, (WIDTH - 150, 150), 60)
        
        # Draw the ground
        draw_ground()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball_velocity_y = jump_strength
        
        # Update ball movement
        ball_velocity_y += gravity
        ball_y += ball_velocity_y

        # Prevent ball from going below the ground
        if ball_y > HEIGHT - HEIGHT // 4 - ball_radius:
            ball_y = HEIGHT - HEIGHT // 4 - ball_radius
            ball_velocity_y = 0
        
        # Draw the ball
        pygame.draw.circle(screen, ORANGE, (ball_x, int(ball_y)), ball_radius)
        
        # Spawn obstacles
        if spawn_timer % 100 == 0:
            obstacles.append([WIDTH, HEIGHT - HEIGHT // 4 - obstacle_height])
        spawn_timer += 1
        
        # Move and draw obstacles
        for obs in obstacles[:]:
            obs[0] -= obstacle_speed
            pygame.draw.rect(screen, GREY, (obs[0], obs[1], obstacle_width, obstacle_height))  # Filled grey rectangle
            draw_dda_line(obs[0], obs[1], obs[0] + obstacle_width, obs[1], GREY)
            draw_dda_line(obs[0], obs[1], obs[0], obs[1] + obstacle_height, GREY)
            draw_dda_line(obs[0] + obstacle_width, obs[1], obs[0] + obstacle_width, obs[1] + obstacle_height, GREY)
            draw_dda_line(obs[0], obs[1] + obstacle_height, obs[0] + obstacle_width, obs[1] + obstacle_height, GREY)
            
            # Check collision
            if obs[0] < ball_x + ball_radius and obs[0] + obstacle_width > ball_x - ball_radius:
                if obs[1] < ball_y + ball_radius:
                    game_over = True
        
        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs[0] > -obstacle_width]

        # Display scoreboard
        draw_text(f"Time Survived: {score} sec", 20, 20)  

        pygame.display.flip()
        clock.tick(30)
    
    # Game over screen
    screen.fill((0, 0, 0))
    draw_text("Game Over", WIDTH // 2 - 80, HEIGHT // 2 - 20)
    draw_text(f"Final Score: {score} sec", WIDTH // 2 - 100, HEIGHT // 2 + 20)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    wait_for_enter()
    main()
