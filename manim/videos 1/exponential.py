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
        rec1 = SurroundingRectangle(obj, stroke_opacity=0, fill_opacity=0.7, fill_color=BLACK,
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
        self.play(LaggedStart(FadeOut(line1, eq5[:3] + eq9[1:]), ReplacementTransform(rec3, definition[1]),
                              lag_ratio=0.5), run_time=1)
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


class PropsNat(ExpNat):
    def create_properties(self):
        eq1 = MathTex(r'a^1=a')[0].set_z_index(2)
        eq2 = MathTex(r'a^{x+y}=a^x\;a^y')[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2)
        box = self.get_defbox(gp, props=True)
        return VGroup(gp, *box[:]).to_edge(UR, buff=0.1)

    def construct(self):
        defs = self.create_def()
        props = self.create_properties()
        props1 = ExpNat.create_properties(self)
        self.add(defs, props1)
        self.wait(0.5)

        eq6 = MathTex(r'a^{x+(y+1)}=a^{(x+y)+1}')[0].set_z_index(2)
        eq7 = MathTex(r'=a^{x+y}\;a')[0].set_z_index(2)
        eq7.next_to(eq6[8], ORIGIN, submobject_to_align=eq7[0])
        line = Line(eq6.get_left(), eq6.get_right(), color=RED, stroke_width=5).set_z_index(1).next_to(eq6, UP)
        eq1_1 = props[0][1].copy().move_to(ORIGIN).next_to(line, UP)
        eq2 = MathTex(r'a^{x+y}=a^{x+0}')[0].set_z_index(2).next_to(line, DOWN).align_to(eq1_1, LEFT)

        eq1 = eq1_1.copy().to_edge(DOWN)
        gp = VGroup(eq1_1, line, eq2, eq6, eq7).to_edge(DOWN)

        box1 = SurroundingRectangle(eq1, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK,
                                    corner_radius=0.2, buff=0.2)
        box2 = SurroundingRectangle(gp, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK,
                                    corner_radius=0.2, buff=0.2)

        eq3 = MathTex(r'=a^x\;1')[0].set_z_index(2)
        eq3.next_to(eq2[4], ORIGIN, submobject_to_align=eq3[0])
        eq4 = MathTex(r'=a^x\;a^0')[0].set_z_index(2)
        eq4.next_to(eq2[4], ORIGIN, submobject_to_align=eq4[0])
        eq5 = MathTex(r'=a^x\;a^y')[0].set_z_index(2)
        eq5.next_to(eq2[4], ORIGIN, submobject_to_align=eq5[0])

        self.play(LaggedStart(FadeIn(box1), FadeIn(eq1), lag_ratio=0.5), run_time=0.5)
        self.wait(0.5)
        self.play(eq1.animate.move_to(eq1_1), FadeIn(line),
                  ReplacementTransform(eq1[:5].copy() + box1, eq2[:5] + box2), run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq2[5:]), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq2[7:]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq3[-1]), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(defs[0][1][:2].copy(), eq4[-2:]), FadeOut(eq3[-1]), run_time=2)
        self.wait(0.1)
        self.play(FadeOut(eq4[-1]), FadeIn(eq5[-1]), ReplacementTransform(eq4[-2], eq5[-2]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq5[-2:], eq2[:7]), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(eq1[:3].copy() + eq1[3].copy() + eq1[4].copy(),
                                       eq6[:3] + eq6[4] + eq6[8]), run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq6[3], eq6[5:8]), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform((eq6[:1] + eq6[1:3] + eq6[3] + eq6[4] + eq6[5:7] + eq6[7]).copy(),
                                       eq6[9:10] + eq6[11:13] + eq6[10] + eq6[13] + eq6[15:17] + eq6[14]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq6[9:10] + eq6[11:14], eq7[1:2] + eq7[2:5]),
                  FadeOut(eq6[10], eq6[14:]), FadeIn(eq7[5]), run_time=2)

        eq8 = MathTex(r'=a^x\;a^y\;a')[0].set_z_index(2)
        eq8.next_to(eq6[8], ORIGIN, submobject_to_align=eq8[0])
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[-4:].copy() + eq7[5], eq8[1:5] + eq8[5]),
                  FadeOut(eq7[1:5]), run_time=1.5)

        eq9 = MathTex(r'=a^x\;a^{y+1}')[0].set_z_index(2)
        eq9.next_to(eq6[8], ORIGIN, submobject_to_align=eq9[0])
        self.play(ReplacementTransform(eq8[1:5], eq9[1:5]),
                  FadeIn(eq9[5:]), FadeOut(eq8[-1], target_position=eq9[3]),
                  run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(line, eq6[:9], eq9[1:]), run_time=1)

        self.wait(0.5)
        self.play(ReplacementTransform(eq1[:] + props1[0][0] + props1[1:], props[0][1][:] + props[0][0] + props[1:]),
                  FadeOut(box2),
                  run_time=2)

        self.wait(0.5)


