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
        ).to_edge(LEFT)
        xaxis=axes.get_x_axis()
        xaxis.add(xaxis.get_tick(1))
        x0, x1 = -0.25, 2.0
        x2 = (x0+x1)/2
        def f(x: float) -> float: return (x-x1)*(x-x0) * 2
        graph = axes.plot(f, (-0.7, 2.45, 0.05), color=RED)
        dot_size = 1.2 * DEFAULT_DOT_RADIUS
        dot1 = Dot(point=axes.c2p(x0, 0), color=BLUE, z_index=1, radius=1.3*dot_size)
        dot2 = Dot(point=axes.c2p(x1, 0), color=BLUE, z_index=1, radius=1.3*dot_size)
        dot3 = Dot(point=axes.c2p(x2, f(x2)), color=GREEN, z_index=1, radius=1.3*dot_size)

        eq1 = MathTex(r'x^2+\frac ba x+\frac ca=0', font_size=60).to_edge(DR, buff=1.5)
        eq2 = MathTex(r'-\frac{b}{2a}').next_to(axes.c2p(x2, 0), UP)

        axes.add(dot1, dot2, dot3, eq2)

        self.add(axes, graph)
        self.add(eq1)

