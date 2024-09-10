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

        for i in range(n):
            pos_l = xpos + i * xdy
            pos_r = pos_l + xpos_w
            line = Arrow(pos_l, pos_r + RIGHT * 0.5, color=WHITE, stroke_width=5, z_index=0,
                         max_tip_length_to_length_ratio=0.05)
            pos_c = (pos_l + pos_r) * 0.5
            if i == 0:
                poss = [pos_c]
                eqs = [MathTex(r'p_1')[0].next_to(pos_c, DOWN, buff=0.15)]
            else:
                poss = [pos_c - dpos * i, pos_c + dpos * (n - i)]
                eqs = [MathTex(r'p_{{{}}}'.format(i+1))[0].next_to(poss[0], DOWN, buff=0.15),
                       MathTex(r'q_{{{}}}'.format(i+1))[0].next_to(poss[1], DOWN, buff=0.15)]

            dots = [Dot(pos, radius=0.1, color=RED, z_index=1) for pos in poss]
            eqx = MathTex(r'X_{{{}}}'.format(i+1), font_size=40).next_to(pos_l, LEFT, buff=0.05)
            xlines.append(VGroup(*eqs, eqx, line, *dots))

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

        eq1 = MathTex(r'\mathbb P(X_1\le X_2) = p_1q_2')[0].next_to(xlines[0], UP)
        box = SurroundingRectangle(VGroup(xlines[1][4], xlines[1][5]), color=BLUE, corner_radius=0.25, stroke_width=6, z_index=3)
        box.shift(-xdy * 0.38 + RIGHT*0.1)
        box.stretch(1.5, dim=1)
        box.rotate(-0.32)
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
            self.play(FadeIn(ax, lines, labels),
                      Group(xlines[0], xlines[1], eq4).animate.shift(xlineshift),
                      run_time=2)
            self.play(FadeIn(label_q), run_time=0.2)
            self.play(Create(crv_yeqx), run_time=1)
            self.play(FadeIn(label_yeqx), run_time=0.5)
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
