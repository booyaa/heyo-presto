# ICON [[(6.59, 7.4), (9.39, 4.6), (1.99, -2.8), (1.99, -12.0), (-2.01, -12.0), (-2.01, -1.2), (6.59, 7.4)], [(-0.01, 18.0), (-2.77, 17.82), (-5.22, 17.33), (-6.81, 16.84), (-9.0, 15.88), (-10.82, 14.83), (-12.37, 13.73), (-13.38, 12.88), (-14.8, 11.47), (-16.53, 9.28), (-17.71, 7.33), (-18.44, 5.84), (-18.93, 4.56), (-19.44, 2.82), (-19.69, 1.62), (-19.93, -0.24), (-19.98, -3.03), (-19.82, -4.82), (-19.36, -7.14), (-18.78, -8.99), (-18.18, -10.41), (-16.87, -12.77), (-15.61, -14.52), (-14.53, -15.77), (-13.03, -17.19), (-11.75, -18.19), (-9.49, -19.6), (-7.63, -20.48), (-5.31, -21.29), (-2.8, -21.81), (-1.17, -21.97), (0.56, -22.0), (2.17, -21.89), (4.17, -21.57), (5.78, -21.15), (6.98, -20.74), (8.54, -20.07), (10.61, -18.95), (12.5, -17.62), (14.56, -15.73), (15.71, -14.38), (16.82, -12.81), (18.11, -10.45), (18.75, -8.94), (19.3, -7.26), (19.84, -4.56), (19.98, -2.76), (19.98, -1.18), (19.8, 0.82), (19.39, 2.89), (18.67, 5.12), (17.97, 6.73), (16.56, 9.2), (15.45, 10.7), (13.58, 12.69), (11.88, 14.09), (10.45, 15.06), (9.16, 15.79), (6.7, 16.87), (5.01, 17.38), (2.25, 17.88), (0.04, 18.0)], [(-0.01, -2.0)], [(-0.01, 14.0), (1.87, 13.9), (3.1, 13.72), (4.92, 13.27), (6.57, 12.65), (7.85, 12.0), (9.95, 10.56), (11.26, 9.38), (12.07, 8.51), (13.65, 6.4), (14.66, 4.51), (15.18, 3.17), (15.75, 0.9), (15.93, -0.48), (15.99, -2.41), (15.75, -4.87), (15.46, -6.25), (14.87, -8.01), (14.31, -9.23), (13.28, -10.95), (12.42, -12.08), (11.05, -13.55), (9.91, -14.56), (8.05, -15.86), (6.45, -16.69), (4.54, -17.39), (3.36, -17.68), (1.71, -17.92), (0.44, -18.0), (-1.44, -17.94), (-2.97, -17.75), (-5.29, -17.16), (-6.71, -16.59), (-8.07, -15.88), (-10.05, -14.49), (-11.32, -13.34), (-12.48, -12.07), (-13.2, -11.12), (-14.1, -9.69), (-14.72, -8.44), (-15.33, -6.79), (-15.77, -4.91), (-15.98, -3.05), (-16.0, -1.85), (-15.9, -0.04), (-15.44, 2.39), (-14.95, 3.89), (-14.24, 5.45), (-13.24, 7.08), (-12.22, 8.41), (-11.39, 9.31), (-10.07, 10.49), (-8.57, 11.58), (-7.27, 12.32), (-5.83, 12.96), (-4.11, 13.51), (-1.72, 13.91), (-0.06, 14.0)]]
# NAME Flip Clock
# DESC Old school flip clock

# source: https://gist.github.com/cvuorinen/96e4934e1d681a5cfd7333c49fcd0f90
import time
import secrets
import ntptime
from presto import Presto
from touch import Button
from picovector import ANTIALIAS_BEST, PicoVector, Polygon

# Setup for the Presto display
presto = Presto()
touch = presto.touch
display = presto.display
vector = PicoVector(display)

presto.set_backlight(0.2)
display.set_font("bitmap8")
vector.set_font("Roboto-Medium.af", 20)
vector.set_antialiasing(ANTIALIAS_BEST)

# Set TIMEZONE_OFFSET in secrets.py (as integer of hours from UTC)
TIMEZONE_OFFSET = getattr(secrets, 'TIMEZONE_OFFSET', 0) * 3600

# Change this to desired background color
BG_COLOR = display.create_pen(50, 50, 50)

# Change to False to use light mode by default (toggle by touching the screen)
dark = True

