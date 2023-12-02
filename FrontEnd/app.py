import tkinter as tk
import math


def move_ball():
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


def check_collision():
    global angle, numCollisions, speed, dx, dy
    
    overlapping_items = canvas.find_overlapping(*canvas.bbox(ball))
    overlapping_items = [item for item in overlapping_items if item != canvas.find_withtag("all")[-1]]

    if overlapping_items:
        numCollisions += 1
        speed = 1.25 + 0.1 * numCollisions

        dx = speed*math.cos(math.radians(angle))
        dy = speed*math.sin(math.radians(angle))
        angle += 90

    # Schedule the collision check again after 25 milliseconds
    root.after(25, check_collision)


root = tk.Tk()
root.title("Pong")

canvas = tk.Canvas(root, width=750, height=500)
canvas.pack()

line1 = canvas.create_line(50, 50, 50, 450, fill="red", width=2)
line2 = canvas.create_line(50, 50, 375, 50, fill="red", width=2)
line3 = canvas.create_line(50, 450, 375, 450, fill="red", width=2)

line4 = canvas.create_line(700, 50, 700, 450, fill="blue", width=2)
line5 = canvas.create_line(375, 50, 700, 50, fill="blue", width=2)
line6 = canvas.create_line(375, 450, 700, 450, fill="blue", width=2)

# Create a ball on the canvas
ball = canvas.create_oval(355, 230, 395, 270, fill="pink")

# Set the initial movement of the ball
numCollisions = 0
angle = 135
speed = 1.25
dx = 1.25
dy = 0

# Start the movement of the ball
collision_started = False
move_ball()

root.mainloop()
