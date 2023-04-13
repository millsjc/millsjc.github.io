import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize mixer
pygame.mixer.init()

# Load fail buzzer sound
fail_sound = pygame.mixer.Sound('fail_buzzer.wav')

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

# Ball dimensions
BALL_WIDTH = 10
BALL_HEIGHT = 10

# Colors
WHITE = (255, 255, 255)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Create paddles and ball
left_paddle = pygame.Rect(0, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_WIDTH // 2, SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)

# Ball velocity
ball_speed_x = 4
ball_speed_y = 4

# Paddle speed
paddle_speed = 2

# Scores
left_score = 0
right_score = 0

# Font
score_font = pygame.font.Font(None, 36)

def ai_move(paddle, ball, speed):
    if paddle.centery < ball.centery and paddle.bottom < SCREEN_HEIGHT:
        paddle.y += speed
    elif paddle.centery > ball.centery and paddle.top > 0:
        paddle.y -= speed

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move left paddle (controlled by AI)
    ai_move(left_paddle, ball, paddle_speed)

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Move right paddle
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.y += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x

    # Ball out of bounds
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        # Play fail sound
        fail_sound.play()

        # Update scores
        if ball.left <= 0:
            right_score += 1
        else:
            left_score += 1

        ball.x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
        ball.y = SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2
        ball_speed_x = -ball_speed_x
        ball_speed_y = -ball_speed_y

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Draw scores
    left_score_text = score_font.render(str(left_score), True, WHITE)
    right_score_text = score_font.render(str(right_score), True, WHITE)
    screen.blit(left_score_text, (SCREEN_WIDTH // 4, 10))
    screen.blit(right_score_text, (SCREEN_WIDTH * 3 // 4, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)