class PropsNat2(PropsNat):
    def create_properties(self):
        eq1 = MathTex(r'a^1=a')[0].set_z_index(2)
        eq2 = MathTex(r'a^{x+y}=a^x\;a^y')[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'(a^x)^y=a^{xy}')[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'(ab)^x=a^x\;b^x')[0].set_z_index(2).next_to(eq3, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2, eq3, eq4)
        box = self.get_defbox(gp, props=True)
        return VGroup(gp, *box[:]).to_edge(UR, buff=0.1)

    def construct(self):
        defs = self.create_def()
        props = self.create_properties()
        props1 = PropsNat.create_properties(self)
        self.add(defs, props1)

        eqs = props[0][:3]
        box1 = self.get_defbox(eqs, props=True)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform(props1[1:] + props1[0][:2], box1[:] + eqs[:2]),
                              FadeIn(eqs[2]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform(box1[:] + eqs[:], props[1:] + props[0][:3]),
                              FadeIn(props[0][3]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.5)


class PropsNatPf(PropsNat2):
    def construct(self):
        defs = self.create_def()
        props = self.create_properties()
        self.add(defs, props)

        self.wait(0.5)
        eq1 = props[0][2].copy()
        eq2 = MathTex(r'y=0:', color=BLUE)[0].set_z_index(2)
        eq3 = MathTex(r'(a^x)^y{{=}}(a^x)^0{{=}}1{{=}}a^0{{=}}a^{x0}{{=}}a^{xy}').set_z_index(2)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3])
        eq3[5:7].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[5])
        eq3[7:9].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[7])
        eq3[9:11].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[9])
        eq4 = Tex(r'induction:', color=BLUE)[0].set_z_index(2)
        eq5 = MathTex(r'(a^x)^{y+1}{{=}}(a^x)^y\;a^x{{=}}a^{xy}\;a^x{{=}}a^{xy+x}{{=}}a^{x(y+1)}').set_z_index(2)
        eq5[3:5].next_to(eq5[1], ORIGIN, submobject_to_align=eq5[3])
        eq5[5:7].next_to(eq5[1], ORIGIN, submobject_to_align=eq5[5])
        eq5[7:9].next_to(eq5[1], ORIGIN, submobject_to_align=eq5[7])
        eq5.move_to(eq3)
        eq4.next_to(eq5, UP).align_to(eq5, LEFT)
        eq2.next_to(eq5, UP).align_to(eq5, LEFT)
        line = Line(eq5.get_left(), eq5.get_right(), buff=0, color=RED, stroke_width=5).next_to(eq4, UP, coor_mask=UP)
        eq1.next_to(line, UP)

        gp = VGroup(eq1, eq2, eq3, eq4, eq5, line).to_edge(DR)

        box = SurroundingRectangle(gp, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK,
                                   corner_radius=0.2, buff=0.2)

        eq6 = props[0][3].copy().next_to(line, UP)
        eq7 = MathTex(r'x=0:', color=BLUE)[0].set_z_index(1).move_to(eq2).align_to(eq2, LEFT)
        eq8 = MathTex(r'(ab)^x{{=}}(ab)^0{{=}}1{{=}}1\;1{{=}}a^0\;b^0{{=}}a^x\;b^x').set_z_index(2)
        eq8[3:5].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[3])
        eq8[5:7].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[5])
        eq8[7:9].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[7])
        eq8[9:11].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[9])
        eq8[4].move_to(eq8[2], coor_mask=RIGHT)
        eq8[6][0].move_to(eq8[8][:2], coor_mask=RIGHT)
        eq8[6][1].move_to(eq8[8][-2:], coor_mask=RIGHT)
        eq8.move_to(eq3)
        eq9 = MathTex(r'(ab)^{x+1}{{=}}(ab)^x\;ab{{=}}a^x\;b^x\;ab{{=}}a^x\;a\;b^x\;b{{=}}a^{x+1}\;b^{x+1}')\
            .set_z_index(2)
        eq9[3:5].next_to(eq9[1], ORIGIN, submobject_to_align=eq9[3])
        eq9[5:7].next_to(eq9[1], ORIGIN, submobject_to_align=eq9[5])
        eq9[7:9].next_to(eq9[1], ORIGIN, submobject_to_align=eq9[7])
        eq9.move_to(eq3)

        dt = 0.35

        self.play(LaggedStart(FadeIn(box), FadeIn(eq1, line), lag_ratio=0.5), run_time=dt)
        self.play(LaggedStart(FadeIn(eq2), ReplacementTransform((eq1[:5] + eq1[5]).copy(),
                                                                eq3[0][:] + eq3[1][0]),
                              lag_ratio=0.5), run_time=dt*2)
        self.play(ReplacementTransform(eq3[0][:4].copy(), eq3[2][:4]),
                  FadeOut(eq3[0][4].copy(), target_position=eq3[2][4]),
                  FadeIn(eq3[2][4], target_position=eq3[0][4]), run_time=dt*2)
        self.play(FadeOut(eq3[2]), FadeIn(eq3[4]), run_time=dt)
        self.play(FadeOut(eq3[4]), FadeIn(eq3[6]), run_time=dt)
        self.play(ReplacementTransform(eq3[6][:1] + eq3[6][1], eq3[8][:1] + eq3[8][2]),
                  FadeIn(eq3[8][1]), run_time=dt)
        self.play(ReplacementTransform(eq3[8][:2], eq3[10][:2]),
                  FadeOut(eq3[8][2]), FadeIn(eq3[10][2]), run_time=dt)
        self.wait(0.5)
        self.play(FadeOut(eq2, eq3[:2], eq3[-1]), run_time=dt)
        self.play(LaggedStart(FadeIn(eq4), ReplacementTransform((eq1[:5] + eq1[5]).copy(), eq5[0][:5] + eq5[1][0]),
                              lag_ratio=0.5), run_time=dt*2)
        self.play(FadeIn(eq5[0][5:]), run_time=dt)
        self.play(ReplacementTransform(eq5[0][:5].copy() + eq5[0][1:3].copy(), eq5[2][:5] + eq5[2][5:7]), run_time=dt*2)
        self.play(ReplacementTransform(eq1[6:].copy() + eq5[2][5:], eq5[4][:3] + eq5[4][3:]),
                  FadeOut(eq5[2][:5]), run_time=dt*2)
        self.play(ReplacementTransform(eq5[4][:3] + eq5[4][4], eq5[6][:3] + eq5[6][4]),
                  FadeIn(eq5[6][3]), FadeOut(eq5[4][3], target_position=eq5[6][0]),
                  run_time=dt)
        self.play(ReplacementTransform(eq5[6][:2] + eq5[6][2:4], eq5[8][:2] + eq5[8][3:5]),
                  FadeOut(eq5[6][4], target_position=eq5[8][5]), FadeIn(eq5[8][2], eq5[8][6]),
                  FadeIn(eq5[8][5], target_position=eq5[6][4]), run_time=dt)
        self.wait(0.5)
        self.play(FadeOut(eq1, eq4, eq5[:2], eq5[8]), run_time=dt)

        self.play(FadeIn(eq6), run_time=dt)
        self.play(LaggedStart(FadeIn(eq7), ReplacementTransform((eq6[:5] + eq6[5]).copy(), eq8[0][:] + eq8[1][0]),
                              lag_ratio=0.5), run_time=dt*2)
        self.play(ReplacementTransform(eq8[0][:4].copy(), eq8[2][:4]),
                  FadeOut(eq8[0][4].copy(), target_position=eq8[2][4]),
                  FadeIn(eq8[2][4], target_position=eq8[0][4]), run_time=dt*2)
        self.play(FadeOut(eq8[2]), FadeIn(eq8[4]), run_time=dt)
        self.play(ReplacementTransform(eq8[4][:1].copy() + eq8[4][0], eq8[6][:1] + eq8[6][1]), run_time=dt)
        self.play(FadeOut(eq8[6]), FadeIn(eq8[8]), run_time=dt)
        self.play(ReplacementTransform(eq8[8][:1] + eq8[8][2], eq8[10][:1] + eq8[10][2]),
                  FadeOut(eq8[8][1], eq8[8][3]), FadeIn(eq8[10][1], eq8[10][3]), run_time=dt)
        self.wait(0.5)
        self.play(FadeOut(eq7, eq8[:2], eq8[10]), run_time=dt)
        self.play(LaggedStart(FadeIn(eq4), ReplacementTransform((eq6[:5]+eq6[5]).copy(), eq9[0][:5] + eq9[1][0]),
                              lag_ratio=0.5), run_time=dt*2)
        self.play(FadeIn(eq9[0][5:]), run_time=dt)
        self.play(ReplacementTransform(eq9[0][:5].copy() + eq9[0][1:3].copy(), eq9[2][:5] + eq9[2][5:]), run_time=dt*2)
        self.play(ReplacementTransform(eq6[6:].copy() + eq9[2][5:], eq9[4][:4] + eq9[4][4:]),
                  FadeOut(eq9[2][:5]), run_time=dt*2)
        self.play(ReplacementTransform(eq9[4][:2] + eq9[4][2:4] + eq9[4][4] + eq9[4][5],
                                       eq9[6][:2] + eq9[6][3:5] + eq9[6][2] + eq9[6][5]), run_time=dt)
        self.play(ReplacementTransform(eq9[6][:2] + eq9[6][3:5], eq9[8][:2] + eq9[8][4:6]),
                  FadeOut(eq9[6][2], target_position=eq9[8][0]),
                  FadeOut(eq9[6][5], target_position=eq9[8][4]),
                  FadeIn(eq9[8][2:4], eq9[8][6:8]), run_time=dt)
        self.wait(0.5)
        self.play(FadeOut(eq6, line, eq4, eq9[:2], eq9[8], box), run_time=dt)
        self.wait(0.5)


