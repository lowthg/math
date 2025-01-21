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

    def get_defbox(self, obj, props=False, e=False):
        color = BLUE if props else RED
        txt = r'properties' if props else r'definition'
        if e:
            txt = r'$e^x$ ' + txt
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
        eq4 = MathTex(r'a^{x+1}=a^xa')[0].next_to(eq3, DOWN).align_to(eq3, LEFT).set_z_index(2)
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
        eq3 = MathTex(r'a^{x+1}=a^xa')[0].next_to(eq2, DOWN).align_to(eq2, LEFT).set_z_index(2)
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

        eq3 = MathTex(r'a^{0+1}=a^0a')[0].set_z_index(2)
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
        eq9 = MathTex(r'=a^0a')[0].set_z_index(2)
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


class PropsNatNew(ExpNat):
    def create_properties(self):
        eq1 = MathTex(r'a^1=a')[0].set_z_index(2)
        eq2 = MathTex(r'a^{x+y}=a^xa^y')[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'(a^x)^y=a^{xy}')[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'(ab)^x=a^xb^x')[0].set_z_index(2).next_to(eq3, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2, eq3, eq4)
        box = self.get_defbox(gp, props=True)
        return VGroup(gp, *box[:]).to_edge(UR, buff=0.1)

    def construct(self):
        prop1 = ExpNat.create_properties(self)
        def1 = ExpNat.create_def(self)
        props = self.create_properties()
        self.add(prop1, def1)
        self.wait(0.5)
        box1 = self.get_defbox(VGroup(props[0][:2]), props=True)
        self.play(LaggedStart(ReplacementTransform(prop1[1:] + prop1[0][0], box1[:] + props[0][0]),
                              FadeIn(props[0][1]), lag_ratio=0.5), run_time=2)

        self.wait(0.1)
        eq1 = MathTex(r's_0,s_1,s_2,\ldots')[0].set_z_index(2)
        eq2 = MathTex(r's_{n+1}=s_na')[0].set_z_index(2).move_to(eq1).align_to(eq1, LEFT)
        eq3 = MathTex(r's_n=s_0a^n')[0].set_z_index(2).next_to(eq2, DOWN, buff=0.1).align_to(eq1, LEFT)
        line1 = Line(eq1.get_left(), eq1.get_right(), color=RED, stroke_width=5).next_to(eq3, DOWN, coor_mask=UP)\
            .set_z_index(2)
        eq4 = MathTex(r's_y=a^{x+y}')[0].set_z_index(2).next_to(line1, DOWN, buff=0.1).align_to(eq1, LEFT)
        eq5 = MathTex(r's_{y+1}{{=}}a^{x+y+1}{{=}}a^{x+y}a{{=}}s_ya').set_z_index(2).next_to(eq4, DOWN, buff=0.05).align_to(eq1, LEFT)
        eq5[3:5].next_to(eq5[1], ORIGIN, submobject_to_align=eq5[3])
        eq5[5:7].next_to(eq5[1], ORIGIN, submobject_to_align=eq5[5])
        eq5[6][:2].move_to(eq5[4][:4], coor_mask=RIGHT)
        eq6 = MathTex(r's_y{{=}}s_0 a^y{{=}}a^xa^y').set_z_index(2)
        eq6.next_to(eq5[1], ORIGIN, submobject_to_align=eq6[1]).align_to(eq1, LEFT)
        eq6[3:5].next_to(eq6[1], ORIGIN, submobject_to_align=eq6[3])

        eq7 = MathTex(r's_y = a^{xy}')[0].set_z_index(2).next_to(line1, DOWN, buff=0.1).align_to(eq1, LEFT)
        eq8 = MathTex(r's_{y+1}{{=}}a^{xy+x}{{=}}a^{xy}a^x{{=}}s_ya^x').set_z_index(2).next_to(eq7, DOWN, buff=0.05).align_to(eq1, LEFT)
        eq8[3:5].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[3])
        eq8[5:7].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[5])
        eq8[6][:2].move_to(eq8[4][:3], coor_mask=RIGHT)
        eq9 = MathTex(r's_y=s_0(a^x)^y')[0].set_z_index(2).move_to(eq8).align_to(eq1, LEFT)

        eq10 = MathTex(r's_x = a^xb^x')[0].set_z_index(2).next_to(line1, DOWN, buff=0.1).align_to(eq1, LEFT)
        eq11 = MathTex(r's_{x+1}{{=}}a^{x+1}b^{x+1}{{=}}a^xab^xb{{=}}a^xb^xab{{=}}s_xab').set_z_index(2).next_to(eq10, DOWN, buff=0.05).align_to(eq1, LEFT)
        eq11[3:5].next_to(eq11[1], ORIGIN, submobject_to_align=eq11[3])
        eq11[5:7].next_to(eq11[1], ORIGIN, submobject_to_align=eq11[5])
        eq11[7:9].next_to(eq11[1], ORIGIN, submobject_to_align=eq11[7])
        eq11[8][:2].move_to(eq11[6][:4], coor_mask=RIGHT)
        eq11[4][3:].align_to(eq11[2][4:], LEFT)
        eq12 = MathTex(r's_x=s_0(ab)^x')[0].set_z_index(2).move_to(eq11).align_to(eq1, LEFT)

        gp = VGroup(line1, eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11, eq12).move_to(ORIGIN).to_edge(DOWN, buff=0.2)
        line1 = Line(gp.get_left(), gp.get_right(), color=RED, stroke_width=5).set_z_index(2).move_to(line1, coor_mask=UP)
        box3 = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0, corner_radius=0.2)

        self.play(FadeIn(box3, eq1), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq1), FadeIn(eq2), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq3), run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(FadeIn(line1), FadeIn(eq4), lag_ratio=0.5), run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform((eq4[:2] + eq4[2] + eq4[3:7]).copy(),
                                                   eq5[0][:2] + eq5[1][0] + eq5[2][:4]),
                              FadeIn(eq5[0][2:4], eq5[2][4:6]), lag_ratio=0.5),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq5[2][:4], eq5[4][:4]),
                  ReplacementTransform(eq5[2][0].copy(), eq5[4][-1]),
                  FadeOut(eq5[2][4:]), run_time=2)
        self.wait(0.1)
        self.play(FadeOut(eq5[4][:4]), FadeIn(eq5[6][:2]), run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq5[:2], eq5[4][-1], eq5[6][:2]),
                  FadeIn(eq6[:3]), run_time=2)
        self.wait(0.1)
        self.play(FadeOut(eq6[2][:2]), FadeIn(eq6[4][:2]),
                  ReplacementTransform(eq6[2][2:], eq6[4][2:]), run_time=2)
        self.wait(0.5)
        self.play(FadeOut(eq4, eq6[:2], eq6[4]), run_time=1)
        self.wait(0.1)

        box2 = self.get_defbox(props[0][:3], props=True)
        self.play(LaggedStart(ReplacementTransform(box1, box2),
                              FadeIn(props[0][2]), lag_ratio=0.5), run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq7), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform((eq7[:2] + eq7[2] + eq7[3:6]).copy(),
                                                   eq8[0][:2] + eq8[1][0] + eq8[2][:3]),
                              FadeIn(eq8[0][2:], eq8[2][3:]), lag_ratio=0.5),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq8[2][:3] + eq8[2][4] + eq8[2][0].copy(),
                                       eq8[4][:3] + eq8[4][4] + eq8[4][3]),
                  FadeOut(eq8[2][3]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq8[4][:3]), FadeIn(eq8[6][:2]), run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq8[:2], eq8[4][3:], eq8[6][:2]), FadeIn(eq9), run_time=2)
        self.wait(0.1)
        self.play(FadeOut(eq9[3:5]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq7, eq9[:3], eq9[5:]), run_time=1)
        self.wait(0.1)

        self.play(LaggedStart(ReplacementTransform(box2[:], props[1:]),
                              FadeIn(props[0][3]), lag_ratio=0.5), run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq10), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform((eq10[:2] + eq10[2] + eq10[3:5] + eq10[5:7]).copy(),
                                                   eq11[0][:2] + eq11[1][0] + eq11[2][:2] + eq11[2][4:6]),
                              FadeIn(eq11[0][2:], eq11[2][2:4], eq11[2][6:8]), lag_ratio=0.5),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq11[2][:2] + eq11[2][4:6] + eq11[2][0].copy() + eq11[2][4].copy(),
                                       eq11[4][:2] + eq11[4][3:5] + eq11[4][2] + eq11[4][-1]),
                  FadeOut(eq11[2][2:4], eq11[2][6:8]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq11[4][:2] + eq11[4][3:5] + eq11[4][2] + eq11[4][5],
                                       eq11[6][:2] + eq11[6][2:4] + eq11[6][4] + eq11[6][5]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq11[6][:4]), FadeIn(eq11[8][:2]), run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq11[:2], eq11[6][4:], eq11[8][:2]), FadeIn(eq12), run_time=2)
        self.wait(0.1)
        self.play(FadeOut(eq12[3:5]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(box3, eq2, eq3, line1, eq10, eq12[:3], eq12[5:]), run_time=1)
        self.wait(0.5)


class PropsNat(ExpNat):
    def create_properties(self):
        eq1 = MathTex(r'a^1=a')[0].set_z_index(2)
        eq2 = MathTex(r'a^{x+y}=a^xa^y')[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
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
        eq5 = MathTex(r'=a^xa^y')[0].set_z_index(2)
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

        eq8 = MathTex(r'=a^xa^y\;a')[0].set_z_index(2)
        eq8.next_to(eq6[8], ORIGIN, submobject_to_align=eq8[0])
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[-4:].copy() + eq7[5], eq8[1:5] + eq8[5]),
                  FadeOut(eq7[1:5]), run_time=1.5)

        eq9 = MathTex(r'=a^xa^{y+1}')[0].set_z_index(2)
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
        eq2 = MathTex(r'a^{x+y}=a^xa^y')[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'(a^x)^y=a^{xy}')[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'(ab)^x=a^xb^x')[0].set_z_index(2).next_to(eq3, DOWN).align_to(eq1, LEFT)
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
        eq8 = MathTex(r'(ab)^x{{=}}(ab)^0{{=}}1{{=}}1\;1{{=}}a^0b^0{{=}}a^xb^x').set_z_index(2)
        eq8[3:5].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[3])
        eq8[5:7].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[5])
        eq8[7:9].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[7])
        eq8[9:11].next_to(eq8[1], ORIGIN, submobject_to_align=eq8[9])
        eq8[4].move_to(eq8[2], coor_mask=RIGHT)
        eq8[6][0].move_to(eq8[8][:2], coor_mask=RIGHT)
        eq8[6][1].move_to(eq8[8][-2:], coor_mask=RIGHT)
        eq8.move_to(eq3)
        eq9 = MathTex(r'(ab)^{x+1}{{=}}(ab)^x\;ab{{=}}a^xb^x\;ab{{=}}a^xa\;b^xb{{=}}a^{x+1}b^{x+1}')\
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


