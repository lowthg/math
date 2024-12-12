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


class EulerIntro(Scene):
    def construct(self):
        eq1 = MathTex(r'e^{i\pi}+1=0', font_size=180)[0]
        eq2 = MathTex(r'0\ 1\ {}^i\ \pi\ e', font_size=180)[0]
        eq3 = MathTex(r'e\ {}^i\ \pi\ 1\ 0', font_size=180)[0]
        eq2[2].scale(1.4).align_to(eq2[1], DOWN)
        eq3[1].scale(1.4).align_to(eq3[3], DOWN)
        self.add(eq2)
        self.play(ReplacementTransform(eq2[2:4] + eq2[0] + eq2[1] + eq2[4],
                                       eq3[1:3] + eq3[4] + eq3[3] + eq3[0]),
                  run_time=2)
        self.play(LaggedStart(ReplacementTransform(eq3[:3] + eq3[3] + eq3[4],
                                                   eq1[:3] + eq1[4] + eq1[6]),
                              FadeIn(eq1[3], eq1[5], run_time=0.5),
                              lag_ratio=0.6),
                  run_time=3)
        self.wait(0.5)
        eq3 = MathTex(r'\sqrt{-1}', font_size=80, color=BLUE)[0].next_to(eq1[1], UL, buff=0.8)
        arr1 = Arrow(eq3.get_corner(DR) + DR * 0.1, eq1[1].get_corner(UL), color=RED, buff=0)
        self.play(FadeIn(eq3, arr1), run_time=1)
        self.wait(0.1)
        rad = 0.7
        circ = Circle(radius=rad, stroke_color=BLUE).next_to(eq1[2], UR).shift(UR*0.4)\
            .next_to(eq3, ORIGIN,coor_mask=UP).set_z_index(5)
        arr2 = Arrow(circ.get_corner(DL), eq1[2].get_corner(UR) + UR*0.1, color=RED, buff=0)
        self.play(FadeIn(circ, arr2), run_time=1)
        self.wait(0.1)
        circ2 = Circle(radius=rad, stroke_opacity=0, fill_opacity=0.4, fill_color=TEAL_E).set_z_index(3).move_to(circ)
        self.play(Create(circ2), run_time=1)
        arc = Arc(radius=rad, arc_center=circ.get_center(), angle=PI, color=RED_D, stroke_width=10, stroke_opacity=1).set_z_index(7)
        self.play(Create(arc), rate_func=linear, run_tim=1)
        self.wait(0.1)
        eq4 = eq1[0].copy().set_color(RED).scale(1.2)
        self.play(Transform(eq1[0], eq4, rate_func=rate_functions.there_and_back), run_time=2)
        self.wait(0.1)
        eq5 = eq1[1:3].copy().set_color(RED).scale(1.2)
        self.play(Transform(eq1[1:3], eq5, rate_func=rate_functions.there_and_back), run_time=2)
        self.wait(0.5)


