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


class Intro(Scene):
    def construct(self):
        bistr = [r'{{{{ \frac{{\sin(x/{0})}}{{x/{0}}} }}}}'.format(i) for i in range(3, 17, 2)]
        bistr = [r'{{\int_{-\infty}^\infty\frac{\sin(x)}{x} }}'] + bistr + [r'dx{{=}}\pi']

        xlen = config.frame_x_radius * 1.8
        ylen = config.frame_y_radius * 1.65

        def get_sinc(n):
            def f(x):
                res = 1.0
                for i in range(1, 2*n+3, 2):
                    res *= math.sin(x/i)*i/x
                return res
            return f

        xrange = 20.0
        ax = Axes(x_range=[-xrange, xrange * 1.05], y_range=[-0.5, 1.1], z_index=2, x_length=xlen, y_length=ylen,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': False}).to_edge(DOWN, buff=0.2).set_z_index(2)
        ax.to_edge(DOWN, buff=0.05)

        eq_width = config.frame_x_radius * 2 * 0.95
        eq0 = VGroup()
        for i in range(8):
            eq1 = MathTex(''.join(bistr[:i+1] + bistr[-1:])).to_edge(UP, buff=0.1)
            scale = min(eq1.width, eq_width, (eq1.width + eq_width) * 0.5 - eq_width * 0.2)/eq1.width
            eq1.scale(scale)
            f = get_sinc(i)
            graph = ax.plot(f, (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
            graphu = ax.plot(lambda x: max(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
            graphl = ax.plot(lambda x: min(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
            areau = ax.get_area(graphu, color=BLUE, x_range=(-xrange, xrange))
            areal = ax.get_area(graphl, color=RED, x_range=(-xrange, xrange))
            if i == 0:
                eq1.shift(RIGHT*0.5)
                eq2 = MathTex(r'{\rm sinc}(x)=\frac{\sin(x)}{x}')[0]
                eq2.next_to(eq1[0][-2], ORIGIN, submobject_to_align=eq2[-2])
                eq3 = eq2.copy().scale(2).move_to(ORIGIN)
                self.add(eq3)
                self.wait(0.5)
                self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq3, eq2), FadeIn(ax)),
                                      Create(graph, rate_func=linear), lag_ratio=0.5), run_time=2)

                self.play(ReplacementTransform(eq2[-8:], eq1[0][-8:]),
                          FadeOut(eq2[:-8]),
                          FadeIn(eq1[0][:-8], eq1[-3:]),
                          FadeIn(areau, areal), run_time=2)
                self.wait(0.5)
            else:
                anims1 = [ReplacementTransform(eq0[:i] + eq0[-3:-1], eq1[:i] + eq1[-3:-1]),
                          FadeIn(eq1[i]), FadeOut(eq0[-1], rate_func=rate_functions.rush_from)]
                anims2 = [ReplacementTransform(graph0, graph),
                          ReplacementTransform(areau0, areau),
                          ReplacementTransform(areal0, areal)]
                if i == 1:
                    self.play(*anims1, run_time=1)
                    self.play(*anims2, run_time=1)
                else:
                    self.play(*anims1, *anims2, run_time=1)
                if i < 7:
                    self.play(FadeIn(eq1[-1]), run_time=0.5)
                    self.wait(1)
            eq0 = eq1
            graph0 = graph
            areau0 = areau
            areal0 = areal

        eq4 = MathTex(r'0.999999999985\ldots\;\pi').next_to(eq0, DOWN).to_edge(RIGHT, buff=0.2)
        self.play(FadeIn(eq4), run_time=0.5)
        self.wait(0.5)


class SceneOpacity(Scene):
    opacity = 0.3

    def __init__(self, *args, **kwargs):
        config.background_color = ManimColor(WHITE.to_rgb()*(1-self.opacity))
        Scene.__init__(self, *args, *kwargs)

    def box(self, *obj: Mobject, corner_radius=0.2, fill_color=BLACK, fill_opacity=None, stroke_opacity=0.,
            buff=0.2, **kwargs):
        if fill_opacity is None:
            fill_opacity = self.opacity
        return SurroundingRectangle(VGroup(*obj), corner_radius=corner_radius,
                                    fill_color=fill_color,
                                    fill_opacity=fill_opacity,
                                    stroke_opacity=stroke_opacity,
                                    buff=buff,
                                    **kwargs)


class ProcessBW(SceneOpacity):
    opacity = 0.7

    def construct(self):
        self.animprocess()

    def animprocess(self, yrange=None, n0=3, n1=17, do_extreme=True, iredlines=7, fast=False, thumb=False, yscale=1):
        if yrange is None:
            yrange = [-1.2, 1.2]
        ax = Axes(x_range=[0, (n1-n0)/2 + 0.3], y_range=yrange, x_length=config.frame_x_radius * 1.6,
                  y_length=config.frame_y_radius * yscale,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': True, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': True}).set_z_index(20)
        origin = ax.coords_to_point(0, 0)
        dx = ax.coords_to_point(1, 0) - origin
        dy = ax.coords_to_point(0, 1) - origin
        xlines = []
        y = 0.
        posx = origin + dx * ((n1-n0)/2 + 0.15)
        u = [0.5, -0.05, 0.6, 0.2, -0.92, -0.1, 0.6]
        for i in range(n0, n1, 2):
            y += 1/i
            xlines.append(DashedLine(origin + dy * y, posx + dy * y, color=WHITE, stroke_width=1).set_z_index(15))
            xlines.append(DashedLine(origin - dy * y, posx - dy * y, color=WHITE, stroke_width=1).set_z_index(15))

        redlines = [Line(origin + dy, posx + dy, color=RED, stroke_width=4).set_z_index(18),
                    Line(origin - dy, posx - dy, color=RED, stroke_width=4).set_z_index(18)]

        ylabels = MathTex(r'{{-1}}{{0}}{{1}}', font_size=40).set_z_index(10)
        ylabels[0].next_to(origin - dy, LEFT)
        ylabels[1].next_to(origin, LEFT)
        ylabels[2].next_to(origin + dy, LEFT)
        if thumb:
            ylabels.set_opacity(0)

        dot0 = Dot(color=BLUE, radius=0.15).set_z_index(50).move_to(origin)
        eqS = MathTex(r'\bf S_0', font_size=50, fill_color=BLUE_C, stroke_width=1.5, stroke_color=BLUE_E)[0]\
            .set_z_index(50).next_to(dot0, RIGHT, buff=0.1)
        eqS0 = eqS.copy().next_to(dot0.copy().shift(dx*(n1-n0)/2), RIGHT, buff=0.1)
        box = VMobject() if thumb else self.box(ax, eqS0, ylabels)

        self.add(box, ax, *xlines, ylabels)
        if iredlines == 0:
            self.add(*redlines)
        self.wait(0.5)
        self.play(FadeIn(dot0, eqS), run_time=0.5)
        if not fast:
            self.wait(0.5)
        pts = [dot0.get_center(), dot0.get_center()]
        polycol = ManimColor(GREY.to_rgb() * 0.8)
        for i in range(n0, n1, 2):
            pts1 = []
            lines = []
            polys = []
            for pt0 in pts:
                pt1 = pt0 + dx + dy/i
                pt2 = pt0 +dx - dy/i
                line1 = Line(pt0, pt1, stroke_width=7, color=WHITE).set_z_index(16)
                line2 = Line(pt0, pt2, stroke_width=7, color=WHITE).set_z_index(16)
                polys.append(Polygon(pt0, pt1, pt2, fill_opacity=1, fill_color=polycol, stroke_opacity=1, stroke_color=polycol))
                pts1 += [pt2, pt1]
                lines += [line2, line1]
            dot0.generate_target()
            dot0.target.shift(dx + u.pop(0) * dy / i)
            eqS1 = MathTex(r'\bf S_{}'.format(i//2), font_size=50, fill_color=BLUE_C, stroke_width=1.5,
                           stroke_color=BLUE_E)[0].set_z_index(50).next_to(dot0.target, RIGHT, buff=0.1)
            pathline = Line(dot0.get_center(), dot0.target.get_center(), color=BLUE, stroke_width=4).set_z_index(15)
            # [ 1, 1/n ], orthogonal [ 1, -n]
            eqstr = r'1/{}'.format(i) if i != 1 else r'1'
            eq = MathTex(eqstr.format(i), font_size=30, color=PURPLE_B, stroke_width=1.5)[0].set_z_index(45).move_to(lines[-1]).shift((LEFT + UP*i)/math.pow(1+i*i, 0.5) * 0.25)
            if not fast:
                self.wait(0.25)
            self.play(FadeIn(*lines, *polys, eq), run_time=0.6)
            if not fast:
                self.wait(0.25)
            poly = Polygon(pts[0], pts1[0], pts1[-1], pts[-1], fill_opacity=1, fill_color=polycol, stroke_opacity=1, stroke_color=polycol).set_z_index(7)
            lines[0].set_z_index(10)
            lines[-1].set_z_index(10)
            anims = [FadeIn(poly), MoveToTarget(dot0, rate_func=linear), Create(pathline, rate_func=linear),
                     ReplacementTransform(eqS[0], eqS1[0], rate_func=linear), abra.fade_replace(eqS[1], eqS1[1], rate_func=linear)]
            if len(lines) > 2:
                anims += [FadeOut(*lines[1:-1])]
            self.play(*anims, run_time=0.6)
            self.remove(*polys)

            if i == iredlines:
                self.wait(0.5)
                self.play(FadeIn(*redlines), run_time=0.5)
                self.wait(0.5)

            pts = [pts1[0], dot0.get_center(), pts1[-1]]
            eqS = eqS1

        if do_extreme:
            self.wait(0.5)
            dot1 = dot0.copy().move_to(origin)
            self.play(FadeIn(dot1), run_time=0.5)
            for i in range(n0, n1, 2):
                dot1.generate_target().shift(dx + dy/i)
                self.play(MoveToTarget(dot1, rate_func=linear, run_time=0.3))


        self.wait(0.5)


class ProcessSum(ProcessBW):
    def construct(self):
        self.animprocess(yrange=[-2.2, 2.2], n0=1, n1=11, do_extreme=False, iredlines=-1)


class ProcessBW2(ProcessBW):
    def construct(self):
        self.animprocess(do_extreme=True, iredlines=0)


class ProcessDisc(SceneOpacity):
    opacity = 0.7

    def construct(self):
        self.animprocess()

    def animprocess(self, yrange=None, n0=3, n1=17, do_extreme=True, iredlines=0, fast=False):
        if yrange is None:
            yrange = [-1.2, 1.2]
        ax = Axes(x_range=[0, (n1-n0)/2 + 0.3], y_range=yrange, x_length=config.frame_x_radius * 1.6,
                  y_length=config.frame_y_radius,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': True, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': True}).set_z_index(20)
        origin = ax.coords_to_point(0, 0)
        dx = ax.coords_to_point(1, 0) - origin
        dy = ax.coords_to_point(0, 1) - origin
        xlines = []
        y = 0.
        posx = origin + dx * ((n1-n0)/2 + 0.15)
        u = [1, -1, 1, 1, -1, -1, 1]
        for i in range(n0, n1, 2):
            y += 1/i
            xlines.append(DashedLine(origin + dy * y, posx + dy * y, color=WHITE, stroke_width=1).set_z_index(15))
            xlines.append(DashedLine(origin - dy * y, posx - dy * y, color=WHITE, stroke_width=1).set_z_index(15))

        redlines = [Line(origin + dy, posx + dy, color=RED, stroke_width=4).set_z_index(18),
                    Line(origin - dy, posx - dy, color=RED, stroke_width=4).set_z_index(18)]

        ylabels = MathTex(r'{{-1}}{{0}}{{1}}', font_size=40).set_z_index(10)
        ylabels[0].next_to(origin - dy, LEFT)
        ylabels[1].next_to(origin, LEFT)
        ylabels[2].next_to(origin + dy, LEFT)

        dot0 = Dot(color=BLUE, radius=0.15).set_z_index(50).move_to(origin)
        eqS = MathTex(r'\bf S_0', font_size=50, fill_color=BLUE_C, stroke_width=1.5, stroke_color=BLUE_E)[0]\
            .set_z_index(50).next_to(dot0, RIGHT, buff=0.1)
        eqS0 = eqS.copy().next_to(dot0.copy().shift(dx*(n1-n0)/2), RIGHT, buff=0.1)
        box = self.box(ax, eqS0, ylabels)

        self.add(box, ax, *xlines, ylabels)
        if iredlines == 0:
            self.add(*redlines)
        self.wait(0.5)
        self.play(FadeIn(dot0, eqS), run_time=0.5)
        if not fast:
            self.wait(0.5)
        pts = [dot0.get_center(), dot0.get_center()]
        for i in range(n0, n1, 2):
            pts1 = []
            lines = []
            for pt0 in pts:
                pt1 = pt0 + dx + dy/i
                pt2 = pt0 +dx - dy/i
                line1 = Line(pt0, pt1, stroke_width=7, color=WHITE).set_z_index(16)
                line2 = Line(pt0, pt2, stroke_width=7, color=WHITE).set_z_index(16)
                pts1 += [pt2, pt1]
                lines += [line2, line1]
            dot0.generate_target()
            dot0.target.shift(dx + u.pop(0) * dy / i)
            eqS1 = MathTex(r'\bf S_{}'.format(i//2), font_size=50, fill_color=BLUE_C, stroke_width=1.5,
                           stroke_color=BLUE_E)[0].set_z_index(50).next_to(dot0.target, RIGHT, buff=0.1)
            pathline = Line(dot0.get_center(), dot0.target.get_center(), color=BLUE, stroke_width=4).set_z_index(15)
            # [ 1, 1/n ], orthogonal [ 1, -n]
            eqstr = r'1/{}'.format(i) if i != 1 else r'1'
            eq = MathTex(eqstr.format(i), font_size=30, color=PURPLE_B, stroke_width=1.5)[0].set_z_index(45).move_to(lines[-1]).shift((LEFT + UP*i)/math.pow(1+i*i, 0.5) * 0.25)
            if not fast:
                self.wait(0.25)
            self.play(FadeIn(*lines, eq), run_time=0.6)
            if not fast:
                self.wait(0.25)
            lines[0].set_z_index(10)
            lines[-1].set_z_index(10)
            anims = [MoveToTarget(dot0, rate_func=linear), Create(pathline, rate_func=linear),
                     ReplacementTransform(eqS[0], eqS1[0], rate_func=linear), abra.fade_replace(eqS[1], eqS1[1], rate_func=linear)]
            if len(lines) > 2:
                anims += [FadeOut(*lines[1:-1])]
            self.play(*anims, run_time=0.6)

            if i == iredlines:
                self.wait(0.5)
                self.play(FadeIn(*redlines), run_time=0.5)
                self.wait(0.5)

            pts = [pts1[0], dot0.get_center(), pts1[-1]]
            eqS = eqS1

        if do_extreme:
            self.wait(0.5)
            dot1 = dot0.copy().move_to(origin)
            self.play(FadeIn(dot1), run_time=0.5)
            for i in range(n0, n1, 2):
                dot1.generate_target().shift(dx + dy/i)
                self.play(MoveToTarget(dot1, rate_func=linear, run_time=0.3))

        self.wait(0.5)


class BorweinProb(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq = MathTex(r'\int_{-\infty}^\infty{\rm sinc}(x){\rm sinc}\left(\frac x3\right)\cdots{\rm sinc}'
                     r'\left(\frac x{2n+1}\right)dx {{=}} \pi{{\mathbb P(\lvert S_n\rvert < 1)}}',
                     font_size=35).set_z_index(1)
        box = self.box(eq, buff=0.15)
        self.add(eq[0], box)
        self.wait(0.5)
        self.play(FadeIn(eq[1]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(eq[2]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(eq[3]), run_time=0.5)
        self.wait(0.5)


class Density(Scene):
    def construct(self):
        xrange = 2.5
        ax = Axes(x_range=[-xrange, xrange + 0.15], y_range=[0, 1], x_length=config.frame_x_radius * 1.4,
                  y_length=config.frame_y_radius * 0.7,
                  axis_config={'color': WHITE, 'stroke_width': 4, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               }).set_z_index(20)
        ax.y_axis.set_opacity(0)
        eqR = MathTex(r'\mathbb R', font_size=40, stroke_width=1.5)[0].set_z_index(20).next_to(ax, DR, buff=0.05)
        self.wait(0.2)
        self.play(Create(ax.x_axis, rate_func=linear), FadeIn(eqR), run_time=0.8)

        def p(x):
            return math.exp(-0.5 * x * x)

        graph = ax.plot(p, (-xrange, xrange, 0.05), color=WHITE, stroke_width=4).set_z_index(10)
        self.wait(0.5)

        origin = ax.coords_to_point(0, 0)
        dx = ax.coords_to_point(1, 0) - origin

        areag = VGroup(VMobject())
        areacol = ManimColor(YELLOW.to_rgb()*0.53)
        areacol = ManimColor(BLUE)

        def f(areag):
            a = (graph.get_end()[0] - origin[0])/dx[0]
            area = ax.get_area(graph, color=areacol, x_range=(-xrange, a), opacity=0.7, stroke_width=0).set_z_index(5)
            areag[0] = area

        areag.add_updater(f)
        self.add(areag)

        eqp = MathTex(r'p_X', font_size=50)[0].set_z_index(8).next_to(ax.coords_to_point(-1.5, p(-1.5)), DOWN, buff=0.25)

        self.play(Create(graph, rate_func=linear), FadeIn(eqp), run_time=1)
        areag.remove_updater(f)



        a = -0.5
        b = 1.5
        pta = ax.coords_to_point(a, 0)
        ptb = ax.coords_to_point(b, 0)
        eqab = MathTex(r'a', r'b', font_size=40).set_z_index(20)
        eqab[0].next_to(pta, DOWN, buff=0.1)
        eqab[1].next_to(ptb, DOWN, buff=0.1)
        linel = Line(pta, ax.coords_to_point(a, p(a)), stroke_width=5, stroke_color=RED).set_z_index(8)
        liner = Line(ptb, ax.coords_to_point(b, p(b)), stroke_width=5, stroke_color=RED).set_z_index(8)
        self.wait(0.5)
        self.play(LaggedStart(FadeIn(eqab),
                              AnimationGroup(Create(linel, rate_func=linear), Create(liner, rate_func=linear)),
                              lag_ratio=0.5), run_time=1)

        areal = ax.get_area(graph, color=areacol, x_range=(-xrange, a), opacity=0.7, stroke_width=0).set_z_index(5)
        areac = ax.get_area(graph, color=areacol, x_range=(a, b), opacity=0.7, stroke_width=0).set_z_index(5)
        arear = ax.get_area(graph, color=areacol, x_range=(b, xrange), opacity=0.7, stroke_width=0).set_z_index(5)
        self.add(areal, arear, areac)
        self.remove(areag)

        eqint = MathTex(r'\mathbb P(a\le X\le b){{=}}\int_a^bp_X(x)dx', font_size=40).set_z_index(20)
        eqint[1:].next_to(eqint[0], DOWN).align_to(eqint[0], LEFT)
        eqint.next_to((pta + ptb)/2, UP, buff=0.2).next_to(pta, RIGHT, buff=0.15, coor_mask=RIGHT)
        eqint[1:].shift(RIGHT*0.2)

        self.play(FadeIn(eqint[0]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(eqint[1:]), areac.animate.set_fill(color=BLUE_E).set_opacity(0.9), run_time=1)
        self.wait(0.5)
        areag2 = VGroup(linel, liner, eqab)

        tval = ValueTracker(0.0)

        def f():
            t = tval.get_value()
            a1 = -xrange * t + a * (1-t)
            b1 = xrange * t + b * (1-t)
            pta = ax.coords_to_point(a1, 0)
            ptb = ax.coords_to_point(b1, 0)
            eqab[0].move_to(pta, coor_mask=RIGHT)
            eqab[1].move_to(ptb, coor_mask=RIGHT)
            obj = VGroup(
                ax.get_area(graph, color=areacol, x_range=(-xrange, a1), opacity=0.7, stroke_width=0).set_z_index(5),
                ax.get_area(graph, color=BLUE_E, x_range=(a1, b1), opacity=0.9, stroke_width=0).set_z_index(5),
                ax.get_area(graph, color=areacol, x_range=(b1, xrange), opacity=0.7, stroke_width=0).set_z_index(5),
                Line(pta, ax.coords_to_point(a1, p(a1)), stroke_width=5, stroke_color=RED).set_z_index(8),
                Line(ptb, ax.coords_to_point(b1, p(b1)), stroke_width=5, stroke_color=RED).set_z_index(8),
                eqab)
            return obj

        self.remove(areal, areac, arear, linel, liner, eqab)
        areag2 = always_redraw(f)
        self.add(areag2)
        self.wait(0.1)
#        areag2.add_updater(f, call_updater=True)
        self.play(tval.animate(rate_func=linear).set_value(1.0), run_time=2)
        self.remove(areag2)
        areag2 = f()
        self.add(areag2)
        self.play(FadeOut(areag2[0], areag2[2:]), run_time=0.5)
        self.wait(0.5)

        eqint2 = MathTex(r'\int_{-\infty}^\infty p_X(x)dx {{=}} 1', font_size=40).set_z_index(40).move_to(ax.coords_to_point(0, 0))
        eqint2.next_to(eqint[1], ORIGIN, submobject_to_align=eqint2[1], coor_mask=UP)
        self.play(LaggedStart(AnimationGroup(
            ReplacementTransform(eqint[2][3:] + eqint[1] + eqint[2][0], eqint2[0][4:] + eqint2[1] + eqint2[0][0]),
            abra.fade_replace(eqint[2][2], eqint2[0][2:4]),
            abra.fade_replace(eqint[2][1], eqint2[0][1]),
            FadeOut(eqint[0])), FadeIn(eqint2[2]), lag_ratio=0.5), run_time=1.5)
        self.wait(0.5)


class SumDensity(Density):
    def construct(self):
        xrange = 2.5
        ax = Axes(x_range=[-xrange, xrange + 0.15], y_range=[0, 1], x_length=config.frame_x_radius * 1.4,
                  y_length=config.frame_y_radius * 0.7,
                  axis_config={'color': WHITE, 'stroke_width': 4, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               }).set_z_index(20)
        ax.y_axis.set_opacity(0)
        eqR = MathTex(r'\mathbb R', font_size=40, stroke_width=1.5)[0].set_z_index(20).next_to(ax, DR, buff=0.05)

        z = 0.5
        z0 = -0.5
        z1 = 1.5
        pt0 = ax.coords_to_point(z0, 0)
        pt1 = ax.coords_to_point(z1, 0)
        ptz = ax.coords_to_point(z, 0)

        def p(x):
            return math.exp(-0.5 * x * x)

        graph = ax.plot(p, (-xrange, xrange, 0.05), color=WHITE, stroke_width=4).set_z_index(10)
        eqp = MathTex(r'p_Y', font_size=50)[0].set_z_index(8).next_to(ax.coords_to_point(-1.5, p(-1.5)), DOWN, buff=0.25)

        linel = Line(pt0, ax.coords_to_point(z0, p(z0)), stroke_width=5, stroke_color=RED).set_z_index(8)
        liner = Line(pt1, ax.coords_to_point(z1, p(z1)), stroke_width=5, stroke_color=RED).set_z_index(8)
        eq01 = MathTex(r'z-a', r'z+a', r'z', font_size=40).set_z_index(20)
        eq01[0].next_to(pt0, DOWN, buff=0.15)
        eq01[1].next_to(pt1, DOWN, buff=0.15)
        eq01[2].next_to(ptz, DOWN, buff=0.15)

        areacol = ManimColor(BLUE)
        areal = ax.get_area(graph, color=areacol, x_range=(-xrange, z0), opacity=0.7, stroke_width=0).set_z_index(5)
        areac = ax.get_area(graph, color=BLUE_E, x_range=(z0, z1), opacity=0.9, stroke_width=0).set_z_index(5)
        arear = ax.get_area(graph, color=areacol, x_range=(z1, xrange), opacity=0.7, stroke_width=0).set_z_index(5)

        eq1 = MathTex(r'p_{X+Y}(z)=', font_size=45, stroke_width=1.5).set_z_index(10)
        eq2 = MathTex(r'{{=}}\int_{-\infty}^\infty\!\!\! p_X(z-x)p_Y(x)\,dx', stroke_width=1.5, font_size=35).set_z_index(10)
        eq3 = MathTex(r'{{=}}\int_{z-a}^{z+a}\frac1{2a}', stroke_width=1.5, font_size=35).set_z_index(10)
        eq4 = MathTex(r'{{=}}\frac1{2a}\int_{z-a}^{z+a}p_Y(x)\,dx', stroke_width=1.5, font_size=35).set_z_index(10)
        eq5 = MathTex(r'{{=}}\frac1{2a}\mathbb P(z-a\! <\! Y\! <\! z+a)', stroke_width=1.5, font_size=35).set_z_index(10)
        eq6 = MathTex(r'{{=}}\frac1{2a}\mathbb P(\lvert Y-z\rvert  < a)', stroke_width=1.5, font_size=40).set_z_index(10)
        eq2.next_to(eq1, DOWN).next_to(eq1.get_left(), RIGHT, submobject_to_align=eq2[1], coor_mask=RIGHT, buff=0)

        VGroup(eq1, eq2).next_to(ax.coords_to_point(z, 0), UP, submobject_to_align=eq2[1])

        eq3.next_to(eq2[0], ORIGIN, submobject_to_align=eq3[0])
        eq3[1][7:].move_to(eq2[1][4:11], coor_mask=RIGHT)
        eq4.next_to(eq2[0], ORIGIN, submobject_to_align=eq4[0])
        eq5.next_to(eq2[0], ORIGIN, submobject_to_align=eq5[0])
        eq6.next_to(eq2[0], ORIGIN, submobject_to_align=eq6[0])

        ticks = [ax.x_axis.get_tick(_) for _ in (z0, z, z1)]

        self.add(ax.x_axis, eqR, graph, linel, liner, eq01, eqp, areal, areac, arear, eq1, eq2[1], *ticks)

        self.wait(0.5)
        self.play(ReplacementTransform(eq2[1][0], eq3[1][0]),
                  abra.fade_replace(eq2[1][1], eq3[1][1:4]),
                  abra.fade_replace(eq2[1][2:4], eq3[1][4:7]),
                  FadeOut(eq2[1][4:11]),
                  FadeIn(eq3[1][7:]),
                  run_time=1)
        self.wait(0.15)
        self.play(ReplacementTransform(eq3[1][7:] + eq3[1][:7] + eq2[1][-7:],
                                       eq4[1][:4] + eq4[1][4:11] + eq4[1][-7:]),
                  run_time=1)
        self.wait(0.15)
        self.play(ReplacementTransform(eq4[1][:4], eq5[1][:4]),
                  FadeOut(eq4[1][4:]),
                  FadeIn(eq5[1][4:]),
                  run_time=1)
        self.play(ReplacementTransform(eq5[1][:6] + eq5[1][10] + eq5[1][-1], eq6[1][:6] + eq6[1][7] + eq6[1][-1]),
                  FadeOut(eq5[1][6:10], eq5[1][11:-1]),
                  FadeIn(eq6[1][6], eq6[1][8:-1]),
                  run_time=0.7)
        self.wait(0.2)


class Characteristic(SceneOpacity):
    opacity = 0.7

    @staticmethod
    def eq1():
        eq1 = MathTex(r'\varphi_X(u){{=}}\mathbb E\left[e^{iuX}\right]{{=}}\int_{-\infty}^\infty e^{iux}p_X(x)\,dx').set_z_index(1)
        eq1[3:].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
        return eq1

    def eq1asFT(self, eq1):
        self.play(FadeOut(eq1[2][:2], eq1[2][-1]),
                  FadeIn(eq1[4][:4], eq1[4][-7:]),
                  ReplacementTransform(eq1[2][2:5], eq1[4][4:7]),
                  abra.fade_replace(eq1[2][5], eq1[4][7]),
                  run_time=1.5)

    def construct(self):
        eq1 = self.eq1()
#        eq2 = MathTex(r'p_X(x){{=}}\frac1{2\pi}\int_{-\infty}^\infty e^{-iux}\varphi_X(u)du').next_to(eq1, DOWN).align_to(eq1, LEFT)

        box = self.box(eq1)

        self.add(box)
        self.wait(0.5)
        self.play(FadeIn(eq1[0]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(eq1[1]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(eq1[2][:2], eq1[2][-1]), run_time=0.8)
        self.wait(0.1)
        self.play(FadeIn(eq1[2][2]), run_time=0.4)
        self.wait(0.1)
        self.play(FadeIn(eq1[2][3]), run_time=0.4)
        self.wait(0.1)
        self.play(FadeIn(eq1[2][4]), run_time=0.4)
        self.wait(0.1)
        self.play(FadeIn(eq1[2][5]), run_time=0.4)
        self.wait(0.1)
        self.play(eq1[0][3].animate(rate_func=there_and_back).set_color(RED).scale(1.5), run_time=1)
        self.play(eq1[2][4].animate(rate_func=there_and_back).set_color(RED).scale(1.5), run_time=1)
        self.wait(0.5)
        self.eq1asFT(eq1)
        self.wait(0.5)


class Rademacher(SceneOpacity):
    opacity = 0.7
    def construct(self):
        eq1 = Tex(r'$X$ is Rademacher').set_z_index(1)
        eq2 = MathTex(r'\mathbb P(X=1){{=}}\mathbb P(X=-1){{=}}\frac12').set_z_index(1)
        eq2.next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'\varphi_X(u){{=}}\mathbb E[e^{iuX}]{{=}}\frac12\left(e^{iu1}+e^{iu(-1)}\right)'
                      r'{{=}}\frac12\left(e^{iu}+e^{-iu}\right)'
                      r'{{=}}\cos u').set_z_index(1)
        eq3.next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq3[3:].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3], coor_mask=RIGHT)
        eq3[5:].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[5], coor_mask=RIGHT)
        eq3[7:].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[7], coor_mask=RIGHT)
        box1 = self.box(eq1, eq2)
        box2 = self.box(eq1, eq2, eq3)
        self.add(box1, eq1)
        self.wait(0.5)
        self.play(FadeIn(eq2[:3]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq2[3]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(eq2[4]), run_time=0.5)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform(box1, box2), FadeIn(eq3[:3]), lag_ratio=0.3), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(AnimationGroup(
            abra.fade_replace(eq3[2][0], eq3[4][:3]),
            abra.fade_replace(eq3[2][1], eq3[4][3]),
            abra.fade_replace(eq3[2][-1], eq3[4][-1]),
            abra.fade_replace(eq3[2][5], eq3[4][7]),
            abra.fade_replace(eq3[2][5].copy(), eq3[4][12:16]),
            ReplacementTransform(eq3[2][2:5], eq3[4][9:12]),
            ReplacementTransform(eq3[2][2:5].copy(), eq3[4][4:7])),
            FadeIn(eq3[4][8], run_time=0.2), lag_ratio=0.6), run_time=2)
        self.wait(0.2)
        eq3_1 = eq3[6][-5:-1].copy()
        eq3_1.next_to(eq3[4][-8], ORIGIN, submobject_to_align=eq3_1[0], coor_mask=RIGHT)
        self.play(FadeOut(eq3[4][7], eq3[4][12], eq3[4][14:16]),
                  ReplacementTransform(eq3[4][-7:-5] + eq3[4][-4], eq3_1[2:4] + eq3_1[1]),
                  run_time=1)
        self.play(ReplacementTransform(eq3[4][:7] + eq3[4][8:10] + eq3_1[1:] + eq3[4][-1],
                                       eq3[6][:7] + eq3[6][7:9] + eq3[6][9:12] + eq3[6][-1]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq3[6]), FadeIn(eq3[8]), run_time=1)
        self.wait(0.5)


class Uniform(SceneOpacity):
    opacity = 0.7
    def construct(self):
        eq1 = Tex(r'$X$ is uniform on $[-1,1]$').set_z_index(1)
        eq2 = MathTex(r'p_X(x)=\begin{cases} 1/2,& {\rm if\ }-1\le x\le 1,\\'
                      r' 0,&{\rm otherwise}\end{cases}').set_z_index(1)\
            .next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'\varphi_X(u){{=}}\frac12\int_{-1}^1e^{iux}\,dx'
                      r'{{=}}\frac12\left[\frac{e^{iux} }{iu}\right]_{x=-1}^{x=1}'
                      r'{{=}}\frac{e^{iu}-e^{-iu}}{2iu}'
                      r'{{=}}\frac{\sin u}{u}'
                      r'{{=}} {\rm sinc}\;u').set_z_index(1)\
            .next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3], coor_mask=RIGHT)
        eq3[5:7].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[5], coor_mask=RIGHT)
        eq3[7:9].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[7], coor_mask=RIGHT)
        eq3[9:11].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[9], coor_mask=RIGHT)
        VGroup(eq1, eq2, eq3).move_to(ORIGIN)
        box1 = self.box(eq1, eq2, eq3)
        self.add(box1, eq1)
        self.wait(0.5)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq2), FadeIn(eq3[:3]), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(eq3[2][:3] + eq3[2][7:11] + eq3[2][4] + eq3[2][5:7],
                                       eq3[4][:3] + eq3[4][4:8] + eq3[4][-5] + eq3[4][-2:]),
                  abra.fade_replace(eq3[2][8:10].copy(), eq3[4][9:11]),
                  FadeIn(eq3[4][3], eq3[4][8], eq3[4][11], eq3[4][-4:-2], eq3[4][-7:-5]),
                  FadeOut(eq3[2][3], eq3[2][-2:]),
                  run_time=1.5)
        self.wait(0.5)
        self.play(ReplacementTransform(eq3[4][9:11] + eq3[4][8] + eq3[4][2] + eq3[4][4:7] + eq3[4][4].copy() + eq3[4][5:7].copy(),
                                       eq3[6][10:12] + eq3[6][8] + eq3[6][9] + eq3[6][:3] + eq3[6][4] + eq3[6][6:8]),
                  FadeOut(eq3[4][0], eq3[4][3], eq3[4][-8:], eq3[4][7]),
                  FadeIn(eq3[6][3]),
                  FadeIn(eq3[6][5]),
                  FadeOut(eq3[4][1], target_position=eq3[6][8]), run_time=1.5)
        self.wait(0.5)
        eqs = eq3[8][:4].copy().move_to(eq3[6][3], coor_mask=RIGHT)
        self.play(FadeOut(eq3[6][9:11]),
                  FadeOut(eq3[6][:8]),
                  FadeIn(eqs),
                  run_time=1.3)
        self.play(ReplacementTransform(eqs, eq3[8][:4]),
                  ReplacementTransform(eq3[6][8], eq3[8][4]),
                  ReplacementTransform(eq3[6][-1], eq3[8][-1]),
                  run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(eq3[8][:3] + eq3[8][3], eq3[10][:3] + eq3[10][4]),
                  ReplacementTransform(eq3[8][5], eq3[10][4]),
                  FadeIn(eq3[10][3], target_position=eq3[8][2]),
                  FadeOut(eq3[8][4]),
                  run_time=1.5)

        self.wait(0.5)