class ExpInt(PropsNatNew):
    def create_def(self):
        eq1 = MathTex(r'x\in\mathbb Z, a\in\mathbb C\setminus\{0\}')[0].set_z_index(2)
        eq2 = MathTex(r'a^0=1')[0].next_to(eq1, DOWN).align_to(eq1, LEFT).set_z_index(2)
        eq3 = MathTex(r'a^{x+1}=a^xa')[0].next_to(eq2, DOWN).align_to(eq2, LEFT).set_z_index(2)
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
        eq2 = MathTex(r'1{{=}}a^0{{=}}a^{-1+1}{{=}}a^{-1}a').set_z_index(2)
        eq2.next_to(eq1[4], ORIGIN, submobject_to_align=eq2[5])
        eq2[2:4].next_to(eq2[5], ORIGIN, submobject_to_align=eq2[3])
        eq2[:2].next_to(eq2[5], ORIGIN, submobject_to_align=eq2[1])
        eq3 = MathTex(r'a^{-(x+1)+1}{{=}}a^{-(x+1)}a').set_z_index(2)
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
    def get_graph(self, a, shift=0.0):
        ax = Axes(x_range=[-5, 5.6], y_range=[0, a ** 5], z_index=2, x_length=6, y_length=3,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': True}).to_edge(DOWN, buff=0.2).set_z_index(2)
        if shift == 0.0:
            gp = ax
        else:
            l = Line(ax.get_bottom(), ax.get_bottom() + DOWN*shift)
            gp = VGroup(ax, l).to_edge(DOWN, buff=0.2)

        box = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=self.opacity, corner_radius=0.2,
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
        eq4 = MathTex(r'a^{x+y}=a^xa^y')[0].set_z_index(2).next_to(eq3, DOWN).align_to(eq1, LEFT)
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

        eq1 = MathTex(r'(a^x)^n{{=}}a^xa^x\cdots a^x{{=}}a^{x+x}\cdots a^x{{=}}a^{x+x+\cdots+x}{{=}}a^{xn}').set_z_index(2)
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
        eq3 = MathTex(r'a^{x+1}=a^xa^1')[0].set_z_index(2).to_edge(DOWN)
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

        eq6 = MathTex(r'a^0a{{=}}a^0a^1{{=}}a^{0+1}{{=}}a^1').set_z_index(2)
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
        eq2 = Tex(r'continuous')[0].next_to(defs[0][-1], DOWN).align_to(eq1, LEFT).set_z_index(2)
        gp = VGroup(eq1, *defs[0][1:], eq2)
        box = self.get_defbox(gp)
        return VGroup(gp, *box[:]).to_edge(UL, buff=0.1)

    def create_properties(self):
        props = PropsRat.create_properties(self)
        eq = Tex(r'convex')[0].next_to(props[0][-1], DOWN).align_to(props[0][0], LEFT).set_z_index(2)
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

        self.animate_dots(ax, a, xvals, dots)

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


class Logarithms(ConvexRat):
    def do_addition(self):
        eq1 = MathTex(r'3.141592')[0].set_z_index(2)
        eq2 = MathTex(r'+4.669201')[0].set_z_index(2).next_to(eq1, DOWN)
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq2[2], coor_mask=RIGHT)
        line0 = Line(eq2[1].get_left(), eq2.get_right(), color=WHITE, stroke_width=5).next_to(eq2, DOWN, coor_mask=UP)
        eq3 = MathTex(r'7.810793')[0].set_z_index(2).next_to(line0, DOWN).align_to(eq2[1], LEFT)
        eq4 = MathTex(r'11', font_size=30)[0].set_z_index(2).move_to(eq3).shift(DOWN*0.3)
        eq4[0].move_to(eq3[2:4], coor_mask=RIGHT)
        eq4[1].move_to(eq3[3:5], coor_mask=RIGHT)
        eq5 = VGroup(eq3[-1], eq3[-2], eq3[-3], eq3[-4], eq4[-1], eq3[-5], eq4[0], eq3[-6], eq3[-7], eq3[-8])
        gp = VGroup(eq1, eq2, line0, eq5).to_edge(DOWN)
        box = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0, corner_radius=0.2)

        self.play(FadeIn(box, eq1, eq2, line0), run_time=1)
        self.wait(0.1)

        for eq in eq5[:]:
            self.play(Write(eq, run_time=linear), run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(box, gp), run_time=1)
        self.wait(0.5)

    def do_graph(self):
        a = 1.5
        ax, box = self.get_graph(a, shift=0.22)
        graph = ax.plot(lambda x: a**x, (-5, 5, 0.05), color=BLUE, stroke_width=5).set_z_index(3)
        self.play(FadeIn(box, ax, graph), run_time=1)
        self.wait(0.5)

        x = 4.0
        y = a**x
        pt1 = ax.coords_to_point(x, 0)
        pt2 = ax.coords_to_point(x, y)
        pt3 = ax.coords_to_point(0, y)
        line1 = Line(pt1, pt2, color=GREY, stroke_width=5).set_z_index(1)
        line2 = Line(pt2, pt3, color=GREY, stroke_width=5).set_z_index(1)

        eqx = MathTex(r'x', font_size=40)[0].next_to(pt1, DOWN, buff=0.13)
        eqlog = MathTex(r'\log_a x', font_size=40)[0].next_to(pt1, DOWN, buff=0.05)
        eqax = MathTex(r'a^x', font_size=40)[0].next_to(pt3, LEFT, buff=0.13)
        self.play(FadeIn(eqx), run_time=0.5)
        self.wait(0.1)
        self.play(Create(line1), run_time=1)
        self.wait(0.1)
        self.play(Create(line2), run_time=1)
        self.play(FadeIn(eqax), run_time=0.5)
        self.wait(0.1)
        self.play(FadeOut(eqx, eqax, line1, line2), run_time=1)
        self.wait(0.1)
        eqx.next_to(pt3, LEFT, buff=0.13)
        self.play(FadeIn(eqx), run_time=0.5)
        self.wait(0.1)
        self.play(Create(line2.reverse_direction()), run_time=1)
        self.wait(0.1)
        self.play(Create(line1.reverse_direction()), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eqlog), run_time=0.5)
        self.wait(0.5)

        gp = VGroup(ax, graph)
        box.set_z_index(10)
        ax.set_z_index(20)
        graph.set_z_index(30)

        self.play(LaggedStart(FadeOut(eqlog, eqx, line1, line2, rate_func=lambda t: min(2*t, 1)),
                              AnimationGroup(gp.animate.rotate(axis=RIGHT+UP, angle=180*DEGREES,
                                             about_point=ax.coords_to_point(-2, 5)).shift(DOWN*0.6+LEFT*2),
                              box.animate.rotate(axis=RIGHT+UP, angle=180*DEGREES,
                                                 about_point=ax.coords_to_point(-2, 5))
                                             .shift(DOWN*0.6+LEFT*2).set_fill(opacity=0.8)),
                              lag_ratio=0.5),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(box, ax, graph), run_time=1)
        self.wait(0.5)

    def construct(self):
        defs = self.create_def()
        props = self.create_properties()
        self.add(defs, props)
        self.wait(0.5)

        self.do_addition()
        self.do_graph()

        eq1 = MathTex(r'a^{\log_a x}=x')[0].set_z_index(2)

        eq3 = MathTex(r'xy{{=}}a^{\log_ax}a^{\log_ay}{{=}}a^{\log_ax + \log_ay}')\
            .set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3])

        gp = VGroup(eq1, eq3).move_to(ORIGIN).to_edge(DOWN)
        box = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0, corner_radius=0.2)

        self.play(FadeIn(box, eq1), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq3[:2]), run_time=1)
        eq3_1 = eq3[0][0].copy()
        eq3_2 = eq3[0][1].copy()
        self.play(eq3_1.animate.move_to(eq3[2][:6], coor_mask=RIGHT),
                  eq3_2.animate.move_to(eq3[2][6:], coor_mask=RIGHT),
                  run_time=2)
        self.play(abra.fade_replace(eq3_1, eq3[2][5]),
                  abra.fade_replace(eq3_2, eq3[2][11]),
                  FadeIn(eq3[2][:5], eq3[2][6:11]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[2][:6] + eq3[2][7:12], eq3[4][:6] + eq3[4][7:12]),
                  ReplacementTransform(eq3[2][6], eq3[4][0]),
                  FadeIn(eq3[4][6]),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(box, eq1, eq3[:2], eq3[4]), run_time=1)

        self.wait(0.5)


