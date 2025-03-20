import configparser

from manim import *
import numpy as np
import math
import random
import csv
import datetime
import sys
import scipy.interpolate

sys.path.append('../abracadabra/')
# noinspection PyUnresolvedReferences
import abracadabra as abra


class BMDraw:
    def __init__(self, m=600):
        self.m = m
        self.n = n = m * 4 + 1
        self.scale = ValueTracker(0.0)
        xrange = 1.0
        self.xvals = xvals = np.linspace(-xrange, xrange, n)
        self.dx = RIGHT * config.frame_x_radius
        self.dy = UP * 2
        self.yvals = yvals = np.zeros(n)
        self.a = a = math.sqrt(xvals[1] - xvals[0])
        b = a * math.sqrt(2)
        for i in range(2, n, 2):
            yvals[i] = yvals[i-2] + random.normalvariate(0, b)
        for i in range(1, n, 2):
            yvals[i] = (yvals[i-1] + yvals[i+1]) * 0.5 + random.normalvariate(0, b/2)
        yvals -= yvals[m*2]
        self.yvals0 = yvals.copy()
        self.prev_scale = 0.0
        self.fill_color = ManimColor([0.3657/2, 0.7526/2, 0.877/2])

    def rescale(self):
        yvals = self.yvals
        yvals1 = yvals.copy()
        yvals0 = self.yvals0
        m = self.m
        n = self.n
        b = self.a / math.sqrt(2)
        for i in range(0, n, 2):
            yvals0[i] = yvals[i] = yvals1[i // 2 + m] * math.sqrt(2)
        for i in range(1, n, 2):
            yvals0[i] = yvals[i] = (yvals[i - 1] + yvals[i + 1]) * 0.5
            yvals[i] += random.normalvariate(0, b)

    def get_obj(self, scale):
        yvals = self.yvals
        yvals0 = self.yvals0
        xvals = self.xvals
        n = self.n
        dx = self.dx
        dy = self.dy

        xs = math.exp(scale)
        ys = math.exp(scale / 2)

        xvals1 = xvals * xs
        p = scale * 4
        if p < 1:
            yvals1 = (yvals * p + yvals0 * (1 - p)) * ys
        else:
            yvals1 = yvals * ys

        pts = [xvals1[i] * dx + yvals1[i] * dy for i in range(n)]
        bottom = DOWN * config.frame_y_radius * 1.02
        right = RIGHT * config.frame_x_radius * 1.02
        pts = pts + [right + bottom, -right + bottom]

        path = Polygon(*pts, stroke_width=1, fill_opacity=1, fill_color=self.fill_color, stroke_color=WHITE)

        return path

    def __call__(self):
        scale = self.scale.get_value() - self.prev_scale
        xs = math.exp(scale)

        if xs > 2:
            self.rescale()
            self.prev_scale += math.log(2)
            scale -= math.log(2)
            xs = math.exp(scale)

        return self.get_obj(scale)


class BMDrawRects(BMDraw):
    def __init__(self, *args, **kwargs):
        BMDraw.__init__(self, *args, **kwargs)
        dx = self.dx
        dy = self.dy
        w = 0.01
        self.rect0 = rect0 = [w * dx[0], math.sqrt(w/2) * 4 * dy[1]]
        xs = 1.5
        self.rects = [[rect0[0] * xs, rect0[1] * math.sqrt(xs)]]

    def get_obj(self, scale):
        xs = math.exp(scale)
        ys = math.exp(scale/2)
        rects = self.rects
        dx = self.dx
        if xs * rects[-1][0] > 2 * config.frame_x_radius and ys * rects[-1][1] > 2 * config.frame_y_radius:
            rects.pop()

        rect0 = self.rect0
        if rects[0][0] * xs > dx[0] * 0.5:
            rects.insert(0, [rect0[0]/xs, rect0[1]/ys])

        rects_plot = [Rectangle(width=xs * rect[0], height=ys * rect[1], stroke_color=RED, stroke_width=4,
                                stroke_opacity=min(0.7, (rect[0] * xs/rect0[0] - 1) * 2)).set_z_index(1)
                      for rect in rects]

        return VGroup(*rects_plot)

    def rescale(self):
        for rect in self.rects:
            rect[0] *= 2
            rect[1] *= math.sqrt(2)


class BMZoom(Scene):
    t = 5
    bmDraw = BMDraw

    def construct(self):
        random.seed(3)

        f = self.bmDraw()
        path = always_redraw(f)
        self.add(path)
        self.play(f.scale.animate.set_value(self.t), run_time=self.t, rate_func=linear)

        self.wait(0.5)


class Weierstrass(Scene):
    def __init__(self, *args, **kwargs):
#        config.background_color = GREY
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        xlen = config.frame_x_radius
        ylen = config.frame_y_radius
        a = 0.5
        b = 4
        xrange = 2.0
        ymax = 1/(1-a)
        ymin = -ymax * 1.15
        xvals = np.linspace(-xrange, xrange, 1000)
        y = np.zeros(len(xvals))
        fill_color = ManimColor([0.3657/2, 0.7526/2, 0.877/2])

        ax = Axes(x_range=[-xrange, xrange], y_range=[ymin, ymax], z_index=2, x_length=xlen, y_length=ylen)
        box = SurroundingRectangle(ax, fill_color=BLACK, fill_opacity=0.6, stroke_opacity=0, corner_radius=0.2)
        VGroup(ax, box).to_edge(DOWN, buff=0.05)

        eq = MathTex(r'f(x)=\sum_{n=0}^\infty 2^{-n}\cos(4^n\pi x)', font_size=32, stroke_width=0.8)[0]\
            .set_z_index(3).next_to(ax.get_bottom(), UP, buff=0.05)

        line = ax.plot_line_graph(xvals, y, line_color=WHITE, add_vertex_dots=False, stroke_width=1).set_z_index(2)
        pts = ax.coords_to_point(list(zip(xvals, y)) + [(xrange, ymin), (-xrange, ymin)])
        poly = Polygon(*pts, stroke_opacity=0, fill_opacity=1, fill_color=fill_color).set_z_index(1)
        graph = VGroup(line, poly)
        self.add(box, graph, eq)
        self.wait(1)
        x = xvals * PI
        c = 1.
        for i in range(15):
            y += np.cos(x) * c
            line = ax.plot_line_graph(xvals, y, line_color=WHITE, add_vertex_dots=False, stroke_width=1).set_z_index(2)
            pts = ax.coords_to_point(list(zip(xvals, y)) + [(xrange, ymin), (-xrange, ymin)])
            poly = Polygon(*pts, stroke_opacity=0, fill_opacity=1, fill_color=fill_color).set_z_index(1)
            graph1 = VGroup(line, poly)
            self.play(ReplacementTransform(graph, graph1), run_time=7/(i+14), rate_func=linear)
            x *= b
            c *= a
            graph = graph1

        self.wait(0.5)


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        Weierstrass().render()



class BMZoomRects(BMZoom):
    bmDraw = BMDrawRects