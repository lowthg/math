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
    multi=False
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
        if self.multi and xs * rects[-1][0] > 2 * config.frame_x_radius and ys * rects[-1][1] > 2 * config.frame_y_radius:
            rects.pop()

        rect0 = self.rect0
        if self.multi and rects[0][0] * xs > dx[0] * 0.5:
            rects.insert(0, [rect0[0]/xs, rect0[1]/ys])

        rects_plot = [Rectangle(width=xs * rect[0], height=ys * rect[1], stroke_color=RED_B, stroke_width=4,
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

class BMZoomRects(BMZoom):
    bmDraw = BMDrawRects

class Circle1(Scene):
    fill_color=GREY
    def __init__(self, *args, **kwargs):
        if config.transparent:
            config.background_color=self.fill_color
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        circ1 = Circle(radius=1, stroke_width=6, stroke_color=BLUE, fill_opacity=0, fill_color=self.fill_color).set_z_index(1).rotate(90*DEGREES)
        circ2 = circ1.copy().set_stroke(opacity=0).set_fill(opacity=0.6).set_z_index(0)
        self.wait(0.5)
        self.play(Create(circ1), rate_func=linear, run_time=0.6)
        self.play(FadeIn(circ2), run_time=0.5, rate_func=linear)
        self.wait(0.5)

class Ellipse1(Circle1):
    fill_color = ORANGE

    def construct(self):
        circ1 = Ellipse(width=2.4, height=1.6, stroke_color=YELLOW, stroke_width=6, fill_opacity=0, fill_color=self.fill_color).set_z_index(1).rotate(30*DEGREES)
        circ2 = circ1.copy().set_stroke(opacity=0).set_fill(opacity=0.6).set_z_index(0)
        self.wait(0.5)
        self.play(Create(circ1), rate_func=linear, run_time=0.6)
        self.play(FadeIn(circ2), run_time=0.5, rate_func=linear)
        self.wait(0.5)

class Conic(ThreeDScene):
    def __init__(self, *args, **kwargs):
        config.background_color=GREY
        ThreeDScene.__init__(self, *args, **kwargs)

    def construct(self):
        cone_height = 1.5
        cone_slope = 0.7
        plane_offset = 0.3
        plane_slope = 0.2
        res = 10

        base_radius = cone_slope * cone_height
        surf_op = 0.6
        cone_op=0.5
        line_op=0.5
        cone1 = Surface(lambda u, v: OUT * u + (RIGHT * math.cos(v) + UP * math.sin(v)) * cone_slope * u,
                        u_range=[-cone_height, cone_height], v_range=[0, TAU], resolution=[10*res, 10*res], fill_color=BLUE,
                        fill_opacity=cone_op, stroke_opacity=0, checkerboard_colors=False)
        plane = Surface(lambda u, v: OUT * u + RIGHT * (plane_offset + plane_slope * u) + UP * v,
                        u_range=[-cone_height, cone_height], v_range=[-cone_height, cone_height],
                        resolution = [10*res, 10*res], fill_color=GREY, fill_opacity=surf_op, stroke_opacity=0,
                        stroke_color=GREY, stroke_width=1,
                        checkerboard_colors=False)
        dot = Dot3D(color=RED, radius=0.3)

        dir = 1

        def pf(t):
            """
            v = t
            cs^2 * u^2 = (po + ps*u)^2 + v^2
            (cs^2 - ps^2)*u^2 - 2*po*ps*u - po^2 - v^2 = 0
            au^2 - 2bu - c=0
            u = (b +- sqrt(b^2 + ac))/a

            bound: u = ch
            """
            a = cone_slope**2 - plane_slope**2
            b = plane_slope * plane_offset
            c = plane_offset**2 + t**2
            u = (b + dir * math.sqrt(b**2 + a*c))/a
            return UP * t * dir + OUT * u + RIGHT * (plane_offset + plane_slope * u)

        t0 = math.sqrt(base_radius**2 - (plane_offset + plane_slope*cone_height)**2)
        t1 = math.sqrt(base_radius**2 - (plane_offset - plane_slope*cone_height)**2)
        t0vec = np.linspace(-t0, t0, 100)
        t1vec = np.linspace(-t1, t1, 100)
        kwargs = {'color': GREY, 'thickness': 0.02, 'fill_opacity': line_op, 'stroke_opacity': line_op, 'stroke_color': GREY, 'resolution': 10}
        curve1 = VGroup(*[Line3D(pf(t0vec[i-1]), pf(t0vec[i]), **kwargs) for i in range(1, 100)])
        dir=-1
        curve2 = VGroup(*[Line3D(pf(t1vec[i-1]), pf(t1vec[i]), **kwargs) for i in range(1, 100)])

        self.set_camera_orientation(phi=90*DEGREES, theta=35*DEGREES)
        self.add(cone1)
        self.add(plane)

        dot = Dot3D(radius=0.08, color=RED, stroke_opacity=1, fill_opacity=1, fill_color=RED, stroke_color=RED)

        tval = ValueTracker(-t0)
        dir = 0

        def g():
            t = tval.get_value()
            if dir == 1:
                curve = curve1
                tvec = t0vec
            elif dir == -1:
                curve = curve2
                tvec = t1vec
            else:
                return VGroup(curve1.copy(), curve2.copy())

            for i in range(1, len(tvec)):
                if tvec[i] + tvec[i-1] < t * 2:
                    curve[i-1].set_stroke(color=RED).set_fill(color=RED).set_opacity(1)

            return VGroup(curve1.copy(), curve2.copy(), dot.copy().move_to(pf(t)))

        move = always_redraw(g)
        self.add(move)
        self.wait(0.5)
        dir = 1
        self.play(tval.animate.set_value(t0), run_time=t0*0.7, rate_func=linear)
        move[-1].set_opacity(0)
        self.wait(0.3)
        dir = -1
        tval.set_value(-t1)
        self.play(tval.animate.set_value(t1), run_time=t1*0.7, rate_func=linear)
        move[-1].set_opacity(0)
        dir=0
        self.wait(0.3)
        self.begin_ambient_camera_rotation(rate=PI*1.2)

        self.wait(4)

class Triangle1(Circle1):
    fill_color = BLUE
    def construct(self):
        p0 = ORIGIN
        p1 = p0 + RIGHT * 2 + UP * 1.9
        p2 = p0 + RIGHT * 3 + DOWN * 0.6
        circ1 = Polygon(p0, p1, p2, stroke_color=GREEN, stroke_width=6, fill_color=self.fill_color, fill_opacity=0).set_z_index(1)
        circ2 = circ1.copy().set_stroke(opacity=0).set_fill(opacity=0.6).set_z_index(0)
        self.wait(0.5)
        self.play(Create(circ1), rate_func=linear, run_time=0.6)
        self.play(FadeIn(circ2), run_time=0.5, rate_func=linear)
        self.wait(0.5)
        dots = [Dot(p, radius=0.1, color=RED).set_z_index(2) for p in [p0, p1, p2]]
        self.play(FadeIn(*dots), run_time=1)
        self.wait()

class Polygon1(Circle1):
    fill_color = ORANGE
    def construct(self):
        circ1 = RegularPolygon(5, radius=1.4, stroke_color=YELLOW, stroke_width=6, fill_color=self.fill_color, fill_opacity=0).set_z_index(1)
        circ2 = circ1.copy().set_stroke(opacity=0).set_fill(opacity=0.6).set_z_index(0)
        self.wait(0.5)
        self.play(Create(circ1), rate_func=linear, run_time=0.6)
        self.play(FadeIn(circ2), run_time=0.5, rate_func=linear)
        self.wait(0.5)

class Poly1(Circle1):
    fill_color=ORANGE
    def construct(self):
        x_range = [0, 2.3]
        def f(x):
            return x**3 - 3*x**2 + 2*x + 1
#            return x*(x-1)*(x-2) + 1/2
        ax = Axes(x_range=[0, x_range[1]*1.1], y_range=[0, f(x_range[1])*1.1], x_length=5, y_length=3,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  ).set_z_index(2)

        eq = MathTex('y=x^3-3x^2+2x+1', font_size=40, stroke_width=1.5)[0].next_to(ax.get_bottom(), UP, buff=0.35).set_z_index(2)
        self.add(ax, eq)
        self.wait(0.5)

        crv = ax.plot(f, x_range=x_range, color=BLUE, stroke_width=6).set_z_index(1)
        area = ax.get_area(crv, x_range=x_range, color=self.fill_color, opacity=0.4)

        self.play(Create(crv), run_time=1, rate_func=linear)
        self.play(FadeIn(area), run_time=1)
        self.wait()

class SmoothZoom(Scene):
    def construct(self):
        x_range = [-1., 1.]
        y_range=[-1,1]
        def f(x):
            return x * 0.4 - 0.3 * (np.cos((x+0.1)*5)-np.cos(0.5))

        ax = Axes(x_range=x_range, y_range=y_range, x_length=config.frame_x_radius, y_length=config.frame_y_radius)
        dl = ax.coords_to_point(x_range[0], y_range[0])
        ur = ax.coords_to_point(x_range[1], y_range[1])
        diag = ur - dl
        edge = Rectangle(width=diag[0], height=diag[1], stroke_width=4, stroke_color=WHITE, fill_color=BLACK, fill_opacity=0).set_z_index(10)
        box = edge.copy().set_stroke(opacity=0).set_fill(opacity=0.6).set_z_index(0)

        xvals = np.linspace(*x_range, 101)
        yvals = f(xvals)

        gp = VGroup(edge, box)
        shift = -gp.get_center()
        gp.to_edge(DOWN, buff=0.05)
        shift += gp.get_center()
        ax.shift(shift)
        crv = ax.plot_line_graph(xvals, yvals, stroke_width=4, line_color=BLUE,
                                 add_vertex_dots=False).set_z_index(5)

        self.add(edge, box)
        self.wait(0.5)
        self.play(Create(crv), run_time=1, rate_func=linear)
        self.wait(0.2)
        a0 = 0.3
        a = a0
#        x = np.linspace(-a, a, 50)
#        y = f(x)
        s_val = ValueTracker(1.0)

        dot = Dot(radius=0.1, color=RED).move_to(shift).set_z_index(7)

        def f():
            s = s_val.get_value()
            crv = ax.plot_line_graph(xvals * s, yvals * s, stroke_width=4, line_color=GREY,
                                     add_vertex_dots=False).set_z_index(4)
            op = min((a*s - 0.3) * 5, 1.) if a < 0.2 else 1
            rect = Rectangle(width=a*s*diag[0], height = a*s*diag[1], stroke_width=4, stroke_color=RED,
                             stroke_opacity=op).set_z_index(7).move_to(shift)
            return VGroup(crv, rect)

        curveZoom = always_redraw(f)
        self.play(FadeIn(curveZoom, dot), run_time=0.5)
        self.wait(0.5)
        self.play(s_val.animate.set_value(1/a), run_time=1.5, rate_func=rate_functions.ease_in_cubic)
        self.wait(0.2)
        a *= a0
        self.play(s_val.animate.set_value(1/a), run_time=1.5, rate_func=linear)
        self.wait(0.2)
        a *= a0
        self.play(s_val.animate.set_value(1/a), run_time=1.5, rate_func=linear)
        self.wait()

class SmoothStock1(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color=GREY
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        tmax = 10
        ymax = 10
        ax = Axes(x_range=[0, tmax*1.1], y_range=[0, ymax], x_length=5, y_length=3,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  ).set_z_index(200)
        box = SurroundingRectangle(ax, corner_radius=0.2, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0,
                                   buff=0.15)
        eq1 = MathTex('t')[0].next_to(ax.x_axis.get_right(), UL).set_z_index(2)
        eq2 = MathTex('S_t')[0].next_to(ax.y_axis.get_top(), DR, buff=0.2).set_z_index(2)

        self.add(box, ax, eq1, eq2)
        n = 100
        x = np.linspace(0, tmax, n)
        xarr = [0, 1, 3, 5, 7.5, 10]
        sprice = scipy.interpolate.CubicHermiteSpline(
            xarr,
            [y-0.5 for y in [4, 3, 7, 4, 9, 5]],
            [-1, 0, 0, 0, 0, -2]
        )
        y = sprice(x)
        pts = ax.coords_to_point([(t, sprice(t)) for t in xarr])
        plot = ax.plot_line_graph(x, y, stroke_width=5, line_color=WHITE, add_vertex_dots=False).set_z_index(1)

        i0 = j0 = i1 = j1 = 0
        for i in range(len(x)):
            if i0 == 0 and x[i] > 1:
                i0 = i
            if j0 == 0 and x[i] > 3:
                j0 = i
            if i1 == 0 and x[i] > 5:
                i1 = i
            if j1 == 0 and x[i] > 7.5:
                j1 = i


        self.wait(0.5)
        self.play(Create(plot), rate_func=linear, run_time=1.5)
        self.wait(0.5)

        tval = ValueTracker(0.0)
        show0 = show1 = show2 = show3 = show4 = False
        green = GREEN_E
        red = RED

        def f():
            t = tval.get_value()
            st = sprice(t)
            dot = Dot(ax.coords_to_point(t, st), radius=0.1).set_z_index(50)
            res = []
            color = red

            if show0:
                k = 0
                for i in range(0, i0 + 1):
                    k = i
                    if x[i] >= t:
                        break
                plot0 = ax.plot_line_graph(x[0:k + 1], y[0:k + 1], stroke_width=6, line_color=RED_E,
                                           add_vertex_dots=False).set_z_index(2)
                res.append(*plot0)

            if show1:
                k = i0
                for i in range(i0, j0 + 1):
                    k = i
                    if x[i] >= t:
                        break
                plot1 = ax.plot_line_graph(x[i0:k+1], y[i0:k+1], stroke_width=6, line_color=green, add_vertex_dots=False).set_z_index(2)
                res.append(*plot1)
                color = green

            if show2:
                k = j0
                for i in range(j0, i1 + 1):
                    k = i
                    if x[i] >= t:
                        break
                plot2 = ax.plot_line_graph(x[j0:k+1], y[j0:k+1], stroke_width=6, line_color=red, add_vertex_dots=False).set_z_index(2)
                res.append(*plot2)
                color = red

            if show3:
                k = i1
                for i in range(i1, j1 + 1):
                    k = i
                    if x[i] >= t:
                        break
                plot3 = ax.plot_line_graph(x[i1:k+1], y[i1:k+1], stroke_width=6, line_color=green, add_vertex_dots=False).set_z_index(2)
                res.append(*plot3)
                color = green

            if show4:
                k = j1
                for i in range(j1, n):
                    k = i
                    if x[i] >= t:
                        break
                dot.set_opacity(math.pow(min((x[-1] - t)*2, 1), 0.3))
                plot4 = ax.plot_line_graph(x[j1:k+1], y[j1:k+1], stroke_width=6, line_color=red, add_vertex_dots=False).set_z_index(2)
                res.append(*plot4)
                color = red


            return VGroup(*res, dot.set_color(color))

        buy = Tex(r'\bf buy', color=green, font_size=35)[0]
        sell = Tex(r'\bf sell', color=red, font_size=35)[0]
        profit = Tex(r'\bf profit!', font_size=30, color=WHITE)[0].set_z_index(200)
        move = always_redraw(f)
        self.add(move)

        show0 = True
        self.play(tval.animate.set_value(x[i0]), run_time=0.5, rate_func=linear)
        dot1 = move[-1].copy().set_color(green).move_to(pts[1]).set_z_index(60)
        self.play(FadeIn(dot1, buy.copy().next_to(pts[1], DOWN, buff=0.1)), run_time=0.2)

        show1 = True
        self.play(tval.animate.set_value(x[j0]), run_time=0.8, rate_func=linear)
        pt = pts[1] * UP + pts[2] * RIGHT
        line1 = DashedLine(pts[1], pt + RIGHT*0.1, stroke_width=2)
        arr1 = Arrow(pt, pts[2], color=ManimColor(WHITE.to_rgb()*0.7), buff=0, stroke_width=4).set_z_index(100)
        dot2 = move[-1].copy().set_color(red).move_to(pts[2]).set_z_index(60)
        profit1 = profit.copy().move_to(pt * 0.6 + pts[2] * 0.4)
        self.play(FadeIn(dot2, sell.copy().next_to(pts[2], UP, buff=0.2)), run_time=0.2)

        show2 = True
        self.play(tval.animate.set_value(x[i1]), run_time=0.8, rate_func=linear)
        dot3 = move[-1].copy().set_color(green).move_to(pts[3]).set_z_index(60)
        self.play(FadeIn(dot3, buy.copy().next_to(pts[3], DOWN, buff=0.1)), run_time=0.2)

        show3 = True
        self.play(tval.animate.set_value(x[j1]), run_time=0.8, rate_func=linear)
        pt = pts[3] * UP + pts[4] * RIGHT
        line2 = DashedLine(pts[3], pt + RIGHT*0.1, stroke_width=2)
        arr2 = Arrow(pt, pts[4], color=ManimColor(WHITE.to_rgb()*0.7), buff=0, stroke_width=4).set_z_index(100)
        dot4 = move[-1].copy().set_color(red).move_to(pts[4]).set_z_index(60)
        profit2 = profit.copy().move_to(pt * 0.6 + pts[4] * 0.4)
        self.play(FadeIn(dot4, sell.copy().next_to(pts[4], UP, buff=0.2)), run_time=0.2)

        show4 = True
        self.play(tval.animate.set_value(x[-1]), run_time=0.5, rate_func=linear)
        self.play(FadeIn(line1, arr1, profit1, line2, arr2, profit2), run_time=29.5/30)
        self.wait(1.5/30)

class BMDefs(Scene):
    def construct(self):
        xlen = config.frame_x_radius * 1.05
        ylen = config.frame_y_radius
        ax = Axes(x_range=[0, 1.05], y_range=[-1, 1], x_length=xlen, y_length=ylen,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  ).set_z_index(2)
#        self.add(ax)
        eq1 = MathTex(r't')[0].next_to(ax.x_axis.get_right(), UL, buff=0.2)
        eq2 = MathTex(r'B_t')[0].next_to(ax.y_axis.get_top(), DR, buff=0.2)
        tarr = np.linspace(0.1, 0.95, 4)
        self.add(eq1, eq2)

        marks = [ax.x_axis.get_tick(t) for t in tarr]
        eq_marks = [MathTex(r't_{}'.format(i), font_size=40).next_to(marks[i], DOWN, buff=0.05) for i in range(4)]
        eq_dB = []
        self.wait(0.5)
        for i in range(len(tarr)):
            tmp = []
            if i > 0:
                pos = (marks[i-1].get_bottom() + marks[i].get_bottom()) * 0.5
                tmp.append(MathTex(r'B_{{t_{} }} - B_{{ t_{} }}'.format(i, i-1), font_size=38)
                           .next_to(pos, DOWN, buff=0.85))
                eq_dB += tmp
            self.play(FadeIn(marks[i], eq_marks[i], *tmp), run_time=1)

        self.wait()
        t0 = 0.6
        mark = ax.x_axis.get_tick(t0)
        eq_mark = MathTex(r't', font_size=40).next_to(mark, DOWN, buff=0.05)
        eq3 = MathTex(r'B_t\sim N(0, t)')[0].next_to(ax.get_bottom(), UP)
        self.play(FadeOut(*marks, *eq_marks, *eq_dB),
                  FadeIn(eq3[:3], mark, eq_mark),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeIn(eq3[3:5], eq3[6], eq3[8]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq3[5]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(eq3[7]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeOut(eq3, mark, eq_mark), run_time=0.5)
        self.wait()
        eq4 = MathTex(r'{\rm Var}(B_t){{=}}t').next_to(ax.get_bottom(), UP).shift(LEFT*1.2)
        eq5 = MathTex(r'{\rm Var}(B_{Nt}){{=}}Nt')
        eq6 = MathTex(r'{\rm Var}(B_{Nt}){{=}}N{\rm Var}(B_t)')
        eq7 = MathTex(r'{\rm std\,dev}(B_{Nt}){{=}}\sqrt{N}\,{\rm std\,dev}(B_t)')
        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1])
        eq6.next_to(eq4[1], ORIGIN, submobject_to_align=eq6[1])
        eq7.next_to(eq4[1], ORIGIN, submobject_to_align=eq7[1])
        self.play(FadeIn(eq4), run_time=0.6)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(eq4[0][:5] + eq4[0][5] + eq4[0][6] + eq4[1] + eq4[2][0],
                                                   eq5[0][:5] + eq5[0][6] + eq5[0][7] + eq5[1] + eq5[2][1]),
                              FadeIn(eq5[0][5], eq5[2][0]), lag_ratio=0.3),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq5[2][0], eq6[2][0]),
                  FadeOut(eq5[2][1]),
                  FadeIn(eq6[2][1:]),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq5[0][-5:] + eq5[1] + eq6[2][0],
                                       eq7[0][-5:] + eq7[1] + eq7[2][2]),
                  FadeOut(eq5[0][:-5] + eq6[2][1:]),
                  FadeIn(eq7[0][:-5] + eq7[2][3:] + eq7[2][:2]),
                  run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(eq7), run_time=0.5)

        self.wait()

