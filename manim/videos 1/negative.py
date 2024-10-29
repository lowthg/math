from manim import *
import numpy as np
import math
import random
import csv
import datetime
import sys

sys.path.append('../abracadabra/')
# noinspection PyUnresolvedReferences
import abracadabra as abra

class RelFreq(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = WHITE
        MathTex.set_default(color=BLACK, stroke_width=1.5, font_size=DEFAULT_FONT_SIZE * 1.08)
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        eq1 = MathTex(r'{\rm Number\ of\ trials} = N')[0]
        eq2 = MathTex(r'{\rm Number\ of\ successes} = M')[0].next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'{\rm Relative\ frequency} = M/N\ge0')[0].next_to(eq2, DOWN).align_to(eq1, LEFT)
        VGroup(eq1, eq2, eq3).to_corner(DR)

        self.wait(0.5)
        self.play(FadeIn(eq1), run_time=1)
        self.play(FadeIn(eq2), run_time=1)
        self.play(FadeIn(eq3[:-2]), run_time=1)
        self.play(FadeIn(eq3[-2:]), run_time=1)
        self.wait(0.5)


class ParticlePaths(Scene):
    bgcolor = GREY

    def __init__(self, *args, **kwargs):
        config.background_color = self.bgcolor
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        scale = 6
        end = ORIGIN + RIGHT * 5
        start = end + LEFT * scale
        radius = 0.5
        dot_rad = DEFAULT_DOT_RADIUS
        end_dot = Dot(color=BLACK, radius=radius, z_index=4).move_to(end)

        np.random.seed(1)

        nsteps = 100
        vol = 2 / math.sqrt(nsteps)
        xvals = np.zeros(nsteps + 1)
        yvals = np.zeros(nsteps + 1)
        times = np.linspace(0, 1, nsteps + 1)

        dot = Dot(color=PURE_BLUE, z_index=3, radius=dot_rad).move_to(start)
        start_dot = dot.copy().set_color(ManimColor(WHITE.to_rgb() * 0.3)).set_z_index(2)
        path_col = BLUE

        def update_dot(dot):
            dot.move_to(crv.get_end())

        dot.add_updater(update_dot)
        self.add(dot, end_dot, start_dot)

        for _ in range(20):
            rands = np.random.normal(0, 1, nsteps*2)
            for i in range(nsteps):
                xvals[i+1] = xvals[i] + rands[i*2] * vol
                yvals[i+1] = yvals[i] + rands[i*2+1] * vol
            xvals -= times * (xvals[-1] - scale)
            yvals -= times * yvals[-1]
            points = [start + RIGHT * xvals[i] + UP * yvals[i] for i in range(nsteps+1)]
            for i in range(1, nsteps+1):
                if np.linalg.norm(points[i] - end) < radius - dot_rad:
                    break
            crv = VMobject(color=path_col, z_index=1).set_points_as_corners(points[:i+1])

            self.play(Create(crv, rate_func=linear), run_time=3)
            crv.set_z_index(1)
            self.play(crv.animate.set_color(ManimColor(path_col.to_rgb() * 0.5 + self.bgcolor.to_rgb()*0.5)),
                      run_time=0.5)

        self.wait(0.5)


