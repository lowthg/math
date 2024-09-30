import manim
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


def color(col=GREEN, scale=1.0):
    return ManimColor(col.to_rgb() * scale)

class SceneAS(Scene):
    transparent_color=WHITE
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = self.transparent_color
        Scene.__init__(self, *args, *kwargs)


class MaxIntrans(Scene):
    prob = 0.27
    skip = False

    def showineq(self, ax, eq):
        size = 38
        eq1 = MathTex(r'y=1-\frac{q}{x}', font_size=size)[0].move_to(ax.coords_to_point(0.01, 0.85), aligned_edge=LEFT)
        self.play(ReplacementTransform(eq.copy(), eq1), run_time=2)

        eq2 = MathTex(r'y=x-(x^2-x+q)/x', font_size=size)[0]
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq2[1])
        self.play(ReplacementTransform(eq1[4:5] + eq1[6] + eq1[3], eq2[-4:-3] + eq2[-1] + eq2[3]),
                  abra.fade_replace(eq1[-2], eq2[-2]),
                  FadeIn(eq2[4], eq2[-3]),
                  run_time=2)
        self.play(abra.fade_replace(eq1[2], eq2[7:10]), run_time=1)
        self.play(FadeIn(eq2[2], eq2[5:7]), run_time=2)

        eq3 = MathTex(r'y=x-(x^2-x+1/4 +q-1/4)/x', font_size=size)[0]
        eq3.next_to(eq1[1], ORIGIN, submobject_to_align=eq3[1])
        self.play(ReplacementTransform(eq2[2:9] + eq2[9:11] + eq2[11:], eq3[2:9] + eq3[13:15] + eq3[19:]), run_time=1)
        self.play(FadeIn(eq3[9:13], eq3[15:19]), run_time=2)
        eq4 = MathTex(r'y=(x-1/2)^2', font_size=size)[0]
        eq4.next_to(eq1[1], ORIGIN, submobject_to_align=eq4[1])
        eq4[2:].move_to(eq3[5:13], coor_mask=RIGHT)
        self.play(FadeIn(eq4[2:]), FadeOut(eq3[5:13]), run_time=2)
        eq5 = MathTex(r'y = x-((x-1/2)^2+q-1/4)/x', font_size=size)[0]
        eq5.next_to(eq1[1], ORIGIN, submobject_to_align=eq5[1])
        self.play(ReplacementTransform(eq3[2:5] + eq4[2:] + eq3[13:],
                                       eq5[2:5] + eq5[5:13] + eq5[13:]),
                  run_time=1)

        txt = Tex(r'positive', font_size=40, color=BLUE)
        br2 = BraceLabel(eq5[4:-3], r'',
                         label_constructor=abra.brace_label(txt),
                         brace_config={'color': BLUE})
        self.play(FadeIn(br2), run_time=2)
        self.wait(1)
        eq6 = MathTex(r'y < x', font_size=40)[0]
        eq6.next_to(eq1[0], ORIGIN, submobject_to_align=eq6[0])
        self.play(ReplacementTransform(eq1[:1] + eq5[2],
                                       eq6[:1] + eq6[2]),
                  abra.fade_replace(eq1[1], eq6[1]),
                  FadeOut(eq5[3:], br2),
                  run_time=2)
        self.wait(1)
        self.play(FadeOut(eq6))

#        label_f = MathTex(r'y=1-\frac{q}{x}=x-(x^2-x+q)/x=x-(x-1/2)^2/x-(q-1/4)/x < x').next_to(graph.get_corner(UR), RIGHT, buff=0.02)


    def construct(self):
        MathTex.set_default(font_size=30)
        title1 = MathTex(r'p=73\%', font_size=40).to_edge(UP, buff=0.3).shift(LEFT * 2)
        title2 = MathTex(r'q=1-p=27\%', font_size=40).next_to(title1, DOWN).align_to(title1, LEFT)
        rec = SurroundingRectangle(VGroup(title1, title2), color=BLUE, corner_radius=0.1, stroke_width=5)
        self.play(FadeIn(title1), run_time=1)
        self.play(FadeIn(title2), run_time=1)
        self.play(FadeIn(rec), run_time=1)
        p_arr = [1]
        while p_arr[-1] > self.prob:
            p_arr.append(1 - self.prob/p_arr[-1])

        print(p_arr)

        ax = Axes(x_range=[0, 1.1], y_range=[0, 1.15], z_index=2, x_length=8,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05},
                  )
        lines = VGroup(
            Line(ax.coords_to_point(1, 0), ax.coords_to_point(1, 1.1), stroke_width=5, stroke_color=GREY, z_index=0),
            Line(ax.coords_to_point(0, 1), ax.coords_to_point(1.1, 1), stroke_width=5, stroke_color=GREY,  z_index=0)
        )

        labels = VGroup(
            MathTex('0').next_to(ax.coords_to_point(0, 0), DOWN),
            MathTex('1').next_to(ax.coords_to_point(1, 0), DOWN),
            MathTex('0').next_to(ax.coords_to_point(0, 0), LEFT),
            MathTex('1').next_to(ax.coords_to_point(0, 1), LEFT),
        )

        Group(ax, lines, labels).to_edge(LEFT, buff=0.05)

        crv_yeqx = Line(ax.coords_to_point(0, 0), ax.coords_to_point(1.05, 1.05), stroke_width=4, stroke_color=RED,
                        z_index=1)
        label_yeqx = MathTex('y=x').next_to(ax.coords_to_point(0.9, 0.9), UL, buff=0.05)
        label_q = MathTex(r'q', color=BLUE).next_to(ax.coords_to_point(self.prob, 0), DOWN)

        def f(x):
            return 1-self.prob/x

        graph = ax.plot(f, (self.prob, 1.1, 0.02), color=BLUE)