# Constants
MONTHS = ('', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
DAYS = ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')
WIDTH, HEIGHT = display.get_bounds()
CX = WIDTH // 2
CY = HEIGHT // 2
BLACK = display.create_pen(10, 10, 10)
WHITE = display.create_pen(200, 200, 200)

# Clear the screen before the network call is made
display.set_pen(BLACK)
display.clear()
presto.update()

def show_message(text):
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    display.text(f"{text}", 5, 10, WIDTH, 2)
    presto.update()


show_message("Connecting...")

try:
    wifi = presto.connect()
except ValueError as e:
    while True:
        show_message(e)
except ImportError as e:
    while True:
        show_message(e)

# Set the correct time using the NTP service.
try:
    ntptime.settime()
except OSError:
    while True:
        show_message("Unable to get time.\n\nCheck your network try again.")

# Make background as a button (so you can tap anywhere), used to switch between dark/light mode
bg = Button(0, 0, WIDTH, HEIGHT)

# Set up boxes with rounded corners and lines in the middle for the "flips"
margin = 10
big_box_size = 100

hour_box_x = CX - big_box_size - margin
hour_box_y = margin
hour_box = Polygon()
hour_box.rectangle(hour_box_x, hour_box_y, big_box_size, big_box_size, (20, 20, 20, 20))
hour_line_y = hour_box_y + (big_box_size // 2)
hour_line = Polygon()
hour_line.line(hour_box_x, hour_line_y, hour_box_x + big_box_size, hour_line_y, 3)

minute_box_x = CX + margin
minute_box_y = hour_box_y
minute_box = Polygon()
minute_box.rectangle(minute_box_x, minute_box_y, big_box_size, big_box_size, (20, 20, 20, 20))
minute_line_y = minute_box_y + (big_box_size // 2)
minute_line = Polygon()
minute_line.line(minute_box_x, minute_line_y, minute_box_x + big_box_size, minute_line_y, 3)

small_box_size = 50

week_day_box_width = 200
week_day_box_x = (WIDTH - week_day_box_width) // 2
week_day_box_y = hour_box_y + big_box_size + margin
week_day_box = Polygon()
week_day_box.rectangle(week_day_box_x, week_day_box_y, week_day_box_width, small_box_size, (10, 10, 10, 10))
week_day_line_y = week_day_box_y + (small_box_size // 2)
week_day_line = Polygon()
week_day_line.line(week_day_box_x, week_day_line_y, week_day_box_x + week_day_box_width, week_day_line_y, 2)

month_box_width = 100
day_box_x = (WIDTH - small_box_size - month_box_width) // 2
day_box_y = week_day_box_y + small_box_size + margin
day_box = Polygon()
day_box.rectangle(day_box_x, day_box_y, small_box_size, small_box_size, (10, 10, 10, 10))
day_line_y = day_box_y + (small_box_size // 2)
day_line = Polygon()
day_line.line(day_box_x, day_line_y, day_box_x + small_box_size, day_line_y, 2)

month_box_x = day_box_x + small_box_size + margin
month_box_y = day_box_y
month_box = Polygon()
month_box.rectangle(month_box_x, month_box_y, month_box_width, small_box_size, (10, 10, 10, 10))
month_line_y = month_box_y + (small_box_size // 2)
month_line = Polygon()
month_line.line(month_box_x, month_line_y, month_box_x + month_box_width, month_line_y, 2)


def draw():
    display.set_pen(BG_COLOR)
    display.rectangle(*bg.bounds)

    display.set_pen(BLACK if dark else WHITE)
    vector.draw(hour_box)
    vector.draw(minute_box)
    vector.draw(week_day_box)
    vector.draw(day_box)
    vector.draw(month_box)

    _, month, day, hour, minute, _, week_day, _ = time.localtime(time.time() + TIMEZONE_OFFSET)

    display.set_pen(WHITE if dark else BLACK)
    vector.set_font_size(75)
    # vector text seems to render a bit weirdly vertically, need this offset (found by trial and error)
    text_offset_y = 70

    hour_text = f"{hour}"
    _, _, hour_text_width, _ = vector.measure_text(hour_text)
    if len(hour_text) > 1:
        hour_text_x = hour_box_x + ((big_box_size - int(hour_text_width)) // 2)
    else:
        hour_text_x = hour_box_x + big_box_size - 20 - int(hour_text_width)
    vector.text(hour_text, hour_text_x, hour_box_y + text_offset_y)

    minute_text = "{:02d}".format(minute)
    _, _, minute_text_width, _ = vector.measure_text(minute_text)
    vector.text(minute_text, minute_box_x + ((big_box_size - int(minute_text_width)) // 2), minute_box_y + text_offset_y)


    vector.set_font_size(35)
    text_offset_y = 35

    week_day_text = DAYS[week_day]
    _, _, week_day_text_width, _ = vector.measure_text(week_day_text)
    vector.text(week_day_text, week_day_box_x + ((week_day_box_width - int(week_day_text_width)) // 2), week_day_box_y + text_offset_y)

    day_text = f"{day}"
    _, _, day_text_width, _ = vector.measure_text(day_text)
    vector.text(day_text, day_box_x + ((small_box_size - int(day_text_width)) // 2), day_box_y + text_offset_y)

    month_text = MONTHS[month]
    _, _, month_text_width, _ = vector.measure_text(month_text)
    vector.text(month_text, month_box_x + ((month_box_width - int(month_text_width)) // 2), month_box_y + text_offset_y)

    display.set_pen(BLACK)
    vector.draw(hour_line)
    vector.draw(minute_line)
    vector.draw(week_day_line)
    vector.draw(day_line)
    vector.draw(month_line)

    presto.update()


while True:
    touch.poll()
    if bg.is_pressed():
        dark = not dark

    draw()
    time.sleep(1)