class ExpInt(PropsNatPf):
    def create_def(self):
        eq1 = MathTex(r'x\in\mathbb Z, a\in\mathbb C\setminus\{0\}')[0].set_z_index(2)
        eq2 = MathTex(r'a^0=1')[0].next_to(eq1, DOWN).align_to(eq1, LEFT).set_z_index(2)
        eq3 = MathTex(r'a^{x+1}=a^x\;a')[0].next_to(eq2, DOWN).align_to(eq2, LEFT).set_z_index(2)
        gp = VGroup(eq1, eq2, eq3)
        box = self.get_defbox(gp)
        return VGroup(gp, *box[:]).to_edge(UL, buff=0.1)

    def create_properties(self):
        eqs = PropsNatPf.create_properties(self)[0]
        eq1 = MathTex(r'a^{-x}=1/a^x')[0].set_z_index(2).next_to(eqs[0], DOWN).align_to(eqs[0], LEFT)
        eqs[1:].next_to(eq1, DOWN, coor_mask=UP)
        gp = VGroup(eqs[0], eq1, *eqs[1:])
        box = self.get_defbox(gp, props=True)
        return VGroup(gp, *box[:]).to_edge(UR, buff=0.1)

    def construct(self):
        defs1 = PropsNatPf.create_def(self)
        props1 = PropsNatPf.create_properties(self)
        defs = self.create_def()
        props = self.create_properties()
        self.add(defs1, props1)
        self.wait(0.5)

        eq1 = defs1[0][2].copy().to_edge(DL)
        eq2 = MathTex(r'1{{=}}a^0{{=}}a^{-1+1}{{=}}a^{-1}\;a').set_z_index(2)
        eq2.next_to(eq1[4], ORIGIN, submobject_to_align=eq2[5])
        eq2[2:4].next_to(eq2[5], ORIGIN, submobject_to_align=eq2[3])
        eq2[:2].next_to(eq2[5], ORIGIN, submobject_to_align=eq2[1])
        eq3 = MathTex(r'a^{-(x+1)+1}{{=}}a^{-(x+1)}\;a').set_z_index(2)
        eq3.next_to(eq1[4], ORIGIN, submobject_to_align=eq3[1][0])

        VGroup(eq1, eq2, eq3).to_edge(DL)
        eq1_1 = eq1.copy()

        eq4 = MathTex(r'1/a^{-(x+1)}{{=}}a/a^{-x}').set_z_index(2)
        eq4.next_to(eq3[1][0], ORIGIN, submobject_to_align=eq4[1][0])
        eq5 = MathTex(r'1/a^{-x}{{=}}a^x').set_z_index(2)
        eq5.next_to(eq3[1][0], ORIGIN, submobject_to_align=eq5[1][0])

        box = SurroundingRectangle(VGroup(eq1, eq2, eq3), stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK,
                                   corner_radius=0.2, buff=0.2)

        self.play(ReplacementTransform(defs1[0][0][:2] + defs1[0][0][3:7], defs[0][0][:2] + defs[0][0][3:7]),
                  FadeIn(defs[0][0][2]), FadeOut(defs1[0][0][2]), run_time=1)
        self.play(FadeIn(box), ReplacementTransform(defs1[0][2].copy(), eq1), run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[:1] + eq1[2:4] + eq1[4] + eq1[5] + eq1[7],
                                       eq2[4][:1] + eq2[4][3:5] + eq2[5][0] + eq2[6][0] + eq2[6][3]),
                  FadeOut(eq1[1], eq1[6]), FadeIn(eq2[4][1:3], eq2[6][1:3]), run_time=1)
        self.play(ReplacementTransform(eq2[4][:1], eq2[2][:1]), FadeOut(eq2[4][1:]), FadeIn(eq2[2][1]), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq2[2]), FadeIn(eq2[0]), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform(defs1[0][1:] + defs1[1:], defs[0][1:] + defs[1:]),
                  FadeIn(defs[0][0][7:]), lag_ratio=0.5), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq2[0], eq2[5:]), FadeIn(eq1_1), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1_1[:1] + eq1_1[2:4] + eq1_1[4] + eq1_1[5] + eq1_1[7],
                                       eq3[0][:1] + eq3[0][7:9] + eq3[1][0] + eq3[2][0] + eq3[2][7]),
                  FadeOut(eq1_1[1], eq1_1[6]), FadeIn(eq3[0][1:7], eq3[2][1:7]),
                  run_time=2)
        self.wait(0.1)
        line1 = Line(eq3[0][5].get_corner(DL) + DL*0.05, eq3[0][5].get_corner(UR) + UR*0.05, color=RED, stroke_width=3).set_z_index(3)
        line2 = Line(eq3[0][8].get_corner(DL) + DL*0.05, eq3[0][8].get_corner(UR) + UR*0.05, color=RED, stroke_width=3).set_z_index(3)
        self.play(FadeIn(line1, line2), run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(FadeOut(line1, line2, eq3[0][4:6], eq3[0][7:9]),
                              FadeOut(eq3[0][2], eq3[0][6]), lag_ratio=0.5), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[0][:2] + eq3[0][3] + eq3[1] + eq3[2][:7] + eq3[2][7],
                                       eq4[2][2:4] + eq4[2][4] + eq4[1] + eq4[0][2:9] + eq4[2][0]),
                  FadeIn(eq4[2][1], eq4[0][:2]),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(eq4[0][4], eq4[0][6:], eq4[2][1]), FadeOut(eq4[2][2], target_position=eq5[2][0]),
                  FadeOut(eq4[2][3], target_position=eq5[2][1]),
                  ReplacementTransform(eq4[1][:] + eq4[2][0] + eq4[2][4], eq5[1][:] + eq5[2][0] + eq5[2][1]),
                  run_time=2)
        self.wait(0.5)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(props1[1:] + props1[0][0] + props1[0][1:],
                                                   props[1:] + props[0][0] + props[0][2:]),
                                             FadeOut(eq4[0][:4], eq4[0][5], eq5[1:], box)),
                              FadeIn(props[0][1]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.5)


