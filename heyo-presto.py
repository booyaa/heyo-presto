from presto import Presto

presto = Presto()

display = presto.display

BLACK = display.create_pen(0, 0, 0)
GREY = display.create_pen(100, 100, 100)

display.set_pen(GREY)
display.clear()

display.set_pen(BLACK)
display.set_font("bitmap8")

y = [5,15,35,60,90,130,180]
for i in range(len(y)):
    display.text(f"{i+1}x Presto!", 10, y[i], scale=i+1)
presto.update()