class BMMorePaths(Scene):
    def construct(self):
        xlen = config.frame_x_radius * 1.05
        ylen = config.frame_y_radius
        random.seed(0)
        ax = Axes(x_range=[0, 1.05], y_range=[-1.5, 1.5], x_length=xlen, y_length=ylen,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  )
        self.add(ax)
        n = 1025
        tvals = np.linspace(0, 1, n)
        a = math.sqrt(tvals[1] - tvals[0])
        plots = []
        colors = [GREY, BLUE_A, GREEN_A, ORANGE, RED_A]
        for i in range(5):
            y = np.zeros(n)
            for j in range(1, n):
                y[j] = y[j-1] + random.normalvariate(0, a)
            plots.append(ax.plot_line_graph(tvals, y, line_color=colors[i], stroke_width=2, add_vertex_dots=False))

        self.wait()
        self.play(*[Create(p) for p in plots], run_time=4, rate_func=linear)
        self.wait()

def get_minmax(v, ileft, iright, jleft=None, jright=None):
    min_val = v[ileft]
    i0 = 0
    for i in range(ileft, iright + 1):
        if v[i] < min_val:
            min_val = v[i]
            i0 = i
    max_val = min_val
    k0 = i0 + 1 if jleft is None else jleft
    k1 = iright if jright is None else jright
    j0 = k0
    for i in range(k0, k1+1):
        if v[i] > max_val:
            max_val = v[i]
            j0 = i
    return i0, j0