class PlotInt(ExpInt):
    def get_graph(self, a):
        ax = Axes(x_range=[-5, 5.6], y_range=[0, a ** 5], z_index=2, x_length=6, y_length=3,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': True}).to_edge(DOWN, buff=0.2).set_z_index(2)
        box = SurroundingRectangle(VGroup(ax), fill_color=BLACK, fill_opacity=self.opacity, corner_radius=0.2,
                                   stroke_opacity=0)
        return ax, box

    def get_dots(self, ax, a, xvals, color=YELLOW, radius=DEFAULT_DOT_RADIUS, shiftx=0., scaley=1.)->VGroup:
        yvals = [a ** xvals[i] for i in range(len(xvals))]
        pts = [ax.coords_to_point(xvals[i] + shiftx, yvals[i] * scaley) for i in range(len(xvals))]
        dots = [Dot(pts[i], color=color, radius=radius).set_z_index(4) for i in range(len(xvals))]
        return VGroup(*dots)

    def construct(self):
        defs = self.create_def()
        props = self.create_properties()
        self.add(defs, props)
        self.wait(0.5)

        a = 1.5
        ax, box = self.get_graph(a)

        eq1 = MathTex(r'a=1.50', font_size=40)[0].move_to(ax.coords_to_point(-2.5, a**5))
        eq1.shift(DOWN*eq1.height)

        xvals = list(range(-5, 6))

        a_anim = ValueTracker(a)

        def generate_dots():
            a = a_anim.get_value()
            return self.get_dots(ax, a, xvals)

        def show_val():
            a = a_anim.get_value()
            eq = MathTex(r'a={:.2f}'.format(a), z_index=1)[0].set_z_index(4)
            eq.next_to(eq1[1], ORIGIN, submobject_to_align=eq[1])
            return eq

        dots = always_redraw(generate_dots)
        val = always_redraw(show_val)

        self.play(FadeIn(box, ax), run_time=2)
        self.wait(0.1)

        self.play(FadeIn(val), run_time=0.5)
        self.play(Create(dots), run_time=2)
        self.wait(0.5)
        self.play(a_anim.animate.set_value(1/a), run_time=2)
        self.play(a_anim.animate.set_value(a), run_time=2)

        self.wait(0.5)

        def f(x: float) -> float: return a**x

        graph = ax.plot(f, (-5, 5, 0.05), color=BLUE, stroke_width=5).set_z_index(2)
        self.play(Create(graph), run_time=2)
        self.wait(0.1)
        self.play(FadeOut(graph), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(box, val, dots, ax), run_time=1)


        self.wait(0.5)


class ExpRat(PlotInt):
    def create_def(self):
        defs = PlotInt.create_def(self)
        eq1 = MathTex(r'x\in\mathbb Q, a > 0,')[0].set_z_index(2)
        eq1_1 = MathTex(r'a^x\in\mathbb R')[0].set_z_index(2).next_to(eq1, DOWN, buff=0.1).align_to(eq1, LEFT)
        eq2 = defs[0][1].next_to(eq1_1, DOWN).align_to(eq1, LEFT)
        eq3 = defs[0][2].next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'(a^x)^n=a^{xn}')[0].set_z_index(2).next_to(eq3, DOWN)
        gp = VGroup(eq1, eq1_1, eq2, eq3, eq4)
        box = self.get_defbox(gp)
        return VGroup(gp, *box[:]).to_edge(UL, buff=0.1)

    def construct(self):
        defs1 = PlotInt.create_def(self)
        defs = self.create_def()
        props1 = PlotInt.create_properties(self)
        self.add(defs1, props1)
        self.wait(0.5)

        eq1 = MathTex(r'\left(a^{\frac mn}\right)^n{{=}}a^{\frac mnn}{{=}}a^m').set_z_index(2)
        eq1[3:].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3])
        eq2 = MathTex(r'a^{\frac mn}{{=}}\sqrt[n]{a^m}').set_z_index(2)
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq1[1])

        gp = VGroup(eq1, eq2).to_edge(DOWN)
        box = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0,
                                   corner_radius=0.2, buff=0.2)

        circ = abra.circle_eq(props1[0][3]).set_z_index(3).shift(RIGHT*0.2)
        self.play(Create(circ), run_time=1)
        self.wait(0.5)

        self.play(LaggedStart(FadeIn(box), FadeIn(eq1[:2]), lag_ratio=0.5), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform((eq1[0][1:5] + eq1[0][6]).copy(), eq1[2][:4] + eq1[2][4]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[2][:2], eq1[4][:]), FadeOut(eq1[2][2:]), run_time=2)
        self.wait(0.1)
        self.play(FadeOut(eq1[0][0], eq1[0][5]), ReplacementTransform(eq1[4][:] + eq1[0][6], eq2[2][3:] + eq2[2][0]),
                  FadeIn(eq2[2][1:3]), run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(defs1[0][0][:2], defs[0][0][:2]),
                  abra.fade_replace(defs1[0][0][2], defs[0][0][2]), run_time=1)
        self.wait(0.1)
        box1 = self.get_defbox(VGroup(defs1[0][0], defs[0][1:4]))
        self.play(ReplacementTransform(defs1[0][1:], defs[0][2:4]), FadeIn(defs[0][1]),
                  ReplacementTransform(defs1[1:], box1[:]), run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(defs1[0][0][3:5], defs[0][0][3:5]), FadeOut(defs1[0][0][5:]),
                  FadeIn(defs[0][0][5:]), run_time=2)
        self.wait(0.5)
        eq3 = props1[0][3].copy().set_z_index(5)
        self.play(ReplacementTransform(box1[:], defs[1:]),
                  eq3.animate.next_to(defs[0][4][6], ORIGIN, submobject_to_align=eq3[6]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[:4] + eq3[5:8], defs[0][4][:4] + eq3[5:8]),
                  abra.fade_replace(eq3[4], defs[0][4][4]),
                  abra.fade_replace(eq3[8], defs[0][4][8]),
                  run_time=1)
        self.wait(0.1)
        self.play(FadeOut(box, eq1[0][1:5], eq1[1], eq2[2], circ), run_time=1)
        self.wait(0.5)