class LogRuler(Logarithms):
    def get_pos(self, x, corners, top=True):
        res = RIGHT * (corners[0] * (1-x) + corners[1] * x)
        res += UP * (corners[1] if top else corners[0])
        return res

    def get_tick(self, x, corners, top=True, length=1.0, width=1.0):
        pos = self.get_pos(x, corners, top=top)
        dir = DOWN if top else UP
        return Line(pos, pos + dir * 0.15 * length, color=BLACK, stroke_width=4*width).set_z_index(1)

    def get_markings(self, corners, xvals, yvals):
        n = len(xvals)
        ticks = []
        labels = []
        ticks2 = []
        labels2 = []
        for i in range(n):
            x = xvals[i]/xvals[-1]
            tick = self.get_tick(x, corners)
            tick2 = self.get_tick(x, corners, top=False)
            ticks.append(tick)
            ticks2.append(tick2)
            label = Tex(r'{}'.format(int(xvals[i])), color=BLACK, font_size=35)[0].next_to(tick, DOWN, buff=0.025).set_z_index(2)
            label2 = Tex(r'{}'.format(int(yvals[i])), color=BLACK, font_size=35)[0].next_to(tick2, UP, buff=0.025).set_z_index(2)
            labels.append(label)
            labels2.append(label2)
        ticks = VGroup(*ticks)
        ticks2 = VGroup(*ticks2)
        labels = VGroup(*labels)
        labels2 = VGroup(*labels2)
        return VGroup(ticks, labels, ticks2, labels2)

    def get_log_markings(self, corners, yinterp):
        major_x = np.concatenate((np.linspace(1.0, 10.0, 10), np.linspace(20.0, 100.0, 9)))
        minor_x = np.concatenate((np.linspace(1.5, 9.5, 9), np.linspace(15.0, 95.0, 9)))
        minor2 = np.linspace(1.1, 1.4, 4)
        minor3 = np.linspace(11.0, 14.0, 4)
        minor_x2 = np.concatenate((minor2, minor2 + 0.5, minor2 + 1.0, minor2 + 1.5, minor2 + 2.0, minor2 + 2.5,
                                   np.array([4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75])))
        minor_x3 = np.concatenate((minor_x2, minor_x2 * 10))

        ticks = []
        labels = []
        for x in major_x:
            y = yinterp(x)
            tick = self.get_tick(y, corners, top=False)
            i = int(x)
            j = i if i < 10 else i // 10
            label = Tex(r'{}'.format(j), color=BLACK, font_size=35)[0].next_to(tick, UP, buff=0.025).set_z_index(2)
            if i == 100:
                label.next_to(tick, UP, buff=0.025, submobject_to_align=label[0])
            ticks.append(tick)
            labels.append(label)

        for x in minor_x:
            y = yinterp(x)
            tick = self.get_tick(y, corners, top=False, length=0.8, width=0.8)
            ticks.append(tick)

        for x in minor_x3:
            y = yinterp(x)
            tick = self.get_tick(y, corners, top=False, length=0.5, width=0.6)
            ticks.append(tick)

        return VGroup(VGroup(*ticks), VGroup(*labels))

    def get_linear_markings(self, corners, xvals, step=1, step2=1, scale=1.0):
        ticks = []
        labels = []
        for i in range(len(xvals)):
            if i % step == 0:
                tick = self.get_tick(xvals[i], corners)
                label = Tex(r'{:g}'.format(i*scale), color=BLACK, font_size=35)[0].next_to(tick, DOWN, buff=0.025).set_z_index(2)
                labels.append(label)
            elif i % step2 == 0:
                tick = self.get_tick(xvals[i], corners, length=0.8, width=0.8)
            else:
                continue

            ticks.append(tick)

        return VGroup(VGroup(*ticks), VGroup(*labels))

    def get_loglinear_markings(self, corners, yinterp, xvals, step=1, step2=1):
        markings1 = self.get_linear_markings(corners, xvals, step=step, step2=step2)
        markings2 = self.get_log_markings(corners, yinterp)
        return VGroup(*markings1[:], *markings2[:])

    def reflect_markings(self, markings):
        top = markings.get_top()
        bot = markings.get_bottom()
        ticks = []
        for tick in markings[0][:]:
            ticks.append(tick.copy().align_to(bot, DOWN))
        ticks2 = []
        for tick in markings[2][:]:
            ticks2.append(tick.copy().align_to(top, UP))
        labels = []
        for label in markings[1][:]:
            dy = (top - label.get_top())[1]
            labels.append(label.copy().align_to(bot, DOWN).shift(UP * dy))
        labels2 = []
        for label in markings[3][:]:
            dy = (label.get_bottom() - bot)[1]
            labels2.append(label.copy().align_to(top, UP).shift(DOWN * dy))

        return VGroup(VGroup(*ticks), VGroup(*labels), VGroup(*ticks2), VGroup(*labels2))

    def slide_add(self, corners, slide, yinterp, x1: float, x2: float, replace=True):
        ruler = slide[0]
        markings = slide[1]
        ruler2 = ruler.copy()
        markings2 = self.reflect_markings(markings)
        shift = ruler.height + 0.04
        slide_pos = slide.get_center()
        slide2 = VGroup(ruler2, markings2, *slide[2:].copy())
        self.play(slide.animate.shift(UP*shift), run_time=1)
        self.play(FadeIn(slide2), run_time=1)

        y1 = yinterp(x1)
        y2 = yinterp(x2)
        line0 = Line(self.get_pos(y1, corners, top=False), self.get_pos(y1, corners), color=RED_E, stroke_width=5)\
            .set_z_index(5).shift(UP*shift)
        line1 = Line(self.get_pos(y2, corners, top=False), self.get_pos(y2, corners), color=RED_E, stroke_width=5)\
            .set_z_index(5)
        self.wait(0.5)
        self.play(FadeIn(line0, line1), run_time=1)
        shift = self.get_pos(y1, corners) - self.get_pos(0, corners)
        self.wait(0.1)
        self.play(VGroup(slide2, line1).animate.shift(shift),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(line0, line1, slide2), run_time=2)
        if replace:
            self.play(slide.animate.move_to(slide_pos), run_time=1)

    def construct(self):
        defs = Logarithms.create_def(self)
        props = Logarithms.create_properties(self)
        self.add(defs, props)
        rcol = ManimColor(np.array([1., 1., .94]) * 0.7)
        ruler = RoundedRectangle(width=10, height=1.2, fill_color=rcol, stroke_opacity=0, fill_opacity=1,
                                 corner_radius=0.05).to_edge(DOWN, buff=0.2)
        corners = (ruler.get_corner(DL) + RIGHT*0.1, ruler.get_corner(UR) + LEFT * 0.3)
        self.wait(0.5)
        self.play(FadeIn(ruler), run_time=1)

        a = 2.0
        eq1 = MathTex(r'a={:g}'.format(a), font_size=35, color=BLACK)[0].move_to(ruler).set_z_index(3)
        self.play(FadeIn(eq1), run_time=1)
        self.wait(0.5)
        n = math.ceil(math.log(100.) / math.log(a))
        xvals = np.linspace(0.0, n, n+1)
        yvals = np.power(a, xvals)
        markings = self.get_markings(corners, xvals, yvals)

        self.play(FadeIn(markings[:2]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(markings[2:]), run_time=1)
        self.wait(0.5)
        slide = VGroup(ruler, markings, eq1)
        yinterp = scipy.interpolate.interp1d(yvals, xvals/xvals[-1])
        self.slide_add(corners, slide, yinterp, 4, 8)
        self.wait(0.5)

        markings_new = self.get_log_markings(corners, yinterp)
        self.play(FadeIn(markings_new), FadeOut(markings[2:]), run_time=2)
        slide = VGroup(ruler, VGroup(*markings[:2], *markings_new[:]), eq1)
        self.slide_add(corners, slide, yinterp, 6.5, 5.5)

        self.wait(0.1)
        self.play(FadeOut(slide[1:]), run_time=1)

        a = 1.1
        eq1 = MathTex(r'a={:g}'.format(a), font_size=35, color=BLACK)[0].move_to(ruler).set_z_index(2)
        self.play(FadeIn(eq1), run_time=1)
        self.wait(0.5)
        n = math.ceil(math.log(100.) / math.log(a))
        xvals = np.linspace(0.0, n, n+1)
        yvals = np.power(a, xvals)
        yinterp = scipy.interpolate.interp1d(yvals, xvals/xvals[-1])
        markings = self.get_loglinear_markings(corners, yinterp, xvals/xvals[-1], step=5, step2=1)
        self.wait(0.1)
        self.play(FadeIn(markings), run_time=1)
        self.wait(0.5)
        markings2 = self.get_linear_markings(corners, xvals/xvals[-1], step=5, step2=1, scale=0.1)
        self.play(FadeOut(markings[:2]), FadeIn(markings2), run_time=1)
        self.wait(0.5)
        markings = VGroup(*markings2[:], *markings[2:])
        self.slide_add(corners, VGroup(ruler, markings, eq1), yinterp, 6.5, 5.5)
        self.wait(0.1)
        self.play(FadeOut(markings, eq1), run_time=1)
        self.wait(0.5)

        a = 1.01
        eq1 = MathTex(r'a={:g}'.format(a), font_size=35, color=BLACK)[0].move_to(ruler).set_z_index(3)
        self.play(FadeIn(eq1), run_time=1)
        self.wait(0.5)
        n = math.ceil(math.log(100.) / math.log(a))
        xvals = np.linspace(0.0, n, n+1)
        yvals = np.power(a, xvals)
        yinterp = scipy.interpolate.interp1d(yvals, xvals/xvals[-1])
        markings = self.get_loglinear_markings(corners, yinterp, xvals/xvals[-1], step=50, step2=10)
        self.wait(0.1)
        self.play(FadeIn(markings), run_time=1)
        self.wait(0.5)
        markings2 = self.get_linear_markings(corners, xvals/xvals[-1], step=50, step2=10, scale=0.01)
        self.play(FadeOut(markings[:2]), FadeIn(markings2), run_time=1)
        self.wait(0.5)
        markings = VGroup(*markings2[:], *markings[2:])
        pos1 = ruler.get_center()
        self.slide_add(corners, VGroup(ruler, markings, eq1), yinterp, 6.5, 5.5, replace=False)
        self.wait(0.5)
        shift = ruler.get_center() - pos1
        x = 100/xvals[-1]
        line1 = Line(self.get_pos(x, corners, top=False), self.get_pos(x, corners), color=RED_E, stroke_width=5).shift(shift)
        self.play(FadeIn(line1), run_time=1)
        self.wait(0.1)
        eq2 = MathTex(r'e')[0].next_to(line1, DOWN, buff=0).shift(DOWN + LEFT*0.5)
        arr1 = Arrow(eq2.get_corner(UR) + UR*0.05, line1.get_bottom() + DOWN*0.05, color=RED, stroke_width=5, buff=0)
        self.play(FadeIn(eq2, arr1), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(ruler, markings, eq1, arr1, eq2, line1), run_time=1)

        self.wait(0.5)


class ExpDeriv(LogRuler):
    def create_properties(self):
        prop1 = LogRuler.create_properties(self)
        eq1 = MathTex(r'\frac{d a^x}{dx}=a^xg')[0].set_z_index(2).next_to(prop1[0], DOWN).set_z_index(2).align_to(prop1[0][0], LEFT)
        eq2 = MathTex(r'a^x=\lim_{n\to\infty}\left(1+\frac xng\right)^n', font_size=40)[0].set_z_index(2).next_to(eq1, DOWN).align_to(prop1[0][0], LEFT)
        gp = VGroup(*prop1[0][:], eq1, eq2)
        box = self.get_defbox(gp, props=True)
        return VGroup(gp, *box[:]).to_edge(UR, buff=0.1)

    def graph_eval(self, ax, a, x, xstr=r'x', ystr=r'a^x', size1=40):
        pt0 = ax.coords_to_point(x, 0)
        pt1 = ax.coords_to_point(x, a**x)
        pt2 = ax.coords_to_point(0, a**x)
        eqx = MathTex(xstr, font_size=size1)[0].next_to(pt0, DOWN, buff=0.13)
        eqax = MathTex(ystr, font_size=40)[0].next_to(pt2, LEFT, buff=0.13)
        line1 = Line(pt0, pt1, color=GREY, stroke_width=5).set_z_index(1)
        line2 = Line(pt1, pt2, color=GREY, stroke_width=5).set_z_index(1)
        return VGroup(eqx, line1, line2, eqax)

    def construct(self):
        def1 = self.create_def()
        prop1 = LogRuler.create_properties(self)
        props = self.create_properties()
        self.add(def1, prop1)
        self.wait(0.5)

        a = 1.5
        ax, _ = self.get_graph(a, shift=0.25)

        eq1 = MathTex(r'a^x{{=}}\left(a^{x/n}\right)^n{{\approx}}\left(1+\frac{x}{n}g\right)^n',
                      font_size=40).set_z_index(2)
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
        eq1.next_to(ax.coords_to_point(0, 6.7), LEFT, buff=0.2)

        x0 = 4.
        gev = self.graph_eval(ax, a, x0)
        gp = VGroup(gev, ax, eq1)

        box = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0,
                                   corner_radius=0.2)
        VGroup(gp, box).to_edge(DOWN, buff=0.1)

        graph = ax.plot(lambda x: a**x, (-5, 5, 0.05), color=BLUE, stroke_width=5).set_z_index(3)
        self.play(FadeIn(box, ax, graph), run_time=1)

        self.play(FadeIn(gev[0]), run_time=1)
        self.wait(0.1)
        self.play(Create(gev[1]), run_time=1)
        self.wait(0.1)
        self.play(Create(gev[2]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(gev[3]), run_time=1)
        self.wait(0.1)

        self.play(FadeIn(eq1[:3]), run_time=1)
        self.wait(0.1)

        gev1 = VGroup()
        for i in range(2, 7):
            xstr = r'x/{}'.format(i)
            ystr = r'a^{{x/{} }}'.format(i)
            gev0 = self.graph_eval(ax, a, x0/i, xstr=xstr, ystr=ystr, size1=34)
            self.play(FadeIn(gev0), FadeOut(gev1), run_time=0.101)
            gev1 = gev0
            self.wait(0.2)

        g = math.log(a)

        line1 = Line(ax.coords_to_point(-1/g, 0), ax.coords_to_point(5, 1+5*g), color=RED, stroke_width=4).set_z_index(4)
        self.play(FadeIn(line1), run_time=1)
        self.wait(0.1)
        eq2 = MathTex(r'g', color=RED, font_size=30).set_z_index(2).next_to(line1.get_end(), UP, buff=0.1).shift(LEFT*0.1)
        self.play(FadeIn(eq2), run_time=0.5)
        self.wait(0.5)

        self.play(ReplacementTransform(eq1[2][5:7] + eq1[2][4] + eq1[2][0] + eq1[1][0],
                                       eq1[4][7:9] + eq1[4][5] + eq1[4][0] + eq1[3][0]),
                  abra.fade_replace(eq1[2][1], eq1[4][1:3]),
                  abra.fade_replace(eq1[2][3], eq1[4][4]),
                  abra.fade_replace(eq1[2][2], eq1[4][3]),
                  FadeIn(eq1[4][6]),
                  run_time=1)
        self.wait(0.1)
        self.play(FadeOut(gev1), run_time=1)
        self.wait(0.1)

        hval = ValueTracker(4.0)

        def gfunc(neg=False):
            def f():
                h = hval.get_value()
                if neg:
                    h = -h
                y = a**h
                pt1 = ax.coords_to_point(h, 0)
                pt2 = ax.coords_to_point(h, y)
                str = r'-h' if neg else r'h'
                eq1 = MathTex(str, font_size=40)[0].set_z_index(2)
                eq1.next_to(pt1, DOWN, buff=0.05, submobject_to_align=eq1[-1])
                line1 = Line(pt1, pt2, color=GREY, stroke_width=5).set_z_index(1)
                g = (y-1) / h
                pt3 = ax.coords_to_point(-1/g, 0)
                pt4 = ax.coords_to_point(5, 1+g*5)
                line2 = Line(pt3, pt4, color=RED, stroke_width=4).set_z_index(4)
                str = r'g_{-h}' if neg else r'g_h'
                eq2 = MathTex(str, color=RED, font_size=30).set_z_index(5).next_to(pt4, UP, buff=0.1).shift(LEFT*0.1)
                if neg:
                    eq2.next_to(pt4, DOWN, buff=0.1)
                return VGroup(eq1, line1, VGroup(line2, eq2))
            return f

        vargrad = always_redraw(gfunc())
        self.play(FadeIn(vargrad[0]), run_time=0.5)
        self.play(Create(vargrad[1]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeIn(vargrad[2]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeOut(eq2), run_time=0.5)
        self.add(vargrad)
        self.play(hval.animate.set_value(0.1), run_time=4)
        self.wait(0.5)
#        eq1 = MathTex(r'a^x = \left(a^{x/n}\right)^n')

        eq3 = MathTex(r'g_h{{=}}\frac{a^h-1}{h}{{=}}a^h\frac{1-a^{-h}}{h}{{=}}a^hg_{-h}{{\sim}}g_{-h}', font_size=40).set_z_index(0)\
            .move_to(ax.coords_to_point(0, 3)).align_to(eq1, LEFT)
        eq3[3:5].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[3])
        eq3[5:7].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[5])
        eq3[7:9].next_to(eq3[1], ORIGIN, submobject_to_align=eq3[7])
        self.play(FadeIn(eq3[:3]), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(eq3[2][:2] + eq3[2][2] + eq3[2][4:],
                                       eq3[4][:2] + eq3[4][3] + eq3[4][7:]),
                  FadeIn(eq3[4][2], target_mobject=eq3[2][0]),
                  abra.fade_replace(eq3[2][3], eq3[4][4:7]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[4][:2], eq3[6][:2]),
                  FadeOut(eq3[4][2:]),
                  FadeIn(eq3[6][2:], target_position=eq3[4][2:].get_center()*RIGHT+eq3[6][2:].get_center()*UP),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeOut(vargrad, line1), run_time=1)
        self.remove(vargrad)
        self.wait(0.1)

        hval.set_value(4)
        vargrad1 = always_redraw(gfunc())
        vargrad2 = always_redraw(gfunc(neg=True))
        self.play(FadeIn(vargrad1, vargrad2), run_time=2)
        self.wait(0.1)
        self.play(hval.animate.set_value(0.1), run_time=4)
        self.wait(0.1)
        self.play(LaggedStart(AnimationGroup(FadeOut(eq3[6][:2]), abra.fade_replace(eq3[1], eq3[7])),
                              ReplacementTransform(eq3[6][2:], eq3[8][:]), lag_ratio=0.6),
                  run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq3[0], eq3[7:], vargrad1, vargrad2, gev), run_time=1)
        self.remove(vargrad1, vargrad2)

        varpos = ValueTracker(0.0)

        def f_grad():
            x = varpos.get_value()
            y = a**x
            g = y * math.log(a)
            xr = 5.0
            yr = g * (xr - x) + y
            xl = x - y/g
            yl = 0
            if xl < -5.0:
                xl = -5.0
                yl = g * (xl - x) + y
            line1 = Line(ax.coords_to_point(xl, yl), ax.coords_to_point(xr, yr), color=RED, stroke_width=4).set_z_index(4)
            line2 = Line(ax.coords_to_point(x, 0), ax.coords_to_point(x, y), color=GREY, stroke_width=5).set_z_index(1)
            dot1 = Dot(ax.coords_to_point(x, 0), color=YELLOW).set_z_index(5)
            dot2 = Dot(ax.coords_to_point(x, y), color=YELLOW).set_z_index(5)

            return VGroup(line1, line2, dot1, dot2)

        grad_line = always_redraw(f_grad)
        self.play(FadeIn(grad_line), run_time=0.5)
        self.play(varpos.animate.set_value(5.0), run_time=1)
        self.play(varpos.animate.set_value(-5.0), run_time=2)
        self.play(varpos.animate.set_value(0.0), run_time=1)
        self.play(FadeOut(grad_line), run_time=1)
        self.remove(grad_line)
        self.wait(0.5)
        eq5 = MathTex(r'a^x\frac{a^{h}-1}{h}', font_size=40)[0].set_z_index(0)\
            .move_to(ax.coords_to_point(0, 3)).align_to(eq1, LEFT).shift(RIGHT*0.2)
        eq4 = MathTex(r'\frac{a^{x+h}-a^x}{h}', font_size=40)[0].set_z_index(0)
        eq4.next_to(eq5[-2], ORIGIN, submobject_to_align=eq4[-2])
        self.play(FadeIn(eq4), run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4[:2] + eq4[0].copy() + eq4[3:5] + eq4[-2:],
                                       eq5[:2] + eq5[2] + eq5[3:5] + eq5[-2:]),
                  ReplacementTransform(eq4[5:7], eq5[:2]),
                  FadeIn(eq5[5]), FadeOut(eq4[2]), run_time=2)

        eq6 = MathTex(r'a^xg')[0]
        eq6.next_to(eq5[:2], ORIGIN, submobject_to_align=eq6[:2])
        self.wait(0.1)
        self.play(ReplacementTransform(eq5[:2], eq6[:2]),
                  FadeOut(eq5[2:]), FadeIn(eq6[2:]), run_time=1)
        self.wait(0.5)
        prop2 = props[0][:-1].copy()
        box4 = self.get_defbox(prop2, props=True)
        VGroup(prop2, box4).to_edge(UR, buff=0.1)
        self.play(LaggedStart(ReplacementTransform(prop1[0][:] + prop1[1:],
                                       prop2[:-1] + box4[:]),
                              AnimationGroup(FadeIn(prop2[-1][:7]),
                                             ReplacementTransform(eq6[:], prop2[-1][7:])),
                              lag_ratio=0.5),
                  run_time=3)
        self.wait(0.5)
        circ1 = abra.circle_eq(eq1).set_z_index(4)
        self.play(Create(circ1), run_time=0.5)
        self.wait(0.5)
        line1 = Line(ax.coords_to_point(-1/g, 0), ax.coords_to_point(5, 1+5*g), color=RED, stroke_width=4).set_z_index(4)
        eq7 = MathTex(r'a^x\ge1+xg')[0].set_z_index(2)\
            .move_to(ax.coords_to_point(0, 3))
        eq8 = MathTex(r'a^{-x}\ge1-xg')[0].set_z_index(2)\
            .next_to(eq7, DOWN, coor_mask=UP).align_to(eq1, LEFT)
        eq7.next_to(eq8[3], ORIGIN, submobject_to_align=eq7[2], coor_mask=RIGHT)
        self.play(FadeIn(eq7, line1), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform((eq7[1:4] + eq7[0] + eq7[-2:]).copy(),
                                       eq8[2:5] + eq8[0] + eq8[-2:]),
                  abra.fade_replace(eq7[-3].copy(), eq8[-3]),
                  FadeIn(eq8[1], target_mobject=eq7[1]), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(ax, graph, line1), run_time=1)
        eq9 = MathTex(r'a^{x}\le(1-xg)^{-1}')[0].set_z_index(2)
        eq9.next_to(eq8[3], ORIGIN, submobject_to_align=eq9[2])
        self.play(ReplacementTransform(eq8[:1] + eq8[2] + eq8[4:8],
                                       eq9[:1] + eq9[1] + eq9[4:8]),
                  FadeIn(eq9[3], eq9[-3:]),
                  FadeOut(eq8[1]),
                  abra.fade_replace(eq8[3], eq9[2]),
                  run_time=1)
        eq10 = MathTex(r'a^{\frac{x}{1+xg}}\le\left(1-\frac{xg}{1+xg}\right)^{-1}')[0].set_z_index(2)
        eq10.align_to(box, DOWN).align_to(eq1, LEFT)
        self.wait(0.1)
        self.play(ReplacementTransform(eq9[:1] + eq9[2:8] + eq9[-3:],
                                       eq10[:1] + eq10[7:13] + eq10[-3:]),
                  FadeIn(eq10[2:7], eq10[-8:-3]),
                  abra.fade_replace(eq9[1], eq10[1]),
                  run_time=1)
        self.wait(0.1)
        eq11 = MathTex(r'\le\frac{1+xg}{1+xg-xg}')[0].set_z_index(2)
        eq11.next_to(eq10[7], ORIGIN, submobject_to_align=eq11[0])
        self.play(ReplacementTransform(eq10[-7:-3] + eq10[10:13] + eq10[-7:-3].copy(),
                                       eq11[1:5] + eq11[10:13] + eq11[6:10]),
                  ReplacementTransform(eq10[9], eq11[1]),
                  FadeIn(eq11[5]),
                  FadeOut(eq10[13], eq10[8], eq10[-3:]),
                  run_time=1.5)
        line1 = Line(eq11[8].get_corner(DL) + DL*0.1, eq11[9].get_corner(UR) + UR*0.1, stroke_width=4, color=RED)\
            .set_z_index(3)
        line2 = Line(eq11[11].get_corner(DL) + DL*0.1, eq11[12].get_corner(UR) + UR*0.1, stroke_width=4, color=RED)\
            .set_z_index(3)
        self.wait(0.1)
        self.play(FadeIn(line1, line2), run_time=0.5)
        self.wait(0.1)
        self.play(FadeOut(line1, line2, eq11[7:13]), run_time=1)
        self.wait(0.1)
        eq12 = MathTex(r'\le 1+xg')[0].set_z_index(2)
        eq12.next_to(eq10[7], ORIGIN, submobject_to_align=eq12[0])
        self.play(FadeOut(eq11[5:7]), ReplacementTransform(eq11[1:5], eq12[1:]), run_time=1)
        self.wait(0.5)
        eq13 = MathTex(r'a^{\frac{x}{1+xg}} {{\le}} 1+xg {{\le}} a^x').set_z_index(2).move_to(box).shift(DOWN*0.2 + LEFT * 0.3)
        self.play(ReplacementTransform(eq10[:7] + eq10[7] + eq12[1:], eq13[0][:] + eq13[1][:] + eq13[2][:]),
                  ReplacementTransform(eq7[:2] + eq7[3:], eq13[4][:] + eq13[2][:]),
                  abra.fade_replace(eq7[2], eq13[3][0]),
                  run_time=2)
        self.wait(0.1)
        eq14 = MathTex(r'a^{\frac{x/n}{1+\frac xn g}} {{\le}} 1+\frac xng {{\le}} a^{x/n}').set_z_index(2)
        eq14.next_to(eq13[1], ORIGIN, submobject_to_align=eq14[1])
        self.play(ReplacementTransform(eq13[0][:2] + eq13[0][-5:-1] + eq13[0][-1] + eq13[1] + eq13[2][:3] + eq13[2][-1] + eq13[3] + eq13[4][:2],
                                       eq14[0][:2] + eq14[0][-7:-3] + eq14[0][-1] + eq14[1] + eq14[2][:3] + eq14[2][-1] + eq14[3] + eq14[4][:2]),
                  FadeIn(eq14[0][2:4], eq14[2][-3:-1], eq14[4][-2:], eq14[0][-3:-1]), run_time=1)
        eq15 = MathTex(r'\left(a^{\frac{x/n}{1+\frac xng}}\right)^n {{\le}}\left(1+\frac xng\right)^n {{\le}}\left(a^{x/n}\right)^n').set_z_index(2)
        eq15.next_to(eq14[2][:], ORIGIN, submobject_to_align=eq15[2][1:-2])
        box2 = SurroundingRectangle(VGroup(gp, eq15), fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0,
                                    corner_radius=0.2)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(box, box2),
                              AnimationGroup(ReplacementTransform(eq14[0][:] + eq14[4][:] + eq14[2][:] + eq14[1] + eq14[3],
                                                                  eq15[0][1:-2] + eq15[4][1:-2] + eq15[2][1:-2] + eq15[1] + eq15[3]),
                                             FadeIn(eq15[0][0], eq15[0][-2:], eq15[2][0], eq15[2][-2:], eq15[4][0], eq15[4][-2:])),
                  lag_ratio=0.5), run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq15[0][0], eq15[0][-2], eq15[4][0], eq15[4][-2], eq15[0][3:5], eq15[4][3:5]),
                  FadeOut(eq15[0][-1], target_position=eq15[0][3]),
                  FadeOut(eq15[4][-1], target_position=eq15[4][3]),
                  run_time=1)
        eq16 = MathTex(r'a^{\frac{x}{1+\frac xng}} {{\le}}\left(1+\frac xng\right)^n {{\le}}a^{x}').set_z_index(2)
        eq16.next_to(eq15[2], ORIGIN, submobject_to_align=eq16[2])
        self.play(ReplacementTransform(eq15[0][1:3] + eq15[0][5:-2] + eq15[4][1:3],
                                       eq16[0][:2] + eq16[0][2:] + eq16[4][:]), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(ReplacementTransform(box4[:] + prop2[:], props[1:] + props[0][:-1]),
                              ReplacementTransform(eq15[2][:].copy() + eq16[4][:].copy(),
                                                   props[0][-1][-9:] + props[0][-1][:2]),
                              FadeIn(props[0][-1][2:-9]), lag_ratio=0.33),
                  FadeOut(box2, circ1, eq1[0], eq1[-2:], eq15[1:4], eq16[0], eq16[4]),
                  run_time=2.5)

        self.wait(0.5)


