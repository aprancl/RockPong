import pygame
import math
import numpy as np
import pdb


def main():

    # Setup
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    clock = pygame.time.Clock()  # Used to calculate Delta time
    running = True
    dt = 0  # Stores seconds between frames
    font = pygame.font.Font(None,70)

    ratio = (screen_info.current_w/1536,screen_info.current_h/864) 

    # Ball dimensions for restart
    BALL = (screen_info.current_w/2, screen_info.current_h/2)


    # Values that can change [[x, y], [width, height]]
    curr_player1 = [[50, screen_info.current_h/2], [15*ratio[0], 100*ratio[1]]]
    curr_player2 = [[screen_info.current_w-50, screen_info.current_h/2], [15*ratio[0], 100*ratio[1]]]
    curr_ball = [[BALL[0], BALL[1]], [40*ratio[0], 40*ratio[1]]]
    scores = [0, 0]

    winner = -1

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

        lines = draw_line_dashed(screen, (screen.get_width()/2, 0), (screen.get_width()/2, screen_info.current_h+35*ratio[1]), width=10, dash_length=16)
        ball = pygame.draw.ellipse(screen, 'pink', (curr_ball[0][0], curr_ball[0][1], curr_ball[1][0], curr_ball[1][1]))
        player1 = pygame.draw.rect(screen, 'red', (curr_player1[0][0], curr_player1[0][1], curr_player1[1][0], curr_player1[1][1]))
        player2 = pygame.draw.rect(screen, 'blue', (curr_player2[0][0], curr_player2[0][1], curr_player2[1][0], curr_player2[1][1]))
        draw_player_scores(screen, scores, font)

        # Check collisions
        if player1.colliderect(ball) or player2.colliderect(ball):
            if first_collision:
                dy = 125*math.sin(math.radians(angle))
                first_collision = False
            dx *= -1.1
            curr_ball[0][0] += dx * dt
            curr_ball[0][1] += dy * dt

        if curr_ball[0][1] <= 0 or curr_ball[0][1] >= screen_info.current_h-40*ratio[1]:
            dy *= -1

        if curr_ball[0][0] <= 0:
            scores[1] += 1
            curr_ball[0][0] = BALL[0]
            curr_ball[0][1] = BALL[1]
            dx = 125 if sum(scores) % 2 == 0 else -125
            dy = 0
            angle = 110 if sum(scores) % 2 == 0 else 290
            first_collision = True

        elif curr_ball[0][0] >= screen_info.current_w:
            scores[0] += 1
            curr_ball[0][0] = BALL[0]
            curr_ball[0][1] = BALL[1]
            dx = 125 if sum(scores) % 2 == 0 else -125
            dy = 0
            angle = 110 if sum(scores) % 2 == 0 else 290
            first_collision = True

        if scores[0]>9:
            winner = "Red"
            break
        elif scores[1]>9:
            winner = "Blue"
            break

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
            if curr_player1[0][1] + delta <= screen_info.current_h-55*ratio[1]:
                curr_player1[0][1] += delta

        if keys[pygame.K_UP]:
            delta = 300 * dt

            # If this movement would not take the player out of bounds
            if curr_player2[0][1] - delta >= 0:
                curr_player2[0][1] -= delta

        if keys[pygame.K_DOWN]:
            delta = 300 * dt

            # If this movement would not take the player out of bounds
            if curr_player2[0][1] + delta <= screen_info.current_h-55*ratio[1]:
                curr_player2[0][1] += delta

        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            running = False
        # Update display
        pygame.display.flip()

    if running:
        screen.fill('white')
        s = f"{winner} Player wins!"
        text = font.render(s,True, 'black')
        screen.blit(text, ((screen.get_width()//2)-12*len(s),(screen.get_height()//2)-25))
        pygame.display.flip()
        while running:
            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                running = False

    pygame.quit()


def draw_line_dashed(surface: pygame.Surface, start: tuple[int], end: tuple[int], width: int = 1, dash_length: float = 17) -> list[pygame.Rect]: 
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

def draw_player_scores(surface: pygame.Surface, scores: list[int], font: pygame.font.Font) -> None:
    red_text = font.render(str(scores[0]), True, 'red')
    blue_text = font.render(str(scores[1]),True,'blue')
    surface.blit(red_text, ((surface.get_width()/2)-50,30))
    surface.blit(blue_text, ((surface.get_width()/2)+27,30))

if __name__ == "__main__":
    main()