class PlotRat(ExpRat):
    def get_rat_graph(self):
        a = 1.5
        ax, box = self.get_graph(a)
        radius = DEFAULT_DOT_RADIUS
        color = YELLOW
        dots = []
        for n in [1, 2, 3, 4, 5]:
            xvals = [i/n for i in range(-5*n, 5*n+1) if math.gcd(i, n) == 1]
            dots.append(self.get_dots(ax, a, xvals, color=color, radius=radius))
            radius = DEFAULT_DOT_RADIUS * 0.35
            color = BLUE

        return VGroup(ax, box, VGroup(*dots))

    def construct(self):
        defs = self.create_def()
        props = self.create_properties()
        self.add(defs, props)
        graph = self.get_rat_graph()

        self.wait(0.5)
        self.play(FadeIn(graph[:2]), run_time=1)
        self.wait(0.1)

        dt = 2
        for dots in graph[2][:]:
            self.play(Create(dots), run_time=dt)
            dt = 1
            self.wait(0.1)

        self.wait(0.5)
        self.play(FadeOut(graph), run_time=1)
        self.wait(0.5)


class PropsRat(PlotRat):
    def create_def(self):
        def1 = PlotRat.create_def(self)
        eq1 = def1[0][0]
        eq2 = def1[0][1]
        eq3 = MathTex(r'a^1=a')[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'a^{x+y}=a^x\;a^y')[0].set_z_index(2).next_to(eq3, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2, eq3, eq4)
        box = self.get_defbox(gp)
        return VGroup(gp, *box[:]).to_edge(UL, buff=0.1)

    def create_properties(self):
        prop1 = PlotRat.create_properties(self)
        eq1 = MathTex(r'a^0=1')[0].set_z_index(2)
        eq2 = prop1[0][1].next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = prop1[0][3].next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = prop1[0][4].next_to(eq3, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2, eq3, eq4)
        box = self.get_defbox(gp, props=True)
        return VGroup(gp, *box[:]).to_edge(UR, buff=0.1)

    def construct(self):
        def1 = PlotRat.create_def(self)
        defs = self.create_def()
        prop1 = PlotRat.create_properties(self)
        props = self.create_properties()

        self.add(def1, prop1)
        self.wait(0.5)

        circ = abra.circle_eq(prop1[0][2]).set_z_index(3)
        self.play(Create(circ), run_time=1)

        eq1 = MathTex(r'(a^x)^n{{=}}a^x\;a^x\cdots a^x{{=}}a^{x+x}\cdots a^x{{=}}a^{x+x+\cdots+x}{{=}}a^{xn}').set_z_index(2)
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3])
        eq1[5:7].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[5])
        eq1[7:9].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[7])
        eq1.move_to(ORIGIN).to_edge(DOWN)
        box1 = SurroundingRectangle(eq1, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0, corner_radius=0.2)

        self.wait(0.5)
        self.play(FadeIn(box1, eq1[:2]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq1[2]), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[2][:2] + eq1[2][3] + eq1[2][-5:], eq1[4][:2] + eq1[4][3] + eq1[4][-5:]),
                  FadeOut(eq1[2][2], target_position=eq1[4][0]), FadeIn(eq1[4][2]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[4][:4] + eq1[4][4:7] + eq1[4][-1], eq1[6][:4] + eq1[6][5:8] + eq1[6][-1]),
                  FadeOut(eq1[4][-2], target_position=eq1[6][0]),
                  FadeIn(eq1[6][4], eq1[6][8]), run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[6][:2], eq1[8][:2]),
                  FadeOut(eq1[6][2], target_position=eq1[8][1]),
                  FadeOut(eq1[6][3], target_position=eq1[8][1]),
                  FadeOut(eq1[6][4], target_position=eq1[8][1]),
                  FadeOut(eq1[6][5:8], target_position=eq1[8][1]),
                  FadeOut(eq1[6][8], target_position=eq1[8][1]),
                  FadeOut(eq1[6][9], target_position=eq1[8][1]),
                  FadeIn(eq1[8][2]), run_time=2)

        self.wait(0.1)
        eq2 = prop1[0][2].set_z_index(4)
        self.play(eq2.animate.move_to(def1[0][4]).align_to(def1[0][0], LEFT),
                  FadeOut(circ, def1[0][4], box1, eq1[:2], eq1[8]), run_time=2)

        self.wait(0.5)
        eq3 = MathTex(r'a^{x+1}=a^x\;a^1')[0].set_z_index(2).to_edge(DOWN)
        box2 = SurroundingRectangle(eq3, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0, corner_radius=0.2)
        eq4 = eq2.copy()
        self.play(FadeIn(box2), eq4.animate.next_to(eq3[4], ORIGIN, submobject_to_align=eq4[4]), run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4[:3] + eq4[4:8], eq3[:3] + eq3[4:8]),
                  abra.fade_replace(eq4[3], eq3[3]), abra.fade_replace(eq4[8], eq3[8]),
                  run_time=1)
        self.wait(0.5)

        eq5 = prop1[0][0]
        self.play(eq5.animate.move_to(def1[0][3]).align_to(def1[0][0], LEFT), FadeOut(def1[0][3], box2, eq3), run_time=2)

        eq6 = MathTex(r'a^0\;a{{=}}a^0\;a^1{{=}}a^{0+1}{{=}}a^1').set_z_index(2)
        eq6[3:5].next_to(eq6[1], ORIGIN, submobject_to_align=eq6[3])
        eq6[5:7].next_to(eq6[1], ORIGIN, submobject_to_align=eq6[5])
        eq6.move_to(ORIGIN).to_edge(DOWN)
        box3 = SurroundingRectangle(eq6, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0, corner_radius=0.2)

        self.wait(0.5)
        self.play(FadeIn(box3, eq6[:2]), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq6[0][:3].copy(), eq6[2][:3]), FadeIn(eq6[2][3], target_position=eq6[1]), run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq6[2][:2] + eq6[2][3], eq6[4][:2] + eq6[4][3]),
                  FadeOut(eq6[2][2], target_position=eq6[4][0]),
                  FadeIn(eq6[4][2]), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq6[4][:1] + eq6[4][3], eq6[6][:1] + eq6[6][1]),
                  FadeOut(eq6[4][1:3]), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq6[6][1]), run_time=1)

        line1 = Line(eq6[0][2].get_corner(DL)+DL*0.1, eq6[0][2].get_corner(UR)+UR*0.1, color=RED, stroke_width=5).set_z_index(3)
        line2 = Line(eq6[6][0].get_corner(DL)+DL*0.1, eq6[6][0].get_corner(UR)+UR*0.1, color=RED, stroke_width=5).set_z_index(3)
        eq7 = MathTex(r'{{=}}1').set_z_index(2)
        eq7.next_to(eq6[1], ORIGIN, submobject_to_align=eq7[0])
        self.wait(0.1)
        self.play(FadeIn(line1, line2), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(line1, line2, eq6[0][2], eq6[6][0]), FadeIn(eq7[1]), run_time=2)
        self.wait(0.5)

        eq8 = def1[0][2]
        self.play(eq8.animate.next_to(prop1[0][1], UP).align_to(prop1[0][1], LEFT), FadeOut(box3, eq6[0][:2], eq6[1], eq7[1]),
                  run_time=2)

        self.wait(0.5)
        self.play(ReplacementTransform(def1[1:] + def1[0][:2] + eq5 + eq2,
                                       defs[1:] + defs[0][:2] + defs[0][2] + defs[0][3]),
                  ReplacementTransform(prop1[1:] + eq8 + prop1[0][1] + prop1[0][3:5],
                                       props[1:] + props[0][0] + props[0][1] + props[0][2:4]),
                  run_time=2)


        self.wait(0.5)