class EulerE(ExpDeriv):
    def create_properties(self):
        return  LogRuler.create_properties(self)

    def create_eprops(self):
        eq1 = MathTex(r'\frac{de^x}{dx}=e^x')[0].set_z_index(2)
        eq2 = MathTex(r'e^x=\lim_{n\to\infty}\left(1+\frac xn\right)^n', font_size=40)[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2)
        box = self.get_defbox(gp, props=True, e=True)
        return VGroup(gp, *box[:]).next_to(self.create_properties(), DOWN, buff=0.1).to_edge(RIGHT, buff=0.1)

    def create_edef(self):
        eq1 = MathTex(r'x\in\mathbb R, e^x\in\mathbb R')[0].set_z_index(2)
        eq2 = MathTex(r'e^{x+y}=e^xe^y')[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'e^x=1+x+o(x)', font_size=40)[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2, eq3)
        box = self.get_defbox(gp, e=True)
        return VGroup(gp, *box[:]).next_to(ExpDeriv.create_def(self), DOWN, buff=0.1).to_edge(LEFT, buff=0.1)

    def construct(self):
        def1 = ExpDeriv.create_def(self)
        prop1 = ExpDeriv.create_properties(self)
        self.add(prop1, def1)
        self.wait(0.5)

        eq1 = MathTex('a^x {{=}} 1 + xg + o(x) {{=}} 1 + x \ln a+o(x)').set_z_index(2)
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3])
        eq1.move_to(ORIGIN)
        eq2 = MathTex('(a^y)^x {{=}} a^{xy} {{=}} 1 + xy\ln a + o(xy)').set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq2[3:5].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[3])
        eq3 = MathTex(r'\ln(a^y)=y\ln a')[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'e=a^{\frac1{\ln a}}')[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq5 = MathTex(r'\ln e {{=}} \frac{\ln a}{\ln a} {{=}} 1').set_z_index(2)
        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1][0]).align_to(eq1, LEFT)
        eq5[4].move_to(eq5[2], coor_mask=RIGHT)

        gp = VGroup(eq1,eq2,eq3,eq4,eq5)
        gp.to_edge(DOWN, buff=0.2).next_to(prop1, LEFT, buff=0.2, coor_mask=RIGHT)
        box = SurroundingRectangle(gp, corner_radius=0.2, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0)
        self.play(FadeIn(eq1[:3], box), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(eq1[2][:3] + eq1[2][-5:],
                                       eq1[4][:3] + eq1[4][-5:]),
                  FadeOut(eq1[2][3]), FadeIn(eq1[4][3:-5]),
                  run_time=1)
        self.wait(0.5)
        self.play(FadeIn(eq2[:3]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq2[2][0]), FadeIn(eq2[4][:2], eq2[4][-9:-3], eq2[4][-1]),
                  ReplacementTransform(eq2[2][-1:]+eq2[2][-1:].copy(), eq2[4][3:4]+eq2[4][-2:-1]),
                  abra.fade_replace(eq2[2][-2], eq2[4][2]),
                  abra.fade_replace(eq2[2][-2].copy(), eq2[4][-3]),
                  run_time=1)

        self.wait(0.5)
        self.play(ReplacementTransform(eq2[0][:4].copy() + eq2[4][3:7].copy(), eq3[2:6] + eq3[-4:]),
                  FadeIn(eq3[:2], eq3[6]), run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(FadeOut(eq2[:2], eq2[4]), eq3.animate.next_to(eq1, DOWN, coor_mask=UP), FadeIn(eq4), lag_ratio=0.333), run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4[:1] + eq4[1] + eq4[2] + eq4[4],
                                       eq5[0][-1:] + eq5[1][0] + eq5[2][2] + eq5[2][-4]),
                  FadeOut(eq4[3], target_position=eq5[2][:3]),
                  FadeIn(eq5[2][:2], eq5[0][:2]),
                  abra.fade_replace(eq4[5:8], eq5[2][-3:]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq5[2]), FadeIn(eq5[4]), run_time=1)
        self.wait(0.5)
        eq6=MathTex(r'e=e')[0].set_z_index(2)
        eq6.next_to(eq3[6], ORIGIN, submobject_to_align=eq6[1])
        eq6[0].move_to(eq3[3], coor_mask=RIGHT)
        eq6[2].move_to(eq3[-1], coor_mask=RIGHT)
        self.play(FadeOut(eq3[3], eq3[-1]), FadeIn(eq6[0], eq6[2]), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq3[-3:-1], eq6[2]), run_time=1)
        eq7 = MathTex(r'e^{\ln y}=y')[0].set_z_index(2)
        eq7.next_to(eq3[6], ORIGIN, submobject_to_align=eq7[-2]).align_to(eq1, LEFT)
        self.wait(0.5)
        self.play(ReplacementTransform(eq6[:1] + eq3[4] + eq3[-5:-3],
                                       eq7[:1] + eq7[3] + eq7[-2:]),
                  abra.fade_replace(eq3[:2], eq7[1:3]),
                  FadeOut(eq3[2], eq3[5]),
                  run_time=1)
        eq8=MathTex(r'e=e')[0].set_z_index(2)
        eq8.next_to(eq1[1][0], ORIGIN, submobject_to_align=eq8[1])
        eq8[0].move_to(eq1[0][0], coor_mask=RIGHT)
        eq8[2].move_to(eq1[4][5], coor_mask=RIGHT)
        self.wait(0.1)
        self.play(FadeOut(eq1[0][0], eq1[4][5]), FadeIn(eq8[0], eq8[2]), run_time=1)
        self.wait(0.1)
        eq1_1 = MathTex(r'x+y')[0]
        eq1_1.next_to(eq1[4][2], ORIGIN, submobject_to_align=eq1_1[0])
        self.play(FadeOut(eq1[4][3:5], eq8[2]), eq1[4][6:].animate.align_to(eq1_1[1], LEFT), run_time=1)
        self.wait(0.5)
        eprop = self.create_eprops()
        props = self.create_properties()
        self.play(ReplacementTransform(prop1[0][:-2] + prop1[1:] + prop1[0][-2][0] + prop1[0][-2][2:7] + prop1[0][-2][-2]
                                       + prop1[0][-1][1:-3] + prop1[0][-1][-2:],
                                       props[0][:] + props[1:] + eprop[0][-2][0] + eprop[0][-2][2:7] + eprop[0][-2][-1]
                                       + eprop[0][-1][1:-2] + eprop[0][-1][-2:]),
                  abra.fade_replace(prop1[0][-2][1], eprop[0][-2][1]),
                  abra.fade_replace(prop1[0][-2][7], eprop[0][-2][7]),
                  FadeOut(prop1[0][-2][-1], target_position=prop1[0][-2][-1].get_center()-prop1[0][-2][-3].get_center()
                          + eprop[0][-2][-2].get_center()),
                  abra.fade_replace(prop1[0][-1][0], eprop[0][-1][0]),
                  FadeOut(prop1[0][-1][-3], target_position=eprop[0][-1][-2]),
                  FadeIn(eprop[1:]),
                  run_time=2)
        self.wait(0.5)
        edef = self.create_edef()
        self.play(FadeIn(edef[0][0], edef[1:]),
                  ReplacementTransform((def1[0][-2][1:5] + def1[0][-2][6] + def1[0][-2][8]).copy(),
                                       edef[0][1][1:5] + edef[0][1][6] + edef[0][1][8]),
                  abra.fade_replace(def1[0][-2][0].copy(), edef[0][1][0]),
                  abra.fade_replace(def1[0][-2][5].copy(), edef[0][1][5]),
                  abra.fade_replace(def1[0][-2][7].copy(), edef[0][1][7]),
                  ReplacementTransform(eq1[0][1:] + eq1[1] + eq1[4][:3] + eq1[4][-5:] + eq8[0],
                                       edef[0][2][1:2] + edef[0][2][2] + edef[0][2][3:6] + edef[0][2][-5:] + edef[0][2][0]),
                  FadeOut(eq5[:2], eq5[-1], eq7, box),
                  run_time=2)

        self.wait(0.5)


