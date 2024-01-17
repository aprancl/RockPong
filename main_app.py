#Imports
import cv2
import mediapipe as mp
import numpy as np

import tkinter as tk
import math
from typing import List
import pdb


def restart(player: int) -> None:
    """
    Parameters:
    player: an int representing the index of the player whose score should be incremented

    Resets the game board
    """
    global dx, dy, angle, speed, num_collisions, scores

    # Update variables
    scores[player] += 1
    num_collisions = 0
    angle = 120 if sum(scores) % 2 == 0 else 300
    speed = 1.25
    dx = 1.25 if sum(scores) % 2 == 0 else -1.25
    dy = 0

    # Update canvas
    canvas.coords(ball, (355, 230, 395, 270))
    canvas.itemconfig(scoreboard, text=f"{scores[0]} - {scores[1]}")


def move_ball() -> None:
    """Moves the ball across the canvas"""
    global dx, dy, collision_started

    # Get the current coordinates of the ball
    x1, y1, x2, y2 = canvas.coords(ball)

    # Check if either player has scored
    if x1 < 0:
        restart(1)
    elif x2 > 750:
        restart(0)

    # Check if ball within canvas
    if y1 < 0 or y2 > 500:
        dy = -dy  # Reverse the vertical direction

    canvas.move(ball, dx, dy)  # Move the ball

    if not collision_started:
        check_collision()
        collision_started = True

    # Call move_ball again after 5 milliseconds
    root.after(5, move_ball)


def check_collision() -> None:
    """Checks if the ball should bounce and changes its direction if it does"""
    global angle, num_collisions, speed, dx, dy

    overlapping_items = canvas.find_overlapping(*canvas.bbox(ball))

    # If ball is colliding with anything other than the players
    overlapping_items = [item for item in overlapping_items if item <= 2]

    if overlapping_items:
        speed = 1.25 + 0.1 * num_collisions
        if num_collisions == 0:
            dx = speed*math.cos(math.radians(angle))
            dy = speed*math.sin(math.radians(angle))
        else:
            dx *= -1.1
        num_collisions += 1

    # Schedule the collision check again after 25 milliseconds
    root.after(25, check_collision)


def populate_canvas() -> List[int]:
    """Adds objects to the canvas"""

    # Player Rectangles
    player1 = canvas.create_rectangle(50, 200, 65, 300, fill="red")
    player2 = canvas.create_rectangle(685, 200, 700, 300, fill="blue")

    # Create a ball on the canvas
    ball = canvas.create_oval(355, 230, 395, 270, fill="pink")

    # Create scoreboard
    scoreboard = canvas.create_text(375, 20, text="0 - 0", font=("Arial", 20), fill="black")

    return [player1, player2, ball, scoreboard]


def move_player(key: str, dy: int, player: int, ID: int) -> None:
    """
    Parameters:
    key: A string representing the key being pressed
    dy: An int representing the change in y
    player: An int representing the canvas ID of the player rectangle
    ID: An int representing the index storing this call's afterID

    Moves the Player Rectangles
    """
    global after_IDs

    if key in active_keys:
        coords = canvas.coords(player)

        # If player movement would not cause player to leave canvas
        if not (coords[1] + dy < 0 or coords[3] + dy > 500):        
            canvas.move(player, 0, dy)

            after_IDs[ID] = canvas.after(10, move_player, key, dy, player, ID)
    # else:
    #     if after_IDs[ID] is not None:
    #         canvas.after_cancel(after_IDs[ID])
    #         after_IDs[ID] = None


def on_press(event: tk.Event) -> None:
    """
    Parameters:
    event: A tk.Event that contains the pressed key

    Adds pressed key to the set of active keys and begins moving player rectangle
    """
    global after_IDs

    key = event.keysym.lower()

    # Prevent multiple instances of "move_player" happening for a singular press
    if key not in active_keys:
        active_keys.add(key)

        if key == 'w':
            move_player(key, -5, player1, 0)
        elif key == 's':
            move_player(key, 5, player1, 1)
        elif key == 'up':
            move_player(key, -5, player2, 2)
        elif key == 'down':
            move_player(key, 5, player2, 3)


