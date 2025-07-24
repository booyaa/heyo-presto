# ICON [[(-14.2, 9.3), (-15.78, 7.45), (-16.62, 6.28), (-17.56, 4.73), (-18.14, 3.59), (-18.88, 1.75), (-19.61, -0.93), (-19.94, -3.27), (-20.0, -4.85), (-19.95, -6.25), (-19.74, -8.12), (-19.17, -10.67), (-18.24, -13.17), (-17.16, -15.22), (-15.5, -17.62), (-14.24, -19.06), (-11.8, -16.7), (-12.55, -15.9), (-13.7, -14.42), (-14.37, -13.34), (-15.33, -11.34), (-16.08, -9.02), (-16.44, -7.18), (-16.58, -5.68), (-16.59, -4.41), (-16.47, -2.85), (-16.14, -1.01), (-15.77, 0.34), (-15.15, 2.0), (-14.66, 3.02), (-13.78, 4.5), (-12.84, 5.76), (-11.84, 6.86), (-14.2, 9.3)], [(-9.4, 4.5), (-10.35, 3.46), (-11.26, 2.22), (-12.11, 0.73), (-12.57, -0.34), (-13.06, -1.98), (-13.39, -4.46), (-13.38, -5.5), (-13.13, -7.51), (-12.73, -9.0), (-12.17, -10.4), (-11.17, -12.15), (-10.38, -13.22), (-9.44, -14.26), (-7.0, -11.9), (-7.83, -11.04), (-8.45, -10.22), (-9.19, -8.84), (-9.85, -6.62), (-9.99, -5.44), (-9.9, -3.59), (-9.45, -1.79), (-9.03, -0.76), (-7.96, 1.0), (-7.04, 2.06), (-9.4, 4.5)], [(-10.0, 19.1), (-3.25, -1.15), (-3.85, -1.76), (-4.53, -2.75), (-4.92, -3.96), (-5.0, -4.75), (-4.92, -5.83), (-4.33, -7.45), (-3.58, -8.42), (-2.22, -9.4), (-1.44, -9.71), (-0.05, -9.9), (0.79, -9.84), (2.34, -9.34), (3.72, -8.27), (4.37, -7.37), (4.9, -5.92), (4.95, -4.23), (4.64, -3.1), (4.21, -2.27), (3.29, -1.18), (10.0, 19.1), (6.0, 19.1), (4.7, 15.1), (-4.65, 15.1), (-6.0, 19.1), (-10.0, 19.1)], [(-3.35, 11.1), (3.35, 11.1), (0.0, 1.1), (-3.35, 11.1)], [(9.4, 4.5), (7.0, 2.1), (8.4, 0.5), (9.07, -0.69), (9.48, -1.73), (9.82, -3.04), (9.98, -4.31), (9.88, -6.36), (9.4, -8.16), (8.72, -9.65), (8.3, -10.32), (7.04, -11.86), (9.4, -14.3), (10.51, -13.05), (11.8, -11.02), (12.73, -8.65), (13.17, -6.8), (13.4, -4.95), (13.33, -3.67), (13.09, -2.17), (12.74, -0.93), (12.22, 0.42), (11.5, 1.81), (10.34, 3.46), (9.44, 4.46)], [(14.2, 9.3), (11.8, 6.9), (13.45, 4.97), (14.46, 3.4), (15.08, 2.18), (15.76, 0.37), (16.26, -1.57), (16.59, -4.27), (16.54, -6.22), (16.26, -8.22), (15.73, -10.24), (14.8, -12.52), (14.04, -13.89), (13.26, -15.02), (11.84, -16.66), (14.2, -19.1), (15.95, -17.01), (16.9, -15.63), (18.02, -13.57), (18.58, -12.26), (19.23, -10.36), (19.75, -8.05), (19.94, -6.43), (20.0, -4.95), (19.86, -2.51), (19.59, -0.76), (19.01, 1.48), (18.31, 3.36), (17.07, 5.71), (15.66, 7.68), (14.24, 9.26)]]
# NAME Meshtastic
# DESC Meshtastic Console
from presto import Presto
from touch import Button
import requests

presto = Presto()
display = presto.display
WIDTH, HEIGHT = display.get_bounds()

# Couple of colours for use later
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(230, 60, 45)
GREEN = display.create_pen(9, 185, 120)
BLACK = display.create_pen(0, 0, 0)

# We'll need this for the touch element of the screen
touch = presto.touch

CX = WIDTH // 2
CY = HEIGHT // 2
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50

# Create a touch button and set the touch region.
# Button(x, y, width, height)
button_1 = Button(10, 155, BUTTON_WIDTH, BUTTON_HEIGHT)
button_2 = Button(70, 155, BUTTON_WIDTH, BUTTON_HEIGHT)
button_3 = Button(130, 155, BUTTON_WIDTH, BUTTON_HEIGHT)

feedback_x = 10
feedback_y = 30

while True:

    # Check for touch changes
    touch.poll()

    # Clear the screen and set the background colour
    display.set_pen(WHITE)
    display.clear()
    display.set_pen(BLACK)

    # Title text
    display.text("Buttons Doing Nothing", 2, 7)

    # Finding the state of a touch button is much the same as a physical button
    # calling '.is_pressed()' on your button object will return True or False
    if button_1.is_pressed():
        display.set_pen(GREEN)
        r = requests.post("http://localhost:5000/send/ping")
        if r.status_code == 200:
            display.text("Sent ping!", feedback_x, feedback_y)
        else: 
            display.text("Failed to send ping.", feedback_x, feedback_y)
    else:
        display.set_pen(RED)

    # We've defined our touch Button object but we need a visual representation of it for the user!
    # We can use the '.bounds' property of our Button object to set the X, Y, WIDTH and HEIGHT
    display.rectangle(*button_1.bounds)

    if button_2.is_pressed():
        display.set_pen(GREEN)
        display.text("You Pressed Button 2!", feedback_x, feedback_y)
    else:
        display.set_pen(RED)

    display.rectangle(*button_2.bounds)

    if button_3.is_pressed():
        display.set_pen(GREEN)
        display.text("You Pressed Button 3!", feedback_x, feedback_y)
    else:
        display.set_pen(RED)

    display.rectangle(*button_3.bounds)

    # Finally, we update the screen so we can see our changes!
    presto.update()