class ExpPosint(Scene):
    bgcolor=GREY_D
    opacity=0.6

    def __init__(self, *args, **kwargs):
        config.background_color = self.bgcolor
        Scene.__init__(self, *args, *kwargs)

    def get_defbox(self, obj, props=False):
        color = BLUE if props else RED
        txt = r'properties' if props else r'definition'
        rec1 = SurroundingRectangle(obj, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK,
                                    corner_radius=0.2, buff=0.2)
        rec2 = RoundedRectangle(width=rec1.width, height=rec1.height, fill_color=0, stroke_opacity=0.8,
                                stroke_color=color, stroke_width=5, corner_radius=0.2).move_to(rec1).set_z_index(1)
        top = rec2.get_subcurve(0.125, 0.25)
        txt2 = Tex(txt, color=color, font_size=30)[0].move_to(top)
        h = txt2.width/top.width*1.05
        edge = VGroup(rec2.get_subcurve(0.1875 + h*0.0625, 1), rec2.get_subcurve(0, 0.1875 - h*0.0625))

        return VGroup(rec1, edge, txt2)

    def create_def(self):
        eq1 = MathTex(r'x=1,2,3,\ldots')[0].set_z_index(2)
        eq3 = MathTex(r'a^1=a')[0].next_to(eq1, DOWN).align_to(eq1, LEFT).set_z_index(2)
        eq4 = MathTex(r'a^{x+1}=a^x\;a')[0].next_to(eq3, DOWN).align_to(eq3, LEFT).set_z_index(2)
        eqs = VGroup(eq1, eq3, eq4)
        box = self.get_defbox(eqs)

        return VGroup(eqs, *box[:]).to_edge(UL, buff=0.1)

    def construct(self):
        definition = self.create_def()
        pos = definition.get_center()

        MathTex.set_default(z_index=2)
        eq1 = definition[0][0]
        eq2 = MathTex(r'a^n{{=}}aa\cdots a').next_to(eq1, DOWN).align_to(eq1, LEFT).set_z_index(2)
        txt1 = MathTex(r'n\ {\rm copies\ of\ }a', font_size=40, color=RED)
        br1 = BraceLabel(eq2[2], r'', brace_direction=DOWN,
                         label_constructor=abra.brace_label(txt1),
                         brace_config={'color': RED})
        eq3 = definition[0][1]
        eq4 = definition[0][2]

        gp1 = VGroup(eq1, eq2, eq3, eq4, br1)
        gp2 = VGroup(eq1, eq2, eq3, eq4)

        line1 = Line(gp2.get_left(), gp2.get_right(), buff=0, stroke_color=RED, stroke_width=4, z_index=1)\
            .next_to(eq4, DOWN, coor_mask=UP)

        eq5 = MathTex(r'a^3=a^{2+1}')[0].next_to(line1, DOWN).align_to(eq4, LEFT)
        eq6 = MathTex(r'=a^2\;a')[0]
        eq6.next_to(eq5[2], ORIGIN, submobject_to_align=eq6[0])
        eq7 = MathTex(r'=a^{1+1}\;a')[0]
        eq7.next_to(eq5[2], ORIGIN, submobject_to_align=eq7[0])
        eq8 = MathTex(r'=a^{1}\;a\;a')[0]
        eq8.next_to(eq5[2], ORIGIN, submobject_to_align=eq8[0])
        eq9 = MathTex(r'=a\;a\;a')[0]
        eq9.next_to(eq5[2], ORIGIN, submobject_to_align=eq9[0])

        gp3 = VGroup(eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9)

        VGroup(definition, eq2, eq5, eq6, eq7, eq8, eq9, line1, br1).to_edge(DL).shift(RIGHT*0.4)
        rec1 = SurroundingRectangle(gp1, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK, corner_radius=0.2,
                                    buff=0.2)
        rec2 = definition[1].copy()
        rec3 = SurroundingRectangle(gp3, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK, corner_radius=0.2,
                                    buff=0.2)


        self.add(rec1)
        self.wait(0.5)
        eq1_1 = MathTex(r'n=')[0].set_z_index(2)
        eq1_1.next_to(eq1[1], ORIGIN, submobject_to_align=eq1_1[1])
        self.play(FadeIn(eq1_1[0], eq1[1:]), run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(FadeIn(eq2), FadeIn(br1), lag_ratio=0.5), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq2, br1), ReplacementTransform(rec1, rec2), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq3), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq4, eq1[0]), FadeOut(eq1_1), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(line1), ReplacementTransform(rec2, rec3), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq5[:3]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeIn(eq5[3:]), run_time=0.5)
        self.play(ReplacementTransform(eq5[3:5] + eq5[3].copy(), eq6[1:3] + eq6[3]),
                  FadeOut(eq5[5:7]), run_time=2)
        self.play(ReplacementTransform(eq6[1:2] + eq6[3], eq7[1:2] + eq7[5]),
                  FadeOut(eq6[2]), FadeIn(eq7[2:5]), run_time=2)
        self.play(ReplacementTransform(eq7[1:3] + eq7[1].copy(), eq8[1:3] + eq8[3]),
                  FadeOut(eq7[3:5]), run_time=2)
        self.play(FadeOut(eq8[2]), ReplacementTransform(eq8[1:2] + eq8[3] + eq7[5], eq9[1:2] + eq9[2] + eq9[3]),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(line1), FadeOut(eq5[:3] + eq9[1:], target_position=eq4), ReplacementTransform(rec3, definition[1]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(definition[2:]), run_time=1)
        self.wait(0.1)
        self.play(definition.animate.move_to(pos), run_time=1.5)
        self.wait(0.5)


class ExpNat(ExpPosint):

    def create_def(self):
        eq1 = MathTex(r'x\in\mathbb N, a\in\mathbb C')[0].set_z_index(2)
        eq2 = MathTex(r'a^0=1')[0].next_to(eq1, DOWN).align_to(eq1, LEFT).set_z_index(2)
        eq3 = MathTex(r'a^{x+1}=a^x\;a')[0].next_to(eq2, DOWN).align_to(eq2, LEFT).set_z_index(2)
        gp = VGroup(eq1, eq2, eq3)
        box = self.get_defbox(gp)
        return VGroup(gp, *box[:]).to_edge(UL, buff=0.1)

    def create_properties(self):
        eq1 = MathTex(r'a^1=a')[0].set_z_index(2)
        box = self.get_defbox(eq1, props=True)
        return VGroup(VGroup(eq1), *box[:]).to_edge(UR, buff=0.1)

    def construct(self):
        def1 = ExpPosint.create_def(self)
        def2 = self.create_def()
        self.add(def1)
        props = self.create_properties()
        self.wait(0.5)

        eq1 = def1[0][0]
        eq2 = MathTex(r'x = 0,1,2,\ldots')[0].set_z_index(2)
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq2[1])
        self.play(ReplacementTransform(eq1[:2] + eq1[2:6] + eq1[8:], eq2[:2] + eq2[4:8] + eq2[8:]),
                  FadeOut(eq1[6:8], target_position=eq2[8:].get_center()*RIGHT + eq1[6:8].get_center()*UP),
                  FadeIn(eq2[2:4]),
                  run_time=1.5)
        self.wait(0.5)

        eq3 = MathTex(r'a^{0+1}=a^0\;a')[0].set_z_index(2)
        rect1 = SurroundingRectangle(eq3, buff=0.2, fill_opacity=self.opacity, stroke_opacity=0,
                                     corner_radius=0.2, fill_color=BLACK)
        VGroup(rect1, eq3).to_edge(DL).shift(RIGHT*0.4)
        eq3_1 = def1[0][2].copy()
        shift = eq3[4].get_center()-eq3_1[4].get_center()
        self.add(eq3_1)
        self.play(eq3_1.animate.shift(shift), FadeIn(rect1), run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq3_1[2:6] + eq3_1[0] + eq3_1[7], eq3[2:6] + eq3[0] + eq3[7]),
                  FadeOut(eq3_1[1], eq3_1[6]), FadeIn(eq3[1], eq3[6]), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq3[1:3]), eq3[3].animate.move_to(eq3[1], coor_mask=RIGHT), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq3[3]), run_time=1)
        self.wait(0.1)
        line1 = Line(eq3[0].get_corner(DL)+DL*0.1, eq3[0].get_corner(UR)+UR*0.1, color=RED, stroke_width=7, buff=-0.2).set_color(RED)
        line2 = Line(eq3[7].get_corner(DL)+DL*0.1, eq3[7].get_corner(UR)+UR*0.1, color=RED, stroke_width=7).set_color(RED)
        eq4 = MathTex(r'1=')[0].set_z_index(2)
        eq4.next_to(eq3[4], ORIGIN, submobject_to_align=eq4[1])
        self.play(FadeIn(line1, line2), run_time=0.5)
        self.wait(0.1)
        self.play(FadeOut(line1, line2, eq3[0], eq3[7]), run_time=1)
        self.play(FadeIn(eq4[0]), run_time=0.5)
        eq5 = MathTex(r'a^0=1')[0]
        eq5.next_to(eq3[4], ORIGIN, submobject_to_align=eq5[2])
        eq6 = eq5.copy()
        eq7 = MathTex(r'0^0=1')[0].set_z_index(2)
        eq7.next_to(eq6[2], ORIGIN, submobject_to_align=eq7[2])
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[5:7] + eq3[4] + eq4[0], eq5[:2] + eq5[2] + eq5[3]), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq5, def2[0][1]), ReplacementTransform(def1[0][2], def2[0][2]),
                  FadeOut(def1[0][1]), run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(def2[0][1].copy(), eq6), run_time=2)
        self.play(ReplacementTransform(eq6[1:], eq7[1:]), FadeOut(eq6[0]), FadeIn(eq7[0]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq7, rect1), run_time=1)

        eq8 = MathTex(r'a^1=a^{0+1}')[0].set_z_index(2)
        eq9 = MathTex(r'=a^0\;a')[0].set_z_index(2)
        eq10 = MathTex(r'=1\;a')[0].set_z_index(2)
        eq11 = MathTex(r'=a')[0].set_z_index(2)
        rect2 = SurroundingRectangle(eq8, buff=0.2, fill_opacity=self.opacity, stroke_opacity=0,
                                     corner_radius=0.2, fill_color=BLACK)
        VGroup(rect2, eq8).to_edge(DL).shift(RIGHT*0.4)
        eq9.next_to(eq8[2], ORIGIN, submobject_to_align=eq9[0])
        eq10.next_to(eq8[2], ORIGIN, submobject_to_align=eq10[0])
        eq11.next_to(eq8[2], ORIGIN, submobject_to_align=eq11[0])

        self.play(FadeIn(rect2), run_time=0.5)
        self.play(FadeIn(eq8), run_time=0.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq8[3:5] + eq8[3].copy(), eq9[1:3] + eq9[3]), FadeOut(eq8[5:7]), run_time=1.5)
        eq10[1].move_to(eq9[1:3], coor_mask=RIGHT)
        self.play(FadeOut(eq9[1:3]), FadeIn(eq10[1]), run_time=1.5)
        self.play(ReplacementTransform(eq9[3], eq11[1]), FadeOut(eq10[1]), run_time=1.5)
        self.wait(0.5)
        p2 = props.copy()
        p2.shift(eq8[2].get_center()-p2[0][0][2].get_center())
        self.play(ReplacementTransform(eq8[:3] + eq11[1] + rect2, p2[0][0][:3] + p2[0][0][3] + p2[1]),
                  run_time=1)
        self.play(FadeIn(p2[2:]), run_time=1.5)
        self.wait(0.1)
        self.play(p2.animate.move_to(props), run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(eq2[0], def2[0][0][0]),
                  ReplacementTransform(def1[1:], def2[1:]),
                  FadeOut(eq2[1:]), FadeIn(def2[0][0][1:3]), run_time=2)
        self.wait(0.1)
        self.play(FadeIn(def2[0][0][3:]), run_time=1)

        self.wait(0.5)