def on_release(event: tk.Event) -> None:
    """
    Parameters:
    event: A tk.Event that contains the released key

    Removes released key from the set of active keys
    """

    key = event.keysym.lower()
    active_keys.discard(key)
# This function is called by main to convert the media pipe pose locations for x and y coordinates
def mediapipe_to_pixel_coords(normalized_x, normalized_y, frame_width, frame_height):
    pixel_x = int(normalized_x * frame_width)
    pixel_y = int(normalized_y * frame_height)

    #Return x and y corrdinates
    return pixel_x, pixel_y


root = tk.Tk()
root.title("Pong")

canvas = tk.Canvas(root, width=750, height=500)
canvas.pack()

relevant_objects = populate_canvas()

    # Canvas item_IDs
player1, player2, ball, scoreboard = relevant_objects[0], relevant_objects[1], relevant_objects[2], relevant_objects[3]

    # Variables that control movement
num_collisions = 0
angle = 120     # Angle the ball will move in
speed = 1.25    # Speed at which the ball will move
dx = 1.25       # Change in the x-axis
dy = 0          # Change in the y-axis

    # Event handlers
canvas.bind("<KeyPress>", on_press)
canvas.bind("<KeyRelease>", on_release)

    # Set of keys currently being pressed
active_keys = set()

    # List of after IDs to save memory
after_IDs = [None, None, None, None]

    # Tracks player scores
scores = [0, 0]

canvas.focus_set()

    # Start the movement of the ball
collision_started = False


# This is the main function of the program to analyze given video capture
def main():
    #Side varaible to be changed based on the side that you want to capture and analyze for the game
    side = 1

    # Begin camera capture
    cap = cv2.VideoCapture(0)

    ## Setup mediapipe instance
    with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # While the camera is running
        while cap.isOpened():
            side = abs( side - 3)

            # Get the current frame 
            ret, frame = cap.read()
            
            # Set varaibles to hold the inital width and height of the camera frame
            #wid = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            #hei = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            frame = frame[0:500, 0:750]
            wid = 750
            hei = 500
            

            print(wid)
            print(hei)
            # Width to split the image fram with
            halfWid = wid/2
            print(halfWid)
            # Get the current coordinates of the ball
            #x1, y1, x2, y2 = canvas.coords(ball)

            # Check which side of the frame to analyze
            if(side == 1): # For left side
                #Set width to be from 0 to the half width mark
                frame = frame[0:500, 0:int(halfWid)]
            else: # For right side
                # Set the width from the half width point to the width of the frame
                frame = frame[0:500, int(halfWid):int(wid)]
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR (RGB?)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                #print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y, wid, hei))
                #print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y, wid, hei))
                #print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y, wid, hei))
                #print(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y, wid, hei))

                # Convert elbow corrdinates to string
                left_elbow_coordinates = str(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y, wid, hei))
                right_elbow_coordinates = str(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y, wid, hei))
                left_wrist_coordinates = str(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y, wid, hei))
                right_wrist_coordinates = str(mediapipe_to_pixel_coords(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y, wid, hei))
                
                # Display the found elbow coordinates for left and right

                cv2.putText(image, left_elbow_coordinates, (15,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

                cv2.putText(image, right_elbow_coordinates, (15,30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                # TODO Move each player piece based on found coordinates.
                
            except:
                print("There was an exception during pose detection. Make sure you are in frame.")
                pass

            # Render detections
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, 
                                    mp.solutions.pose.POSE_CONNECTIONS,
                                    mp.solutions.drawing_utils.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp.solutions.drawing_utils.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            # Display pose detections to screen
            cv2.imshow('Mediapipe Feed', image)

            #!!!!TO ADD!!!!
            #This function while loop shoud also be the loop running the window for the game and pong ball functionalities
            #take left_elbow_coordinates/ left_wrist_coordinates and right_elbow_corrdinates/ right_wrist_corrdinates, get their range of 
            #contact corrdinates and compare to ball location
            # If the ball is out of bounds, opposing player gets a point and and ball resets
            # If the ball location is within the contact range perform the physics movement to opposite direction
            
            move_ball()

            # root.mainloop()
            root.update()
            # Check if user wants to quit the program
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
       
    
    


if __name__ == "__main__":
    main()