class UniformInt(SceneOpacity):
    opacity = 0.7
    def construct(self):
        eq1 = Tex(r'$X$ is uniform on $\{-n, -n+1,\ldots,n\}$').set_z_index(1)
        eq2 = MathTex(r'\mathbb P(X=-n)=\mathbb P(X=-n+1)=\cdots=\mathbb P(X=n){{=}}\frac1{2n+1}').set_z_index(1)
        eq2.next_to(eq1, DOWN)#.align_to(eq1, LEFT)
        eq3 = MathTex(r'\varphi_X(u){{=}}\mathbb E\left[e^{iuX}\right]'
                      r'{{=}}\frac1{2n+1}\sum_{k=-n}^ne^{iuk}'
                      r'{{=}}\frac1{2n+1}\sum_{k=0}^{2n}e^{iu(k-n)}'
                      r'{{=}}\frac1{2n+1}\frac{e^{-iun}(e^{iu(2n+1)}-1)}{e^{iu}-1}'
                      r'{{=}}\frac1{2n+1}\frac{e^{-iu(n+1/2)}(e^{iu(2n+1)}-1)}{e^{-iu/2}(e^{iu}-1)}'
                      r'{{=}}\frac1{2n+1}\frac{(e^{iu(n+1/2)}-e^{-iu(n+1/2)})/2i}{(e^{iu/2}-e^{-iu/2})/2i}'
                      r'{{=}}\frac{\sin(u(n+1/2))}{(2n+1)\sin(u/2)}'
                      ).set_z_index(1).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3])
        eq3[5:7].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[5])
        eq3[7:9].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[7])
        eq3[9:11].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[9])
        eq3[11:13].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[11])
        eq3[13:15].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[13])

        box1 = self.box(eq1, eq2)
        box2 = self.box(eq1, eq3[:10])
        box3 = self.box(eq1, eq3)
        box4 = self.box(eq1, eq3[:2], eq3[14])
        self.add(box1, eq1)
        self.wait(0.5)
        self.play(FadeIn(eq2[0]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq2[1]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(eq2[2]), run_time=1)

        self.wait(0.5)
        self.play(LaggedStart(AnimationGroup(FadeIn(eq3[:3]), FadeOut(eq2)),
                              ReplacementTransform(box1, box2), lag_ratio=0.3), run_time=1.5)
        self.wait(0.5)
        self.play(abra.fade_replace(eq3[2][:2], eq3[4][:12]),
                  ReplacementTransform(eq3[2][2:5], eq3[4][12:15]),
                  FadeOut(eq3[2][-1]),
                  abra.fade_replace(eq3[2][-2], eq3[4][-1]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq3[4][:6] + eq3[4][6] + eq3[4][7:10] + eq3[4][12:15] + eq3[4][15],
                                       eq3[6][:6] + eq3[6][7] + eq3[6][8:11] + eq3[6][12:15] + eq3[6][16]),
                  FadeIn(eq3[6][6], eq3[6][15], eq3[6][17:20]),
                  abra.fade_replace(eq3[4][10:12], eq3[6][11]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(LaggedStart(
            FadeOut(eq3[6][8:12], eq3[6][15:17], eq3[6][19]),
            ReplacementTransform(eq3[6][:6] + eq3[6][6:8] + eq3[6][12] + eq3[6][13:15] + eq3[6][17] + eq3[6][18]
                                       + eq3[6][12:15].copy() + eq3[6][12:15].copy(),
                                       eq3[8][:6] + eq3[8][16:18] + eq3[8][6] + eq3[8][8:10] + eq3[8][7] + eq3[8][10]
                                       + eq3[8][12:15] + eq3[8][25:28]),
            FadeIn(eq3[8][11], eq3[8][15], eq3[8][18:25], eq3[8][28:]),
            lag_ratio=0.3), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq3[8][:10] + eq3[8][10] + eq3[8][11:25] + eq3[8][25:30],
                                       eq3[10][:10] + eq3[10][11] + eq3[10][17:31] + eq3[10][38:43]),
                  FadeIn(eq3[10][10], eq3[10][16], eq3[10][37], eq3[10][43]),
                  ReplacementTransform(box2, box3),
                  run_time=1)
        self.play(FadeIn(eq3[10][12:16], eq3[10][31:37]), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq3[10][:6] + eq3[10][6:17] + eq3[10][17] + eq3[10][18:22] + eq3[10][26:28]
                                       + eq3[10][29] + eq3[10][31:37] + eq3[10][37:41] + eq3[10][41] + eq3[10][43],
                                       eq3[12][:6] + eq3[12][18:29] + eq3[12][6] + eq3[12][7:11] + eq3[12][16:18]
                                       + eq3[12][29] + eq3[12][41:47] + eq3[12][34:38] + eq3[12][40] + eq3[12][47]),
                  abra.fade_replace(eq3[10][22:26], eq3[12][11:16]),
                  FadeOut(eq3[10][28], target_position=eq3[12][18]),
                  FadeOut(eq3[10][42], target_position=eq3[12][41]),
                  FadeIn(eq3[12][38:40], target_position=eq3[10][40]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeIn(eq3[12][30:33], eq3[12][48:51]),
                  ReplacementTransform(eq3[10][30], eq3[12][33]),
                  run_time=1)
        self.wait(0.2)
        sin1 = eq3[14][:13].copy().move_to(eq3[12][6:30], coor_mask=RIGHT)
        sin2 = eq3[14][20:28].copy().move_to(eq3[12][34:48], coor_mask=RIGHT)
        self.play(FadeOut(eq3[12][6:33], eq3[12][34:51]),
                  FadeIn(sin1, sin2),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(box3, box4),
                  ReplacementTransform(sin1 + sin2 + eq3[12][2:6] + eq3[12][33],
                                       eq3[14][:13] + eq3[14][20:28] + eq3[14][15:19] + eq3[14][13]),
                  FadeOut(eq3[12][:2]),
                  FadeIn(eq3[14][14], eq3[14][19]),
                  run_time=1.5)
        self.wait(0.5)


class SincPlot(Scene):
    def construct(self):
        xlen = config.frame_x_radius * 1.8
        ylen = config.frame_y_radius * 1.65

        def get_sinc(n):
            def f(x):
                res = 1.0
                for i in range(1, 2*n+3, 2):
                    res *= math.sin(x/i)*i/x
                return res
            return f

        xrange = 20.0
        ax = Axes(x_range=[-xrange, xrange * 1.05, 20], y_range=[-0.5, 1.1], z_index=2, x_length=xlen, y_length=ylen,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': True, 'length': 20}).set_z_index(2)

        def get_f(n):
            def f(x):
                return math.sin(x)/(2*n+1)/math.sin(x/(2*n+1))
            return f

        linew = 4
        graph = ax.plot(lambda x: math.sin(x)/x, (-xrange, xrange, 0.05), color=RED, stroke_width=linew).set_z_index(10)

        labels = MathTex(r'{\rm sinc}(u)', r'\varphi_X(u)').set_z_index(30)
        labels[1].next_to(labels[0], DOWN, buff=0.2).align_to(labels[0], LEFT)
        labels.move_to(ax.coords_to_point(15, 0.8))
        line1 = Line(labels[0].get_left() + LEFT * 0.1, labels[0].get_left() + LEFT * 0.4, color=RED, stroke_width=linew).set_z_index(30)
        line2 = Line(labels[1].get_left() + LEFT * 0.1, labels[1].get_left() + LEFT * 0.4, color=BLUE, stroke_width=linew).set_z_index(30)
        eq1 = MathTex(r'n=1')[0].set_z_index(30).next_to(labels, DOWN).align_to(labels, LEFT)

        box1 = SurroundingRectangle(VGroup(line1, line2, labels, eq1), fill_color=BLACK, fill_opacity=0.8,
                                    corner_radius=0.1, stroke_width=3, stroke_color=WHITE, stroke_opacity=1,
                                    buff=0.2).set_z_index(25)

        eqr = Tex(r'${\rm sinc}$ range: $[-20, 20]$', r'$\varphi_X$ range: $[-20/(n+1/2), 20/(n+1/2)]$', font_size=35)
        eqr[1].next_to(eqr[0], DOWN, buff=0.1).align_to(eqr[0], LEFT)
        eqr.move_to(ax.coords_to_point(11, 0)).align_to(ax, DOWN)

        self.add(ax, graph, labels[0], line1, box1, eqr)

        self.wait(0.5)

        graph1 = ax.plot(get_f(1), (-xrange, xrange, 0.05), color=BLUE, stroke_width=linew).set_z_index(20)
        self.play(FadeIn(graph1, line2, labels[1], eq1), run_time=1)


        dt = [2.5, 1.5, 1, 1, 0.6]
        for i in range(2, 11):
            graph2 = ax.plot(get_f(i), (-xrange, xrange, 0.05), color=BLUE, stroke_width=linew).set_z_index(20)
            eq2 = MathTex(r'n={}'.format(i))[0].set_z_index(30).align_to(eq1, DL)
            self.wait(0.5)
            self.play(ReplacementTransform(graph1, graph2),
                      ReplacementTransform(eq1[:2], eq2[:2]),
                      FadeIn(eq2[2:]),
                      FadeOut(eq1[2:]),
                      run_time=dt[min(i, len(dt)) - 1])
            graph1 = graph2
            eq1 = eq2

        self.wait(0.5)


class FourierInvert(Characteristic):
    opacity = 0.7

    def construct(self):
        eq1 = self.eq1()
        eq2 = MathTex(r'p_X(x){{=}}\frac1{2\pi}\int_{-\infty}^\infty e^{-iux}\varphi_X(u)\,du')\
            .set_z_index(10).next_to(eq1, DOWN).align_to(eq1, LEFT)

        box1 = self.box(eq1)
        box2 = self.box(eq1, eq2)

        self.add(box1, eq1[:3])
        self.wait(0.5)
        self.eq1asFT(eq1)
        self.wait(0.5)

        self.play(LaggedStart(AnimationGroup(ReplacementTransform((eq1[0][:] + eq1[1] + eq1[4][:5] + eq1[4][5:8] + eq1[4][8:13] + eq1[4][13]).copy(),
                                       eq2[2][13:18] + eq2[1] + eq2[2][4:9] + eq2[2][10:13] + eq2[0][:] + eq2[2][18]),
                  abra.fade_replace(eq1[4][-1].copy(), eq2[2][-1]),
                  ReplacementTransform(box1, box2),
                  FadeIn(eq2[2][9], target_position=eq1[4][5])),
                  FadeIn(eq2[2][:4]), lag_ratio=0.4),
                  run_time=2)
        self.wait(0.5)
        eq3 = MathTex(r'p_X(0){{=}}\frac1{2\pi}\int_{-\infty}^\infty\varphi_X(u)\,du{{=}}e^{-iu0}{{=}}1').set_z_index(10)
        eq3.next_to(eq2[1], ORIGIN, submobject_to_align=eq3[1])
        eq3[4].next_to(eq2[2][8], ORIGIN, submobject_to_align=eq3[4][0])
        eq3[6].move_to(eq2[2][8:12], coor_mask=RIGHT)
        self.play(ReplacementTransform(eq2[0][:3] + eq2[0][4],
                                       eq3[0][:3] + eq3[0][4]),
                  abra.fade_replace(eq2[0][3], eq3[0][3]),
                  abra.fade_replace(eq2[2][12], eq3[4][-1]),
                  run_time=1)
        self.play(FadeOut(eq2[2][8:12], eq3[4][-1]),
                  FadeIn(eq3[6]),
                  run_time=1)
        self.play(ReplacementTransform(eq2[2][:8] + eq2[2][13:20] + eq2[1],
                                       eq3[2][:8] + eq3[2][8:15] + eq3[1]),
                  FadeOut(eq3[6]),
                  run_time=1)
        self.wait(0.5)


class Independent(SceneOpacity):
    opacity = 0.7
    def construct(self):
        eq1 = MathTex(r'\varphi_{X_1+X_2+\cdots+X_n}(u){{=}}\mathbb E\left[e^{iu(X_1+X_2+\cdots+X_n)}\right]'
                      r'{{=}}\mathbb E\left[e^{iuX_1+iuX_2+\cdots+iuX_n}\right]'
                      r'{{=}}\mathbb E\left[e^{iuX_1}e^{iuX_2}\cdots e^{iuX_n}\right]'
                      r'{{=}}\mathbb E\left[e^{iuX_1}\right]\mathbb E\left[e^{iuX_2}\right]\cdots\mathbb E\left[e^{iuX_n}\right]'
                      r'{{=}}\varphi_{X_1}(u)\varphi_{X_2}(u)\cdots\varphi_{X_n}(u)')
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
        eq1[5:7].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[5], coor_mask=RIGHT)
        eq1[7:9].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[7], coor_mask=RIGHT)
        eq1[9:11].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[9], coor_mask=RIGHT)
        eq1.set_z_index(10).move_to(ORIGIN)
        eq2 = eq1[10].copy()
        eq2[:6].move_to(eq1[8][:8], coor_mask=RIGHT)
        eq2[6:12].move_to(eq1[8][8:16], coor_mask=RIGHT)
        eq2[12:15].move_to(eq1[8][16:19], coor_mask=RIGHT)
        eq2[15:21].move_to(eq1[8][19:27], coor_mask=RIGHT)

        box1 = self.box(eq1[:2], eq1[10])
        box2 = self.box(eq1)
        box3 = box1.copy()

        self.add(box1, eq1[:2], eq1[10])
        self.wait(0.5)
        self.play(FadeOut(eq1[10]), run_time=1)
        self.play(ReplacementTransform(box1, box2), FadeIn(eq1[2]), run_time=1)
        self.wait(0.5)

        self.play(ReplacementTransform(eq1[2][:3] + eq1[2][3:5] + eq1[2][3:5].copy() + eq1[2][3:5].copy(),
                                       eq1[4][:3] + eq1[4][3:5] + eq1[4][8:10] + eq1[4][17:19]),
                  ReplacementTransform(eq1[2][6:9] + eq1[2][9:12] + eq1[2][16:18] + eq1[2][12:16],
                                       eq1[4][5:8] + eq1[4][10:13] + eq1[4][19:21] + eq1[4][13:17]),
                  FadeOut(eq1[2][5], eq1[2][-2]),
                  abra.fade_replace(eq1[2][-1],  eq1[4][-1]),
                  run_time=2)
        self.wait(0.2)
        self.play(ReplacementTransform(eq1[4][:7] + eq1[4][-5:] + eq1[4][2].copy() + eq1[4][2].copy(),
                                       eq1[6][:7] + eq1[6][-5:] + eq1[6][7] + eq1[6][15]),
                  ReplacementTransform(eq1[4][8:12] + eq1[4][13:16],
                                       eq1[6][8:12] + eq1[6][12:15]),
                  FadeOut(eq1[4][7], eq1[4][12], eq1[4][16]),
                  run_time=2)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(eq1[6][:7] + eq1[6][7:12] + eq1[6][12:15] + eq1[6][15:],
                                       eq1[8][:7] + eq1[8][10:15] + eq1[8][16:19] + eq1[8][21:]),
                  FadeIn(eq1[8][7:10], eq1[8][15], eq1[8][19:21]), lag_ratio=0.4),
                  run_time=2)
        self.wait(0.2)
        self.play(FadeOut(eq1[8][:8], eq1[8][8:16], eq1[8][19:27]),
                  FadeIn(eq2[:6], eq2[6:12], eq2[15:21]),
                  ReplacementTransform(eq1[8][16:19], eq2[12:15]),
                  run_time=1.5)
        self.play(ReplacementTransform(eq2, eq1[10]),
                  ReplacementTransform(box2, box3), run_time=1.5)
        self.wait(0.5)


