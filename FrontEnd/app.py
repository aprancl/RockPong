import tkinter as tk
import math

def move_ball():
    global dx, dy, collision_started
    # Get the current coordinates of the ball
    x1, y1, x2, y2 = canvas.coords(ball)
    
    # Check if the ball is within the box boundaries
    canvas.move(ball, dx, dy)  # Move the ball 5 pixels to the right

    if not collision_started:
        check_collision()
        collision_started = True
    
    # Call move_ball again after 50 milliseconds
    root.after(30, move_ball)

def check_collision():
    global numCollisions, speed, dx, dy
    overlapping_items = canvas.find_overlapping(*canvas.bbox(ball))
    overlapping_items = [item for item in overlapping_items if item != 3]

    if overlapping_items:
        print(numCollisions)
        print(overlapping_items)
        print()
        numCollisions+=1
        speed = 5 + 0.2 * numCollisions

        dx = speed*math.cos(math.radians(45)*numCollisions)
        dy = speed*math.sin(math.radians(45)*numCollisions)

    root.after(50, check_collision)  # Schedule the collision check again after 10 milliseconds

root = tk.Tk()
root.title("Moving Ball Example")

canvas = tk.Canvas(root, width=1500, height=500)
canvas.pack()

box1 = canvas.create_rectangle(50, 50, 500, 450, outline="red", width=2)

box2 = canvas.create_rectangle(501, 50, 951, 450, outline="blue", width=2)

# Create a ball on the canvas
ball = canvas.create_oval(730, 230, 770, 270, fill="pink")

# Set the initial movement of the ball
numCollisions = 0
speed = 5
dx = 5
dy = 0

# Start the movement of the ball
collision_started = False
move_ball()

root.mainloop()