class ImpossibleTrade(Scene):
    def construct(self):
        xlen = config.frame_x_radius * 1.05
        ylen = config.frame_y_radius
        random.seed(3)
        ax = Axes(x_range=[0, 1.05], y_range=[-1.5, 1.5], x_length=xlen, y_length=ylen)

        corners = ax.coords_to_point([(0, -1.5), (1, 1.5)])
        ax.shift(-(corners[0] + corners[1]) * 0.5)
        diag = corners[1] - corners[0]
        edge = Rectangle(width=diag[0], height=diag[1], stroke_color=WHITE, stroke_width=4).set_z_index(100)
        box = Rectangle(width=diag[0], height=diag[1], stroke_opacity=0, fill_opacity=0.7, fill_color=BLACK)
        draw = BMDraw(m=200)
        tvals = (draw.xvals + 1) * 0.5
        yvals = draw.yvals
        n = len(tvals)
        path = ax.plot_line_graph(tvals, yvals, line_color=BLUE, stroke_width=4, add_vertex_dots=False).set_z_index(2)
        self.add(box, path, edge)
        self.wait(0.5)
        trade_arr = []
        buy = True
        eq_buy = Tex(r'\bf buy', color=GREEN_E, font_size=35).set_z_index(1)
        eq_sell = Tex(r'\bf sell', color=RED, font_size=35).set_z_index(1)
        for i in range(35, 775, 10):
            if buy:
                trade_arr.append(eq_buy.copy().next_to(ax.coords_to_point(tvals[i], yvals[i]), DOWN, buff=0.2))
            else:
                trade_arr.append(eq_sell.copy().next_to(ax.coords_to_point(tvals[i], yvals[i]), UP, buff=0.2))
            buy = not buy
        ntrade = len(trade_arr)

        tval = ValueTracker(0.0)
        def f():
            t = tval.get_value()
            return VGroup(*trade_arr[:int(t * ntrade)])

        trades = always_redraw(f)
        self.add(trades)
        self.play(tval.animate.set_value(1.0), run_time=4, rate_func=linear)
        self.wait(0.2)
        self.play(FadeOut(trades), run_time=1)
        self.wait(0.2)
        i0, j0 = get_minmax(yvals, 100, 600)
        i1, j1 = get_minmax(-yvals, i0 + 10, i0+150)
        i2, j2 = get_minmax(-yvals, j1 + 10, j1+150, j1+160, j1+200)
        i3, j3 = get_minmax(-yvals, j2, j0-10, j0-30)
        i4, j4 = get_minmax(yvals, i1, j1-20, j1-17)
        i5, j5 = get_minmax(yvals, i2, j2)
        i6, j6 = get_minmax(yvals, i3, j3)
        print(i0, j0)
        print(i1, j1)
        print(i4, j4)
        print(i2, j2)
        lines = [DashedLine(ax.coords_to_point(tvals[i0], -1.5), ax.coords_to_point(tvals[i0], 1.5), color=WHITE)
                 .set_z_index(1),
                 DashedLine(ax.coords_to_point(tvals[j0], -1.5), ax.coords_to_point(tvals[j0], 1.5), color=WHITE)
                 .set_z_index(1)
                 ]
        op = 0.4
        p = [ax.coords_to_point(tvals[i1], -1.5), ax.coords_to_point(tvals[j1], 1.5)]
        range1 = Rectangle(width=(p[1] - p[0])[0], height=(p[1]-p[0])[1], stroke_opacity=0,
                           fill_opacity=op, fill_color=WHITE).move_to((p[0] + p[1])/2).set_z_index(1)
        p = [ax.coords_to_point(tvals[i2], -1.5), ax.coords_to_point(tvals[j2], 1.5)]
        range2 = Rectangle(width=(p[1] - p[0])[0], height=(p[1]-p[0])[1], stroke_opacity=0,
                           fill_opacity=op, fill_color=WHITE).move_to((p[0] + p[1])/2).set_z_index(1)
        p = [ax.coords_to_point(tvals[i3], -1.5), ax.coords_to_point(tvals[j3], 1.5)]
        range3 = Rectangle(width=(p[1] - p[0])[0], height=(p[1]-p[0])[1], stroke_opacity=0,
                           fill_opacity=op, fill_color=WHITE).move_to((p[0] + p[1])/2).set_z_index(1)
        p = [ax.coords_to_point(tvals[i4], -1.5), ax.coords_to_point(tvals[j4], 1.5)]
        range4 = Rectangle(width=(p[1] - p[0])[0], height=(p[1]-p[0])[1], stroke_opacity=0,
                           fill_opacity=op, fill_color=WHITE).move_to((p[0] + p[1])/2).set_z_index(1)
        p = [ax.coords_to_point(tvals[i5], -1.5), ax.coords_to_point(tvals[j5], 1.5)]
        range5 = Rectangle(width=(p[1] - p[0])[0], height=(p[1]-p[0])[1], stroke_opacity=0,
                           fill_opacity=op, fill_color=WHITE).move_to((p[0] + p[1])/2).set_z_index(1)
        p = [ax.coords_to_point(tvals[i6], -1.5), ax.coords_to_point(tvals[j6], 1.5)]
        range6 = Rectangle(width=(p[1] - p[0])[0], height=(p[1]-p[0])[1], stroke_opacity=0,
                           fill_opacity=op, fill_color=WHITE).move_to((p[0] + p[1])/2).set_z_index(1)
        self.play(FadeIn(*lines), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(range1, range2, range3), run_time=1)
        self.wait(0.2)
        for range0 in [range1, range2, range3]:
