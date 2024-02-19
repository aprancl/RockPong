import pygame
import math
import numpy as np


# Ball dimensions for restart
BALL = (355, 230)


def main():

    # Setup
    pygame.init()
    screen = pygame.display.set_mode((750, 500))
    clock = pygame.time.Clock()  # Used to calculate Delta time
    running = True
    dt = 0  # Stores seconds between frames

    # Values that can change [[x, y], [width, height]]
    curr_player1 = [[50, 200], [15, 100]]
    curr_player2 = [[685, 200], [15, 100]]
    curr_ball = [[355, 230], [40, 40]]
    scores = [0, 0]

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

        lines = draw_line_dashed(screen, (screen.get_width()/2, 0), (screen.get_width()/2, 500), width=10)
        ball = pygame.draw.ellipse(screen, 'pink', (curr_ball[0][0], curr_ball[0][1], curr_ball[1][0], curr_ball[1][1]))
        player1 = pygame.draw.rect(screen, 'red', (curr_player1[0][0], curr_player1[0][1], curr_player1[1][0], curr_player1[1][1]))
        player2 = pygame.draw.rect(screen, 'blue', (curr_player2[0][0], curr_player2[0][1], curr_player2[1][0], curr_player2[1][1]))

        # Check collisions
        if player1.colliderect(ball) or player2.colliderect(ball):
            if first_collision:
                dy = 125*math.sin(math.radians(angle))
                first_collision = False
            dx *= -1.1
            curr_ball[0][0] += dx * dt
            curr_ball[0][1] += dy * dt

        if curr_ball[0][1] <= 0 or curr_ball[0][1] >= 470:
            dy *= -1

        if curr_ball[0][0] <= 0:
            scores[0] += 1
            curr_ball[0][0] = BALL[0]
            curr_ball[0][1] = BALL[1]
            dx = 125 if sum(scores) % 2 == 0 else -125
            dy = 0
            angle = 110 if sum(scores) % 2 == 0 else 290
            first_collision = True

        elif curr_ball[0][0] >= 750:
            scores[1] += 1
            curr_ball[0][0] = BALL[0]
            curr_ball[0][1] = BALL[1]
            dx = 125 if sum(scores) % 2 == 0 else -125
            dy = 0
            angle = 110 if sum(scores) % 2 == 0 else 290
            first_collision = True

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


def draw_line_dashed(surface: pygame.Surface, start: tuple[int], end: tuple[int], width: int = 1, dash_length: float = 15.5) -> list[pygame.Rect]: 
    """Draws a dashed line from start to end with desired width and length
       Parameters:
       surface:     The screen where the dashes are to be drawn
       start:       The start point
       end:         The end point
       width:       The desired width of each dash
       dash_length: The length of each dash
       
       Returns:
       A list of references to pygame.Rect objects"""
    
    # Convert tuples to numpy arrays
    start = np.array(start)
    end = np.array(end)

    # Calculate the length of the line
    length = np.linalg.norm(end - start)

    # Determine the number of dashes
    num_dashes = int(length / dash_length)

    # Calculate the positions of the dashes
    dash_segments = np.array(
        [np.linspace(start[i], end[i], num_dashes) for i in range(2)]).transpose()

    # Draw dashed line segments
    # Each line is drawn from dash_segments[i] to dash_segments[i+1]
    # Alternates between red and blue
    return [pygame.draw.line(surface, "Blue" if n % 2 == 0 else "Red", tuple(dash_segments[n]), tuple(dash_segments[n + 1]), width)
            for n in range(0, num_dashes-1, 3)]


if __name__ == "__main__":
    main()