class ScaleChar(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\varphi_{cX}(u){{=}}\mathbb E\left[e^{iu cX}\right]'
                      r'{{=}}\mathbb E\left[e^{icuX}\right]'
                      r'{{=}}\varphi_X(cu)')
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
        eq1[5:7].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[5], coor_mask=RIGHT)
        eq1.move_to(ORIGIN).set_z_index(10)
        box = self.box(eq1)
        self.add(box, eq1[:3])
        self.wait(0.5)
        self.play(ReplacementTransform(eq1[2][:4] + eq1[2][6:] + eq1[2][4] + eq1[2][5],
                                       eq1[4][:4] + eq1[4][6:] + eq1[4][5] + eq1[4][4]),
                  run_time=1)
#        pos = eq1[6].get_center()
#        eq1[6].move_to(eq1[4], coor_mask=RIGHT)
        self.play(FadeOut(eq1[4]), FadeIn(eq1[6]), run_time=2)
#        self.play(eq1[6].animate.move_to(pos), run_time=1)
        self.wait(0.5)


class SeqChar(SceneOpacity):
    opacity=0.7

    def construct(self):
        eq1 = MathTex(r'X_0,X_1,X_2,\ldots')[0].set_z_index(10)
        eq2 = MathTex(r'X_0\sim U([-1,1])')[0].next_to(eq1, DOWN).set_z_index(10).align_to(eq1, LEFT)
        eq3 = MathTex(r'X_1\sim U([-1/3,1/3])')[0].next_to(eq1, DOWN).set_z_index(10).align_to(eq1, LEFT)
        eq4 = MathTex(r'X_n\sim U([-1/(2n+1),1/(2n+1)])')[0].next_to(eq1, DOWN).set_z_index(10).align_to(eq1, LEFT)
        eq5 = MathTex(r'\varphi_{X_0}(u)={\rm sinc}(u)')[0].set_z_index(10).next_to(eq4, DOWN).align_to(eq1, LEFT)
        eq6 = MathTex(r'\varphi_{X_n}(u)={\rm sinc}(u/(2n+1))')[0].set_z_index(10).next_to(eq4, DOWN).align_to(eq1, LEFT)
        eq7 = MathTex(r'S_n=X_0+X_1+X_2+\cdots+X_n')[0].set_z_index(10).align_to(eq1, DL)
        eq8 = MathTex(r'\varphi_{S_n}(u){{=}}\varphi_{X_0}(u)\varphi_{X_1}(u)\cdots\varphi_{X_n}(u)'
                      r'{{=}}{\rm sinc}(u){\rm sinc}(u/3)\cdots{\rm sinc}(u/(2n+1))')
        eq8[3:5].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[3], coor_mask=RIGHT)
        eq8.set_z_index(10).next_to(eq7, DOWN).align_to(eq7, LEFT)

        gp = VGroup(eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8)
        gp.move_to(ORIGIN)
        box = self.box(gp)
        box2 = self.box(eq7, eq8)

        self.add(box)
        self.wait(0.5)
        self.play(FadeIn(eq1[:2]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(eq1[2:5]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(eq1[5:8]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(eq1[8:]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.2)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq2[:1] + eq2[2:8] + eq2[8:10] + eq2[10:],
                                       eq3[:1] + eq3[2:8] + eq3[10:12] + eq3[14:]),
                  abra.fade_replace(eq2[1], eq3[1])),
                  FadeIn(eq3[8:10], eq3[12:14]), lag_ratio=0.4),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq3[:1] + eq3[2:9] + eq3[10:13] + eq3[14:],
                                       eq4[:1] + eq4[2:9] + eq4[15:18] + eq4[24:]),
                  abra.fade_replace(eq3[1], eq4[1]),
                  abra.fade_replace(eq3[9:10], eq4[9:15]),
                  abra.fade_replace(eq3[13:14], eq4[18:24]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeIn(eq5), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq5[:2] + eq5[3:13] + eq5[13],
                                       eq6[:2] + eq6[3:13] + eq6[20]),
                  abra.fade_replace(eq5[2], eq6[2]),
                  FadeIn(eq6[13:20]),
                  run_time=1.5)
        self.wait(0.5)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq1[:2] + eq1[3:5] + eq1[6:8] + eq1[9:12],
                                       eq7[3:5] + eq7[6:8] + eq7[9:11] + eq7[12:15]),
                  abra.fade_replace(eq1[2], eq7[5]),
                  abra.fade_replace(eq1[5], eq7[8]),
                  abra.fade_replace(eq1[8], eq7[11]),
                  FadeIn(eq7[:3])), FadeIn(eq7[15:]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(eq4), run_time=1)
        self.play(FadeIn(eq8[:3]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(eq8[4]), FadeOut(eq8[2], eq6), ReplacementTransform(box, box2), run_time=1.5)
        self.wait(0.5)


class BorweinDensity(SceneOpacity):
    opacity = 0.8

    def construct(self):
        eq1 = MathTex(r'S_n=X_0+X_1+X_2+\cdots+X_n')[0].set_z_index(10)
        eq2 = MathTex(r'X_n\sim U([-1/(2n+1),1/(2n+1)])')[0].set_z_index(10).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'\varphi_{S_n}(u)={\rm sinc}(u){\rm sinc}(u/3)\cdots{\rm sinc}(u/(2n+1))')[0].set_z_index(10).next_to(eq2, DOWN).align_to(eq1, LEFT)
        g = VGroup(eq1, eq2, eq3).move_to(ORIGIN)
        eq4 = MathTex(r'\int_{-\infty}^\infty\varphi_{S_n}(u)\,du=2\pi p_{S_n}(0)')[0].set_z_index(10).move_to(eq2).align_to(eq1, LEFT)
        eq5 = MathTex(r'\int_{-\infty}^\infty{\rm sinc}(u){\rm sinc}(u/3)\cdots{\rm sinc}(u/(2n+1))\,du=2\pi p_{S_n}(0)')[0]\
            .set_z_index(10).move_to(ORIGIN)
        eq5.next_to(eq4[-7], ORIGIN, submobject_to_align=eq5[-7], coor_mask=UP)
        box1 = self.box(g)
        box2 = self.box(eq4)
        box3 = self.box(eq4, eq5)
        self.add(box1, g)
        self.wait(0.5)
        self.play(FadeOut(eq1, eq2, eq3), FadeIn(eq4), ReplacementTransform(box1, box2), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq4[:4] + eq4[-11:],
                                       eq5[:4] + eq5[-11:]),
                  ReplacementTransform(box2, box3),
                  eq4[4:-11].animate.move_to(eq5[4:-11], coor_mask=RIGHT),
                  run_time=2)
        self.play(FadeOut(eq4[4:-9]), FadeIn(eq5[4:-11]), run_time=1.5)
        self.wait(0.5)