class ConvexRat(PropsRat):
    def create_def(self):
        defs = PropsRat.create_def(self)
        eq1 = MathTex(r'x\in\mathbb R, a > 0,')[0].set_z_index(2)
        defs[0][1:].next_to(eq1, DOWN, buff=0.1).align_to(eq1, LEFT)
        eq2 = Tex(r'continuous')[0].next_to(defs[0][-1], DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, *defs[0][1:], eq2)
        box = self.get_defbox(gp)
        return VGroup(gp, *box[:]).to_edge(UL, buff=0.1)

    def create_properties(self):
        props = PropsRat.create_properties(self)
        eq = Tex(r'convex')[0].next_to(props[0][-1], DOWN).align_to(props[0][0], LEFT)
        gp = VGroup(*props[0][:], eq)
        box = self.get_defbox(gp, props=True)
        return VGroup(gp, *box[:]).to_edge(UR, buff=0.1)

    def animate_dots(self, ax, a, xvals, dots):
        x_anim = ValueTracker(0.)
        y_anim = ValueTracker(1.)

        def shifted_dots():
            dx = x_anim.get_value()
            dy = y_anim.get_value()
            dots = self.get_dots(ax, a, xvals, color=GREY, radius=DEFAULT_DOT_RADIUS * 0.4, shiftx=dx, scaley=dy).set_z_index(3)
            return dots

        sdots = always_redraw(shifted_dots)
        dx = 1.5
        self.add(sdots)
        self.play(x_anim.animate.set_value(dx), run_time=1.5)
        dots.set_z_index(2.5)
        self.wait(0.1)
        self.play(y_anim.animate.set_value(a**dx), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(sdots), run_time=1)
        self.remove(sdots)
        self.wait(0.5)

    def construct(self):
        def1 = PropsRat.create_def(self)
        prop1 = PropsRat.create_properties(self)
        self.add(def1, prop1)
        self.wait(0.5)

        a = 1.5
        n = 10 * 6 + 1
        xvals = np.linspace(-5.0, 5.0, n)
        ax, box = self.get_graph(a)

        self.play(FadeIn(box, ax), run_time=1)
        dots = self.get_dots(ax, a, xvals, color=BLUE, radius=DEFAULT_DOT_RADIUS*0.4)
        self.wait(0.1)
        self.play(Create(dots), run_time=1)
        self.wait(0.1)

