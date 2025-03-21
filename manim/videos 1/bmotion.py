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
        xvals = np.linspace(-xrange, xrange, 2000)
        y = np.zeros(len(xvals))
        fill_color = ManimColor([0.3657/2, 0.7526/2, 0.877/2])

        ax = Axes(x_range=[-xrange, xrange], y_range=[ymin, ymax], z_index=2, x_length=xlen, y_length=ylen)
        box = SurroundingRectangle(ax, fill_color=BLACK, fill_opacity=0.6, stroke_opacity=0, corner_radius=0.2)
        VGroup(ax, box).to_edge(DOWN, buff=0.05)

        eq = MathTex(r'f(x)=\sum_{n=0}^\infty 2^{-n}\cos(4^n\pi x)', font_size=32*2, stroke_width=0.8)[0]\
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
            self.play(ReplacementTransform(graph, graph1), run_time=7/(i+14) * 4, rate_func=linear)
            x *= b
            c *= a
            graph = graph1

        self.wait(0.5)

def bmcovs(times, H):
    n = len(times)
    cov = np.ndarray(shape=(n, n))
    for i in range(0, n):
        t = times[i]
        cov[i, i] = math.pow(t, H * 2)
        for j in range(0, i):
            dt = abs(t - times[j])
            cov[i, j] = cov[j, i] = (cov[i, i] + cov[j, j] - math.pow(dt, H * 2))/2
    return cov

def bmpath(times, H, seed):
    np.random.seed(seed)
    npts = len(times)
    mean = np.zeros(shape=(npts,))
    cov = bmcovs(times, H)
    return np.random.multivariate_normal(mean, cov)


def bmpath2(times, H, rands):
    if H >= 0.99999:
        return times * rands[0]
    cov = bmcovs(times, H)
    U = gs(cov)
    return np.matmul(U, rands)



def gs(M):
    """
    return U with M = U U^T
    """
    n = len(M)
    U = M.copy()
    for i in range(n):
        s = U[i, i]
#        U[i+1:] -= np.matmul(U[i], np.transpose(U[i+1:, i]))/s
        for j in range(i + 1, n):
            U[j] -= U[i] * (U[j, i]/s)
        U[i] /= math.sqrt(s)

    return np.transpose(U)


class FractionalBM(Scene):
    def construct(self):
        xlen = config.frame_x_radius * 1.8
        ylen = config.frame_y_radius * 1.8
        xmax = 1.0
        ymax = 2
        ymin = -1.3
        m = 10
        n = 2**m + 1
        xvals = np.linspace(0, xmax, n)

        ax = Axes(x_range=[0, 1], y_range=[ymin, ymax], z_index=2, x_length=xlen, y_length=ylen)
        box = SurroundingRectangle(ax, fill_color=BLACK, fill_opacity=0.6, stroke_opacity=0, corner_radius=0.2)
        diag = ax.coords_to_point(xmax, ymax) - ax.coords_to_point(0, ymin)
        edge = Rectangle(width=diag[0], height=diag[1], fill_opacity=0, stroke_opacity=1, stroke_width=2, stroke_color=YELLOW).set_z_index(10)

        eq = MathTex(r'H = 0.51').next_to(ax.get_bottom(), UP, buff=0.1)
        pt = eq[0][0].get_center()
#        VGroup(ax, box).to_edge(DOWN, buff=0.05)

        xvals2 = np.zeros(n-1)
        indices = [0] * (n-1)

        j = 0
        for r in range(m+1):
            step = 2**(m-r)
            for i in range(step, n, step * 2):
                xvals2[j] = xvals[i]
                indices[j] = i
                j += 1

        np.random.seed(1)
        rands = np.random.normal(size=n-1)

        self.add(box, edge)

        h_value = ValueTracker(0.002)

        def f():
            h = h_value.get_value()
            yvals2 = bmpath2(xvals2, h, rands)
            yvals = np.zeros(n)
            for i in range(n-1):
                yvals[indices[i]] = yvals2[i]
            plot = ax.plot_line_graph(xvals, yvals, add_vertex_dots=False, stroke_width=2, line_color=BLUE).set_z_index(1)
            eq = MathTex(r'H={:.2f}'.format(h))[0].set_z_index(15)
            eq.next_to(pt, ORIGIN, submobject_to_align=eq[0])
            return VGroup(plot, eq)

        path = always_redraw(f)

        self.add(path)
        self.play(h_value.animate.set_value(0.5), run_time=4)
        self.play(h_value.animate.set_value(1), run_time=4)

        self.wait(0.5)





if __name__ == "__main__":
    times = np.array([1.0, 0.5, 0.25, 0.75, 0.125, 0.375, 0.625, 0.875])
    path = bmpath2(times, 0.4, 3)
    print(path)
#    C = bmcovs(times, 0.4)
#    print(C)
#    M = gs(C)
#    print(M)
#    print(np.matmul(M, np.transpose(M)))
#    with tempconfig({"quality": "low_quality", "preview": True}):
#        FractionalBM().render()



class BMZoomRects(BMZoom):
    bmDraw = BMDrawRects