class ProbSum(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'X+Y,\ X\sim U([-a,a])').set_z_index(10)
        eq3 = MathTex(r'\mathbb P(z\le X+Y\le z+dz\vert Y)'
                      r'{{=}}\mathbb P(z-Y\le X\le z-Y+dz\vert Y)'
                      r'{{=}} \begin{cases}0, &{\rm if\ }\lvert z-Y\rvert > a+dz \\ dz/(2a), & {\rm if\ }|z-Y| < a-dz\end{cases}')
        eq4 = MathTex(r'p_{X+Y}(z\vert Y){{=}}\begin{cases}0, &{\rm if\ }\lvert z-Y\rvert > a \\ 1/(2a), & {\rm if\ }|z-Y| < a\end{cases}'
                      r'{{=}}I(\lvert Y-z\rvert < a)/(2a)').set_z_index(10)
        eq5 = MathTex(r'p_{X+Y}(z){{=}}\mathbb P(\lvert Y-z\rvert < a)/(2a)').set_z_index(10)
        eq6 = MathTex(r'p_{X+Y}(0){{=}}\mathbb P(\lvert Y\rvert < a)/(2a)').set_z_index(10)
        eq7 = MathTex(r'Y-0')[0].set_z_index(10)
        eq8 = eq1.copy().next_to(eq6, UP, coor_mask=UP)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3], coor_mask=RIGHT)
        eq3.next_to(eq1, DOWN)
        eq4[3:5].next_to(eq4[1], ORIGIN, submobject_to_align=eq4[3], coor_mask=RIGHT)
        eq4.next_to(eq3[1], ORIGIN, submobject_to_align=eq4[1])
        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1])
        eq6.next_to(eq5[1], ORIGIN, submobject_to_align=eq6[1])
        eq7.next_to(eq5[2][4], ORIGIN, submobject_to_align=eq7[1])

        g = VGroup(eq1, eq3, eq4, eq5, eq6, eq7).move_to(ORIGIN)
        box1 = self.box(g)
        box2 = self.box(eq8, eq5)
        self.add(box1, eq1)
        self.wait(0.5)
        self.play(FadeIn(eq3[:2]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq3[2]), FadeIn(eq3[4]), run_time=1.5)
        self.wait(0.5)
        self.play(LaggedStart(FadeOut(eq3[0][3], eq3[0][7], eq3[0][9:12]),
            AnimationGroup(ReplacementTransform(eq3[0][1:2] + eq3[0][5:7] + eq3[0][2] + eq3[0][-3:] + eq3[1],
                                       eq4[0][4:5] + eq4[0][2:4] + eq4[0][5] + eq4[0][-3:] + eq4[1]),
                  ReplacementTransform(eq3[0][8], eq4[0][5]),
                  abra.fade_replace(eq3[0][0], eq4[0][0]),
                  abra.fade_replace(eq3[0][4], eq4[0][1]),
                  ReplacementTransform(eq3[4][:12] + eq3[4][17:32],
                                       eq4[2][:12] + eq4[2][13:28]),
                  FadeOut(eq3[4][12:15], eq3[4][32:35]),
                  abra.fade_replace(eq3[4][15:17], eq4[2][12])
                           ), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(eq4[2]), FadeIn(eq4[4]), run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(box1, box2),
                  eq1.animate.move_to(eq8),
            FadeOut(eq4[0][6:8]),
                  ReplacementTransform(eq4[0][:6] + eq4[0][8] + eq4[1] + eq4[4][1:],
                                       eq5[0][:6] + eq5[0][6] + eq5[1] + eq5[2][1:]),
                  abra.fade_replace(eq4[4][0], eq5[2][0]),
                  run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(eq5[0][:5] + eq5[0][6] + eq5[1],
                                       eq6[0][:5] + eq6[0][6] + eq6[1]),
                  abra.fade_replace(eq5[0][5], eq6[0][5]),
                  abra.fade_replace(eq5[2][5], eq7[2]),
                  run_time=1.5)
        self.play(FadeOut(eq5[2][4], eq7[2]),
                  ReplacementTransform(eq5[2][:4] + eq5[2][6:], eq6[2][:4] + eq6[2][4:]),
                  run_time=1)
        self.wait(0.5)


class BorweinSn(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'S_n=X_1+X_2+\cdots+X_n')[0].set_z_index(10)
        eq2 = MathTex(r'\int_{-\infty}^\infty \varphi_{X_0+S_n}(u)\,du'
                      r'{{=}}2\pi p_{X_0+S_n}(0)'
                      r'{{=}}2\pi\mathbb P(\lvert S_n\rvert\le1)/2'
                      r'{{=}}\pi\mathbb P(\lvert S_n\rvert\le 1)').set_z_index(10)
        eq3 = MathTex(r'\int_{-\infty}^\infty {\rm sinc}(u){\rm sinc}(u/3)\cdots{\rm sinc}(u/(2n+1))\,du'
                      r'{{=}}\pi\mathbb P(\lvert S_n\rvert\le 1)').set_z_index(10)

        eq2[3:5].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[3], coor_mask=RIGHT)
        eq2[5:7].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[5], coor_mask=RIGHT)
        eq2.next_to(eq1, DOWN)
        eq3.next_to(eq2[1], ORIGIN, submobject_to_align=eq3[1], coor_mask=UP)

        box1 = self.box(eq1, eq2)
        box2 = self.box(eq1, eq3)
        self.add(box1, eq1[:3])
        self.wait(0.5)
        self.play(FadeIn(eq1[3:]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq2[0]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq2[1]), run_time=0.5)
        self.play(FadeIn(eq2[2]), run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq2[2][:2] + eq2[2][6:8] + eq2[2][8] + eq2[2][10],
                                       eq2[4][:2] + eq2[4][5:7] + eq2[4][3] + eq2[4][10]),
                  abra.fade_replace(eq2[2][2], eq2[4][2]),
                  FadeOut(eq2[2][3:6], eq2[2][9]),
                  FadeIn(eq2[4][4], eq2[4][7:10], eq2[4][11:]),
                  run_time=1.5)
        self.wait(0.2)
        line1 = Line(eq2[4][0].get_corner(DL) + DL * 0.1, eq2[4][0].get_corner(UR) + UR*0.1, color=RED,
                     stroke_width=4).set_z_index(20)
        line2 = line1.copy().shift(eq2[4][-1].get_center()-eq2[4][0].get_center())
        self.play(FadeIn(line1, line2), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(eq2[4][0], eq2[4][-2:], line1, line2), run_time=1)
