from algan import *

circle = Circle()
square = Square()
square.rotate(-3 * TAU / 8)
circle.set(border_color=PINK, border_opacity=0.5)

square.spawn()
square.become(circle)

render_to_file()