class ExpSeries(EulerE):
    def create_eprops(self):
        prop1 = EulerE.create_eprops(self)
        eq = MathTex(r'e^x=\sum_{n=0}^\infty \frac{x^n}{n!}', font_size=40)[0].set_z_index(2).next_to(prop1[0][-1], DOWN).align_to(prop1[0][0], LEFT)
        gp = VGroup(*prop1[0][:], eq)
        box = self.get_defbox(gp, props=True, e=True)
        return VGroup(gp, *box[:]).next_to(self.create_properties(), DOWN, buff=0.1).to_edge(RIGHT, buff=0.1)

    def construct(self):
        prop1 = self.create_properties()
        eprop1 = EulerE.create_eprops(self)
        def1 = self.create_def()
        edef = self.create_edef()
        self.add(prop1, eprop1, def1, edef)
        self.wait(0.5)

        eq1 = MathTex(r'(1+x)^n {{=}} 1 + nx + \frac{n(n-1)}{2}x^2+\cdots+x^n '
                      r'{{=}} 1 + \binom{n}{1}x+\binom{n}{2}x^2+\cdots+x^n').set_z_index(2)
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3])
        eq1.move_to(ORIGIN).to_edge(DOWN, buff=0.2)
        eq2 = MathTex(r'(1+x)^n{{=}}\sum_{k=0}^n\binom{n}{k}x^k{{=}}\sum_{k=0}^n\frac{n(n-1)\cdots(n-(k-1))}{k!}x^k').set_z_index(2)
        eq2[3:5].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[3])
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq2[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq3 = MathTex(r'\left(1+\frac xn\right)^n{{=}}\sum_{k=0}^n\left(1-\frac1n\right)\cdots\left(1-\frac{k-1}{n}\right)\frac{x^k}{n^k}')
        eq3.next_to(eq2[1], ORIGIN, submobject_to_align=eq3[1])
        eq5 = MathTex(r'\left(1+\frac xn\right)^n{{=}}\sum_{k=0}^\infty\frac{x^k}{k!}').set_z_index(2)
        eq5.next_to(eq3[1], ORIGIN, submobject_to_align=eq5[1]).move_to(ORIGIN, coor_mask=RIGHT)
        gp = VGroup(eq1, eq2, eq3, eq5)
        box = SurroundingRectangle(gp, corner_radius=0.2, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0)

        self.play(FadeIn(box, eq1[:3]), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(eq1[2][3:5],
                                       eq1[4][6:8]),
                  FadeOut(eq1[2][2], eq1[2][5:13]),
                  FadeIn(eq1[4][2:6], eq1[4][8:12]),
                  run_time=1)
        self.wait(0.5)
        eq2_1 = eq2[2][7].copy()
        eq2_2 = eq2[2][-1].copy()
        self.play(LaggedStart(AnimationGroup(
                  ReplacementTransform(eq1[4][2:4] + eq1[4][5],
                                       eq2[2][5:7] + eq2[2][8]),
                  ReplacementTransform(eq1[4][8:10] + eq1[4][11],
                                       eq2[2][5:7] + eq2[2][8]),
                  ReplacementTransform(eq1[:2], eq2[:2]),
                  ReplacementTransform(eq1[4][6], eq2[2][-2]),
                  ReplacementTransform(eq1[2][-2], eq2[2][-2]),
                  ReplacementTransform(eq1[2][-9], eq2[2][-2]),
                  abra.fade_replace(eq1[2][-1], eq2[2][-1]),
                  abra.fade_replace(eq1[2][-8], eq2_2),
                  abra.fade_replace(eq1[4][4], eq2[2][7]),
                  abra.fade_replace(eq1[4][10], eq2_1),
                  FadeOut(eq1[2][1], eq1[4][7], eq1[2][-7:-2]),
                  FadeOut(eq1[2][0], target_position=eq2[2][-2])),
                  FadeIn(eq2[2][:5]),
                  lag_ratio=0.5),
                  run_time=2)
        self.remove(eq2_1, eq2_2)
        self.wait(0.5)
        self.play(ReplacementTransform(eq2[2][-2:], eq2[4][-2:]),
                  FadeOut(eq2[2][5:-2], target_position=eq2[4][5:-2]),
                  FadeIn(eq2[4][5:-2]),
                  run_time=2)
        self.wait(0.5)
        eq3_2 = eq3[2][-5:].copy()
        eq3[2][-5:].move_to(eq2[4][-2:], coor_mask=RIGHT)
        self.play(ReplacementTransform(eq2[0][:4] + eq2[0][-2:],
                                       eq3[0][:4] + eq3[0][-2:]),
                  ReplacementTransform(eq2[4][-2:], eq3[2][-5:-3]),
                  FadeIn(eq3[0][4:-2]),
                  FadeIn(eq3[2][-3:]),
                  run_time=1)
        self.wait(0.1)
        self.play(eq3[2][-2:].animate.move_to(eq2[4][-4:-2], coor_mask=RIGHT),
                  eq2[4][-4:-2].animate.move_to(eq3[2][-2:], coor_mask=RIGHT),
                  run_time=2)
        self.wait(0.5)
        eq4 = MathTex(r'\frac nn \frac{(n-1)}{n} \cdots \frac{(n-(k-1))}{n}')[0].set_z_index(2)
        eq4[:3].next_to(eq2[4][5], ORIGIN, submobject_to_align=eq4[0])
        eq4[3:10].next_to(eq2[4][7], ORIGIN, submobject_to_align=eq4[4])
        eq4[10:13].move_to(eq2[4][11:14], coor_mask=RIGHT).move_to(eq2[4][-5], coor_mask=UP)
        eq4[13:24].next_to(eq2[4][15], ORIGIN, submobject_to_align=eq4[14])
        self.play(ReplacementTransform(eq2[4][5], eq4[0]),
                  ReplacementTransform(eq2[4][6:11], eq4[3:8]),
                  ReplacementTransform(eq2[4][11:14], eq4[10:13]),
                  ReplacementTransform(eq2[4][14:23], eq4[13:22]),
                  FadeOut(eq2[4][-5], eq3[2][-1]),
                  FadeIn(eq4[1], eq4[8], eq4[22]),
                  ReplacementTransform(eq3[2][-2], eq4[2]),
                  ReplacementTransform(eq3[2][-2].copy(), eq4[9]),
                  ReplacementTransform(eq3[2][-2].copy(), eq4[23]),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(eq4[:3]),
                  ReplacementTransform(eq4[5:7] + eq4[3] + eq4[8] + eq4[9] + eq4[7],
                                       eq3[2][7:9] + eq3[2][5] + eq3[2][9] + eq3[2][10] + eq3[2][11]),
                  abra.fade_replace(eq4[4], eq3[2][6]),
                  ReplacementTransform(eq4[10:13], eq3[2][12:15]),
                  ReplacementTransform(eq4[13:14] + eq4[15] + eq4[17:20] + eq4[22] + eq4[23] + eq4[21],
                                       eq3[2][15:16] + eq3[2][17] + eq3[2][18:21] + eq3[2][21] + eq3[2][22] + eq3[2][23]),
                  abra.fade_replace(eq4[14], eq3[2][16]),
                  FadeOut(eq4[16], eq4[20]),
                  ReplacementTransform(eq3[2][-5:-2], eq3_2[-5:-2]),
                  eq2[4][-4:-2].animate.move_to(eq3_2[-2:], coor_mask=RIGHT),
                  run_time=2)

        self.wait(0.1)
        self.play((eq3_2[-5:-2]+eq2[4][-4:-2]).animate.set_color(BLUE), run_time=1)
        self.wait(0.5)
        self.play((eq3_2[-5:-2]+eq2[4][-4:-2]).animate.set_color(WHITE),
                  eq3[2][5:-5].animate.set_color(BLUE), run_time=1)
        self.wait(0.5)
        self.play(eq3[2][5:-5].animate.set_color(WHITE), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq3[2][5:-5]), run_time=1)
        self.play(ReplacementTransform(eq3[0], eq5[0]),
                  ReplacementTransform(eq2[1], eq5[1]),
                  ReplacementTransform(eq2[2][1:5], eq5[2][1:5]),
                  abra.fade_replace(eq2[2][0], eq5[2][0]),
                  ReplacementTransform(eq3_2[-5:-2]+eq2[4][-4:-2], eq5[2][-5:-2] + eq5[2][-2:]),
                  run_time=1)

        self.wait(0.5)
        eprop = self.create_eprops()
        self.play(
            ReplacementTransform(eprop1[1:], eprop[1:]),
            FadeIn(eprop[0][-1][:2]),
            FadeOut(eq5[0], box),
            ReplacementTransform(eq5[1][0], eprop[0][-1][2]),
            ReplacementTransform(eq5[2][:2] + eq5[2][3:6] + eq5[2][7:8] + eq5[2][9:],
                                 eprop[0][-1][3:5] + eprop[0][-1][6:9] + eprop[0][-1][10:11] + eprop[0][-1][12:]),
            abra.fade_replace(eq5[2][2], eprop[0][-1][5]),
            abra.fade_replace(eq5[2][6], eprop[0][-1][9]),
            abra.fade_replace(eq5[2][8], eprop[0][-1][11]),
            run_time=2
        )

        self.wait(0.5)