#        self.play(ReplacementTransform(eq2[4][1:-2], eq2[6][:]), run_time=0.8)
        self.wait(0.5)
        self.play(ReplacementTransform(box1, box2),
            ReplacementTransform(eq2[0][:4] + eq2[0][-2:] + eq2[1] + eq2[4][1:-2],
                                       eq3[0][:4] + eq3[0][-2:] + eq3[1] + eq3[2][:]),
                  eq2[0][4:-2].animate.move_to(eq3[0][4:-2], coor_mask=RIGHT),
                  run_time=1.5)
        self.play(FadeOut(eq2[0][4:-2]), FadeIn(eq3[0][4:-2]), run_time=1)
        self.wait(0.5)


class AltInt(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\mathbb P\left(X_n=\frac1{2n+1}\right)=\mathbb P\left(X_n=\frac{-1}{2n+1}\right)=\frac12').set_z_index(10)
        eq2 = MathTex(r'\varphi_{X_n}(u){{=}}\cos (u/(2n+1))').set_z_index(10).next_to(eq1, DOWN)
        eq3 = MathTex(r'\varphi_{X_0+S_n}(u){{=}}{\rm sinc}(u)\cos(u/3)\cdots\cos(u/(2n+1))').set_z_index(10).next_to(eq1, DOWN)
        eq4 = MathTex(r'\int_{-\infty}^\infty\varphi_{X_0+S_n}(u)\,du {{=}} \pi\mathbb P(\lvert S_n\rvert < 1)'
                      r'{{=}}0.984375\pi').set_z_index(10).next_to(eq1, DOWN)
        eq5 = MathTex(r'\pi\mathbb P(\lvert S_7\rvert < 1)')[0].set_z_index(10)
        eq6 = MathTex(r'\mathbb P(S_7 \ge 1){{=}}(1/2)^7').set_z_index(10)
        eq7 = MathTex(r'\mathbb P(\lvert S_7\rvert \ge 1){{=}}2(1/2)^7{{=}}(1/2)^6').set_z_index(10)
        eq8 = MathTex(r'\mathbb P(\lvert S_7\rvert < 1){{=}}1-(1/2)^6{{=}}0.984375')
        eq4[3:5].next_to(eq4[1], ORIGIN, submobject_to_align=eq4[3], coor_mask=RIGHT)
        eq7[3:5].next_to(eq7[1], ORIGIN, submobject_to_align=eq7[3], coor_mask=RIGHT)
        eq7.move_to(ORIGIN, coor_mask=RIGHT)
        eq8[3:5].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[3], coor_mask=RIGHT)
        eq3_1 = eq3.copy().align_to(eq1, UP)
        eq4.next_to(eq3_1, DOWN, coor_mask=UP)
        eq5.next_to(eq4[2][0], ORIGIN, submobject_to_align=eq5[0])
        eq5[5].set_color(PURE_RED)

        box1 = self.box(eq1, eq2, eq3)
        box2 = self.box(eq3_1, eq4)
        self.add(box1, eq1)
        self.wait(0.5)
        self.play(FadeIn(eq2), run_time=2)
        self.wait(0.5)
        self.play(FadeOut(eq2), FadeIn(eq3), run_time=2)
        self.play(ReplacementTransform(box1, box2),
                  eq3.animate.move_to(eq3_1), FadeIn(eq4[:3]), FadeOut(eq1), run_time=2)
        self.wait(0.5)
        eqtmp0 = eq4[0][9]
        for i in range(1, 8):
            eqtmp = MathTex(r'\varphi_{{X_0+S_{{\bf {} }} }}'.format(i), color=PURE_RED)[0].set_z_index(10)
            eqtmp.next_to(eq4[0][4], ORIGIN, submobject_to_align=eqtmp[0][0])
            eqtmp1 = eqtmp[-1]
            FO = [eqtmp0]
            FI = [eqtmp1]
            if i == 1:
                FO.append(eq4[2][1:])
            if i == 7:
                FI.append(eq5[1:])
            self.play(FadeOut(*FO), FadeIn(*FI), run_time=0.5)
            eqtmp0 = eqtmp1
            self.wait(0.5)

        eq4[0][9].set_opacity(0)
        eq4[2][1:].set_opacity(0)
        eq5[0].set_opacity(0)
        eq4[3:].set_opacity(0)
        gp = VGroup(eq4, eqtmp0, eq5)
        eq6.next_to(gp.copy().align_to(eq3, UP), DOWN, coor_mask=UP)
        eq7.next_to(eq6[1], ORIGIN, submobject_to_align=eq7[1], coor_mask=UP)
        eq8.next_to(eq6[1], ORIGIN, submobject_to_align=eq8[1])

        self.play(FadeOut(eq3), gp.animate.align_to(eq3, UP),
                  FadeIn(eq6),
                  run_time=1.5)
        self.wait(0.5)
        self.play(ReplacementTransform(eq6[0][:2] + eq6[0][2:4] + eq6[0][4:] + eq6[1] + eq6[2][:],
                                       eq7[0][:2] + eq7[0][3:5] + eq7[0][6:] + eq7[1] + eq7[2][1:]),
                  FadeIn(eq7[0][2], eq7[0][5], eq7[2][0]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq7[2][0]),
                  ReplacementTransform(eq7[2][1:6], eq7[4][:5]),
                  abra.fade_replace(eq7[2][6], eq7[4][5]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq7[0][:6] + eq7[0][7:] + eq7[1] + eq7[4][:],
                                       eq8[0][:6] + eq8[0][7:] + eq8[1] + eq8[2][2:]),
                  abra.fade_replace(eq7[0][6], eq8[0][6]),
                  FadeIn(eq8[2][:2]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq8[2]), FadeIn(eq8[4]), run_time=1.5)
        self.wait(0.2)
        eq4[4].set_opacity(1)
        self.remove(eq4[4])
        self.play(FadeOut(eq5[1:]),
                  ReplacementTransform(eq8[4][:].copy() + eq4[2][0], eq4[4][:-1] + eq4[4][-1]),
                  run_time=1.5)

        self.wait(0.5)