class EMField(ThreeDScene):
    def __init__(self, *args, **kwargs):
        config.background_color = BLUE
        ThreeDScene.__init__(self, *args, *kwargs)

    def construct(self):
        arrows = VGroup(Line(start=ORIGIN, end=RIGHT, buff=0, color=RED).add_tip(),
                        Line(start=ORIGIN, end=UP, buff=0, color=GREEN).add_tip(),
                        Line(start=ORIGIN, end=OUT, buff=0, color=BLUE).add_tip())


        dy = 1

        n = 120
        x_vals = np.linspace(-13*PI, 3*PI, n)
        dx = (x_vals[-1] - x_vals[0]) / (n - 1)
        rdir = RIGHT /(x_vals[-1]+dx/2) * 9
        x_axis = Line(rdir * (x_vals[0]-dx/2), rdir * (x_vals[-1] + dx/2))
        Ecol = BLUE
        Bcol = RED

        rectE = Rectangle(width=dx * 0.8 * rdir[0], height=1, fill_color=Ecol, fill_opacity=1, stroke_opacity=0).shift(UP/2).rotate(PI/2,RIGHT, ORIGIN)
        rectB = Rectangle(width=dx * 0.8 * rdir[0], height=1, fill_color=Bcol, fill_opacity=1, stroke_opacity=0).shift(UP/2)
        txtE = MathTex(r'\bf E', color=Ecol, stroke_color=WHITE, stroke_width=1).rotate(PI/2, RIGHT).next_to(OUT * 1, OUT).set_z_index(300)
        txtB = MathTex(r'\bf B', color=Bcol, stroke_color=WHITE, stroke_width=1).next_to(DOWN * 1, DOWN).set_z_index(300)

        for i in range(n):
            if x_vals[i] > 0:
                break
        ilabel = i
        ipolar = ilabel - 5
        p = RIGHT * x_vals[ipolar]

        field = VGroup(VGroup(*[rectE.copy().shift(RIGHT*x_vals[i] + UP/2).set_z_index(i+2) for i in range(n)]),
                       VGroup(*[rectB.copy().shift(RIGHT*x_vals[i] + UP/2).set_z_index(i+2) for i in range(n)]), txtE, txtB,
                       VGroup(Arrow(p, p + OUT * 2, color=BLUE, buff=0, z_index=ipolar+2), Arrow(p, p + IN * 2, color=BLUE, buff=0)).set_opacity(0))
        angles = np.zeros(n)

        self.set_camera_orientation(phi=80*DEGREES, theta=-20*DEGREES)
        self.add(x_axis)

        c = 4
        starttime = 0.0
        endtime = 20 * PI / c
        starttime = 13 * PI / c
        endtime = 32 * PI / c

        starttime = 0.0
        endtime = 33.0
        tpolar = [14.9]
        rottime = 23
        fieldtime = 12


        time = ValueTracker(starttime)

        def wavefun(x):
            if x + fieldtime*c > 0:
                return 0.0, 0.0
            return math.sin(x) * (1.0 - math.exp(-((x+fieldtime*c)/PI)**2)), -max(min(0.0, ((x+rottime*c)/PI) * 15), -90) * DEGREES

        def f():
            t = time.get_value()
            for i in range(n):
                x = x_vals[i]
                y, angle = dy * wavefun(x - c * t)
                if abs(y) < 0.001:
                    y = 0.001
                p = rdir * x
                field[0][i].rotate(-angles[i], RIGHT, p)
                field[1][i].rotate(-angles[i], RIGHT, p)
                field[0][i].stretch_to_fit_depth(y).move_to(p).shift(OUT*y/2)
                field[1][i].stretch_to_fit_height(y).move_to(p).shift(DOWN*y/2)
                field[0][i].rotate(angle, RIGHT, p)
                field[1][i].rotate(angle, RIGHT, p)
                if t > tpolar[0]:
                    op = min((t - tpolar[0]) * 1, 1)
                    if op == 1:
                        tpolar[0] = 1e10
                    field[4].set_opacity(op)
                if i == ilabel:
                    field[2].rotate(angle - angles[i], RIGHT, p)
                    field[3].rotate(angle - angles[i], RIGHT, p)
                if i == ipolar:
                    field[4].rotate(angle - angles[i], RIGHT, p)
                angles[i] = angle
            return field

        field = always_redraw(f)
        self.add(field)
        self.wait(0.5)
        self.play(time.animate(rate_func=linear).set_value(endtime), run_time=endtime - starttime)

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "fps": 15, "preview": True}):
        EMField().render()