# how to download images from the web and display them without saving
import jpegdec
from urllib import urequest
from presto import Presto

# Setup for the Presto display
presto = Presto()
display = presto.display
WIDTH, HEIGHT = display.get_bounds()
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(255, 0, 0)

# Clear the screen before the network call is made
display.set_pen(BLACK)
display.clear()
presto.update()

def show_message(text):
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(RED)
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

show_message("Image loading...")

try:
    # source: https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/pico_inky/placekitten.py#L55
    url = "https://placehold.co/240/jpg" # image must fit in RAM for this to work (try greyscaling and dithering)
    socket = urequest.urlopen(url)
    data = bytearray(1024 * 10)
    socket.readinto(data)
    socket.close()

    j = jpegdec.JPEG(display)
    j.open_RAM(data)
    j.decode(0, 0)
except OSError as e:
    print(f"failed to load image: {e}")
    display.set_pen(BLACK)
    display.clear()

presto.set_backlight(0.5)
presto.update()