class CosInt(Scene):
    def construct(self):
        n1 = 115
#        n1 = 7
        str = r'{{\int_{-\infty}^\infty 2\cos x\frac{\sin(x)}{x} }}'
        for i in range(3, n1, 2): # 117
            str += r'{{{{\frac{{\sin(x/{0})}}{{x/{0} }} }}}}'.format(i)
        eq = MathTex(str, stroke_width=1.5)
        pt = Point().to_edge(DL).get_corner(DL)
        eq.next_to(pt, UR, submobject_to_align=eq[0])
        eq_tmp = MathTex(r'{{ \frac{\sin(x)}{x} }}{{dx=\pi}}')
        eq1 = eq_tmp[1]
        eq_shift = eq1.get_left() - eq_tmp[0].get_right()
        right = config.frame_x_radius - 0.01
        bottom = 0.02-config.frame_y_radius
        eq.set_opacity(0)
        eq[0].set_opacity(1)
        eq1.move_to(eq[0].get_right() + eq_shift, LEFT)
#        eq1.next_to(eq[0], RIGHT)
        self.add(eq, eq1)
        self.wait(0.5)
        for i in range(1, len(eq)):
            if eq[i].get_right()[0] > right:
                eq[i:].next_to(eq[i-1], DOWN).align_to(eq[0], LEFT)
            shift_up = bottom - eq[i].get_bottom()[1]
            eq[i].set_opacity(1)
            if i == len(eq)-1:
                anims = [eq1[-1].animate.set_opacity(0)]
            else:
                anims = []
            if shift_up > 0:
                self.play(FadeIn(eq[i]),
                          eq.animate.shift(UP*shift_up),
                          eq1.animate.move_to(eq[i].get_right() + eq_shift + UP*shift_up, LEFT),
                          *anims,
                          run_time=0.1)

            self.play(FadeIn(eq[i]),
                      eq1.animate(rate_func=linear).move_to(eq[i].get_right()+eq_shift, LEFT),
                      *anims,
                      run_time=0.1)
            self.wait(0.5)
            eq2 = MathTex(r'=0.' + r'9' * 137 + r'85\cdots\pi')[0] #137
            eq2.next_to(eq1[-2], ORIGIN, submobject_to_align=eq2[0]).set_opacity(0)

        for i in range(len(eq2[:]) - 1):
            if eq2[i].get_right()[0] + 0.2 > right:
                eq2[i:].next_to(VGroup(eq, eq1, eq2[i-1]), DOWN).align_to(eq[0], LEFT)
            shift_up = bottom - eq2[i].get_bottom()[1]
            if shift_up > 0:
                self.play(VGroup(eq, eq1, eq2).animate.shift(UP*shift_up), run_time=0.1)
            self.add(eq2[i].set_opacity(1))
            self.wait(1/config.frame_rate * 1.1)
        self.wait(0.5)
        self.play(eq2[-1].animate.set_opacity(1), run_time=1)


        self.wait(0.1)


class CosIntMath(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\mathbb P(Y=1)=\mathbb P(Y=-1)=1/2').set_z_index(10)
        eq2 = MathTex(r'\varphi_Y(u)=\cos(u)').set_z_index(10).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'\varphi_{Y+X_0+S_n}(u)'
                      r'{{=}}\varphi_Y(u)\varphi_{X_0+S_n}(u)'
                      r'{{=}}\cos(u){\rm sinc}(u){\rm sinc}(u/3)\cdots{\rm sinc}(u/(2n+1))').set_z_index(10).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3], coor_mask=RIGHT)
        gp = VGroup(eq1, eq2, eq3).move_to(ORIGIN)

        box1 = self.box(eq1, eq2)
        box2 = self.box(eq1, eq3[:3])
        box3 = self.box(eq1, eq3)

        self.add(box1, eq1, eq2)

        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform(box1, box2), FadeIn(eq3[:3]), lag_ratio=0.5), run_time=1)
        self.wait(0.2)
        self.play(abra.fade_replace(eq3[2][:5], eq3[4][:6], coor_mask=RIGHT), run_time=1.2)
        self.play(LaggedStart(ReplacementTransform(box2, box3), AnimationGroup(FadeOut(eq3[2][5:]), FadeIn(eq3[4][6:])),
                              lag_ratio=0.5), run_time=1.2)
        eq3[2:4].set_opacity(0)
        self.play(FadeOut(eq1, eq2), eq3.animate.align_to(eq1, UP), run_time=1.2)
        self.wait(0.2)
        eq5 = MathTex(r'Y+X_0\sim\begin{cases}U([0,2]) & {\rm if\ }Y=1,\\ U([-2,0]) & {\rm if\ }Y=-1\end{cases}')[0].set_z_index(10).next_to(eq3, DOWN).align_to(eq3, LEFT)
        eq4 = MathTex(r'X_0\sim U([-1,1])')[0].set_z_index(10)
        eq4.next_to(eq5[2:5], ORIGIN, submobject_to_align=eq4[:3])
        box4 = self.box(eq3, eq5)
        self.play(ReplacementTransform(box3, box4), FadeIn(eq4), run_time=1)
        self.wait(0.2)
        self.play(FadeOut(eq4), FadeIn(eq5), run_time=1.5)
        self.wait(0.2)

        eq6 = MathTex(r'Y+X_0\sim U([-2, 2])')[0].set_z_index(10)
        eq6_1 = eq6.copy().next_to(eq3, DOWN).align_to(eq3, LEFT)
        eq6.next_to(eq5[4], ORIGIN, submobject_to_align=eq6[4])
        eq6[5:].align_to(eq5[6], LEFT)

        self.play(eq5[11:14].animate.align_to(eq6[11], LEFT), run_time=0.6)
        self.play(ReplacementTransform(eq5[:5], eq6[:5]),
                  ReplacementTransform(eq5[6:9], eq6[5:8]),
                  ReplacementTransform(eq5[20:26], eq6[5:11]),
                  ReplacementTransform(eq5[11:14], eq6[11:14]),
                  ReplacementTransform(eq5[27:29], eq6[12:14]),
                  FadeOut(eq5[5], eq5[14:20], eq5[29:]),
                  FadeOut(eq5[9:11], target_position=eq6[8]),
                  FadeOut(eq5[26], target_position=eq6[11]),
                  run_time=2)
        self.play(ReplacementTransform(eq6, eq6_1), run_time=1)
        self.wait(0.2)

        eq7 = MathTex(r'\int_{-\infty}^\infty \varphi_{Y+X_0+S_n}(u)\,du'
                      r'{{=}}2\pi p_{Y+X_0+S_n}(0)'
                      r'{{=}}2\pi\mathbb P(\lvert S_n\rvert < 2)/4').set_z_index(10)
        eq7[3:5].next_to(eq7[1], ORIGIN, submobject_to_align=eq7[3], coor_mask=RIGHT)
        eq7.next_to(eq6_1, DOWN).align_to(eq3, LEFT)
        eq7_1 = MathTex(r'2').move_to(eq7[4][-1]).set_z_index(10)

        eq8 = MathTex(r'\int_{-\infty}^\infty 2\varphi_{Y+X_0+S_n}(u)\,du'
                      r'{{=}}\pi\mathbb P(\lvert S_n\rvert < 2)').set_z_index(10).move_to(eq7).align_to(eq7, LEFT)
        box5 = self.box(eq3, eq7)

        self.play(LaggedStart(ReplacementTransform(box4, box5), FadeIn(eq7[:3]), lag_ratio=0.5), run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq7[2][:2] + eq7[2][8:10] + eq7[2][10] + eq7[2][12],
                                       eq7[4][:2] + eq7[4][5:7] + eq7[4][3] + eq7[4][10]),
                  abra.fade_replace(eq7[2][2], eq7[4][2]),
                  FadeOut(eq7[2][3:8], eq7[2][11]),
                  FadeIn(eq7[4][4], eq7[4][7:10], eq7[4][11:]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq7[4][0], eq7[4][-1]), FadeIn(eq7_1), run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq7[0][:4] + eq7[0][4:] + eq7_1 + eq7[1] + eq7[4][1:-2],
                                       eq8[0][:4] + eq8[0][5:] + eq8[0][4] + eq8[1] + eq8[2][:]),
                  FadeOut(eq7[4][-2]),
                  run_time=2)
        self.wait(0.2)
        self.play(FadeOut(eq6_1), eq8.animate.next_to(eq3, DOWN, coor_mask=UP), run_time=1)
        self.wait(0.2)

        eq9 = MathTex(r'1/3+1/5+\cdots+1/113 = 2.0032\ldots').next_to(eq8, DOWN)
        self.play(FadeIn(eq9), run_time=1)

        self.wait(0.5)


class BigNumber(Scene):
    def construct(self):
        num = '001569077070516060928419448874747821551524926829820273852815836448212983665876813483232100703157659223980553468025374126831601055511443556277350638168485268670581505978001035213957013220119308355774556826995014546530662974055048240333477592898399601659803106957890547802814016489317314012540596568503675217623424090233844693031044330866338901649257171209259349727479870471070229558275972160005597077140997595562858828631593176726962223613086208611784047251824501164252220812534634727675751476613624404767871484636683298978159342499577103531615819215167517705897209337522512438255293032766035839849809366559417153502392937165484021304018990053794223563792922467989147962933238674467542103007498929180550306476430528205796520520822099932869221650202860450483774498660610909669824829771782814518455310762100173471158886158031343099553120048438206253288540064495450101249872360507906465'
        num1 = ''
        for i in range(3, len(num), 3):
            num1 += num[max(i-3,0):i] + '\,'
        num1 += num[i:]

        eq1 = MathTex(num1, font_size=47)[0].to_edge(UL, buff=0.2)
        right = config.frame_x_radius - 0.2

        for i in range(3, len(eq1[:]), 3):
            if eq1[i+2].get_right()[0] > right:
                eq1[i:].next_to(eq1[:i], DOWN, buff=0.1).align_to(eq1[0], LEFT)

        eq1.move_to(ORIGIN)
        self.add(eq1[2:])


