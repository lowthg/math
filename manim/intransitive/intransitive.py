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
        ABC_Cycle().render()