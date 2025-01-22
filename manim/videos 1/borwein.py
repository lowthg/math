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
    def construct(self):
        ax = Axes(x_range=[0, 7.3], y_range=[-1.2, 1.2], x_length=config.frame_x_radius * 1.6,
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
        posx = origin + dx * 7.15
        u = [0.5, -0.05, 0.6, 0.2, -0.92, -0.1, 0.6]
        for i in range(3, 17, 2):
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
        eqS0 = eqS.copy().next_to(dot0.copy().shift(dx*7), RIGHT, buff=0.1)
        box = self.box(ax, eqS0, ylabels)

        self.add(box, ax, *xlines, ylabels)
        self.wait(0.5)
        self.play(FadeIn(dot0, eqS), run_time=0.5)
        self.wait(0.5)
        pts = [dot0.get_center(), dot0.get_center()]
        polycol = ManimColor(GREY.to_rgb() * 0.8)
        for i in range(3, 17, 2):
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
            eq = MathTex(r'1/{}'.format(i), font_size=30, color=PURPLE_B, stroke_width=1.5)[0].set_z_index(45).move_to(lines[-1]).shift((LEFT + UP*i)/math.pow(1+i*i, 0.5) * 0.25)
            self.wait(0.25)
            self.play(FadeIn(*lines, *polys, eq), run_time=0.6)
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

            if i == 7:
                self.wait(0.5)
                self.play(FadeIn(*redlines), run_time=0.5)
                self.wait(0.5)

            pts = [pts1[0], dot0.get_center(), pts1[-1]]
            eqS = eqS1

        self.wait(0.5)
        dot1 = dot0.copy().move_to(origin)
        self.play(FadeIn(dot1), run_time=0.5)
        for i in range(3, 17, 2):
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


class Characteristic(SceneOpacity):
    opacity = 0.7

    def construct(self):
        eq1 = MathTex(r'\varphi_X(u){{=}}\mathbb E\left[e^{iuX}\right]{{=}}\int_{-\infty}^\infty e^{iux}p_X(x)\,dx').set_z_index(1)
        eq1[3:].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
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

        self.play(FadeOut(eq1[2][:2], eq1[2][-1]),
                  FadeIn(eq1[4][:4], eq1[4][-7:]),
                  ReplacementTransform(eq1[2][2:5], eq1[4][4:7]),
                  abra.fade_replace(eq1[2][5], eq1[4][7]),
                  run_time=1.5)
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


class CosInt(Scene):
    def construct(self):
        str = r'{{\int_{-\infty}^\infty 2\cos x\frac{\sin(x)}{x} }}'
        for i in range(3, 20, 2): # 117
            str += r'{{{{\frac{{\sin(x/{0})}}{{x/{0} }} }}}}'.format(i)
        eq = MathTex(str).to_edge(UL)
        eq2 = MathTex(r'=\pi')
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
            if shift_up > 0:
                self.play(FadeIn(eq[i]),
                          eq.animate.shift(UP*shift_up),
                          eq1.animate.move_to(eq[i].get_right() + eq_shift + UP*shift_up, LEFT),
                          run_time=0.1)

            self.play(FadeIn(eq[i]),
                      eq1.animate(rate_func=linear).move_to(eq[i].get_right()+eq_shift, LEFT),
                      run_time=0.1)

            self.wait(0.1)


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


def GEL():
    num = '1569077070516060928419448874747821551524926829820273852815836448212983665876813483232100703157659223980553468025374126831601055511443556277350638168485268670581505978001035213957013220119308355774556826995014546530662974055048240333477592898399601659803106957890547802814016489317314012540596568503675217623424090233844693031044330866338901649257171209259349727479870471070229558275972160005597077140997595562858828631593176726962223613086208611784047251824501164252220812534634727675751476613624404767871484636683298978159342499577103531615819215167517705897209337522512438255293032766035839849809366559417153502392937165484021304018990053794223563792922467989147962933238674467542103007498929180550306476430528205796520520822099932869221650202860450483774498660610909669824829771782814518455310762100173471158886158031343099553120048438206253288540064495450101249872360507906465'
    print(len(num))


class Sinc(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = WHITE
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
        ax = Axes(x_range=[-xrange, xrange * 1.05], y_range=[-0.25, 1.05], z_index=2, x_length=ylen * 1.1, y_length=ylen,
                  axis_config={'color': BLACK, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05,
                               "tip_width": 0.3 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.4 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': False}).to_edge(DOWN, buff=0.2).set_z_index(2)
        ax.to_edge(DOWN, buff=0.05)


        f = get_sinc(0)
        graph = ax.plot(f, (-xrange, xrange, 0.05), color=BLUE_E, stroke_width=4).set_z_index(3)
        graphu = ax.plot(lambda x: max(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
        graphl = ax.plot(lambda x: min(f(x), 0.), (-xrange, xrange, 0.05), color=BLUE, stroke_width=4).set_z_index(3)
        areau = ax.get_area(graphu, color=BLUE_D, x_range=(-xrange, xrange), opacity=0.5)
        areal = ax.get_area(graphl, color=RED, x_range=(-xrange, xrange), opacity=0.6)
        self.add(VGroup(ax, graph, areau, areal).rotate(90*DEGREES).move_to(ORIGIN).to_edge(RIGHT, buff=0.4))



if __name__ == "__main__":
    calc_prob(2, 2)
#    with tempconfig({"quality": "low_quality", "preview": True}):
#        Intro().render()