class SincHarmonic(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\int_{-\infty}^\infty {\rm sinc}(x)\,dx{{=}}\pi').set_z_index(10)
        eq2 = MathTex(r'\int_{-\infty}^\infty {\rm sinc}(x){\rm sinc}(x/2)\,dx{{=}}\pi').set_z_index(10)
        eq3 = MathTex(r'\int_{-\infty}^\infty {\rm sinc}(x){\rm sinc}(x/2){\rm sinc}(x/3)\,dx{{=}}\pi').set_z_index(10)

        box1 = self.box(eq1)
        box2 = self.box(eq2)
        box3 = self.box(eq3)

        self.add(eq1, box1)
        self.wait(0.2)
        self.play(ReplacementTransform(box1, box2),
            ReplacementTransform(eq1[0][:11] + eq1[0][11:] + eq1[1:],
                                       eq2[0][:11] + eq2[0][20:] + eq2[1:]),
                  FadeIn(eq2[0][11:20]),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(box2, box3),
            ReplacementTransform(eq2[0][:20] + eq2[0][20:] + eq2[1:],
                                       eq3[0][:20] + eq3[0][29:] + eq3[1:]),
                  FadeIn(eq3[0][20:29]),
                  run_time=1)
        self.wait(0.5)


class Sinc2025(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'{{\int_{-\infty}^\infty\frac{\sin(2025x)}{x} }}\,dx {{=}} \pi').set_z_index(1)
        eq2 = MathTex(r'{{\int_{-\infty}^\infty\frac{\sin(2025x)}{x} }}{{ {\rm sinc}(x)}}\,dx {{=}} \pi').set_z_index(1)
        eq3 = MathTex(r'{{\int_{-\infty}^\infty\frac{\sin(2025x)}{x} }}{{ {\rm sinc}(x)}}{{ {\rm sinc}(x/2) }}'
                      r'\,dx {{=}} \pi').set_z_index(1)
        eq4 = MathTex(r'{{\int_{-\infty}^\infty\frac{\sin(2025x)}{x} }}{{ {\rm sinc}(x)}}{{ {\rm sinc}(x/2) }}'
                      r'{{ {\rm sinc}(x/3)}}\,dx {{=}} \pi').set_z_index(1)
        eq5 = MathTex(r'{{\int_{-\infty}^\infty\frac{\sin(2025x)}{x} }}{{ {\rm sinc}(x)}}{{ {\rm sinc}(x/2) }}'
                      r'{{ {\rm sinc}(x/3)}}{{ {\rm sinc}(x/4)}}\,dx {{=}} \pi').set_z_index(1)

        box1 = self.box(eq1)
        box2 = self.box(eq2)
        box3 = self.box(eq3)
        box4 = self.box(eq4)
        box5 = self.box(eq5)

        self.add(box1, eq1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq1[1:] + eq1[0], eq2[2:] + eq2[0]),
                  FadeIn(eq2[1]),
                  ReplacementTransform(box1, box2),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq2[:2] + eq2[2:], eq3[:2] + eq3[3:]),
                  FadeIn(eq3[2]),
                  ReplacementTransform(box2, box3),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq3[:3] + eq3[3:], eq4[:3] + eq4[4:]),
                  FadeIn(eq4[3]),
                  ReplacementTransform(box3, box4),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq4[:4] + eq4[4:], eq5[:4] + eq5[5:]),
                  FadeIn(eq5[4]),
                  ReplacementTransform(box4, box5),
                  run_time=1)
        self.wait(0.5)


class SincSquared(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\int_{-\infty}^\infty{\rm sinc}(x)\,dx{{=}}\pi').set_z_index(1)
        eq2 = MathTex(r'\int_{-\infty}^\infty{\rm sinc}(x)^2\,dx{{=}}{\rm ?} {{=}} \pi\mathbb P(\lvert X\rvert < 1)'
                      r'{{\pi}}{{=}}\int_{-\infty}^\infty{\rm sinc}(x)\,dx')\
            .set_z_index(1)
        eq2.next_to(ORIGIN, ORIGIN, submobject_to_align=eq2[:3])
        eq2[3:5].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[3], coor_mask=RIGHT)
        eq2[5:8].next_to(eq2[4][0], ORIGIN, submobject_to_align=eq2[5][0], coor_mask=RIGHT)
        eq3 = MathTex(r'X\sim U([-1,1])')[0].set_z_index(1).next_to(eq2[4], DOWN).align_to(eq2[4], RIGHT)
        eq2_1 = eq2[4][-2].copy().move_to(eq2[4][1:], coor_mask=RIGHT)

        box1 = self.box(eq1)
        box2 = self.box(eq2[:5], eq3)
        eq4 = VGroup(*eq2[:2], eq2[4][0], *eq2[6:]).copy().move_to(ORIGIN)
        box3 = self.box(eq4)

        self.add(box1, eq1)
        self.wait(0.5)
        self.play(ReplacementTransform(eq1[0][:11] + eq1[0][11:] + eq1[1],
                                       eq2[0][:11] + eq2[0][12:] + eq2[1]),
                  FadeIn(eq2[0][11]),
                  FadeOut(eq1[2]),
                  run_time=0.8)
        self.play(FadeIn(eq2[2]), run_time=0.6)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform(box1, box2),
                              AnimationGroup(FadeOut(eq2[2]), FadeIn(eq2[4], eq3)),
                              lag_ratio=0.5), run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq2[4][1:]), FadeIn(eq2_1), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(eq2_1, eq3), run_time=0.7)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(box2, box3),
                              AnimationGroup(ReplacementTransform(eq2[:2] + eq2[4][0], eq4[:2] + eq4[2]),
                                             FadeIn(eq4[3:])), lag_ratio=0.5), run_time=2)
        self.wait(0.5)


class EVInt(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\mathbb E\left[ f(U)\right]{{=}}\int_0^1 f(x)\,dx{{=}}1').set_z_index(1)
        eq2 = MathTex(r'\mathbb E\left[ f(U)^2\right]{{=}}\int_0^1 f(x)^2\,dx{{=}}1').set_z_index(1)
        eq2.next_to(eq1[0], DOWN, submobject_to_align=eq2[0]).align_to(eq1[0], LEFT)
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
        eq2[3:5].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[3], coor_mask=RIGHT)

        VGroup(eq1, eq2).move_to(ORIGIN)

        eq3 = MathTex(r'{\rm Var}\left(f(U)\right){{=}}\mathbb E\left[f(U)^2\right]-\mathbb E\left[f(U)\right]^2{{=}}0').set_z_index(1)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3], coor_mask=RIGHT)
        eq3.next_to(eq2[0], DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'{{=}}11').set_z_index(1)
        eq4.next_to(eq3[1], ORIGIN, submobject_to_align=eq4[0])
        eq4[1][0].move_to(eq3[2][:8], coor_mask=RIGHT)
        eq4[1][1].move_to(eq3[2][9:], coor_mask=RIGHT)

        eq5 = MathTex(r'\mathbb E\left[ f(U)^p\right]{{=}}1').set_z_index(1).next_to(eq2[0], DOWN).align_to(eq1, LEFT)

        box1 = self.box(eq1)
        box2 = self.box(eq1[:2], eq1[4], eq2)
        box3 = self.box(eq1[:2], eq3)
        box4 = self.box(eq1[:2], eq1[4], eq3[:2], eq3[4])
        self.add(box1, eq1[:2])
        self.wait(0.2)
        self.play(FadeOut(eq1[2]), FadeIn(eq1[4]), run_time=1.5)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(box1, box2), FadeIn(eq2[:3]), lag_ratio=0.5), run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq2[2]), FadeIn(eq2[4]), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(box2, box3), FadeIn(eq3[:2]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq3[2][:8]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq3[2][8:]), run_time=1)
        self.wait(0.2)
        self.play(FadeOut(eq3[2][:8], eq3[2][9:]), FadeIn(eq4[1]), run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq4[1][0], target_position=eq3[4][0]),
                  FadeOut(eq4[1][1], target_position=eq3[4][0]),
                  FadeOut(eq3[2][8], target_position=eq3[4][0]),
                  FadeIn(eq3[4]),
                  ReplacementTransform(box3, box4),
                  run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(eq3[:2], eq3[4]),
                  FadeIn(eq5),
                  run_time=1.5)
        self.wait(0.5)


class Question2025(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'{{\int_0^1 f(x)g(x)^ndx}}=1,\ n=0,1,\ldots,2025').set_z_index(1)
        eq2 = MathTex(r'{{\int_0^1 f(x)g(x)^ndx}}\begin{cases}=1,& n=0,1,\ldots,2025, \\ < 1, &n > 2025\end{cases').set_z_index(1)
        eq1.next_to(eq2[0], ORIGIN, submobject_to_align=eq1[0])

        box = self.box(eq1, eq2)

        self.add(box, eq1[0])
        self.wait(0.2)
        self.play(FadeIn(eq1[1][:2]), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(eq1[1][2:]), run_time=1)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(eq1[1][:] + eq1[0], eq2[1][1:18] + eq2[0]),
                  FadeIn(eq2[1][0], eq2[1][18]), lag_ratio=0.5),
                  run_time=1.8)
        self.wait(0.2)
        self.play(FadeIn(eq2[1][19:]), run_time=1)
        self.wait(0.5)


class CharacteristicInt(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\varphi_X(u){{=}}\mathbb E\left[e^{iuX}\right]').set_z_index(1)
        eq2 = MathTex(r'\int_0^1\varphi_X(2\pi u)\,du{{=}}\int_0^1\mathbb E\left[e^{2\pi iuX}\right]du'
                      r'{{=}}\mathbb E\left[\int_0^1e^{2\pi iuX}du\right]').set_z_index(1)
        eq2[3:5].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[3], coor_mask=RIGHT)
        eq2.next_to(eq1, DOWN)#.align_to(eq1, LEFT)
        eq2_2 = eq2.copy().align_to(eq1, UP)
        eq3 = MathTex(r'\int_0^1e^{2\pi iuX}du{{=}}\begin{cases}0, &{\rm if\ }X\not=0,\\ 1,&{\rm if\ }X=0\end{cases}').set_z_index(1)
        eq3.next_to(eq2_2, DOWN).align_to(eq2, LEFT)
        eq4 = MathTex(r'{{=}}I(X=0)').set_z_index(1)
        eq4.next_to(eq2_2[1], ORIGIN, submobject_to_align=eq4[0])
        eq4[1].move_to(eq2_2[4][2:-1], coor_mask=RIGHT)
        eq5 = MathTex(r'\int_0^1\varphi_X(2\pi u)\,du{{=}}\mathbb P(X=0)').set_z_index(1)
        eq5.next_to(eq2_2[1], ORIGIN, submobject_to_align=eq5[0]).move_to(ORIGIN, coor_mask=RIGHT)

        box = self.box(eq1, eq2, eq3)

        self.add(box, eq1)
        self.wait(0.2)
        self.play(FadeIn(eq2[0]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq2[1:3]), run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq2[2][:3] + eq2[2][3:5] + eq2[2][-2:] + eq2[2][5:-3],
                                       eq2[4][2:5] + eq2[4][:2] + eq2[4][-3:-1] + eq2[4][5:-3]),
                  abra.fade_replace(eq2[2][-3], eq2[4][-1]),
                  run_time=1.5)
        self.wait(0.2)
        eq2[2:4].set_opacity(0)
        self.play(eq2.animate.move_to(eq2_2), FadeIn(eq3[:2], eq3[2][:9]), FadeOut(eq1), run_time=1.5)
        self.wait(0.2)
        self.play(FadeIn(eq3[2][9:]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq4[1]), FadeOut(eq2[4][2:-1]), run_time=1.5)
        self.wait(0.2)
        self.play(LaggedStart(FadeOut(eq4[1][0], eq2[4][1], eq2[4][-1], eq3),
                  AnimationGroup(ReplacementTransform(eq4[1][1:] + eq2[:2], eq5[2][1:] + eq5[:2]),
                  abra.fade_replace(eq2[4][0], eq5[2][0])), lag_ratio=0.5),
                  run_time=2)

        self.wait(0.5)


