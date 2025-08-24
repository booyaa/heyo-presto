from presto import Presto
from picovector import PicoVector, ANTIALIAS_BEST

presto = Presto(ambient_light=True)
display = presto.display

MAGENTA = display.create_pen(255, 0, 255)
BLACK = display.create_pen(0, 0, 0)

vector = PicoVector(presto.display)
vector.set_antialiasing(ANTIALIAS_BEST)
# vector.set_font_line_height(80)

display.set_pen(MAGENTA)
display.clear()
display.set_pen(BLACK)

y = [10,25,45,75,110,150,200]
for i in range(len(y)):
    vector.set_font("Roboto-Medium.af", 10 * i + 10)
    vector.text(f"{i+1}x Presto", 0, y[i], max_width=480) # width of 480 is a bit of a bodge to stop 7x from wrapping

presto.update()