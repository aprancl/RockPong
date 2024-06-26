import pygame
import math
import cv2
import mediapipe as mp
import numpy as np


# Ball dimensions for restart
BALL = (355, 230, 40, 40)


def mediapipe_to_pixel_coords(normalized_x, normalized_y, frame_width, frame_height):
    pixel_x = int(normalized_x * frame_width)
    pixel_y = int(normalized_y * frame_height)

    # Return x and y corrdinates
    return pixel_x, pixel_y


def main():

    # Setup
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode(
        (screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    clock = pygame.time.Clock()  # Used to calculate Delta time
    running = True
    dt = 0  # Stores seconds between frames
    font = pygame.font.Font(None, 70)

    testing_ratio = 1536/864


    curr_ratio = (screen_info.current_w/screen_info.current_h)

    ratio = curr_ratio/testing_ratio

    print(ratio)

    # Ball dimensions for restart
    BALL = (screen_info.current_w/2, screen_info.current_h/2)

    # Values that can change [[x, y], [width, height]]
    curr_player1 = [[50, screen_info.current_h/2-20], [15*ratio, 100*ratio]]
    curr_player2 = [[screen_info.current_w-50,
                     screen_info.current_h/2-20], [15*ratio, 100*ratio]]
    curr_ball = [[BALL[0], BALL[1]], [40*ratio, 40*ratio]]
    scores = [0, 0]

    # Movement Values
    dx = 125
    dy = 0
    angle = 110
    first_collision = True
    cap = cv2.VideoCapture(0)
    side = 1

    with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():

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

            lines = draw_line_dashed(screen, (screen.get_width(
            )/2, 0), (screen.get_width()/2, screen_info.current_h), width=10, dash_length=17)
            ball = pygame.draw.ellipse(
                screen, 'pink', (curr_ball[0][0], curr_ball[0][1], curr_ball[1][0], curr_ball[1][1]))
            player1 = pygame.draw.rect(
                screen, 'red', (curr_player1[0][0], curr_player1[0][1], curr_player1[1][0], curr_player1[1][1]))
            player2 = pygame.draw.rect(
                screen, 'blue', (curr_player2[0][0], curr_player2[0][1], curr_player2[1][0], curr_player2[1][1]))
            draw_player_scores(screen, scores, font)

            # TODO paste here
            # Get the current frame
            ret, frame = cap.read()

            # Set varaibles to hold the inital width and height of the camera frame
            wid = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            hei = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            # frame = frame[0:500, 0:750]
            # wid = 750
            # hei = 500


            # Width to split the image fram with
            halfWid = wid/2
            # Get the current coordinates of the ball
            # x1, y1, x2, y2 = canvas.coords(ball)
            # (canvas.coords(ball)[0] + canvas.coords(ball)[2]) // 2
            mid_ball_x = curr_ball[0][0]
            if mid_ball_x <= (screen_info.current_w / 2) and side == 2:
                side = 1
            elif mid_ball_x > (screen_info.current_w / 2) and side == 1:
                side = 2

            # Check which side of the frame to analyze
            if (side == 1):  # For left side
                # Set width to be from 0 to the half width mark
                frame = frame[0:int(hei), 0:int(halfWid)]
            else:  # For right side
                # Set the width from the half width point to the width of the frame
                frame = frame[0:int(hei), int(halfWid):int(wid)]
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            # Make detection
            results = pose.process(image)

            # Recolor back to BGR (RGB?)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                # print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y, wid, hei))
                # print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y, wid, hei))
                # print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y, wid, hei))
                # print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y, wid, hei))

                # Convert elbow corrdinates to string
                left_elbow_coordinates = mediapipe_to_pixel_coords(
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y, screen_info.current_w, screen_info.current_h)
                right_elbow_coordinates = mediapipe_to_pixel_coords(
                    landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y, screen_info.current_w, screen_info.current_h)
                left_wrist_coordinates = mediapipe_to_pixel_coords(
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y, screen_info.current_w, screen_info.current_h)
                right_wrist_coordinates = mediapipe_to_pixel_coords(
                    landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y, screen_info.current_w, screen_info.current_h)
                # canvas.move(ball, )
                # TODO update where the pong paddles are based on the coordinates defined right here

                # If the wrist corrdinates are out of bounds set them to the edge of the screens

                # curr_player1[0][0] = right_wrist_coordinates[0]
                # curr_player1[0][1] = right_wrist_coordinates[1] - cur_player.y

                # cur_player = player1 if side == 1 else player2
                if side == 1:  # player1
                    # Check if player would out of bounds. If so, place them on edge
                    curr_player1[0][0] = right_wrist_coordinates[0]
                    # - player1.y
                    curr_player1[0][1] = right_wrist_coordinates[1]
                    curr_player1[0][0] /= 2

                    if curr_player1[0][0] > screen_info.current_w:
                        curr_player1[0][0] = screen_info.current_w - 5

                    elif curr_player1[0][0] < 0:
                        curr_player1[0][0] = 1

                    if curr_player1[0][1] > screen_info.current_h:
                        curr_player1[0][1] = screen_info.current_h
                    elif curr_player1[0][1] < 0:
                        curr_player1[0][1] = 1

                    # curr_player1[0][0] = right_wrist_coordinates[0]
                    # curr_player1[0][1] = right_wrist_coordinates[1] #- player1.y
                    # curr_player1[0][0] /= 2

                else:  # player2
                    # Check if player would be on the wrong side
                    curr_player2[0][0] = left_wrist_coordinates[0]
                    # - player2.y
                    curr_player2[0][1] = left_wrist_coordinates[1]
                    curr_player2[0][0] = (curr_player2[0][0] / 2) + (screen_info.current_w / 2)

                    if curr_player2[0][0] <= (screen_info.current_w / 2):
                        curr_player2[0][0] = (screen_info.current_w / 2) + 5

                    elif curr_player2[0][0] > screen_info.current_w:
                        curr_player2[0][0] = screen_info.current_w

                    if left_wrist_coordinates[1] > screen_info.current_h:
                        curr_player2[0][1] = screen_info.current_h
                    elif curr_player2[0][1] < 0:
                        curr_player2[0][1] = 1

                    # curr_player2[0][0] = left_wrist_coordinates[0]
                    # curr_player2[0][1] = left_wrist_coordinates[1]# - player2.y

                # f side == 1: # player1
                #     curr_player1[0][0] = right_wrist_coordinates[0]
                #     curr_player1[0][1] = right_wrist_coordinates[1] - cur_player.yelse: # player2
                # if(right_wrist_coordinates[0] < 0):
                #     dx = 50

                # cur_player = pygame.draw.rect(screen, 'blue', (dx, right_wrist_coordinates[1], cur_player[1][0], cur_player[1][1]))
                # canvas.move(cur_player, dx, dy)

                # Display the found elbow coordinates for left and right

                cv2.putText(image, str(left_wrist_coordinates), (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                cv2.putText(image, str(right_wrist_coordinates), (15, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                # TODO Move each player piece based on found coordinates.

            except:
                # print("There was an exception during pose detection. Make sure you are in frame.")
                pass

            # Render detections
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks,
                                                      mp.solutions.pose.POSE_CONNECTIONS,
                                                      mp.solutions.drawing_utils.DrawingSpec(
                                                          color=(245, 117, 66), thickness=2, circle_radius=2),
                                                      mp.solutions.drawing_utils.DrawingSpec(
                                                          color=(245, 66, 230), thickness=2, circle_radius=2)
                                                      )

            # Display pose detections to screen
            cv2.imshow('Mediapipe Feed', image)

            # Check collisions
            if player1.colliderect(ball) or player2.colliderect(ball):
                if first_collision:
                    dy = 125*math.sin(math.radians(angle))
                    first_collision = False
                dx *= -1.1
                curr_ball[0][0] += dx * dt
                curr_ball[0][1] += dy * dt

            if curr_ball[0][1] <= 0 or curr_ball[0][1] >= screen_info.current_h-5*ratio:
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

            if scores[0] > 9:
                winner = "Red"
                break
            elif scores[1] > 9:
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
                if curr_player1[0][1] + delta <= screen_info.current_h-55*ratio:
                    curr_player1[0][1] += delta

            if keys[pygame.K_UP]:
                delta = 300 * dt

                # If this movement would not take the player out of bounds
                if curr_player2[0][1] - delta >= 0:
                    curr_player2[0][1] -= delta

            if keys[pygame.K_DOWN]:
                delta = 300 * dt

                # If this movement would not take the player out of bounds
                if curr_player2[0][1] + delta <= screen_info.current_h-55*ratio:
                    curr_player2[0][1] += delta

            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                running = False
            # Update display
            pygame.display.flip()

        if running:
            screen.fill('white')
            s = f"{winner} Player wins!"
            text = font.render(s, True, 'black')
            screen.blit(text, ((screen.get_width()//2)-12 *
                        len(s), (screen.get_height()//2)-25))
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
    blue_text = font.render(str(scores[1]), True, 'blue')
    surface.blit(red_text, ((surface.get_width()/2)-50, 30))
    surface.blit(blue_text, ((surface.get_width()/2)+27, 30))


if __name__ == "__main__":
    main()