class RandomIntXY(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\mathbb P(X=-2025)=\mathbb P(X=-2024)=\cdots=\mathbb P(X=2025){{=}}\frac1{5051}').set_z_index(1)
        eq1.move_to(ORIGIN)
        eq2 = MathTex(r'\mathbb P(Y_n=1)=\mathbb P(Y_n=-1){{=}}\frac12').set_z_index(1)
        eq2.next_to(eq1[0], DOWN).move_to(ORIGIN, coor_mask=RIGHT)

        eq3 = MathTex(r'\varphi_X(x){{=}}\frac{\sin(5051x/2)}{\sin(x/2)}').set_z_index(1)
        eq3.align_to(eq1, UP)
        eq4 = MathTex(r'\varphi_{Y_k}(x){{=}}\cos(x)').set_z_index(1)
        eq4.next_to(eq2[1], ORIGIN, submobject_to_align=eq4[1], coor_mask=UP).align_to(eq3, LEFT)

        eq5 = MathTex(r'S_n{{=}}Y_1+Y_2+\cdots+Y_n').set_z_index(1)
        eq5.next_to(eq4, DOWN).align_to(eq4, LEFT)
        eq6 = MathTex(r'\varphi_{X+S_n}(x){{=}}\varphi_X(x)\varphi_{Y_k}(x)^n').set_z_index(1)
        eq6.next_to(eq5, DOWN).align_to(eq5, LEFT)

        eq7 = MathTex(r'f(x){{=}}5051\varphi_X(2\pi x){{=}}\frac{\sin(5051\pi x)}{\sin(\pi x)}').set_z_index(1)
        eq7.align_to(eq1, UP).align_to(eq6, LEFT).shift(LEFT)
        eq8 = MathTex(r'g(x){{=}}\varphi_{Y_k}(2\pi x){{=}}\cos(2\pi x)').set_z_index(1)
        eq8.next_to(eq7, DOWN).align_to(eq7, LEFT)

        eq9 = MathTex(r'\int_0^1\varphi_X(2\pi x)\varphi_{Y_k}(2\pi x)^ndx{{=}}\mathbb P(X+S_n=0)'
                      r'{{=}}\frac{\mathbb P(\lvert S_n\rvert\le 2025)}{5051}').set_z_index(1)
        eq9[3:5].next_to(eq9[1], ORIGIN, submobject_to_align=eq9[3], coor_mask=RIGHT)
        eq9.next_to(eq8, DOWN).align_to(eq8, LEFT)

        eq10 = MathTex(r'\int_0^1 5051\varphi_X(2\pi x)\varphi_{Y_k}(2\pi x)^ndx{{=}}\mathbb P(\lvert S_n\rvert\le 2025)').set_z_index(1)
        eq10.next_to(eq9[1], ORIGIN, submobject_to_align=eq10[1])

        eq11 = MathTex(r'\int_0^1f(x)g(x)^ndx{{=}}\mathbb P(\lvert S_n\rvert\le 2025)').set_z_index(1)
        eq11.next_to(eq10[1], ORIGIN, submobject_to_align=eq11[1], coor_mask=UP)
        eq11_1 = eq11[0][3:7].copy().move_to(eq10[0][3:14], coor_mask=RIGHT)
        eq11_2 = eq11[0][7:12].copy().move_to(eq10[0][14:23], coor_mask=RIGHT)

        box1 = self.box(eq1, eq2)
        box2 = self.box(eq2, eq3, eq4, eq5, eq6, eq7, eq8)
        box3 = self.box(eq7, eq8, eq9)
        box4 = self.box(eq7, eq8, eq9, eq10, eq11)
        box5 = self.box(eq11)

        self.add(box1, eq1[0])
        self.wait(0.2)
        self.play(FadeIn(eq1[1:]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.2)
        self.play(LaggedStart(AnimationGroup(FadeOut(eq1), FadeIn(eq3)),
                  ReplacementTransform(box1, box2), lag_ratio=0.5), run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq2), FadeIn(eq4), run_time=1.5)
        self.wait(0.2)
        self.play(FadeIn(eq5), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq6[0]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq6[1:]), run_time=1)
        self.wait(0.2)
        self.play(FadeOut(eq3, eq4, eq5), FadeIn(eq7[:3], eq8[:3]), run_time=1.5)
        self.wait(0.2)
        self.play(FadeIn(eq7[3:], eq8[3:]), run_time=1)
        self.wait(0.2)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq6[2][:3] + eq6[2][3:9] + eq6[2][9:12],
                                       eq9[0][3:6] + eq9[0][8:14] + eq9[0][16:19]),
                  FadeOut(eq6[:2])),
                  FadeIn(eq9[0][:3], eq9[0][-2:], eq9[0][6:8], eq9[0][14:16]),
                              lag_ratio=0.5), run_time=2)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(box2, box3), FadeIn(eq9[1:3]), lag_ratio=0.5), run_time=1.5)
        self.wait(0.2)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq9[2][:2] + eq9[2][4:6] + eq9[2][8],
                                       eq9[4][:2] + eq9[4][3:5] + eq9[4][11]),
                  FadeOut(eq9[2][2:4], eq9[2][6:8])),
                  FadeIn(eq9[4][2], eq9[4][5:11], eq9[4][12]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.2)
        self.play(FadeIn(eq9[4][13:]), run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq9[0][:3] + eq9[4][-4:] + eq9[0][3:] + eq9[1] + eq9[4][:12],
                                       eq10[0][:3] + eq10[0][3:7] + eq10[0][7:] + eq10[1] + eq10[2][:]),
                  ReplacementTransform(box3, box4),
                  FadeOut(eq9[4][12]),
                  run_time=2)
        self.wait(0.2)
        self.play(FadeOut(eq10[0][3:23]), FadeIn(eq11_1, eq11_2), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq10[0][:3] + eq11_1 + eq11_2 + eq10[0][23:] + eq10[1:],
                                       eq11[0][:3] + eq11[0][3:7] + eq11[0][7:12] + eq11[0][12:] + eq11[1:]),
                  run_time=2)
        self.wait(0.2)
        self.play(LaggedStart(FadeOut(eq7, eq8), ReplacementTransform(box4, box5), lag_ratio=0.5), run_time=1.5)

        self.wait(0.5)


class WalkSn(Scene):
    def construct(self):
        xrange = 2030
        yrange = xrange
        xmax = 2125
        ax = Axes(x_range=[0, xrange+150, 2025], y_range=[-2400, 2400, 2025], x_length=config.frame_x_radius * 1.6,
                  y_length=config.frame_y_radius * 1.3,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': True, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': True}).set_z_index(20).shift(UP * 0.8)

        pa = ax.coords_to_point(0, 2025)
        pb = ax.coords_to_point(0, -2025)
        p0 = ax.coords_to_point(0, 0)
        w = ax.coords_to_point(2125, 0) - p0
        dx = 1000.0/((ax.coords_to_point(1000, 0) - p0)[0])
        line1=Line(pa, pa+w, stroke_width=4, color=RED).set_z_index(15)
        line2=Line(pb, pb+w, stroke_width=4, color=RED).set_z_index(15)
        eq1 = MathTex(r'2025', font_size=40).next_to(pa, LEFT, buff=0.2).set_z_index(10)
        eq2 = MathTex(r'-2025', font_size=40).next_to(pb, LEFT, buff=0.2).set_z_index(10)
        eq0 = MathTex(r'2025', font_size=40).next_to(ax.coords_to_point(2025, 0), DOWN, buff=0.2).set_z_index(10)

        np.random.seed(1)
        XVals = [x * 1.0 for x in range(0, xmax + 1)]
        YVals = [0.0] * (xmax + 1)
        for i in range(1, 500):
            YVals[i] = YVals[i-1] + np.random.choice((-1, 1, 1))
        for i in range(500, 900):
            YVals[i] = YVals[i-1] + np.random.choice((-1, -1, 1))
        for i in range(900, 1000):
            YVals[i] = YVals[i-1] + np.random.choice((-1, 1))
        for i in range(1000, 1600):
            YVals[i] = YVals[i-1] + np.random.choice((-1, 1, 1))
        for i in range(1600, xmax+1):
            YVals[i] = YVals[i-1] + np.random.choice((1, 1, -1, 1))

        interp = scipy.interpolate.interp1d(np.array(XVals), np.array(YVals))

        def f(x):
            return interp(x) + 0

        path = ax.plot(f, (0, 2125, 2), color=BLUE, stroke_width=5)

        self.add(ax, eq1, eq2, line1, line2, eq0)
        self.wait(0.5)

        gp = VGroup(MathTex(r'S_n', color=BLUE).set_z_index(30).next_to(p0, RIGHT),
                    VGroup(), VGroup(), MathTex(r'S^{\rm max}', color=GREY).set_z_index(25).next_to(p0, RIGHT).set_opacity(0),
                    MathTex(r'S^{\rm min}', color=GREY).set_z_index(25).next_to(p0, RIGHT).set_opacity(0))

        def updatefunc(obj):
            end = path.get_end()
            obj[0].next_to(end, RIGHT)
            x = (end - p0)[0] * dx
            up = ax.coords_to_point(x, x)
            dn = ax.coords_to_point(x, -x)
            obj[1] = Line(p0, up, color=GREY, stroke_width=4).set_z_index(10)
            obj[2] = Line(p0, dn, color=GREY, stroke_width=4).set_z_index(10)
            obj[3].next_to(up, RIGHT).set_opacity(min(x/200, 1))
            obj[4].next_to(dn, RIGHT).set_opacity(min(x/200, 1))

        self.play(FadeIn(gp), run_time=1)
        gp.add_updater(updatefunc)
        self.add(gp)
        self.play(Create(path, rate_func=linear), run_time=15)
        self.wait(0.5)


def calc_prob(n=1., m=2):
    s = 0.0
    k = 1
    i = 0
    p = 2.
    while s < n:
        k += m
        i += 1
        s += 1/k
        p *= k / 2 / i
    eps = s - n
    p *= math.pow(eps, i)
    print(k)
    print(p)




class Sinc(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = BLACK
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        xlen = config.frame_x_radius * 1.8
        ylen = config.frame_y_radius * 1.7

        def get_sinc(n):
            def f(x):
                res = 1.0
                for i in range(1, 2*n+3, 2):
                    res *= math.sin(x/i)*i/x
                return res
            return f

        xrange = math.pi*3
        ax = Axes(x_range=[-xrange, xrange * 1.05], y_range=[-0.25, 1.05], z_index=2, x_length=xlen, y_length=ylen,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05,
                               "tip_width": 0.3 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.4 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': False}).to_edge(DOWN, buff=0.2).set_z_index(2)
        ax.to_edge(DOWN, buff=0.05)


        f = get_sinc(6)
        graph = ax.plot(f, (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
        graphu = ax.plot(lambda x: max(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
        graphl = ax.plot(lambda x: min(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
        areau = ax.get_area(graphu, color=ManimColor(BLUE.to_rgb()*0.3), x_range=(-xrange, xrange), opacity=1)
        areal = ax.get_area(graphl, color=ManimColor(RED.to_rgb()*0.3), x_range=(-xrange, xrange), opacity=1)

#        self.add(VGroup(ax, graph, areau, areal).rotate(90*DEGREES).move_to(ORIGIN).to_edge(RIGHT, buff=0.4))
        self.add(VGroup(ax, graph, areau, areal))

class IntThumb(Scene):
    def construct(self):
        eq = MathTex(r'\int\limits_{-\infty}^\infty\frac{\sin(x)}{x}\frac{\sin(x/3)}{x/3}\frac{\sin(x/5)}{x/5}\frac{\sin(x/7)}{x/7}'
                     r'\frac{\sin(x/9)}{x/9}\frac{\sin(x/11)}{x/11}\frac{\sin(x/13)}{x/13}\frac{\sin(x/15)}{x/15}dx', font_size=40, stroke_width=1.5)

        self.add(eq)


class ProcessThumb(ProcessBW):
    def construct(self):
        self.animprocess(yrange=None, n0=3, n1=17, do_extreme=True, iredlines=0, fast=True, thumb=True, yscale=1.428)

class PiThumb(Scene):
    def construct(self):
        eq = MathTex(r'\pi', stroke_width=2, font_size=200)
        self.add(eq)


class Intro_Short(Scene):  # manim -p -r1080,1920 --fps 30 borwein.py Intro_Short
    nTerms = 8

    def __init__(self, *args, **kwargs):
        config.frame_y_radius = config.frame_x_radius * 1.77777777
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        print(config.frame_x_radius)
        print(config.frame_y_radius)

        bistr = [r'{{{{ \frac{{\sin\frac{{x}}{{ {0} }} }}{{x/{0}}} }}}}'.format(i) for i in range(3, 17, 2)]
        bistr = [r'{{\int\limits_{-\infty}^\infty\frac{\sin x}{x} }}'] + bistr + [r'dx{{=}}\pi']

        xlen = config.frame_x_radius * 1.8
        ylen = config.frame_y_radius * 1

        def get_sinc(n):
            def f(x):
                res = 1.0
                for i in range(1, 2*n+3, 2):
                    res *= math.sin(x/i)*i/x
                return res
            return f

        xrange = 10.0
        ax = Axes(x_range=[-xrange, xrange * 1.05], y_range=[-0.5, 1.1], z_index=2, x_length=xlen, y_length=ylen,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': False}).move_to(ORIGIN).set_z_index(2)

        eq_width = config.frame_x_radius * 2 * 0.9
        eq0 = VGroup()
        for i in range(self.nTerms):
            eq1 = MathTex(''.join(bistr[:i+1] + bistr[-1:]), font_size=80).to_edge(UP, buff=2.7)
            scale = min(eq1.width, eq_width, (eq1.width + eq_width) * 0.5 - eq_width * 0.2)/eq1.width
            eq1.scale(scale)
            f = get_sinc(i)
            graph = ax.plot(f, (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
            graphu = ax.plot(lambda x: max(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
            graphl = ax.plot(lambda x: min(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
            areau = ax.get_area(graphu, color=BLUE, x_range=(-xrange, xrange))
            areal = ax.get_area(graphl, color=RED, x_range=(-xrange, xrange))
            if i == 0:
                eq2 = MathTex(r'{\rm sinc}(x)=\frac{\sin x}{x}', font_size=80)[0]
                eq2.next_to(eq1[0][-2], ORIGIN, submobject_to_align=eq2[-2])
                eq2.move_to(ORIGIN, coor_mask=RIGHT)
                eq3 = eq2.copy().scale(1.6).move_to(ORIGIN)
                self.add(eq3)
                self.wait(0.5)
                self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq3, eq2), FadeIn(ax)),
                                      Create(graph, rate_func=linear), lag_ratio=0.5), run_time=2)

                self.play(ReplacementTransform(eq2[-6:], eq1[0][-6:]),
                          FadeOut(eq2[:-6]),
                          FadeIn(eq1[0][:-6], eq1[-3:]),
                          FadeIn(areau, areal), run_time=2)
                self.wait(0.5)
            else:
                anims1 = [ReplacementTransform(eq0[:i] + eq0[-3:-1], eq1[:i] + eq1[-3:-1]),
                          FadeIn(eq1[i]), FadeOut(eq0[-1], rate_func=rate_functions.rush_from)]
                anims2 = [ReplacementTransform(graph0, graph),
                          ReplacementTransform(areau0, areau),
                          ReplacementTransform(areal0, areal)]
                if i == 1:
                    self.play(*anims1, run_time=1)
                    self.play(*anims2, run_time=1)
                else:
                    self.play(*anims1, *anims2, run_time=1)
                if i < 7:
                    self.play(FadeIn(eq1[-1]), run_time=0.5)
                    self.wait(1)
            eq0 = eq1
            graph0 = graph
            areau0 = areau
            areal0 = areal

        eq4 = MathTex(r'0.999999999985\ldots\pi', font_size=80).next_to(eq0, DOWN).to_edge(RIGHT, buff=0.8)
        self.play(FadeIn(eq4), run_time=0.5)
        self.wait(0.5)


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        WalkSn().render()