#        self.add(graph)
        label_f = MathTex(r'y=1-\frac{q}{x}', z_index=4)[0].next_to(ax.coords_to_point(1.04, f(1.04)), UL, buff=0.02)

        n = len(p_arr)

        xpos = ax.get_right() * RIGHT + UP * config.frame_y_radius + DOWN * 1 + RIGHT
        xpos_w = xpos * UP + RIGHT * config.frame_x_radius + LEFT * 0.4 - xpos

        xdy = (DOWN * (config.frame_y_radius - 1) + xpos * DOWN) / (n-1)
        dpos = xpos_w * 0.45 / (n - 1)

        xlines = []
        vlines_x = []

        for i in range(n):
            pos_l = xpos + i * xdy
            pos_r = pos_l + xpos_w
            line = Arrow(pos_l + + LEFT * 0.2, pos_r + RIGHT * 0.5, color=WHITE, stroke_width=5, z_index=1,
                         max_tip_length_to_length_ratio=0.05)
            pos_c = (pos_l + pos_r) * 0.5
            if i == 0:
                poss = [pos_c]
                eqs = [MathTex(r'p_1', z_index=3)[0].next_to(pos_c, DOWN, buff=0.15)]
            else:
                poss = [pos_c - dpos * i, pos_c + dpos * (n - i)]
                eqs = [MathTex(r'p_{{{}}}'.format(i+1), z_index=3)[0].next_to(poss[0], DOWN, buff=0.15),
                       MathTex(r'q_{{{}}}'.format(i+1), z_index=3)[0].next_to(poss[1], DOWN, buff=0.15)]

            dots = [Dot(pos, radius=0.1, color=RED, z_index=2) for pos in poss]
            eqx = MathTex(r'X_{{{}}}'.format(i+1), font_size=40).next_to(pos_l, LEFT, buff=0.05)
            xlines.append(VGroup(*eqs, eqx, line, *dots))
            vlines_x += poss

        vtop = xlines[0][-1].get_center() * UP + UP * 0.5
        vbottom = xlines[-1][-1].get_center() * UP + DOWN * 0.5
        vlines = [DashedLine(x * RIGHT + vtop, x * RIGHT + vbottom, stroke_width=2,
                             dash_length=DEFAULT_DASH_LENGTH * 0.5).set_opacity(0.35)
                  for x in vlines_x]

        x0pos = xlines[0].get_center()
        xlines[0].move_to(ORIGIN)
        xlineshift = (x0pos - xlines[0].get_center()) * RIGHT

        self.play(LaggedStart(FadeIn(xlines[0][1]),
                              Create(xlines[0][2], rate_func=linear),
                              FadeIn(xlines[0][3:]),
                              lag_ratio=0.5),
                  run_time=2)
        self.play(FadeIn(xlines[0][0]), run_time=0.5)
        eq = MathTex(r'p_1=1')
        eq.next_to(xlines[0][0][:2], ORIGIN, submobject_to_align=eq[0][:2])
        self.play(FadeIn(eq[0][2:]), run_time=1)
        self.wait(1)
        self.play(FadeOut(eq[0][2:]), run_time=1)

        xlines[1].move_to(ORIGIN)
        self.play(LaggedStart(xlines[0].animate.shift(-xdy),
                              FadeIn(xlines[1][2]),
                              Create(xlines[1][3], rate_func=linear),
                              FadeIn(xlines[1][4:]),
                              lag_ratio=0.5),
                  run_time=2)
        self.play(FadeIn(xlines[1][:2]), run_time=0.5)

        eq1 = MathTex(r'\mathbb P(X_1\le X_2) = p_1q_2', z_index=3)[0].next_to(xlines[0], UP)
        box = SurroundingRectangle(VGroup(xlines[1][4], xlines[1][0], xlines[1][5], xlines[1][1]),
                                   color=BLUE, corner_radius=0.35, stroke_width=6, z_index=5)
        box.shift(-xdy * 0.53 + RIGHT*0.12)
        box.rotate(-0.332)
        self.play(FadeIn(eq1[:-4], run_time=1))
        self.play(FadeIn(box), run_time=1)
        self.play(ReplacementTransform(xlines[0][0][:2].copy(), eq1[-4:-2]),
                  ReplacementTransform(xlines[1][1][:2].copy(), eq1[-2:]), run_time=2)
        self.play(FadeOut(box), run_time=1)

        eq2 = MathTex(r'q=')[0]
        eq2.next_to(eq1[-5], ORIGIN, submobject_to_align=eq2[-1])
        eq2[0].move_to(eq1[:-5], coor_mask=RIGHT)
        self.play(FadeOut(eq1[:-5]), FadeIn(eq2[0]), run_time=2)
        eq3 = MathTex(r'q_2=\frac{q}{p_1}')[0]
        eq3.next_to(eq1[-5], ORIGIN, submobject_to_align=eq3[2])
        self.play(
            ReplacementTransform(eq1[-4:-2] + eq1[-2:] + eq2[0] + eq1[-5], eq3[-2:] + eq3[:2] + eq3[3] + eq3[2]),
            FadeIn(eq3[4]),
            run_time=2
        )
        eq4 = MathTex(r'p_2=1-\frac{q}{p_1}')[0]
        eq4.next_to(eq3[2], ORIGIN, submobject_to_align=eq4[2])
        eq5 = MathTex(r'=1-q_2')[0]
        eq5.next_to(eq4[4], ORIGIN, submobject_to_align=eq5[2])
        self.play(LaggedStart(eq3.animate.next_to(eq4, UP, coor_mask=UP),
                              FadeIn(eq4[:-4], eq5[-2:]), lag_ratio=0.5),
                  run_time=2)
        self.play(ReplacementTransform(eq3[-4:].copy(), eq4[-4:]), FadeOut(eq5[-2:]), run_time=2)
        self.play(FadeOut(eq3), run_time=1)

        if False:
            self.add(ax, lines, labels, crv_yeqx, label_q, label_yeqx, graph, label_f)
        else:
            self.play(FadeIn(ax, lines, labels, *vlines),
                      Group(xlines[0], xlines[1], eq4).animate.shift(xlineshift),
                      run_time=2)
            self.play(Create(crv_yeqx), run_time=1)
            self.play(FadeIn(label_yeqx), run_time=0.5)
            self.play(FadeIn(label_q), run_time=0.2)
            self.play(Create(graph), run_time=1)
            self.play(FadeIn(label_f), run_time=0.5)

        # animate calc
        point1 = ax.coords_to_point(p_arr[0], 0)
        point2 = ax.coords_to_point(p_arr[0], p_arr[1])
        eqp1 = MathTex(r'p_1').next_to(point1, DOWN, buff=0.1)
        dot1 = Dot(point1, radius=0.07, color=YELLOW, z_index=3)
        dot2 = Dot(point2, radius=0.07, color=YELLOW, z_index=3)
        line1 = Line(point1, point2, color=YELLOW, z_index=2).set_opacity(0.8)
        self.play(FadeIn(eqp1), FadeOut(labels[1]), run_time=0.2)
        self.play(FadeIn(dot1), run_time=0.2)
        self.play(Create(line1), run_time=1)
        self.play(FadeIn(dot2), run_time=0.2)

        for i in range(n-1):
            point1 = ax.coords_to_point(p_arr[i], p_arr[i+1])
            point2 = ax.coords_to_point(p_arr[i+1], p_arr[i+1])
            point3 = ax.coords_to_point(p_arr[i+1], 0)
            eqp1 = MathTex(r'p_{{{}}}'.format(i+2)).next_to(point3, DOWN, buff=0.1)
            dot1 = Dot(point1, radius=0.07, color=YELLOW, z_index=3)
            dot2 = Dot(point2, radius=0.07, color=YELLOW, z_index=3)
            dot3 = Dot(point3, radius=0.07, color=YELLOW, z_index=3)
            line1 = Line(point1, point2, color=YELLOW, z_index=2).set_opacity(0.8)
            line2 = Line(point2, point3, color=YELLOW, z_index=2).set_opacity(0.8)

            # add new X line
            if i > 0:
                if i == 1:
                    self.play(FadeOut(eq4), run_time=0.2)
                pos1 = xlines[i+1].get_center()
                pos2 = xlines[i].get_center()
                pos1[1] = min(pos1[1], pos2[1])
                shift = (pos1 - xdy) - pos2
                if shift[1] > 0.01:
                    xlines[i+1].move_to(pos1)
                    if not self.skip:
                        self.play(LaggedStart(VGroup(*xlines[:i+1]).animate.shift(shift),
                                              FadeIn(xlines[i+1]),
                                              lag_ratio=0.5),
                                  run_time=2)
                else:
                    if not self.skip:
                        self.play(FadeIn(xlines[i+1]), run_time=1.5)

            if not self.skip:
                self.play(FadeIn(dot1), run_time=0.2)
                self.play(Create(line1), run_time=1)
                self.play(FadeIn(dot2), run_time=0.2)
                self.play(Create(line2), run_time=1)
                self.play(FadeIn(dot3), run_time=0.2)
                self.play(FadeIn(eqp1), run_time=0.2)

            if i == 0:
                self.showineq(ax, label_f)

        eq10 = MathTex(r'\mathbb P(X_{{{}}}\le X_1){{{{=}}}}p_{{{}}}{{{{\le}}}} q'.format(n, n), font_size=40)
        eq10.move_to(ax.coords_to_point(0.05, 0.9), aligned_edge=LEFT)
        rect = SurroundingRectangle(eq10, color=BLUE, stroke_width=5, corner_radius=0.1)
        self.play(FadeIn(eq10[:2], rect), run_time=1)
        self.play(ReplacementTransform(eqp1[0].copy(), eq10[2]), run_time=2)
        self.play(FadeIn(eq10[3]), run_time=0.2)
        self.play(ReplacementTransform(label_q[0].copy(), eq10[4]), run_time=2)


        self.wait(1)