class ComplexExp(ExpSeries):
    def create_edef(self):
        def1 = ExpSeries.create_edef(self)
        eq = MathTex(r'x\in\mathbb C, e^x\in\mathbb C')[0].set_z_index(2).move_to(def1[0][0]).align_to(def1[0][0], LEFT)
        return VGroup(VGroup(eq, *def1[0][1:]), *def1[1:]).next_to(ComplexExp.create_def(self), DOWN, buff=0.1).to_edge(LEFT, buff=0.1)

    def create_def(self):
        def1 = ExpSeries.create_def(self)
        eq1 = MathTex(r'x\in\mathbb C, a > 0,')[0].set_z_index(2).align_to(def1[0][0], DL)
        eq2 = MathTex(r'a^x\in\mathbb C')[0].set_z_index(2).align_to(def1[0][1], DL)
        eq3 = MathTex(r'\frac{da^x}{dx}\Big\vert_{x=0}\in\mathbb{R}')[0].set_z_index(2).next_to(def1[0][-2], DOWN).align_to(def1[0][0], LEFT)
        gp = VGroup(eq1, eq2, *def1[0][2:-1], eq3)
        box = self.get_defbox(gp)
        return VGroup(gp, *box[:]).to_edge(UL, buff=0.1)

    def construct(self):
        def1 = ExpSeries.create_def(self)
        edef1 = ExpSeries.create_edef(self)
        prop1 = ExpSeries.create_properties(self)
        eprop1 = ExpSeries.create_eprops(self)
        self.add(def1, edef1, prop1, eprop1)
        self.wait(0.5)
        width = (eprop1.get_left() - edef1.get_right())[0] * 0.6
        center = (eprop1.get_left() + edef1.get_right()) * 0.5
        ax = Axes(x_range=[-3, 3], y_range=[-3, 3], z_index=2, x_length=width, y_length=width, tips=False,
                  axis_config={'color': WHITE, 'stroke_width': 3, 'include_ticks': True, 'tick_size': 0.05},
                  x_axis_config={'include_ticks': True})
        ax.move_to(center).to_edge(DOWN, buff=0.2)
        box = SurroundingRectangle(ax, corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)
        pts = []
        eqs = []
        for (x,y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            pts.append(ax.coords_to_point(x, y))
        dots = []
        for pt in pts:
            dots.append(Dot(pt, color=ORANGE).set_z_index(5))
        eqs.append(MathTex(r'1', font_size=30).set_z_index(2).next_to(dots[0], DOWN, buff=0.1))
        eqt = MathTex(r'-1', font_size=30).set_z_index(2)
        eqs.append(eqt.next_to(dots[1], DOWN, buff=0.1, submobject_to_align=eqt[0][1]))
        eqs.append(MathTex(r'i', font_size=30).set_z_index(2).next_to(dots[2], LEFT, buff=0.1))
        eqs.append(MathTex(r'-i', font_size=30).set_z_index(2).next_to(dots[3], LEFT, buff=0.1))

        ndots = VGroup(*[Dot(ax.coords_to_point(x, 0), color=YELLOW).set_z_index(4) for x in [-3, -2, 0, 2, 3]])
        qdots = VGroup(*[Dot(ax.coords_to_point(x, 0), color=BLUE, radius=DEFAULT_DOT_RADIUS*0.6)
                       .set_z_index(3) for x in np.linspace(-3, 3, 27)])
        rline = Line(ax.coords_to_point(-3,0), ax.coords_to_point(3,0), color=BLUE, stroke_width=3).set_z_index(3)

        self.play(FadeIn(box, ax, *dots[:], *eqs[:]), run_time=1)
        self.wait(0.1)
        self.play(Create(ndots), run_time=1)
        self.wait(0.1)
        self.play(Create(qdots), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(qdots, ndots), FadeIn(rline), run_time=1)
        self.wait(0.1)

        points = [
            (2.5, 0),
            (2.5, 5),
            (-6, 2),
            (-2,-5),
            (1, -2.5),
            (2.5, 2.5)
        ]
        bez = bezier([ax.coords_to_point(*pt) for pt in points])
        plot = ParametricFunction(bez, color=RED, stroke_width=5).set_z_index(4).set_opacity(0)

        def dot_move():
            plot.get_end()
            return Dot(plot.get_end(), color=YELLOW, radius=DEFAULT_DOT_RADIUS * 1.5).set_z_index(4)

        dot = always_redraw(dot_move).move_to(plot.get_start())
        self.play(FadeIn(dot), run_time=1)
        self.play(Create(plot), run_time=3)
        self.remove(dot)
        dot = dot.copy()
        self.add(dot)

        # extend to C
        self.wait(0.5)
        ecc = MathTex(r'\mathbb C\mathbb C')[0].set_z_index(2)
#        self.play(ReplacementTransform(edef1[1:] + edef1[0][1:] + edef1[0][0][:2] + edef1[0][0][3:7],
#                                       edef[1:] + edef[0][1:] + edef[0][0][:2] + edef[0][0][3:7]),
#                  abra.fade_replace(edef1[0][0][2], edef[0][0][2]),
#                  abra.fade_replace(edef1[0][0][7], edef[0][0][7]),
#                  run_time=1)
        self.play(abra.fade_replace(edef1[0][0][2], ecc[0].move_to(edef1[0][0][2])),
                  abra.fade_replace(edef1[0][0][7], ecc[1].move_to(edef1[0][0][7])),
                  run_time=1
                  )
        self.wait(0.5)

        pt = points[-1]
        eq1 = MathTex(r'x', font_size=25).next_to(dot, RIGHT, buff=0.1).set_z_index(2)
        self.play(FadeIn(eq1), run_time=0.5)

        eq2 = MathTex(r'e^x=\left(e^{\frac xn}\right)^n', font_size=32)[0].set_z_index(2)
        eq2.align_to(box, UL).shift(DOWN*0.2 + RIGHT*0.05)
        self.wait(0.1)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.1)
        dot0 = VGroup()
        for i in [2, 3, 4, 5, 6, 7]:
            pt1 = ax.coords_to_point(*[x/i for x in pt])
            dot1 = Dot(pt1, color=GREY).set_z_index(4)
            dot1 = VGroup(dot1, MathTex(r'\frac{{x}}{{{}}}'.format(i), font_size=25).set_z_index(2).next_to(dot1, RIGHT, buff=0.1))
            self.play(FadeIn(dot1), FadeOut(dot0), run_time=0.3)
            self.wait(0.4)
            dot0 = dot1
        self.wait(0.1)
        eq3 = MathTex(r'e^x\!\!\approx\!\!\left(1+{\frac xn}\right)^{\!n}', font_size=32)[0].set_z_index(2)
        eq3.next_to(eq2[:2], ORIGIN, submobject_to_align=eq3[:2])
        self.play(ReplacementTransform(eq2[:2] + eq2[3] + eq2[-5:],
                                       eq3[:2] + eq3[3] + eq3[-5:]),
                  abra.fade_replace(eq2[2], eq3[2]),
                  FadeOut(eq2[4:-5]), FadeIn(eq3[4:-5]),
                  run_time=1)

        self.wait(0.5)

        circ = abra.circle_eq(eprop1[0][1]).set_z_index(4)
        self.play(Create(circ), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(circ), run_time=0.5)
        circ = abra.circle_eq(eprop1[0][2]).set_z_index(4)
        self.play(FadeOut(eq3, dot1), Create(circ), run_time=1)
        self.wait(0.1)

        eq4 = MathTex(r'e^x=1+x+x^2\sum_{n=2}^\infty\frac{x^{n-2}}{n!}')[0].set_z_index(2).move_to(ORIGIN).to_edge(DOWN).shift(LEFT*0.5)

        box1 = SurroundingRectangle(eq4, corner_radius=0.2, fill_color=BLACK, fill_opacity=self.opacity, stroke_opacity=0)

        eq5 = eprop1[0][-1].copy()
        self.play(LaggedStart(FadeOut(ax, rline, dot, *dots, *eqs, eq1),
                  eq5.animate.next_to(eq4[2], ORIGIN, submobject_to_align=eq5[2]),
                              lag_ratio=0.4),
                  ReplacementTransform(box, box1),
                  run_time=2.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq5[:3] + eq5[3:7] + eq5[8:10] + eq5[-3:],
                                       eq4[:3] + eq4[9:13] + eq4[14:16] + eq4[-3:]),
                  abra.fade_replace(eq5[7], eq4[13]),
                  FadeIn(eq4[3:7]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4[-6].copy(), eq4[7]),
                  FadeIn(eq4[8], eq4[-5:-3]),
                  run_time=1)
        eq6 = MathTex(r'{}+o(x)')[0].set_z_index(2)
        eq6.next_to(eq4[6], ORIGIN, submobject_to_align=eq6[0])
        self.wait(0.1)
        self.play(FadeOut(eq4[7:]),
                  FadeIn(eq6[1:]),
                  run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq4[:7], eq6[1:], box1), run_time=1)
        self.wait(0.1)
        circ2 = abra.circle_eq(edef1[0][1]).set_z_index(4)
        self.play(Create(circ2), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(circ, circ2), run_time=1)
        self.wait(0.5)
        circ = abra.circle_eq(eprop1[0][0]).set_z_index(4)
        self.play(Create(circ), run_time=1)

        eq7 = MathTex(r'\frac{d}{dx}\exp(x)=\exp(x)')[0].set_z_index(2)
        eq8 = MathTex(r'\frac{d}{dx}\left(\exp(x)e^{-x}\right){{=}}\left(\frac{d}{dx}\exp(x)\right)e^{-x}'
                      r'+\exp(x)\frac{d}{dx}e^{-x}', font_size=40).set_z_index(2)
        eq8.to_edge(DL, buff=0.2)
        eq7.next_to(eq8, UP, coor_mask=UP)
        eq10 = MathTex(r'\left(-e^{-x}\right)', font_size=40)[0].set_z_index(2)
        eq10.next_to(eq8[2][-3:], ORIGIN, submobject_to_align=eq10[-4:-1])
        box2 = SurroundingRectangle(eq7, corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)
        box3 = SurroundingRectangle(VGroup(eq8, eq10), corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)

        self.wait(0.5)
        self.play(FadeIn(box2, eq7[4:10]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq7[:4], eq7[10:]), run_time=1)
        self.wait(0.1)
        eq9 = eq8[0].copy().align_to(eq7, LEFT)
        self.play(FadeIn(box3, eq9), run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(eq9, eq8[0]), FadeIn(eq8[1]), lag_ratio=0.5), run_time=1.5)
        self.play(FadeIn(eq8[2]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq8[2][:5], eq8[2][11]), run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq8[2][-7:-3]),
                  ReplacementTransform(eq8[2][-3:], eq10[-4:-1]),
                  FadeIn(eq10[-6:-4], eq10[-1]),
                  run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq8[2][15], eq10[0], eq10[-1]), eq10[1].animate.move_to(eq8[2][15]), run_time=1.2)
        eq11 = MathTex(r'=0', font_size=40)[0].set_z_index(2)
        eq11.next_to(eq8[1][0], ORIGIN, submobject_to_align=eq11[0])
        self.wait(0.5)
        self.play(FadeOut(eq8[2][5:11], eq8[2][12:15], eq8[2][16:22], eq10[1:5]),
                  FadeIn(eq11[1]), run_time=1.5)

        eq12 = MathTex(r'\exp(x)e^{-x}=ce^x')[0].set_z_index(2)
        eq12.next_to(eq7[-7], ORIGIN, submobject_to_align=eq12[-4]).align_to(eq7, LEFT)
        self.wait(0.5)
        self.play(ReplacementTransform(eq7[4:10], eq12[:6]),
                  FadeIn(eq12[6:11]),
                  FadeOut(eq7[:4], eq7[10:]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq12[6:7] + eq12[8], eq12[-2:-1] + eq12[-1]),
                  FadeOut(eq12[7], target_position=eq12[-1]),
                  run_time=1)
        self.wait(0.1)
        self.play(FadeOut(eq12[-3]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(box2, box3, circ, eq12[:6], eq12[9], eq12[11:], eq11[1], eq8[:2]), run_time=1)

        self.wait(0.5)

        ecc2 = MathTex(r'\mathbb C\mathbb C')[0].set_z_index(2)


        eq1 = MathTex(r'a^x=e^{x\ln a}')[0].set_z_index(2)
        eq2 = MathTex(r'a^x=e^{xc}')[0].set_z_index(2).next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'a = e^c')[0].set_z_index(2).next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4 = MathTex(r'c=\ln a')[0].set_z_index(2).next_to(eq3, DOWN).align_to(eq1, LEFT)
        gp = VGroup(eq1, eq2, eq3, eq4).move_to(ORIGIN).to_edge(DOWN, buff=0.1)
        box4 = SurroundingRectangle(gp, corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)

        self.play(FadeIn(eq1, box4), run_time=1)
        self.wait(0.5)
        self.play(abra.fade_replace(def1[0][0][2], ecc2[0].move_to(def1[0][0][2])),
                  abra.fade_replace(def1[0][1][-1], ecc2[1].move_to(def1[0][1][-1])),
                  run_time=1)
        self.wait(0.1)
        self.play(FadeOut(def1[0][-1]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq3), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq4), run_time=1)
        self.wait(0.5)

        edef = self.create_edef()
        defs = self.create_def()
        self.play(ReplacementTransform(edef1[1:] + edef1[0][1:] + edef1[0][0][:2] + ecc[0] + edef1[0][0][3:7] + ecc[1],
                                       edef[1:] + edef[0][1:] + edef[0][0][:2] + edef[0][0][2] + edef[0][0][3:7] + edef[0][0][7]),
                  ReplacementTransform(def1[1:] + def1[0][2:-1] + def1[0][0][:2] + ecc2[0] + def1[0][0][3:] + def1[0][1][:3] + ecc2[1],
                                       defs[1:] + defs[0][2:-1] + defs[0][0][:2] + defs[0][0][2] + defs[0][0][3:] + defs[0][1][:3] + defs[0][1][3]),
                  FadeIn(defs[0][-1]),
                  run_time=1.5)

        self.play(FadeOut(eq2, eq3, eq4), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq1, box4), run_time=1)
        self.wait(0.5)
        
        eq13 = MathTex(r'a^{x+iy}=a^xa^{iy}')[0].set_z_index(2).to_edge(DOWN, buff=1)
        box5 = SurroundingRectangle(eq13, corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)

        self.play(FadeIn(eq13, box5), run_time=1)
        eq14 = eq13[-3:].copy().set_color(RED).scale(1.2)
        self.play(Transform(eq13[-3:], eq14, rate_func=rate_functions.there_and_back), run_time=2)

        self.wait(0.5)
        self.play(FadeOut(eq13, box5), run_time=1)

        self.wait(0.5)


