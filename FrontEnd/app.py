import tkinter as tk
import math
from typing import List


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
move_ball()

root.mainloop()