#        self.animate_dots(ax, a, xvals, dots)

        # convex
        x1 = 1.0
        x2 = 5.0
        dots2 = self.get_dots(ax, a, [x1, x2], color=YELLOW).set_z_index(5)
        self.play(Create(dots2), run_time=1)
        line1 = Line(dots2[0].get_center(), dots2[1].get_center(), color=RED, stroke_width=3).set_z_index(1)
        self.play(Create(line1), run_time=1)
        self.wait(0.1)
        xvals2 = np.linspace(x1, x2, 4)
        dots3 = self.get_dots(ax, a, xvals2, color=YELLOW, radius=DEFAULT_DOT_RADIUS*0.8).set_z_index(5)
        i1 = 2
        x = xvals2[i1]
        dot = dots3[i1]
        self.play(FadeIn(dot), run_time=1)
        self.wait(0.1)

        pt = ax.coords_to_point(x, ((a**x1)*(x2-x) + (a**x2)*(x-x1))/(x2-x1))
        line2 = Line(dot.get_center(), pt, color=GREY, stroke_width=5).set_z_index(2)
        self.play(Create(line2), run_time=1)
        self.wait(0.5)
        self.play(Create(dots3[1:i1] + dots3[i1+1:-1]), run_time=1)
        self.wait(0.1)
        lines=VGroup()
        for i in range(1, len(xvals2)):
            lines += Line(dots3[i-1], dots3[i], color=RED, stroke_width=6).set_z_index(3)
        self.play(Create(lines), run_time=2)
        self.wait(0.1)

        eq1 = MathTex(r'\frac{a^{x+2h}-a^{x+h}}{h}-\frac{a^{x+h}-a^x}{h}')[0].move_to(box).to_edge(LEFT, buff=0.3)
        box2 = SurroundingRectangle(VGroup(eq1, ax), fill_opacity=self.opacity, fill_color=BLACK, stroke_opacity=0, corner_radius=0.2)
        box3 = box.copy()
        self.play(LaggedStart(ReplacementTransform(box, box2), FadeIn(eq1), lag_ratio=0.5), run_time=1)
        self.wait(0.1)
        eq2 = MathTex(r'\frac{a^xa^{2h}-a^xa^h}{h}-\frac{a^xa^h-a^x}{h}')[0].move_to(eq1).align_to(eq1, LEFT)
        self.play(ReplacementTransform(eq1[:2] + eq1[0].copy() + eq1[3:8] + eq1[6].copy() + eq1[9:15] + eq1[13].copy() + eq1[16:],
                                       eq2[:2] + eq2[2] + eq2[3:8] + eq2[8] + eq2[9:15] + eq2[15] + eq2[16:]),
                  FadeOut(eq1[2], eq1[8], eq1[15]),
                  run_time=2)
        self.wait(0.1)
        eq3 = MathTex(r'\frac{a^xa^{2h}-a^xa^h-a^xa^h+a^x}{h}')[0]
        eq3.next_to(eq2[-2], ORIGIN, submobject_to_align=eq3[-2]).align_to(eq2, LEFT)
        self.play(ReplacementTransform(eq2[:10] + eq2[10] + eq2[12:17] + eq2[18:20] + eq2[-1],
                                       eq3[:10] + eq3[-2] + eq3[10:15] + eq3[16:18] + eq2[11]),
                  abra.fade_replace(eq2[17], eq3[15]),
                  FadeOut(eq2[-2]),
                  run_time=2)
        self.wait(0.1)
        eq4 = MathTex(r'\frac{a^x}{h}\left(a^{2h}-a^h-a^h+1\right)')[0]
        eq4.next_to(eq3[-2], ORIGIN, submobject_to_align=eq4[2]).align_to(eq3, LEFT)
        self.play(ReplacementTransform(eq3[:2], eq4[:2]),
                  ReplacementTransform(eq3[6:8], eq4[:2]),
                  ReplacementTransform(eq3[11:13], eq4[:2]),
                  ReplacementTransform(eq3[16:18], eq4[:2]),
                  ReplacementTransform(eq3[2:6] + eq3[8:11] + eq3[13:16] + eq3[-2] + eq2[11],
                                       eq4[5:9] + eq4[9:12] + eq4[12:15] + eq4[2] + eq4[3]),
                  FadeIn(eq4[-2], target_position=eq3[-4]),
                  FadeIn(eq4[4], eq4[-1]),
                  run_time=2)
        self.wait(0.1)
        eq5 = MathTex(r'\frac{a^x}{h}\left(a^{2h}-2a^h+1\right)')[0]
        eq5.next_to(eq4[2], ORIGIN, submobject_to_align=eq5[2])
        self.play(ReplacementTransform(eq4[:9] + eq4[9:11], eq5[:9] + eq5[10:12]),
                  ReplacementTransform(eq4[12:14] + eq4[11] + eq4[14:], eq5[10:12] + eq5[8] + eq5[12:]),
                  FadeIn(eq5[9]),
                  run_time=2)
        self.wait(0.1)
        eq6 = MathTex(r'\frac{a^x}{h}\left(a^h-1\right)^2\ge0')[0]
        eq6.next_to(eq5[2], ORIGIN, submobject_to_align=eq6[2])
        self.play(ReplacementTransform(eq5[:6] + eq5[6] + eq5[7:9] + eq5[13:15],
                                       eq6[:6] + eq6[10] + eq6[6:8] + eq6[8:10]),
                  FadeOut(eq5[12], target_position=eq6[7]),
                  FadeOut(eq5[9:12]),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq6[-2:]), run_time=1)
        self.wait(0.5)
        line3 = Line(dots2[0], dots3[i1], color=RED, stroke_width=6).set_z_index(3)
        self.play(FadeOut(dots3[1:i1], lines[:i1]), Create(line3, rate_func=linear), run_time=1)
        self.wait(0.1)
        line4 = Line(dots3[i1], dots2[1], color=RED, stroke_width=6).set_z_index(3)
        self.play(FadeOut(dots3[i1+1:-1], lines[i1:]), Create(line4, rate_func=linear), run_time=1)
        self.wait(0.1)

        self.play(LaggedStart(FadeOut(eq6), ReplacementTransform(box2, box3), lag_ratio=0.3), run_time=1)
        self.wait(0.5)

        props = self.create_properties()
        self.play(LaggedStart(ReplacementTransform(prop1[1:] + prop1[0][:], props[1:] + props[0][:-1]),
                              FadeIn(props[0][-1]), lag_ratio=0.5),
                  FadeOut(dots2, dots3[i1], line3, line4, line1, line2),
                  run_time=1)
        self.wait(0.5)

        dots2 = self.get_dots(ax, a, [-1.0, 4.0], color=YELLOW).set_z_index(5)
        self.play(Create(dots2), run_time=1)
        dots3 = self.get_dots(ax, a, [-3.0, 5.0], color=YELLOW).set_z_index(5)
        line1 = Line(dots3[0], dots2[0], color=GREY, stroke_width=5).set_z_index(4)
        line2 = Line(dots3[1], dots2[1], color=GREY, stroke_width=5).set_z_index(4)
        self.wait(0.1)
        self.play(Create(VGroup(line1, line2)), run_time=1)
        self.wait(0.1)
        dots4 = self.get_dots(ax, a, [1, 2], color=RED).set_z_index(5)
        line3 = Line(dots4[0], dots4[1], color=RED, stroke_width=6).set_z_index(4)
        self.play(FadeIn(dots4), Create(line3), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(dots2, line1, line2, line3, dots4))
        self.wait(0.5)

        graph = ax.plot(lambda x: a**x, (-5, 5, 0.05), color=BLUE, stroke_width=5).set_z_index(3)
        self.play(FadeOut(dots), FadeIn(graph), run_time=1)
        self.wait(0.5)

        defs = self.create_def()
        self.play(ReplacementTransform(def1[0][1:] + def1[0][0][:2] + def1[0][0][3:],
                                       defs[0][1:-1] + defs[0][0][:2] + defs[0][0][3:]),
                  abra.fade_replace(def1[0][0][2], defs[0][0][2]),
                  run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(def1[1:], defs[1:]),
                              FadeIn(defs[0][-1]), lag_ratio=0.5),
                  FadeOut(box3, ax, graph),
                  run_time=2)

        self.wait(0.5)


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "fps": 15, "preview": True}):
        PlotInt().render()