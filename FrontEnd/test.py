import pygame
import math

# Setup
pygame.init()
screen = pygame.display.set_mode((750, 500))
clock = pygame.time.Clock()  # Used to calculate Delta time
running = True
dt = 0  # Stores seconds between frames

# Important positions
PLAYER1 = (50, 200, 15, 100)
PLAYER2 = (685, 200, 15, 100)
BALL = (355, 230, 40, 40)

# Values that can change [[x, y], [width, height]]
curr_player1 = [[50, 200], [15, 100]]
curr_player2 = [[685, 200], [15, 100]]
curr_ball = [[355, 230], [40, 40]]

# Movement Values
dx = 125
dy = 0
angle = 110
first_collision = True

while running:

    # Limits FPS 60
    # Calculates delta time for framerate-independent physics
    dt = clock.tick(60) / 1000

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cover last frame's graphics
    screen.fill("white")

    # Move the ball
    curr_ball[0][0] += dx * dt
    curr_ball[0][1] += dy * dt

    ball = pygame.draw.ellipse(screen, 'pink', (curr_ball[0][0], curr_ball[0][1], curr_ball[1][0], curr_ball[1][1]))
    player1 = pygame.draw.rect(screen, 'red', (curr_player1[0][0], curr_player1[0][1], curr_player1[1][0], curr_player1[1][1]))
    player2 = pygame.draw.rect(screen, 'blue', (curr_player2[0][0], curr_player2[0][1], curr_player2[1][0], curr_player2[1][1]))

    # Check collisions
    if player1.colliderect(ball) or player2.colliderect(ball):
        if first_collision:
            dy = 125*math.sin(math.radians(angle))
            first_collision = False
        dx*=-1.1
        curr_ball[0][0] += dx * dt
        curr_ball[0][1] += dy * dt

        print(dy)

    if curr_ball[0][1] <=0 or curr_ball[0][1] >= 470:
        dy*=-1

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        delta = 300 * dt

        # If this movement would not take the player out of bounds
        if curr_player1[0][1] - delta >= 0:
            curr_player1[0][1] -= delta

    if keys[pygame.K_s]:
        delta = 300 * dt

        # If this movement would not take the player out of bounds
        if curr_player1[0][1] + delta <= 400:
            curr_player1[0][1] += delta

    if keys[pygame.K_UP]:
        delta = 300 * dt

        # If this movement would not take the player out of bounds
        if curr_player2[0][1] - delta >= 0:
            curr_player2[0][1] -= delta

    if keys[pygame.K_DOWN]:
        delta = 300 * dt

        # If this movement would not take the player out of bounds
        if curr_player2[0][1] + delta <= 400:
            curr_player2[0][1] += delta            

    # Update display
    pygame.display.flip()

pygame.quit()