class EulerDemo(Scene):
    def get_demoplot(self, ax: Axes, n):
        parts = []
        z0 = 1. + 0j
        w = 1. + 1j/n * math.pi
        origin = ax.coords_to_point(0, 0)
        p0 = ax.coords_to_point(z0.real, z0.imag)
        for i in range(n):
            z1 = z0 * w
            p1 = ax.coords_to_point(z1.real, z1.imag)
            line1 = Line(p0, p1, color=WHITE).set_z_index(3)
            line2 = Line(p1, origin, color=WHITE).set_z_index(3)
            dot = Dot(p1, color=BLUE, radius=DEFAULT_DOT_RADIUS*1).set_z_index(4)
            parts.append(VGroup(line1, dot, line2))
            p0 = p1
            z0 = z1

        line1 = Line(p0, p1, color=WHITE).set_z_index(3)
        line2 = Line(p1, origin, color=WHITE).set_z_index(3)
        dot = Dot(p1, color=BLUE, radius=DEFAULT_DOT_RADIUS*1).set_z_index(4)
        extra = VGroup(line1, dot, line2)


        gp1 = VGroup(*parts)
        z1 *= (1 + 0.6 * (1-1/n)/abs(z1))
        eq = MathTex(r'z^{{{}}}'.format(n), font_size=60, color=RED, z_index=6, stroke_width=1.4)[0].set_z_index(6)
        eq.next_to(ax.coords_to_point(z1.real, z1.imag), ORIGIN, submobject_to_align=eq[0])
        shift = (ax.coords_to_point(0, 0) - eq.get_bottom())[1]+0.05
        eq.shift(UP * max(shift, 0.))

        eq1 = MathTex(r'z=1+i\pi/{}'.format(n))[0].set_z_index(2)
        eq1.next_to(ax.coords_to_point(w.real, w.imag), RIGHT)
        shift = (ax.coords_to_point(0, 0) - eq1.get_bottom())[1]+0.05
        eq1.shift(UP * max(shift, 0.))
        return VGroup(gp1, eq, eq1, extra)

    def construct(self):
        y1m = config.frame_y_radius * 0.9
        ym = 3.15
        scale = 1.4
        xm = ym * scale
        ax = Axes(x_range=[-xm, xm], y_range=[-ym, ym], z_index=2, x_length=2 * y1m * scale, y_length=2 * y1m, tips=False,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05
                               }).set_z_index(2)

        axlines = []
        y = 0.5
        while y < ym:
            axlines.append(DashedLine(ax.coords_to_point(-xm, y), ax.coords_to_point(xm, y), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            axlines.append(DashedLine(ax.coords_to_point(-xm, -y), ax.coords_to_point(xm, -y), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            y += 0.5
        x = 0.5
        while x < xm:
            axlines.append(DashedLine(ax.coords_to_point(x, -ym), ax.coords_to_point(x, ym), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            axlines.append(DashedLine(ax.coords_to_point(-x, -ym), ax.coords_to_point(-x, ym), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            x += 0.5

        pts = []
        eqs = []
        for (x,y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            pts.append(ax.coords_to_point(x, y))
        dots = []
        fs = 50
        for pt in pts:
            dots.append(Dot(pt, color=YELLOW).set_z_index(5))
        eqs.append(MathTex(r'1', font_size=fs).set_z_index(2).next_to(dots[0], DOWN, buff=0.1))
        eqt = MathTex(r'-1', font_size=fs).set_z_index(2)
        eqs.append(eqt.next_to(dots[1], DOWN, buff=0.1, submobject_to_align=eqt[0][1]))
        eqs.append(MathTex(r'i', font_size=fs).set_z_index(2).next_to(dots[2], LEFT, buff=0.1))
        eqs.append(MathTex(r'-i', font_size=fs).set_z_index(2).next_to(dots[3], LEFT, buff=0.1))


        fs = 100
        fs2 = 60
        eq1 = MathTex(r'e^{i\pi}{{=}}\left(e^{\frac{i\pi}{n}}\right)^n', font_size=fs)
        eq1.shift(-eq1[:3].get_center())
        eq1_1 = eq1[0][:].copy().move_to(ORIGIN, coor_mask=RIGHT)
        eq3 = MathTex(r'e^{i\pi}{{\approx}}\left(1+\frac{i\pi}{n}\ln e\right)^n', font_size=fs)
        eq3.next_to(eq1[1], ORIGIN, submobject_to_align=eq3[1], coor_mask=UP)
        eq4 = MathTex(r'e^{i\pi}{{\approx}}\left(1+\frac{i\pi}{n}\right)^n', font_size=fs)
        eq4.next_to(eq1[1], ORIGIN, submobject_to_align=eq4[1], coor_mask=UP)
        eq5 = MathTex(r'e^{i\pi}{{=}}-1', font_size=fs).scale(fs2/fs).to_edge(UL, buff=0.5)

        self.play(FadeIn(eq1_1), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(AnimationGroup(
            FadeIn(eq1[1]),
            ReplacementTransform(eq1_1[:1].copy(), eq1[2][1:2]),
            abra.fade_replace(eq1_1[1:3].copy(), eq1[2][2:4]),
            ReplacementTransform(eq1_1, eq1[0]),
            FadeIn(eq1[2][0], eq1[2][6:])),
            FadeIn(eq1[2][4:6]), lag_ratio=0.5),
            run_time=1.5)
        self.wait(0.1)
        eq2 = MathTex(r'e^{\frac{i\pi}{n}\ln e}', font_size=fs)[0].set_opacity(0).set_z_index(2)
        eq2.next_to(eq1[2][2:-2], ORIGIN, submobject_to_align=eq2[1:5])
        self.play(ReplacementTransform(eq1[2][:1] + eq1[2][4:-2] + eq1[2][-2:],
                                       eq3[2][:1] + eq3[2][5:-5] + eq3[2][-2:]),
                  abra.fade_replace(eq1[2][2:4], eq3[2][3:5]),
                  FadeOut(eq1[2][1]), FadeIn(eq3[2][1:3]),
                  abra.fade_replace(eq2[-3:], eq3[2][-5:-2]),
                  ReplacementTransform(eq1[1], eq3[1]),
                  ReplacementTransform(eq1[0], eq3[0]),
                  run_time=1.5
                  )
        line = Line(eq3[2][-5:-2].get_corner(DL) + DL*0.2, eq3[2][-5:-2].get_corner(UR) + UR*0.2, color=RED, stroke_width=10)
        self.wait(0.1)
        self.play(FadeIn(line), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(line, eq3[2][-5:-2]),
                  ReplacementTransform(eq3[:2] + eq3[2][:-5] + eq3[2][-2:], eq4[:2] + eq4[2][:-2] + eq4[2][-2:]), run_time=1)

        self.wait(0.5)
        self.play(eq4.animate.scale(fs2/fs).to_edge(UL, buff=0.5),
                  FadeIn(ax, *dots, *eqs, *axlines), run_time=2)
        self.wait(0.5)

        demo = self.get_demoplot(ax, 1)
        self.play(FadeIn(demo[:-1]), run_time=1)

        for i in range(2, 51):
#            self.wait(3/30 + 0.01)
            demo1 = self.get_demoplot(ax, i)

            run_time = 2.0/i + 1.1/15
            self.play(ReplacementTransform(demo[0][:], demo1[0][:-1], rate_func=linear),
                      ReplacementTransform(demo[-1], demo1[0][-1], rate_func=linear),
#                      FadeIn(demo1[0][-1], rate_func= lambda t: max(t*2-1, 0.)),
                      ReplacementTransform(demo[1][0], demo1[1][0], rate_func=linear),
                      abra.fade_replace(demo[1][1:], demo1[1][1:]),
                      ReplacementTransform(demo[2][:7], demo1[2][:7]),
                      abra.fade_replace(demo[2][7:], demo1[2][7:]),
                      rate_func=linear,
                      run_time=run_time)
            demo = demo1

        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1])
        self.play(ReplacementTransform(eq4[1], eq5[1]),
                  FadeOut(eq4[2]), FadeIn(eq5[2]),
                  run_time=1.5)
        self.wait(0.5)

        angle = ValueTracker(0.0)
        eq8 = MathTex(r'e^{it}', font_size=60)[0].set_z_index(11)
        end = PI * 4 + 0.6
        dt = PI/2

        def rotfunc():
            a = angle.get_value()
            pos = (math.cos(a), math.sin(a))
            pt = ax.coords_to_point(pos[0], pos[1])
            dot = Dot(pt, color=GREEN, radius=DEFAULT_DOT_RADIUS*1.5).set_z_index(10).move_to(pt)
            pt2 = ax.coords_to_point(pos[0] * 1.4, pos[1] * 1.4)
            eq8.move_to(pt2)
            if a < dt:
                opacity = max(a/dt, 1.)
            elif a > end-dt:
                opacity = max((end-a)/dt, 1.)
            else:
                opacity=1.0
            return VGroup(dot, eq8.copy()).set_opacity(opacity)

        rotpt = always_redraw(rotfunc)
        self.add(rotpt)
        self.play(angle.animate(rate_func=linear).set_value(end), run_time=5.2)
        self.remove(rotpt)

        self.wait(0.5)


class Taylor(ExpPosint):
    def construct(self):
        eq1 = MathTex(r'S_yf(x)=f(x+y)')[0].set_z_index(2)
        eq2 = MathTex(r'\frac{dS_y}{dy}f(x){{=}}\frac{d}{dy}f(x+y){{=}}Df(x+y){{=}}S_yDf(x)').set_z_index(2)
        eq2[3:5].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[3])
        eq2[5:7].next_to(eq2[1], ORIGIN, submobject_to_align=eq2[5])
        eq2.next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'\frac{dS_y}{dy}{{=}}S_yD').set_z_index(2)
        eq3.next_to(eq2[1], ORIGIN, submobject_to_align=eq3[1]).align_to(eq1, LEFT)
        eq4 = MathTex(r'S_y{{=}}e^{yD}{{=}}\sum_{n=0}^\infty\frac{y^n}{n!}D^n').set_z_index(2)
        eq4.next_to(eq2[1], ORIGIN, submobject_to_align=eq4[1]).align_to(eq1, LEFT)
        eq4[3:5].next_to(eq4[1], ORIGIN, submobject_to_align=eq4[3])
        eq5 = MathTex(r'S_yf(x){{=}}\sum_{n=0}^\infty\frac{y^n}{n!}D^nf(x)').set_z_index(2)
        eq5.next_to(eq2[1], ORIGIN, submobject_to_align=eq5[1]).align_to(eq1, LEFT)
        eq6 = MathTex(r'f(x+y){{=}}\sum_{n=0}^\infty\frac{y^n}{n!}f^{(n)}(x)').set_z_index(2)
        eq6.next_to(eq5[1], ORIGIN, submobject_to_align=eq6[1])
        gp = VGroup(eq1, eq2, eq3, eq4, eq5, eq6).to_edge(DOWN, buff=0.4)
        box = SurroundingRectangle(gp, corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)
        self.play(FadeIn(box, eq1), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq2[0]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq2[1:3]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq2[4][0]), FadeOut(eq2[2][:4]),
                  ReplacementTransform(eq2[2][-6:], eq2[4][-6:]),
                  run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq2[4][:4] + eq2[4][-1] + eq2[4][5], eq2[6][2:6] + eq2[6][-1] + eq2[6][1]),
                  FadeOut(eq2[4][4]), FadeIn(eq2[6][0]),
                  run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(FadeOut(eq2[0][-4:], eq2[6][-4:]),
                              ReplacementTransform(eq2[0][:-4] + eq2[6][:-4] + eq2[1], eq3[0][:] + eq3[2][:] + eq3[1]),
                              lag_ratio=0.5),
                  run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(eq3[0][0], eq3[0][3:]),
                  abra.fade_replace(eq3[2][0], eq4[2][0]),
                  ReplacementTransform(eq3[0][1:3] + eq3[1] + eq3[2][1:],
                                       eq4[0][:] + eq4[1] + eq4[2][1:]),
                  run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4[2][1:2] + eq4[2][2], eq4[4][5:6] + eq4[4][10]),
                  FadeIn(eq4[4][:5], eq4[4][6:10], eq4[4][11:]),
                  FadeOut(eq4[2][0], target_position=eq4[4][7].get_left()),
                  run_time=1.5)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(eq4[0][:] + eq4[1] + eq4[4][:], eq5[0][:-4] + eq5[1] + eq5[2][:-4]),
                  FadeIn(eq5[0][-4:], eq5[2][-4:]), lag_ratio=0.5), run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq5[0][1:2] + eq5[0][2:5] + eq5[0][5] + eq5[1],
                                       eq6[0][4:5] + eq6[0][:3] + eq6[0][5] + eq6[1]),
                  FadeOut(eq5[0][0]),
                  FadeIn(eq6[0][-3]),
                  run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(
            eq5[2][:-6] + eq5[2][-5] + eq5[2][-3:] + eq5[2][-4],
            eq6[2][:-7] + eq6[2][-5] + eq6[2][-3:] + eq6[2][-7]),
                  FadeOut(eq5[2][-6]),
                  FadeIn(eq6[2][-6], eq6[2][-4]),
                  run_time=1.5)
        self.wait(0.5)


class Year2025(ExpPosint):
    def construct(self):
        MathTex.set_default(font_size=80)
        eq0 = MathTex(r'45^2').set_z_index(2)
        eq1 = MathTex(r'45^2{{=}}45\cdot 45{{=}}2025').set_z_index(2)
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3])
        eq1.move_to(ORIGIN)
        gp = VGroup(eq0, eq1).to_edge(DOWN, buff=1)
        box = SurroundingRectangle(gp, corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)
        box2 = SurroundingRectangle(eq1[:2] + eq1[4], corner_radius=0.2, stroke_opacity=0, fill_opacity=self.opacity, fill_color=BLACK)
        self.wait(0.5)
        self.play(FadeIn(box, eq0), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq1[1]),
                  ReplacementTransform(eq0[0][:] + eq0[0][:2].copy() + eq0[0][:2].copy(), eq1[0][:] + eq1[2][:2] + eq1[2][-2:]),
                  FadeIn(eq1[2][2]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq1[-1]), FadeOut(eq1[2]), ReplacementTransform(box, box2), run_time=1.5)
        self.wait(0.5)


class ZeroNat(ExpPosint):
    def construct(self):
        eq = MathTex(r'\bf 0\!\in\!\mathbb N', stroke_width=1, stroke_color=BLACK, font_size=400)
        self.add(eq)