#            self.add(range0.copy().set_fill(opacity=0).set_stroke(opacity=op, color=WHITE, width=1))
            self.add(range0.copy().set_fill(color=GREY, opacity=op))
            range0.set_fill(opacity=op*0.8)
        self.play(ReplacementTransform(range1, range4),
                  ReplacementTransform(range2, range5),
                  ReplacementTransform(range3, range6),
                  run_time=0.8)
        self.wait()


class ExpBM(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color=GREY
        Scene.__init__(self, *args, **kwargs)
    def construct(self):
        fs = 80
        eq1 = MathTex(r'S_t{{=}}S_0+B_t', font_size=fs)
        eq2 = MathTex(r'S_t{{=}}S_0\exp(B_t)', font_size=fs)
        eq3 = MathTex(r'S_t{{=}}S_0\exp(\sigma B_t)', font_size=fs)
        eq4 = MathTex(r'S_t{{=}}S_0\exp(\sigma B_t + \mu t)', font_size=fs)
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq2[1])
        eq3.next_to(eq1[1], ORIGIN, submobject_to_align=eq3[1])
        eq4.next_to(eq1[1], ORIGIN, submobject_to_align=eq4[1])
        VGroup(eq1, eq2, eq3, eq4).set_z_index(1)
        op = 0.7
        box1 = SurroundingRectangle(eq1, corner_radius=0.1, stroke_opacity=0, fill_opacity=op, fill_color=BLACK)
        box2 = SurroundingRectangle(eq2, corner_radius=0.1, stroke_opacity=0, fill_opacity=op, fill_color=BLACK)
        box3 = SurroundingRectangle(eq3, corner_radius=0.1, stroke_opacity=0, fill_opacity=op, fill_color=BLACK)
        box4 = SurroundingRectangle(eq4, corner_radius=0.1, stroke_opacity=0, fill_opacity=op, fill_color=BLACK)
        self.add(eq1, box1)
        self.wait(0.5)
        self.play(LaggedStart(FadeOut(eq1[2][2]),
            ReplacementTransform(eq1[2][:2] + eq1[2][3:] + box1,
                                       eq2[2][:2] + eq2[2][6:8] + box2),
                  FadeIn(eq2[2][2:6], eq2[2][8:]), lag_ratio=0.2),
                  run_time=1.5)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(eq2[2][:6] + eq2[2][6:] + box2,
                                       eq3[2][:6] + eq3[2][7:] + box3),
                  FadeIn(eq3[2][6]), lag_ratio=0.2), run_time=1)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(eq3[2][:9] + eq3[2][9] + box3,
                                       eq4[2][:9] + eq4[2][12] + box4),
                  FadeIn(eq4[2][9:12]), lag_ratio=0.3),
                  run_time=1.6)
        self.wait()

