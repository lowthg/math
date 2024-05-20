"""
Attempt to recreate mathologer video
"""

from manim import *
import numpy as np


class Quadratic(Scene):
    def construct(self):
        axes = Axes(
            #    [start,end,step]
            x_range=[-2, 2.7, 10],
            y_range=[-3, 3, 10],
            # Size of each axis
            x_length=6.3,
            y_length=7.5,
            # axis_config: the settings you make here
            # will apply to both axis, you have to use the
            # NumberLine options
            axis_config={"include_numbers": False},
            # While axis_config applies to both axis,
            # x_axis_config and y_axis_config only apply
            # to their respective axis.
            x_axis_config={
                "color": GREY,
                "include_tip": True,
                "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
            },
            y_axis_config={
                "color": GREY,
                "include_tip": True,
                "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
            },
        ).to_edge(LEFT, buff=-0.1)
        xaxis=axes.get_x_axis()
        x0, x1 = -0.25, 2.0
        def f(x: float) -> float: return (x-x1)*(x-x0) * 2
        x2 = (x0+x1)/2
        y2 = f(x2)
        tick: Line = xaxis.get_tick(x2)
        xaxis.add(tick)
        graph = axes.plot(f, (-0.7, 2.45, 0.05), color=RED)
        dot_size = 1.2 * DEFAULT_DOT_RADIUS
        dot1 = Dot(point=axes.c2p(x0, 0), color=BLUE, z_index=1, radius=1.3*dot_size)
        dot2 = Dot(point=axes.c2p(x1, 0), color=BLUE, z_index=1, radius=1.3*dot_size)
        dot3 = Dot(point=axes.c2p(x2, y2), color=GREEN, z_index=1, radius=1.3*dot_size)

        eq1 = MathTex(r'x^2+\frac ba x+\frac ca=0', font_size=60).to_edge(DR).shift(UP)
        eq2 = MathTex(r'-\frac{b}{2a}').next_to(axes.c2p(x2, 0), UP)
        eq3 = MathTex(r'\left(x-\frac{b}{2a}\right)^2+\frac ba\left(x-\frac{b}{2a}\right)+\frac ca=0',
                      font_size=60)#.to_edge(DR).shift(UP)
        eq3.shift(eq1[0][11].get_center() - eq3[0][25].get_center()) # align equals sign

        axes.add(dot1, dot2, dot3, eq2)

        self.add(axes, graph, eq1)
#        self.add(index_labels(eq1[0]))
#        self.add(index_labels(eq3.copy().next_to(eq1, UP).shift(LEFT*4)))
        self.wait(1)
        self.play(graph.animate.move_to(axes.c2p(0, 0)),
                  tick.animate.set_opacity(0),
                  dot1.animate.move_to(axes.c2p(x0-x2, 0)),
                  dot2.animate.move_to(axes.c2p(x1-x2, 0)),
                  dot3.animate.move_to(axes.c2p(0, y2)),
                  Transform(eq1[0][0], eq3[0][1]),
                  Transform(eq1[0][1], eq3[0][8]),
                  Transform(eq1[0][2], eq3[0][9]),
                  Transform(eq1[0][3:6], eq3[0][10:13]),
                  Transform(eq1[0][6], eq3[0][14]),
                  Transform(eq1[0][7:13], eq3[0][21:27]),
                  FadeIn(eq3[0][0], eq3[0][7], eq3[0][13], eq3[0][20]),
                  Transform(eq2[0][0:5], eq3[0][2:7]),
                  Transform(eq2.copy()[0][0:5], eq3[0][15:20]),
                  duration=1.5
                  )
        self.wait(0.5)




if __name__ == "__main__":
    Quadratic().construct()