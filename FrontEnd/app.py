import tkinter as tk
import math
from typing import List


def move_ball() -> None:
    """Moves the ball across the canvas"""
    global dx, dy, collision_started

    # Get the current coordinates of the ball
    x1, y1, x2, y2 = canvas.coords(ball)

    # Check if the ball is within the box boundaries
    if x1 < 0 or x2 > canvas.winfo_width():
        dx = -dx  # Reverse the horizontal direction
    if y1 < 0 or y2 > canvas.winfo_height():
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
    overlapping_items = [
        item for item in overlapping_items if item != canvas.find_withtag("all")[-1]]

    if overlapping_items:
        num_collisions += 1
        speed = 1.25 + 0.1 * num_collisions

        dx = speed*math.cos(math.radians(angle))
        dy = speed*math.sin(math.radians(angle))
        angle += 90

    # Schedule the collision check again after 25 milliseconds
    root.after(25, check_collision)


def populate_canvas() -> List[int]:
    """Adds objects to the canvas"""

    # Red Lines
    canvas.create_line(50, 50, 50, 450, fill="red", width=2)
    canvas.create_line(50, 50, 375, 50, fill="red", width=2)
    canvas.create_line(50, 450, 375, 450, fill="red", width=2)

    # Blue Lines
    canvas.create_line(700, 50, 700, 450, fill="blue", width=2)
    canvas.create_line(375, 50, 700, 50, fill="blue", width=2)
    canvas.create_line(375, 450, 700, 450, fill="blue", width=2)

    # Player Rectangles
    player1 = canvas.create_rectangle(50, 200, 65, 300, fill="red")
    player2 = canvas.create_rectangle(685, 200, 700, 300, fill="blue")

    # Create a ball on the canvas
    ball = canvas.create_oval(355, 230, 395, 270, fill="pink")
    return [player1, player2, ball]


root = tk.Tk()
root.title("Pong")

canvas = tk.Canvas(root, width=750, height=500)
canvas.pack()

relevant_objects = populate_canvas()

player1, player2, ball = relevant_objects[0], relevant_objects[1], relevant_objects[2]

# Variables that control movement
num_collisions = 0
angle = 135     # Angle the ball will move in
speed = 1.25    # Speed at which the ball will move
dx = 1.25       # Change in the x-axis
dy = 0          # Change in the y-axis

# Start the movement of the ball
collision_started = False
move_ball()

root.mainloop()