class AbsDiff(Scene):
    def __init__(self, *args, **kwargs):
#        config.background_color=GREY
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        ymax = 1.05
        ymin = -0.2
        ax = Axes(x_range=[-1.05, 1.05], y_range=[-0.2, 1.05], x_length=config.frame_x_radius, y_length=config.frame_y_radius,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  ).set_z_index(2)
        box = SurroundingRectangle(ax, corner_radius=0.2, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0)
        eqx = MathTex(r'x', font_size=40).next_to(ax.x_axis.get_right(), UL, buff=0.2).set_z_index(2)
        eqy = MathTex(r'y', font_size=40).next_to(ax.y_axis.get_top(), DR, buff=0.2).set_z_index(2)

        self.add(box, ax, eqx, eqy)
        self.wait(0.2)
        xvals = [-1., 0., 1.]
        yvals = [1., 0., 1.]
        plot = ax.plot_line_graph(xvals, yvals, line_color=BLUE, stroke_width=6, add_vertex_dots=False).set_z_index(2)

        eq = MathTex(r'y=\lvert x\rvert').move_to(ax.coords_to_point(0.4, 0.7)).set_z_index(3)
        self.play(Create(plot), FadeIn(eq), run_time=1, rate_func=linear)
        dot = Dot(ax.coords_to_point(0, 0), radius=0.12, color=RED).set_z_index(4)
        self.wait(0.2)
        self.play(FadeIn(dot), run_time=0.5)
        self.wait(0.2)

        gval = ValueTracker(0.3)
        def f():
            g = gval.get_value()
            y0 = -0.5
            len = 1
            # x^2 + g^2 x^2 = len^2
            s = 1/math.sqrt(1 + g*g)
            p0 = ax.coords_to_point(-s, -g*s)
            p1 = ax.coords_to_point(s, g*s)
            return Line(p0, p1, stroke_width=4, stroke_color=YELLOW).set_z_index(3)

        move = always_redraw(f)
        self.play(Create(move), run_time=1, rate_func=linear)
        self.wait(0.2)
        dt = 1.3
        self.play(gval.animate.set_value(0.95), run_time=0.65 * dt)
        self.play(gval.animate.set_value(-0.95), run_time=1.9 * dt)
        self.play(gval.animate.set_value(0.3), run_time=1.25 * dt)
        self.wait()