class ExpPi(ExpPosint):
    bgcolor=WHITE
    def construct(self):
        eq = MathTex(r'e^{\pi}{{=}}eeee', font_size=100)
        self.wait(0.1)
        self.play(FadeIn(eq[0][0]), run_time=0.5)
        self.wait(0.05)
        self.play(FadeIn(eq[0][1]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeIn(eq[1]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeIn(eq[2][0]), run_time=0.5)
        self.play(FadeIn(eq[2][1]), run_time=0.5)
        self.play(FadeIn(eq[2][2]), run_time=0.5)
        self.play(FadeIn(eq[2][3]), run_time=0.5)
        self.wait(0.5)


class Apown(ExpPosint):
    bgcolor = WHITE

    def construct(self):
        eq = MathTex(r'a^n{{=}}aa\cdots a', font_size=100)
        txt = MathTex(r'n\ {\rm copies\ of\ }a', font_size=60, color=RED, stroke_width=1.5)
        br1 = BraceLabel(eq[2], r'', brace_direction=UP,
                         label_constructor=abra.brace_label(txt),
                         brace_config={'color': RED})
        self.wait(0.1)
        self.play(FadeIn(eq[0][0]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeIn(eq[0][1]), run_time=0.5)
        self.wait(0.1)
        self.play(FadeIn(eq[1]), run_time=0.5)
        self.wait(0.1)
        self.play(LaggedStart(FadeIn(eq[2]), FadeIn(br1), lag_ratio=0.5), run_time=1)
        self.wait(0.5)


class Epii(ExpPosint):
    def construct(self):
        self.add(MathTex(r'e^{i\pi}+1=0', font_size=100))


class PowS_im(ExpPosint):
    def construct(self):
        MathTex.set_default(color=BLACK, stroke_width=1.5)
        self.add(MathTex(r'e^x=\sum_{n=0}^\infty\frac{x^n}{n!}', font_size=30))


class Lim_im(ExpPosint):
    def construct(self):
        MathTex.set_default(color=BLACK, stroke_width=1.5)
        self.add(MathTex(r'e^x=\lim_{n\to\infty}\left(1+\frac xn\right)^n', font_size=30))


class Deriv_im(ExpPosint):
    def construct(self):
        self.add(MathTex(r'\frac{d}{dx}e^x=e^x', font_size=60))


class Trig_im(ExpPosint):
    def construct(self):
        self.add(MathTex(r'e^{ix}=\cos x+i\sin x', font_size=60))


class E_im(ExpPosint):
    def construct(self):
        eq = MathTex(r'e{{=}}2.7182818\ldots', font_size=100)
        self.add(eq)


class Outtro1(ExpPosint):
    bgcolor = BLACK

    def construct(self):
        self.wait(0.5)
        MathTex.set_default(font_size=60)
        eq1 = MathTex(r'2025{{=}}45^2')
        eq2 = MathTex(r'2025{{=}}(1+2+3+4+5+6+7+8+9)^2')
        eq3 = MathTex(r'2025{{=}}1^3+2^3+3^3+4^3+5^3+6^3+7^3+8^3+9^3')
        eq2.move_to(eq1)
        eq3.move_to(eq1)
        gp = VGroup(eq1, eq2, eq3).move_to(ORIGIN)
#        eq3.next_to(eq2[1], ORIGIN, submobject_to_align=eq3[1])
        self.play(FadeIn(eq1), run_time=1)
        self.wait(3)
        self.play(abra.fade_replace(eq1[2][:-1], eq2[2][:-1]),
                  ReplacementTransform(eq1[2][-1], eq2[2][-1]),
                  ReplacementTransform(eq1[:2], eq2[:2]),
                  run_time=3)

        j = 2
        anims = [ReplacementTransform(eq2[2][1], eq3[2][0])]

        for i in range(2, 18, 2):
            anims.append(ReplacementTransform(eq2[2][i:i+2], eq3[2][j:j+2]))
            j += 3
        for i in range(1, 28, 3):
            anims.append(FadeIn(eq3[2][i]))#, target_position=eq2[2][-1]))

        self.wait(3)
        self.play(FadeOut(eq2[2][0], eq2[2][-2]),
                  ReplacementTransform(eq2[:2], eq3[:2]),
                  FadeOut(eq2[2][-1]),#, target_position=eq3[2][-1]),
                  *anims, run_time=3)
        self.wait(3)
        self.play(FadeOut(eq3), run_time=2)

class EulerDemoThumb(Scene):
    def get_demoplot(self, ax: Axes, n):
        parts = []
        z0 = 1. + 0j
        w = 1. + 1j/n * math.pi
        origin = ax.coords_to_point(0, 0)
        p0 = ax.coords_to_point(z0.real, z0.imag)
        for i in range(n):
            z1 = z0 * w
            p1 = ax.coords_to_point(z1.real, z1.imag)
            line1 = Line(p0, p1, color=WHITE).set_z_index(3)
            line2 = Line(p1, origin, color=WHITE).set_z_index(3)
            dot = Dot(p1, color=BLUE, radius=DEFAULT_DOT_RADIUS*1).set_z_index(4)
            parts.append(VGroup(line1, dot, line2))
            p0 = p1
            z0 = z1

        line1 = Line(p0, p1, color=WHITE).set_z_index(3)
        line2 = Line(p1, origin, color=WHITE).set_z_index(3)
        dot = Dot(p1, color=BLUE, radius=DEFAULT_DOT_RADIUS*1).set_z_index(4)
        extra = VGroup(line1, dot, line2)


        gp1 = VGroup(*parts)
        z1 *= (1 + 0.6 * (1-1/n)/abs(z1))
        eq = MathTex(r'z^{{{}}}'.format(n), font_size=60, color=RED, z_index=6, stroke_width=1.4)[0].set_z_index(6)
        eq.next_to(ax.coords_to_point(z1.real, z1.imag), ORIGIN, submobject_to_align=eq[0])
        shift = (ax.coords_to_point(0, 0) - eq.get_bottom())[1]+0.05
        eq.shift(UP * max(shift, 0.))

        eq1 = MathTex(r'z=1+i\pi/{}'.format(n))[0].set_z_index(2)
        eq1.next_to(ax.coords_to_point(w.real, w.imag), RIGHT)
        shift = (ax.coords_to_point(0, 0) - eq1.get_bottom())[1]+0.05
        eq1.shift(UP * max(shift, 0.))
        return VGroup(gp1, eq, eq1, extra)

    def construct(self):
        y1m = config.frame_y_radius * 0.9
        ym = 3.15
        scale = 1.4
        xm = ym * scale
        ax = Axes(x_range=[-xm, xm], y_range=[-ym, ym], z_index=2, x_length=2 * y1m * scale, y_length=2 * y1m, tips=False,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05
                               }).set_z_index(2)

        axlines = []
        y = 0.5
        while y < ym:
            axlines.append(DashedLine(ax.coords_to_point(-xm, y), ax.coords_to_point(xm, y), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            axlines.append(DashedLine(ax.coords_to_point(-xm, -y), ax.coords_to_point(xm, -y), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            y += 0.5
        x = 0.5
        while x < xm:
            axlines.append(DashedLine(ax.coords_to_point(x, -ym), ax.coords_to_point(x, ym), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            axlines.append(DashedLine(ax.coords_to_point(-x, -ym), ax.coords_to_point(-x, ym), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            x += 0.5

        pts = []
        eqs = []
        for (x,y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            pts.append(ax.coords_to_point(x, y))
        dots = []
        fs = 50
        for pt in pts:
            dots.append(Dot(pt, color=YELLOW).set_z_index(5))
        eqs.append(MathTex(r'1', font_size=fs).set_z_index(2).next_to(dots[0], DOWN, buff=0.1))
        eqt = MathTex(r'-1', font_size=fs).set_z_index(2)
        eqs.append(eqt.next_to(dots[1], DOWN, buff=0.1, submobject_to_align=eqt[0][1]))
        eqs.append(MathTex(r'i', font_size=fs).set_z_index(2).next_to(dots[2], LEFT, buff=0.1))
        eqs.append(MathTex(r'-i', font_size=fs).set_z_index(2).next_to(dots[3], LEFT, buff=0.1))


        fs = 100
        fs2 = 60

        demo = self.get_demoplot(ax, 11)
        self.add(ax, *eqs, *dots, *axlines, demo[:-1])
        return

        self.play(FadeIn(demo[:-1]), run_time=1)

        for i in range(2, 51):
#            self.wait(3/30 + 0.01)
            demo1 = self.get_demoplot(ax, i)

            run_time = 2.0/i + 1.1/15
            self.play(ReplacementTransform(demo[0][:], demo1[0][:-1], rate_func=linear),
                      ReplacementTransform(demo[-1], demo1[0][-1], rate_func=linear),
#                      FadeIn(demo1[0][-1], rate_func= lambda t: max(t*2-1, 0.)),
                      ReplacementTransform(demo[1][0], demo1[1][0], rate_func=linear),
                      abra.fade_replace(demo[1][1:], demo1[1][1:]),
                      ReplacementTransform(demo[2][:7], demo1[2][:7]),
                      abra.fade_replace(demo[2][7:], demo1[2][7:]),
                      rate_func=linear,
                      run_time=run_time)
            demo = demo1

        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1])
        self.play(ReplacementTransform(eq4[1], eq5[1]),
                  FadeOut(eq4[2]), FadeIn(eq5[2]),
                  run_time=1.5)
        self.wait(0.5)

        angle = ValueTracker(0.0)
        eq8 = MathTex(r'e^{it}', font_size=60)[0].set_z_index(11)
        end = PI * 4 + 0.6
        dt = PI/2

        def rotfunc():
            a = angle.get_value()
            pos = (math.cos(a), math.sin(a))
            pt = ax.coords_to_point(pos[0], pos[1])
            dot = Dot(pt, color=GREEN, radius=DEFAULT_DOT_RADIUS*1.5).set_z_index(10).move_to(pt)
            pt2 = ax.coords_to_point(pos[0] * 1.4, pos[1] * 1.4)
            eq8.move_to(pt2)
            if a < dt:
                opacity = max(a/dt, 1.)
            elif a > end-dt:
                opacity = max((end-a)/dt, 1.)
            else:
                opacity=1.0
            return VGroup(dot, eq8.copy()).set_opacity(opacity)

        rotpt = always_redraw(rotfunc)
        self.add(rotpt)
        self.play(angle.animate(rate_func=linear).set_value(end), run_time=5.2)
        self.remove(rotpt)

        self.wait(0.5)


class EulerDemo_short(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def get_demoplot(self, ax: Axes, n):
        parts = []
        z0 = 1. + 0j
        w = 1. + 1j/n * math.pi
        origin = ax.coords_to_point(0, 0)
        p0 = ax.coords_to_point(z0.real, z0.imag)
        for i in range(n):
            z1 = z0 * w
            p1 = ax.coords_to_point(z1.real, z1.imag)
            line1 = Line(p0, p1, color=WHITE).set_z_index(3)
            line2 = Line(p1, origin, color=WHITE).set_z_index(3)
            dot = Dot(p1, color=BLUE, radius=DEFAULT_DOT_RADIUS*1).set_z_index(4)
            parts.append(VGroup(line1, dot, line2))
            p0 = p1
            z0 = z1

        line1 = Line(p0, p1, color=WHITE).set_z_index(3)
        line2 = Line(p1, origin, color=WHITE).set_z_index(3)
        dot = Dot(p1, color=BLUE, radius=DEFAULT_DOT_RADIUS*1).set_z_index(4)
        extra = VGroup(line1, dot, line2)


        gp1 = VGroup(*parts)
        z1 *= (1 + 0.6 * (1-1/n)/abs(z1))
        eq = MathTex(r'z^{{{}}}'.format(n), font_size=50, color=RED, z_index=6, stroke_width=1.4)[0].set_z_index(6)
        eq.next_to(ax.coords_to_point(z1.real, z1.imag), ORIGIN, submobject_to_align=eq[0])
        shift = (ax.coords_to_point(0, 0) - eq.get_bottom())[1]+0.05
        eq.shift(UP * max(shift, 0.))

        eq1 = MathTex(r'z=1+\frac{{i\pi}}{{ {} }}'.format(n), font_size=35)[0].set_z_index(2)
        eq1.next_to(ax.coords_to_point(w.real, w.imag), RIGHT)
        shift = (ax.coords_to_point(0, 0) - eq1.get_bottom())[1]+0.05
        eq1.shift(UP * max(shift, 0.))
        return VGroup(gp1, eq, eq1, extra)

    def eqns(self):
        fs = 100
        fs2 = 60
        eq1 = MathTex(r'e^{i\pi}{{=}}\left(e^{\frac{i\pi}{n}}\right)^n', font_size=fs)
        eq1.shift(-eq1[:3].get_center())
        eq1_1 = eq1[0][:].copy().move_to(ORIGIN, coor_mask=RIGHT)
        eq3 = MathTex(r'e^{i\pi}{{\approx}}\left(1+\frac{i\pi}{n}\ln e\right)^n', font_size=fs)
        eq3.next_to(eq1[1], ORIGIN, submobject_to_align=eq3[1], coor_mask=UP)
        eq4 = MathTex(r'e^{i\pi}{{\approx}}\left(1+\frac{i\pi}{n}\right)^n', font_size=fs)
        eq4.next_to(eq1[1], ORIGIN, submobject_to_align=eq4[1], coor_mask=UP)
        eq5 = MathTex(r'e^{i\pi}{{=}}-1', font_size=fs)
        eq5.next_to(eq1[1], ORIGIN, submobject_to_align=eq5[1], coor_mask=UP)
        eq6 = MathTex(r'e^{i\pi}+1 {{=}} 0', font_size=fs)
        eq6.next_to(eq1[1], ORIGIN, submobject_to_align=eq6[1], coor_mask=UP)
        self.play(FadeIn(eq1_1), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(AnimationGroup(
            FadeIn(eq1[1]),
            ReplacementTransform(eq1_1[:1].copy(), eq1[2][1:2]),
            abra.fade_replace(eq1_1[1:3].copy(), eq1[2][2:4]),
            ReplacementTransform(eq1_1, eq1[0]),
            FadeIn(eq1[2][0], eq1[2][6:])),
            FadeIn(eq1[2][4:6]), lag_ratio=0.5),
            run_time=1.5)
        self.wait(0.1)
        eq2 = MathTex(r'e^{\frac{i\pi}{n}\ln e}', font_size=fs)[0].set_opacity(0).set_z_index(2)
        eq2.next_to(eq1[2][2:-2], ORIGIN, submobject_to_align=eq2[1:5])
        self.play(ReplacementTransform(eq1[2][:1] + eq1[2][4:-2] + eq1[2][-2:],
                                       eq3[2][:1] + eq3[2][5:-5] + eq3[2][-2:]),
                  abra.fade_replace(eq1[2][2:4], eq3[2][3:5]),
                  FadeOut(eq1[2][1]), FadeIn(eq3[2][1:3]),
                  abra.fade_replace(eq2[-3:], eq3[2][-5:-2]),
                  ReplacementTransform(eq1[1], eq3[1]),
                  ReplacementTransform(eq1[0], eq3[0]),
                  run_time=1.5
                  )
        line = Line(eq3[2][-5:-2].get_corner(DL) + DL*0.2, eq3[2][-5:-2].get_corner(UR) + UR*0.2, color=RED, stroke_width=10)
        self.wait(0.1)
        self.play(FadeIn(line), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(line, eq3[2][-5:-2]),
                  ReplacementTransform(eq3[:2] + eq3[2][:-5] + eq3[2][-2:], eq4[:2] + eq4[2][:-2] + eq4[2][-2:]), run_time=1)

        self.wait(0.5)
#        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1])
        self.play(ReplacementTransform(eq4[1], eq5[1]),
                  ReplacementTransform(eq4[0], eq5[0]),
                  FadeOut(eq4[2]), FadeIn(eq5[2]),
                  run_time=1.5)
        self.wait(0.5)
        self.play(ReplacementTransform(eq5[0][:3] + eq5[1] + eq5[2][-1],
                                       eq6[0][:3] + eq6[1] + eq6[0][-1]),
                  abra.fade_replace(eq5[2][0], eq6[0][-2]),
                  FadeIn(eq6[2]),
                  run_time=1.5)

    def plots(self):
        y1m = config.frame_y_radius * 0.9
        scale = 1.4
        xm = 2.9
        ym = 3.6
        scale = config.frame_y_radius / ym * 0.9 * 2
        ax = Axes(x_range=[-xm, xm], y_range=[-ym, ym], z_index=2, x_length= xm * scale, y_length=ym * scale, tips=False,
                  axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05
                               }).set_z_index(2)

        axlines = []
        y = 0.5
        while y < ym:
            axlines.append(DashedLine(ax.coords_to_point(-xm, y), ax.coords_to_point(xm, y), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            axlines.append(DashedLine(ax.coords_to_point(-xm, -y), ax.coords_to_point(xm, -y), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            y += 0.5
        x = 0.5
        while x < xm:
            axlines.append(DashedLine(ax.coords_to_point(x, -ym), ax.coords_to_point(x, ym), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            axlines.append(DashedLine(ax.coords_to_point(-x, -ym), ax.coords_to_point(-x, ym), color=GREY,
                                      stroke_opacity=0.5, stroke_width=2, dash_length=DEFAULT_DASH_LENGTH * 0.5))
            x += 0.5

        pts = []
        eqs = []
        for (x,y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            pts.append(ax.coords_to_point(x, y))
        dots = []
        fs = 50
        for pt in pts:
            dots.append(Dot(pt, color=YELLOW).set_z_index(5))
        eqs.append(MathTex(r'1', font_size=fs).set_z_index(2).next_to(dots[0], DOWN, buff=0.1))
        eqt = MathTex(r'-1', font_size=fs).set_z_index(2)
        eqs.append(eqt.next_to(dots[1], DOWN, buff=0.1, submobject_to_align=eqt[0][1]))
        eqs.append(MathTex(r'i', font_size=fs).set_z_index(2).next_to(dots[2], LEFT, buff=0.1))
        eqs.append(MathTex(r'-i', font_size=fs).set_z_index(2).next_to(dots[3], LEFT, buff=0.1))

        fs = 100
        fs2 = 60


        self.play(FadeIn(ax, *dots, *eqs, *axlines), run_time=2)

        demo = self.get_demoplot(ax, 1)
        self.play(FadeIn(demo[:-1]), run_time=1)

        for i in range(2, 51):
            demo1 = self.get_demoplot(ax, i)

            run_time = 2.0/i + 1.1/15
            self.play(ReplacementTransform(demo[0][:], demo1[0][:-1], rate_func=linear),
                      ReplacementTransform(demo[-1], demo1[0][-1], rate_func=linear),
#                      FadeIn(demo1[0][-1], rate_func= lambda t: max(t*2-1, 0.)),
                      ReplacementTransform(demo[1][0], demo1[1][0], rate_func=linear),
                      abra.fade_replace(demo[1][1:], demo1[1][1:]),
                      ReplacementTransform(demo[2][:7], demo1[2][:7]),
                      abra.fade_replace(demo[2][7:], demo1[2][7:]),
                      rate_func=linear,
                      run_time=run_time)
            demo = demo1


        angle = ValueTracker(0.0)
        eq8 = MathTex(r'e^{it}', font_size=60)[0].set_z_index(11)
        end = PI * 4 + 0.6
        dt = PI/2

        def rotfunc():
            a = angle.get_value()
            pos = (math.cos(a), math.sin(a))
            pt = ax.coords_to_point(pos[0], pos[1])
            dot = Dot(pt, color=GREEN, radius=DEFAULT_DOT_RADIUS*1.5).set_z_index(10).move_to(pt)
            pt2 = ax.coords_to_point(pos[0] * 1.4, pos[1] * 1.4)
            eq8.move_to(pt2)
            if a < dt:
                opacity = max(a/dt, 1.)
            elif a > end-dt:
                opacity = max((end-a)/dt, 1.)
            else:
                opacity=1.0
            return VGroup(dot, eq8.copy()).set_opacity(opacity)

        rotpt = always_redraw(rotfunc)
        self.add(rotpt)
        self.play(angle.animate(rate_func=linear).set_value(end), run_time=5.2)
        self.remove(rotpt)

        self.wait(0.5)

    def construct(self):
        self.eqns()

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "fps": 15, "preview": True}):
        Logarithms().render()