class DiceUnfold(ThreeDScene):
    def construct(self):
        pass


class ABC_Cycle(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        rad = 0.4
        h = 2

        a = LabeledDot(Text("A", font="Helvetica", color=WHITE, weight=SEMIBOLD), radius=rad,
                       color=color(DARK_BLUE, 0.8), stroke_color=WHITE, stroke_width=3)
        b = LabeledDot(Text("B", font="Helvetica", color=WHITE, weight=SEMIBOLD), radius=rad,
                       color=color(ORANGE, 0.8), stroke_color=WHITE, stroke_width=3)
        c = LabeledDot(Text("C", font="Helvetica", color=WHITE, weight=SEMIBOLD), radius=rad,
                       color=color(GREEN, 0.5), stroke_color=WHITE, stroke_width=3)

        b_c = b.get_center()
        a.move_to(b_c + LEFT * h)
        c.move_to(b_c + RIGHT * h)
        a_c = a.get_center()
        c_c = c.get_center()

        ab = Arrow(a_c + RIGHT * rad, b_c + LEFT * rad, color=WHITE, stroke_width=5, z_index=1, buff=0)
        bc = Arrow(b_c + RIGHT * rad, c_c + LEFT * rad, color=WHITE, stroke_width=5, z_index=1, buff=0)
        ca = Arrow(c_c + LEFT * rad, a_c + RIGHT * rad, color=WHITE, stroke_width=5, z_index=1, buff=0).set_opacity(0)

        ur = (RIGHT + UP * math.sqrt(3)) * 0.5

        b2 = b.copy().shift(UP * h * math.sqrt(3)/2)
        b2_c = b2.get_center()
        a2 = a.copy().move_to(b2_c + ur * DL * h)
        c2 = c.copy().move_to(b2_c + ur * DR * h)
        a2_c = a2.get_center()
        c2_c = c2.get_center()

        ab2 = Arrow(a2_c + ur * rad, b2_c + ur * DL * rad, color=WHITE, stroke_width=5, z_index=1, buff=0)
        bc2 = Arrow(b2_c + ur * DR * rad, c2_c + ur * UL * rad, color=WHITE, stroke_width=5, z_index=1, buff=0)
        ca2 = Arrow(c2_c + LEFT * rad, a2_c + RIGHT * rad, color=WHITE, stroke_width=5, z_index=1, buff=0)

        self.wait(0.5)

        self.play(LaggedStart(FadeIn(a, b), FadeIn(ab), lag_ratio=0.5), run_time=1)
        self.play(LaggedStart(FadeIn(c), FadeIn(bc), lag_ratio=0.5), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(a, a2),
                  ReplacementTransform(b, b2),
                  ReplacementTransform(c, c2),
                  ReplacementTransform(ab, ab2),
                  ReplacementTransform(bc, bc2),
                  ReplacementTransform(ca, ca2),
                  run_time=2)
        self.wait(0.5)


class ABC_Table(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = BLACK
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        Tex.set_default(font_size=50)
        w = 1.2
        h1 = 0.9
        h2 = 0.8
        colors = [color(DARK_BLUE, 0.8), color(ORANGE, 0.8), color(GREEN, 0.5)]

        headings = []
        for i in range(3):
            rec = Rectangle(width=w, height=h1, stroke_opacity=0, z_index=0, fill_opacity=1, fill_color=colors[i])
            txt = Text('ABC'[i], font="Helvetica", color=WHITE, weight=SEMIBOLD, z_index=1).move_to(rec)
            headings.append(VGroup(rec, txt))

        rec2 = Rectangle(width=w, height=h2, stroke_opacity=0, z_index=0, fill_opacity=1, fill_color=BLACK)

        rows = [headings] + [[rec2.copy() for _ in range(3)] for _ in range(3)]

        ts = []
        for row in rows:
            ts.append(MobjectTable([row.copy()], include_outer_lines=True, v_buff=0, h_buff=0))

        self.add(ts[0].to_edge(DOWN))

        rows = [[3, 2, 1], [2, 1, 3], [1, 3, 2]]

        self.wait(0.5)
        ts[1].to_edge(DOWN)
        t = ts[1].copy().next_to(ts[0], DOWN, buff=0)
        self.play(ts[0].animate.next_to(ts[1], UP, buff=0), FadeIn(ts[1], target_position=t), run_time=1)
        self.wait(0.5)
        txt = [Tex(r'\bf {}'.format(rows[0][j]), z_index=1).move_to(ts[1][0][j]) for j in range(3)]
        self.play(FadeIn(*txt), run_time=1)

        done = [ts[0], ts[1]] + txt
        for i in range(1, 3):
            t = ts[i+1].copy().next_to(ts[i], DOWN, buff=0)
            ts[i+1].to_edge(DOWN)
            txt = [Tex(r'\bf {}'.format(rows[i][j]), z_index=1).move_to(ts[i+1][0][j]) for j in range(3)]
            self.wait(0.5)
            self.play(VGroup(*done).animate.next_to(ts[i+1], UP, buff=0),
                      FadeIn(VGroup(ts[i+1], *txt), target_position=t), run_time=1)
            done += [ts[i+1]] + txt

        self.wait(0.5)


def seqboxed(seq, font_size=55):
    txt = Text(seq, font='Helvetica', weight=SEMIBOLD, font_size=font_size)
    for i in range(len(seq)):
        if seq[i] == 'H':
            txt[i].set_color(BLUE).set_z_index(1)
        else:
            txt[i].set_color(YELLOW).set_z_index(1)
    box = SurroundingRectangle(txt, corner_radius=0.4, stroke_color=GREEN, fill_opacity=1,
                               fill_color=BLACK, stroke_width=6, buff=0.2, z_index=0)

    return VGroup(txt, box)


def seqarr(source:Mobject, dest, odds: (int, None) = 1, label_size=50):
    dx = dest.get_center() - source.get_center()
    print(dx)
    for i in range(len(dx)):
        if math.fabs(dx[i]) < 0.01:
            dx[i] = 0

    arr_func = DoubleArrow if odds == 1 else Arrow
    arr = arr_func(source.get_corner(dx), dest.get_corner(-dx), color=WHITE,
                   stroke_width=5, z_index=1, buff=0)

    if odds != 1 and odds is not None:
        dir, buff = (RIGHT, 0) if dx[1] != 0 else (UP, -0.05)
        label = Tex(r'\bf {}'.format(odds), font_size=label_size,
                    color=color(PURE_RED, 0.5)).next_to(arr, dir, buff=buff)
        label.set_stroke(width=1, color=WHITE)
        arr = VGroup(arr, label)
    return arr


class HT_Cycle(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        h = RIGHT * 2.5
        v = DOWN * 2
        th = seqboxed('TH')
        c = th.get_center()
        hh = seqboxed('HH').move_to(c + h)
        ht = seqboxed('HT').move_to(c + h + v)
        tt = seqboxed('TT').move_to(c + v)

        hh_arr = seqarr(th, hh, 3)
        ht_arr = seqarr(hh, ht, 1)
        tt_arr = seqarr(ht, tt, 3)
        th_arr = seqarr(tt, th, 1)

        self.wait(0.5)
        self.play(FadeIn(th, hh, hh_arr), run_time=1)
        self.wait(0.05)
        self.play(FadeIn(ht, ht_arr), run_time=1)
        self.wait(0.05)
        self.play(FadeIn(tt, tt_arr), run_time=1)
        self.wait(0.05)
        self.play(FadeIn(th_arr), run_time=1)
        self.wait(0.5)


class Penneys_Cycle(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        h = RIGHT * 2.5
        v = DOWN * 1.5
        font_size = 40
        label_size = 45
        hhh = seqboxed('HHH', font_size=font_size).to_edge(UL)
        c = hhh.get_center()
        thh = seqboxed('THH', font_size=font_size).move_to(c + v)
        hht = seqboxed('HHT', font_size=font_size).move_to(c + v + h)
        hth = seqboxed('HTH', font_size=font_size).move_to(c + h)
        tth = seqboxed('TTH', font_size=font_size).move_to(c + v * 2)
        htt = seqboxed('HTT', font_size=font_size).move_to(c + v * 2 + h)
        tht = seqboxed('THT', font_size=font_size).move_to(c + v * 3)
        ttt = seqboxed('TTT', font_size=font_size).move_to(c + v * 3 + h)

        hhha = seqarr(thh, hhh, 7, label_size)
        hhta = seqarr(thh, hht, 3, label_size)
        htha = seqarr(hht, hth, 2, label_size)
        htta = seqarr(hht, htt, 2, label_size)
        thha = seqarr(tth, thh, 2, label_size)
        thta = seqarr(tth, tht, 2, label_size)
        ttha = seqarr(htt, tth, 3, label_size)
        ttta = seqarr(htt, ttt, 7, label_size)

        self.add(hhh, hht, hth, htt, thh, tht, tth, ttt,
                 hhha, hhta, htha, htta, thha, thta, ttha, ttta)


class Penneys_Method(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        h = DOWN * 1.5
        thh = seqboxed('THH', font_size=40)
        c = thh.get_center()
        tth = seqboxed('TTH', font_size=40).move_to(c + h)
        arr = seqarr(tth, thh, None)
        c2 = (thh[0][0].get_center() + tth[0][0].get_center()) * 0.5
        h = thh[0][1].copy().move_to(c2)
        t = tth[0][0].copy().move_to(c2)

        self.add(thh)
        self.wait(0.1)
        self.play(LaggedStart(FadeIn(arr), FadeIn(tth[1:]), lag_ratio=0.2), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(thh[0][:2].copy(), tth[0][-2:]), run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(thh[0][1].copy(), h), run_time=2)
        self.wait(0.1)
        self.play(*abra.fade_replace(h, t), run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(t, tth[0][0]), run_time=2)
        self.wait(0.5)


class Efron(SceneAS):
    def construct(self):
        face_scale = 0.3
        z_index = 0
        colors = [color(DARK_BLUE, 0.8), color(ORANGE, 0.8), color(RED, 0.8), color(GREEN, 0.5)]
        faces = abra.get_dice_faces(dot_color=WHITE)
        faces = [VGroup(faces[0][0], *faces[0][1:].copy().set_opacity(0))] + faces

        arranged = [
            [3, 3, 3, 3, 3, 3],
            [6, 2, 6, 2, 2, 2],
            [1, 1, 1, 5, 5, 5],
            [0, 4, 0, 4, 4, 4]
        ]
        ordered = [
            [0, 1, 2, 3, 4, 5],
            [3, 1, 4, 5, 0, 2],
            [0, 1, 2, 3, 4, 5],
            [0, 2, 3, 1, 4, 5]
        ]

        numbers = [[]] * 4
        dice = []

        for i in range(len(arranged)):
            f = [None] * 6
            f[1] = faces[arranged[i][1]].copy().scale(face_scale)
            f[0] = faces[arranged[i][0]].copy().scale(face_scale).next_to(f[1], LEFT, buff=0)
            f[2] = faces[arranged[i][2]].copy().scale(face_scale).next_to(f[1], RIGHT, buff=0)
            f[3] = faces[arranged[i][3]].copy().scale(face_scale).next_to(f[1], UP, buff=0)
            f[4] = faces[arranged[i][4]].copy().scale(face_scale).next_to(f[1], DOWN, buff=0)
            f[5] = faces[arranged[i][5]].copy().scale(face_scale).next_to(f[4], DOWN, buff=0)

            f1 = []
            for j in range(6):
                x = f[ordered[i][j]]
                x[0].set_fill(color=colors[i])
                x[0].set_z_index(z_index)
                x[1:].set_z_index(z_index + 1)
                z_index += 2
                f1.append(x)
                numbers[i].append(arranged[i][ordered[i][j]])

            dice.append(VGroup(*f1))

        dice_g = VGroup(*dice[::-1]).arrange(RIGHT)

        self.add(dice_g)

        rows = []
        numrows = []
        for i in range(len(ordered)):
            row = dice[i].copy().arrange(RIGHT, buff=0)
            for f in row[:]:
                f[0] = Rectangle(width=f[0].width, height=f[0].height, fill_color=f[0].fill_color, fill_opacity=1,
                                 stroke_width=f[0].stroke_width, stroke_color=WHITE, z_index=f[0].z_index)\
                    .move_to(f[0])
            rows.append(row)

            numrow = MathTex(r'{}{}{}{}{}{}'.format(*numbers[i]))[0].move_to(rows[i])
            for j in range(6):
                numrow[j].move_to(row[j], coor_mask=RIGHT)
            numrows.append(numrow)

        t = VGroup(*rows).arrange(DOWN, buff=0).next_to(dice[1], RIGHT)
        self.wait(1)
        for i in range(4):
            self.play(ReplacementTransform(dice[i], rows[i]), run_time=2)

        # self.wait(1)
        # dots = []
        # for i in range(4):
        #     for j in range(6):
        #         dots.append(rows[i][j][1:])
        #         numrows[i][j].set_z_index(rows[i][j][1].get_z_index())
        #         self.play(FadeOut(*dots), FadeIn(*numrows[i]), run_time=1)

        self.wait(1)

        #rcolor = manim.rgb_to_color([0, 255, 255])
        rcolor = PURE_RED
        r2 = SurroundingRectangle(rows[1][4:], stroke_width=8, stroke_color=rcolor,
                                  corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        self.play(FadeIn(r2), run_time=1)
        self.wait(0.5)


        r1 = SurroundingRectangle(rows[1][:4], stroke_width=8, stroke_color=rcolor,
                                  corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        r2.target = SurroundingRectangle(rows[2][3:], stroke_width=8, stroke_color=rcolor,
                                  corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)

        self.play(FadeIn(r1), MoveToTarget(r2), run_time=1)
        self.wait(0.5)
        r2.target = SurroundingRectangle(rows[3][2:], stroke_width=8, stroke_color=rcolor,
                                  corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        r1.target = SurroundingRectangle(rows[2][:3], stroke_width=8, stroke_color=rcolor,
                                  corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        self.play(MoveToTarget(r1), MoveToTarget(r2), run_time=1)
        self.wait(0.5)
        r2.target = SurroundingRectangle(rows[0][:], stroke_width=8, stroke_color=rcolor,
                                  corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        r1.target = SurroundingRectangle(rows[3][:2], stroke_width=8, stroke_color=rcolor,
                                  corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        self.play(MoveToTarget(r1), MoveToTarget(r2), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(r1, r2), run_time=0.5)
        self.wait(0.5)

        # number lines

        points = [[(3, '1')], [(2, '2/3'), (6, '1/3')], [(1, '1/2'), (5, '1/2')], [(0, '1/3'), (4, '2/3')]]
        posl = rows[0].get_left() * RIGHT
        posr = RIGHT * (config.frame_x_radius - 1)
        dx = (posr - posl)/6

        vlines = []
        vtop = rows[0].get_top() * UP
        vbottom = rows[-1].get_bottom() * UP
        for i in range(7):
            vlines.append(DashedLine(dx * i + vtop + posl, dx * i + vbottom + posl, stroke_width=4,
                       dash_length=DEFAULT_DASH_LENGTH * 0.5, z_index=1).set_opacity(0.6))

        lines = []
        for i in range(len(colors)):
            line = Arrow(posl - dx * 0.5, posr + RIGHT * 0.7, color=colors[i], stroke_width=8, z_index=2,
                         max_tip_length_to_length_ratio=0.08, buff=0)
            dots = []
            for pos in points[i]:
                dot = Dot(posl + dx * pos[0], radius=0.1, color=WHITE, z_index=3)
                eq = MathTex(r'\bf ' + pos[1], z_index=3, font_size=30)[0].next_to(dot, DL, buff=0).shift(RIGHT*0.05)
                dots.append(Group(dot, eq))
            obj = Group(line, *dots)
            obj.next_to(rows[i], ORIGIN, coor_mask=UP, submobject_to_align=obj[0])
            lines.append(obj)

        self.play(Group(*rows).animate.next_to(lines[0], LEFT, coor_mask=RIGHT, buff=1), FadeIn(*lines, *vlines),
                  run_time=1)

        for i in range(4):
            self.wait(0.5)
            dot1 = lines[i][1].get_corner(LEFT) + UP * 0.05
            if i < 3:
                l2 = lines[i+1][2] if i < 3 else lines[0][1]
            else:
                l1 = lines[0].copy()
                l1.next_to(lines[i][0], ORIGIN, coor_mask=UP, submobject_to_align=l1[0])\
                    .shift((lines[i][0].get_center() - lines[i-1][0].get_center())*UP)
                l2 = l1[1]
            dot2 = l2.get_corner(RIGHT)
            dx = dot2 - dot1
            h = np.linalg.norm(dx)
            r = RoundedRectangle(width=h, height=0.65, corner_radius=0.3, stroke_color=rcolor, fill_color=BLACK,
                                 fill_opacity=0.5, z_index=4)
            r.rotate(math.atan(dx[1]/dx[0]))
            r.move_to((dot1+dot2)/2)
            if i == 0:
                self.play(FadeIn(r), run_time=1)
            elif i < 3:
                self.play(ReplacementTransform(r0, r), run_time=1)
            else:
                self.play(ReplacementTransform(lines[0].copy(), l1), ReplacementTransform(r0, r), run_time=1)
            r0 = r

        self.wait(0.5)
        self.play(FadeOut(r0, l1), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(*lines, *vlines), run_time=1)
        self.wait(0.5)

        # optimal
        lastrow = rows[0].copy()
        lastrow[0].set_z_index(z_index)
        lastrow[1:].set_z_index(z_index + 1)
        z_index += 2
        self.play(lastrow.animate.move_to(rows[-1]), Group(*rows).animate.next_to(rows[-1], UP, buff=0), run_time=2)
        r = SurroundingRectangle(Group(rows[0][2], lastrow[2]), stroke_width=8, stroke_color=rcolor,
                                 corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        self.play(FadeIn(r), run_time=1)
        self.wait(0.5)
        r1 = SurroundingRectangle(Group(rows[2][2], rows[3][2]), stroke_width=8, stroke_color=rcolor,
                                 corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        self.play(ReplacementTransform(r, r1), run_time=2)
        r2 = SurroundingRectangle(rows[2][:3], stroke_width=8, stroke_color=rcolor,
                                 corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        r3 = SurroundingRectangle(rows[3][2:], stroke_width=8, stroke_color=rcolor,
                                 corner_radius=0.15, buff=0, z_index=z_index, fill_opacity=0.5, fill_color=BLACK)
        self.wait(0.5)
        self.play(FadeOut(r1), FadeIn(r2, r3), run_time=2)
        self.wait(1)


class Medians(SceneAS):
    transparent_color = BLACK
    medians = [0, -1, -2, -3, 3, 2, 1, 0]
    dotlabels = [r'M_1', r'M_2', '', r'M_i', r'M_{i+1}', '', r'M_n', r'M_1']
    labels = [r'X_1', r'X_2', '', r'X_i', r'X_{i+1}', '', r'X_n', r'X_1']

    def construct(self):
        posl = RIGHT * config.frame_x_radius * 0.51
        posr = RIGHT * config.frame_x_radius * 0.8
        top = ORIGIN
        bottom = DOWN * config.frame_y_radius * 0.9
        n = len(self.medians)
        medians = [m - min(self.medians) for m in self.medians]
        max_m = max(medians)
        dx = (posr - posl) / max_m
        dy = (bottom - top) / n
        lines = []
        color = WHITE
        dotcolor = RED
        lines = []
        for i in range(n):
            y = top + (i+0.5) * dy
            line = Arrow(posl - dx * 2 + y, posr + RIGHT * 0.7 + y + dx * 1.5, color=color, stroke_width=5, z_index=2,
                         max_tip_length_to_length_ratio=0.05, buff=0)
            dot = Dot(posl + dx * medians[i] + y, radius=0.1, color=dotcolor, z_index=3)
            if len(self.dotlabels[i]) > 0:
                eq = MathTex(r'\bf ' + self.dotlabels[i], z_index=3, font_size=25)[0].next_to(dot, DR, buff=0).shift(LEFT*0.45)
                dot = Group(dot, eq)
            objs = [line, dot]
            if len(self.labels[i]) > 0:
                label = MathTex(r'\bf ' + self.labels[i], z_index=3, font_size=30)[0]\
                    .next_to(line.get_left() + LEFT * 0.5, RIGHT, buff=0)
                label.shift(DOWN * 0.1)
                objs.append(label)
            obj = Group(*objs)
            lines.append(obj)

        vlines = []
        for i in range(-1, 8):
            vlines.append(DashedLine(dx * i + top + posl, dx * i + bottom + posl, stroke_width=4,
                       dash_length=DEFAULT_DASH_LENGTH * 0.5, z_index=1).set_opacity(0.6))

        gp = Group(*lines, *vlines)
        eq = MathTex(r'\bf M_i={\rm Median}(X_i)', font_size=30).next_to(gp, UP, buff=0.1)
        box = SurroundingRectangle(Group(gp, eq), fill_opacity=0.6, fill_color=BLACK, stroke_color=BLUE,
                                   stroke_width=5, corner_radius=0.3, buff=0.1)
        disp = Group(box, eq, *vlines, *lines)

        self.add(disp)
        self.wait(0.5)

        dot1 = lines[3][1].get_corner(LEFT)
        dot2 = lines[4][1].get_corner(RIGHT)
        dx = dot2 - dot1
        h = np.linalg.norm(dx)
        r = RoundedRectangle(width=h, height=0.6, corner_radius=0.3, stroke_color=PURE_RED, z_index=4)
        r.rotate(math.atan(dx[1] / dx[0]))
        r.move_to((dot1 + dot2) / 2)
        self.play(FadeIn(r))

        MathTex.set_default(stroke_width=1.5)

        eq2 = MathTex(r'\mathbb P(X_i\le X_{i+1})\ge\mathbb P(X_i\le M_i\le X_{i+1})')[0]
        eq2.to_edge(DOWN).to_edge(LEFT, buff=0.05)
        self.wait(0.5)
        self.play(FadeIn(eq2[:10]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(eq2[10]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeIn(eq2[11:]), run_time=0.5)

        eq3 = MathTex(r'\ge\mathbb P(X_i\le M_i)\mathbb P(M_i\le X_{i+1})')[0]
        eq3.next_to(eq2[10], ORIGIN, submobject_to_align=eq3[0])
        self.wait(0.5)
        self.play(ReplacementTransform(eq2[11:18] + eq2[16:18].copy() + eq2[-6:],
                                       eq3[1:8] + eq3[11:13] + eq3[-6:]),
                  FadeIn(eq3[8:11]),
                  run_time=2)

        eq4 = MathTex(r'\ge\frac12\frac12')[0]
        eq4.next_to(eq2[10], ORIGIN, submobject_to_align=eq4[0])
        eq4[1:4].move_to(eq3[1:9], coor_mask=RIGHT)
        eq4[4:].move_to(eq3[9:], coor_mask=RIGHT)
        self.wait(0.5)
        self.play(abra.fade_replace(eq3[1:9], eq4[1:4]),
                  abra.fade_replace(eq3[9:], eq4[4:]))

        eq5 = MathTex(r'\mathbb P(X_i\le X_{i+1})\ge\frac14')[0]
        eq5.next_to(eq4[2], ORIGIN, submobject_to_align=eq5[12])
        eq6 = eq5[11:13].copy()
        eq7 = eq5[13].copy()
        self.wait(0.5)
        self.play(ReplacementTransform(eq2[:10] + eq2[10] + eq4[1:3] + eq4[4:6],
                                       eq5[:10] + eq5[10] + eq5[11:13] + eq6),
                  abra.fade_replace(eq4[3], eq5[13]),
                  abra.fade_replace(eq4[6], eq7),
                  run_time=2)
        self.remove(eq6, eq7)

        eq8 = MathTex(r'>')[0].move_to(eq5[10])
        self.wait(0.5)
        self.play(abra.fade_replace(eq5[10], eq8[0]), run_time=0.5)
        eq9 = MathTex(r'\mathbb P(X_i > X_{i+1}) < \frac34')[0].move_to(eq5)
        self.wait(0.5)
        self.play(ReplacementTransform(eq5[:4] + eq5[5:10] + eq5[12:], eq9[:4] + eq9[5:10] + eq9[12:]),
                  abra.fade_replace(eq5[4], eq9[4]),
                  abra.fade_replace(eq8[0], eq9[10]),
                  abra.fade_replace(eq5[11], eq9[11]),
                  run_time=2
                  )

        self.wait(1)



class One(ThreeDScene):
    def construct(self):
        l = 2
        w = 4
        h = 1
        rect_prism = Prism(dimensions=[l, w, h]).to_edge(LEFT, buff=1)
        kwargs = {"stroke_color": BLUE_D, "fill_color": BLUE_B, "fill_opacity": 1}
        bottom = Rectangle(width=w, height=l, **kwargs)
        s1 = Rectangle(height=h, width=w, **kwargs).next_to(bottom, UP, buff=0)
        s2 = Rectangle(height=h, width=w, **kwargs).next_to(bottom, DOWN, buff=0)
        l1 = Rectangle(height=l, width=h, **kwargs).next_to(bottom, LEFT, buff=0)
        l2 = Rectangle(height=l, width=h, **kwargs).next_to(bottom, RIGHT, buff=0)
        top = Rectangle(width=w, height=l, **kwargs).next_to(bottom, LEFT, buff=0)
        net = VGroup(top, bottom, s1, s2, l1, l2).rotate(-PI/2).to_edge(RIGHT, buff=1)

        arrow = Line(
            start=rect_prism.get_right(), end=net.get_left(), buff=0.2
        ).add_tip()

        self.begin_ambient_camera_rotation()
        self.set_camera_orientation(phi=45*DEGREES, theta=-45*DEGREES)
        self.play(Create(rect_prism))
        self.play(
            LaggedStart(Create(arrow), Transform(rect_prism.copy(), net)),
            run_time=2,
            lag_ratio=0.5
        )

        self.wait()
        self.play(FadeOut(Group(*self.mobjects)))
        self.stop_ambient_camera_rotation()

class SeqChoice(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    seq = 'HHTTTH'
    seq = 'HTTTH'
    show_choice = False
    pause = 1.5/30

    def construct(self):
        txt1 = Text(self.seq[-2:], font='Helvetica', z_index=1, weight=SEMIBOLD, font_size=55)
        txt1[0].set_color(YELLOW)
        txt1[1].set_color(BLUE)
        box1 = SurroundingRectangle(txt1, corner_radius=0.4, stroke_color=GREEN, fill_opacity=1,
                                    fill_color=BLACK, stroke_width=6, buff=0.2)
        choice = VGroup(txt1, box1)
        n = len(self.seq)
        coins = VGroup(*[abra.get_coin(x).scale(0.8) for x in self.seq]).arrange(RIGHT)\
            .next_to(choice, DOWN).align_to(choice, LEFT)
        flipped = []

        self.wait(0.5)
        if self.show_choice:
            self.play(FadeIn(choice), run_time=0.5)
            self.wait(0.5)
        for x in coins:
            flipped.append(abra.animate_flip(self, x).set_z_index(1))
            if self.pause > 0:
                self.wait(self.pause)
        rect = SurroundingRectangle(VGroup(*flipped[-2:]), color=GREEN, fill_opacity=1, stroke_width=6,
                                    corner_radius=0.2, buff=0.067, fill_color=BLACK)
        self.play(FadeIn(rect), run_time=0.2)
        self.wait(0.5)

        self.add(choice)

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "fps": 15, "preview": True}):
        Efron().render()