class Weierstrass(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = GREY
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

        eq = MathTex(r'f(x)=\sum_{n=0}^\infty 2^{-n}\cos(4^n x)', font_size=32, stroke_width=0.8)[0]\
            .set_z_index(3).next_to(ax.get_bottom(), UP, buff=0.05)

        line = ax.plot_line_graph(xvals, y, line_color=WHITE, add_vertex_dots=False, stroke_width=1).set_z_index(2)
        pts = ax.coords_to_point(list(zip(xvals, y)) + [(xrange, ymin), (-xrange, ymin)])
        poly = Polygon(*pts, stroke_opacity=0, fill_opacity=1, fill_color=fill_color).set_z_index(1)
        graph = VGroup(line, poly)
        self.add(box, graph, eq)
        self.wait(1)
        x = xvals * PI
        c = 1.
        for i in range(12):
            y += np.cos(x) * c
            line = ax.plot_line_graph(xvals, y, line_color=WHITE, add_vertex_dots=False, stroke_width=1).set_z_index(2)
            pts = ax.coords_to_point(list(zip(xvals, y)) + [(xrange, ymin), (-xrange, ymin)])
            poly = Polygon(*pts, stroke_opacity=0, fill_opacity=1, fill_color=fill_color).set_z_index(1)
            graph1 = VGroup(line, poly)
            self.play(ReplacementTransform(graph, graph1), run_time=7/(i+14) * 2, rate_func=linear)
            x *= b
            c *= a
            graph = graph1

        self.wait(0.5)

class HermiteEqn(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color=WHITE
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        self.add(MathTex(r'\int_0^\infty\frac{\cos(x-\frac12)iz}{\cos\frac12iz}e^{-az}dz',
                         color=BLACK, stroke_width=5, stroke_color=BLACK))


def get_crossings(xvals, yvals, kval):
    n = len(xvals)
    result = []
    for i in range(1, n):
        if yvals[i-1] < kval <= yvals[i] or yvals[i-1] > kval >= yvals[i]:
            t = (yvals[i] - kval)/(yvals[i] - yvals[i-1])
            result.append(xvals[i-1] * t + xvals[i] * (1-t))
    return result

def interpBM(xvals, yvals, a):
    n = len(xvals)
    n1 = 2 * n - 1
    xvals1 = np.zeros(n1)
    yvals1 = np.zeros(n1)
    for i in range(n):
        xvals1[2*i] = xvals[i]
        yvals1[2*i] = yvals[i]
    for i in range(1, n1, 2):
        xvals1[i] = (xvals1[i-1] + xvals1[i+1])*0.5
        yvals1[i] = (yvals1[i-1] + yvals1[i+1])*0.5 + random.normalvariate(0.0, a/2)

    return xvals1, yvals1, a/math.sqrt(2)


class SmoothvsBM(Scene):
    do_all = True

    def construct(self):
        ax = Axes(x_range=[0, 1], y_range=[0, 1], x_length=config.frame_x_radius, y_length=config.frame_y_radius)
        ax.shift(-ax.coords_to_point(0.5, 0.5))
        corners = ax.coords_to_point([(0,0), (1,1)])
        diag = corners[1] - corners[0]
        box = Rectangle(width=diag[0], height=diag[1], fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0)
        edge = Rectangle(width=diag[0], height=diag[1], fill_opacity=0, stroke_opacity=1, stroke_color=WHITE, stroke_width=6).set_z_index(100)

        edge.to_edge(DOWN, buff=0.05)
        shift = edge.get_center()
        box.shift(shift)
        ax.shift(shift)
        self.add(box, edge)

        def finc(x):
            return (math.pow(2, x) - 1) * 0.6 + 0.2

        def fdec(x):
            return math.pow(2, -x) - 0.2

        xpts = [0,   0.2, 0.4, 0.6, 0.8, 1]
        ypts = [0.15, 0.55, 0.35, 0.75, 0.45, 0.55]
        fosc = scipy.interpolate.CubicHermiteSpline(
            xpts, ypts, [1,   0,   0,   0,   0,  0.2])

        plotinc = ax.plot(finc, [0, 1], color=BLUE).set_z_index(10)
        plotdec = ax.plot(fdec, [0, 1], color=BLUE).set_z_index(10)
        plotosc = ax.plot(fosc, [0, 1], color=BLUE).set_z_index(10)

        ranges = [
            DashedLine(*ax.coords_to_point([(xpts[i], 0), (xpts[i], 1)]), color=WHITE, stroke_opacity=0.5).set_z_index(5)
            for i in range(1, 5)
        ]
        colors = [GREEN_E, RED]
        dots = [Dot(radius=0.1, color=color).set_z_index(20) for color in colors]
        extrema = [dots[i % 2].copy().move_to(ax.coords_to_point(xpts[i], ypts[i])) for i in range(1, 5)]

        n = 961
        xvals = np.linspace(0, 1, n)
        yvals = np.zeros(n) + 0.5
        a = math.sqrt(xvals[1]) * 0.5
        random.seed(3)
        for i in range(1, n):
            yvals[i] = yvals[i-1] - random.normalvariate(0.0, a)

        xvals1, yvals1, a = interpBM(xvals, yvals, a)
        xvals1, yvals1, a = interpBM(xvals1, yvals1, a)
        xvals1, yvals1, a = interpBM(xvals1, yvals1, a)
        xvals1, yvals1, a = interpBM(xvals1, yvals1, a)
        xvals1, yvals1, a = interpBM(xvals1, yvals1, a)
        xvals1, yvals1, a = interpBM(xvals1, yvals1, a)
        xvals1, yvals1, a = interpBM(xvals1, yvals1, a)
        xvals1, yvals1, a = interpBM(xvals1, yvals1, a)

        plotbm = ax.plot_line_graph(xvals, yvals, line_color=BLUE, stroke_width=2, add_vertex_dots=False).set_z_index(5)

        minima = []
        maxima = []
        dots = [dot.scale(0.5) for dot in dots]

        for step in [n-1, n//2, n//4, n//8, n//16, n//32, n//64, n//128]:
            for i0 in range(0, n - step):
                i1 = i0 + step
                minval = maxval = yvals[i0]
                imin = imax = i0
                for i in range(i0, i1 + 1):
                    if yvals[i] < minval:
                        minval = yvals[i]
                        imin = i
                    if yvals[i] > maxval:
                        maxval = yvals[i]
                        imax = i
                if i0 < imin < i1:
                    minima.append(dots[0].copy().move_to(ax.coords_to_point(xvals[imin], minval)))
                if i0 < imax < i1:
                    maxima.append(dots[1].copy().move_to(ax.coords_to_point(xvals[imax], maxval)))

        if self.do_all:
            self.wait(0.5)
            self.play(Create(plotinc), rate_func=linear, run_time=0.7)
            self.wait(0.5)
            plotinc2 = plotinc.copy()
            self.play(ReplacementTransform(plotinc, plotdec), rate_func=linear, run_time=0.7)
            plotinc = plotinc2
            self.wait(0.5)
            self.play(ReplacementTransform(plotdec, plotosc), rate_func=linear, run_time=0.7)
            self.wait(0.5)
            self.play(FadeIn(*ranges), run_time=0.7)
            self.wait(0.5)
            self.play(FadeIn(*extrema), run_time=0.7)
            self.wait(0.5)
            self.play(FadeOut(*ranges, *extrema), run_time=0.5)
            self.play(ReplacementTransform(plotosc, plotbm), run_time=1.5)
            self.wait(0.5)
            self.play(Create(VGroup(*minima)), Create(VGroup(*maxima)), run_time=3)
            self.wait(0.2)
            self.play(FadeOut(*minima, *maxima), run_time=1)
            self.wait(0.4)
        else:
            self.add(*plotbm)

        # infinite variation
        for step, s in [(n//40, 0.3)]:
            ivec = list(range(0, n - step // 2 - 1, step)) + [n-1]
            xvals2 = [xvals[i] for i in ivec]
            yvals2 = [yvals[i] for i in ivec]
            print(yvals2)
            pts2 = ax.coords_to_point(list(zip(xvals2, yvals2)))
            p0 = pts2[0]
            varplot = VGroup()
            plotdot = Dot(radius=0.07, color=RED).set_z_index(30).move_to(p0)
            varplot += plotdot
            self.play(FadeIn(plotdot), run_time=0.1*s, rate_func=linear)

            for i in range(1, len(ivec)):
                p = ax.coords_to_point(xvals2[i], yvals2[i])
                plotline = Line(p0, p, stroke_color=YELLOW, stroke_width=4).set_z_index(20)
                plotdot2 = plotdot.copy().move_to(p)
                varplot += plotline
                varplot += plotdot2
                self.play(Create(plotline), FadeIn(plotdot2), run_time=0.3*s, rate_func=linear)
                p0 = p

    #        plot2 = ax.plot_line_graph(xvals2, yvals2, add_vertex_dots=False, line_color=YELLOW, stroke_width=3).set_z_index(20)
    #        self.play(Create(plot2), run_time=1.5, rate_func=linear)
            self.wait()

            varplot2 = varplot.copy()
            for i in range(1, len(ivec)):
                if yvals2[i] < yvals2[i-1]:
                    shift = (pts2[i-1] - pts2[i])*2 * UP
                    line = varplot2[2*i-1]
                    varplot2[2*i-1] = Line(line.get_start(), line.get_end()+shift, stroke_color=YELLOW, stroke_width=4).set_z_index(18)
                    varplot2[2*i:].shift(shift)
                    self.play(ReplacementTransform(varplot, varplot2), run_time=s)
#                    self.wait(0.1)

                    varplot = varplot2
                    varplot2 = varplot.copy()

            self.play(FadeOut(varplot), run_time=s)


        kval = 0.5
        line = DashedLine(*ax.coords_to_point([(0, kval), (1, kval)]), stroke_color=WHITE, stroke_opacity=0.5).set_z_index(10)

#        (math.pow(2, x) - 1) * 0.6 + 0.2
        x = math.log2((kval - 0.2)/0.6 + 1)
        dotint = Dot(radius = 0.1, color=RED).set_z_index(10)

        if self.do_all:
            self.play(FadeIn(line), run_time=1)
            self.wait(0.2)
            dot1 = dotint.copy().move_to(ax.coords_to_point(x, kval))
            plotbm1 = plotbm.copy()
            self.play(LaggedStart(ReplacementTransform(plotbm, plotinc), FadeIn(dot1), lag_ratio=0.2), run_time=1.5)
            plotbm = plotbm1
            self.wait(0.2)
            self.play(LaggedStart(FadeOut(dot1), ReplacementTransform(plotinc, plotbm), lag_ratio=0.3), run_time=1.5)

            self.wait(0.2)

        dotints = dotint.copy().scale(0.5)
        xint = get_crossings(xvals, yvals, kval)
        pts_int = ax.coords_to_point([(x, kval) for x in xint])
        dots_int = VGroup(*[dotints.copy().move_to(p) for p in pts_int])

        xint0 = get_crossings(xvals1, yvals1, kval)
        xint1 = [x for x in xint0 if 0.2 < x < 0.6]
        x0 = 0.5
        xint2 = [0.2 + (x - x0) * 6 for x in xint1]
        kval2 = 0.8

        pts_int1 = ax.coords_to_point([(x, kval) for x in xint1])
        pts_int2 = ax.coords_to_point([(x, kval2) for x in xint2])
        dots_int1 = VGroup(*[dotints.copy().move_to(p) for p in pts_int1]).set_opacity(0)
        dots_int2 = VGroup(*[dotints.copy().move_to(p) for p in pts_int2])
        line1 = Line(*ax.coords_to_point([(xint1[0], kval), (xint1[-1], kval)]), stroke_width=1, stroke_color=WHITE, stroke_opacity=0.5).set_z_index(1)
        line2 = Line(*ax.coords_to_point([(xint2[0], kval2), (xint2[-1], kval2)]), stroke_width=3, stroke_color=WHITE, stroke_opacity=0.5).set_z_index(1)

        if self.do_all:
            self.play(Create(dots_int), run_time=1)
            self.wait(0.5)
            self.play(ReplacementTransform(dots_int1, dots_int2),
                      ReplacementTransform(line1, line2), run_time=2)

#        i0 = 0
#        for i in range(len(xint)):
#            if xint[i] > 0.2:
#                i0 = i
#                break

#        x0 = xint[i0]
#        p0 = ax.coords_to_point(x0, kval)
#        bigdotint = dotint.copy().move_to(p0).set_color(YELLOW)
#        self.wait(0.2)
#        self.play(ReplacementTransform(dots_int[i0], bigdotint), run_time=1)



        self.wait()

class Dimension(Scene):
    def construct(self):
        eq = MathTex(r'{\rm dimension} = \frac12', stroke_width=1, font_size=40)[0]
        self.add(eq)

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
    with tempconfig({"quality": "low_quality", "preview": True}):
        SmoothStock1().render()
