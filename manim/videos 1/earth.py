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



distance_str = r'77.64'
height_str = r'316'
radius_str1 = r'9\,538'
radius_str2 = r'8\,184'
radiusE_str = r'6\,371'
me_str = r'2'
adjust1_str = r'1.165'


class RadiusCalc(Scene):
    still = False


    def get_earth(self, center, radius):
        earth_0 = ImageMobject(r"images/earth_bg.png", z_index=2)
        pa = earth_0.pixel_array.copy()
        m, n, _ = pa.shape
        for i in range(m):
            for j in range(n):
                for k in range(3):
                    pa[i, j, k] = int(pa[i, j, k] * 0.6)
        earth = ImageMobject(pa, z_index=2)
        mountain = ImageMobject(r"images/mountain11.png", z_index=1)
        wojak = ImageMobject(r'../abracadabra/wojak.png', z_index=15)
        earth.move_to(center).rotate(-30*DEGREES).scale(0.891).shift(RIGHT*0.1315 + DOWN*0.02)

        theta_is = 35.8*DEGREES
        p_is = center + (UP * math.cos(theta_is) + RIGHT * math.sin(theta_is)) * radius
        mountain.scale(0.17).next_to(p_is, UP, buff=0).rotate(-theta_is, about_point=p_is).shift((center-p_is) * 0.02)
        wojak.scale(0.2).next_to(center + UP * radius, LEFT, buff=0.2)

        return earth, mountain, wojak

    def get_trig(self, radius, theta2=33*DEGREES):
        cdot = Dot(radius=0.2, color=RED).to_edge(DOWN, buff=0.3).shift(LEFT * 1.5).set_z_index(10)
        center = cdot.get_center()
        surf = Arc(radius=radius, arc_center=center, start_angle=184*DEGREES, angle=-188*DEGREES, color=BLUE, stroke_width=5).set_z_index(10)
        p0 = center + UP * radius
        p2 = center + (UP + RIGHT * math.tan(theta2)) * radius
        p3 = center + (UP * math.cos(theta2) + RIGHT * math.sin(theta2)) * radius
        line = VGroup(
            Line(center, p0, stroke_color=LIGHT_BROWN, stroke_width=5).set_z_index(5),
            Line(p0, p2, stroke_color=WHITE, stroke_width=5).set_z_index(20),
            Line(p3, p2, stroke_color=WHITE, stroke_width=5).set_z_index(20),
            Line(center, p3, stroke_color=LIGHT_BROWN, stroke_width=5).set_z_index(5)
        )
        rightangle = RightAngle(line[0], line[1], length=0.5, stroke_color=WHITE, stroke_width=5,
                                quadrant=(-1, 1)).set_z_index(20)

        eq = VGroup(  # d, h, R0, R2
            MathTex(r'd')[0].next_to(line[1], UP, buff=0.2).set_z_index(30),
            MathTex(r'h', stroke_width=1.5)[0].move_to(line[2]).shift(DR * 0.25).set_z_index(30),
            MathTex(r'R')[0].next_to(line[0], LEFT, buff=0.1).set_z_index(30),
            MathTex(r'R')[0].move_to(line[3]).shift(DR * 0.25).set_z_index(30)
        )

        return cdot, surf, line, rightangle, eq

    def construct(self):
        radius = config.frame_y_radius * 1.5
        cdot, surf, line, rightangle, eq = self.get_trig(radius)
        earth, mountain, wojak = self.get_earth(cdot.get_center(), radius)

        gp = Group(VGroup(cdot, surf, line, rightangle, eq),
                   earth, mountain, wojak)

        eq_py = MathTex(r'(R+h)^2{{=}}R^2+d^2').set_z_index(30).to_edge(RIGHT).shift(UP)
        eq2 = MathTex(r'R^2+2Rh+h^2{{=}}').set_z_index(30)
        eq2.next_to(eq_py[1], ORIGIN, submobject_to_align=eq2[1])

        eq3 = MathTex(r'(2R+h)h{{=}}d^2').set_z_index(30)
        eq3.next_to(eq2[1], ORIGIN, submobject_to_align=eq3[1]).to_edge(RIGHT, buff=1)

        eq4 = MathTex(r'R{{\approx}}\frac{d^2}{2h}')
        eq4.next_to(eq3[1], ORIGIN, submobject_to_align=eq4[1]).shift(LEFT)

        if self.still:
            self.add(Group(earth, mountain, wojak, surf, line, eq, cdot, rightangle).shift(LEFT))
            return

        self.wait(0.5)

        self.play(FadeIn(earth, mountain), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(wojak), run_time=0.6)
        self.wait(0.2)

        self.play(Create(surf), run_time=1.5)

        self.wait(0.2)
        self.play(Create(line[1]), FadeIn(eq[0]), run_time=1.2)
        self.wait(0.2)

        self.play(Create(line[2]), FadeIn(eq[1]), run_time=0.8)
        self.wait(0.2)
        self.play(Create(line[0]), Create(line[3]), FadeIn(eq[2], eq[3], cdot), run_time=1.7)
        self.wait(0.2)
        self.play(Create(rightangle), run_time=0.8)
        self.wait(0.2)

        self.play(ReplacementTransform(eq[3][0].copy(),
                                       eq_py[0][1]),
                  ReplacementTransform(eq[1][0].copy(), eq_py[0][3]),
                  FadeIn(eq_py[0][2]),
                  gp.animate.shift(LEFT),
                  run_time=1.5)
        self.play(FadeIn(eq_py[0][0], eq_py[0][4:]), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq_py[1]), run_time=0.6)
        self.wait(0.2)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq[2][0].copy(), eq_py[2][0]),
                  ReplacementTransform(eq[0][0].copy(), eq_py[2][3]),
                  FadeIn(eq_py[2][2])),
                  FadeIn(eq_py[2][1], eq_py[2][4]),
                              lag_ratio=0.5),
                  run_time=2)
        self.wait(0.2)
        self.play(ReplacementTransform(eq_py[0][1], eq2[0][0]),
                  ReplacementTransform(eq_py[0][3], eq2[0][7]),
                  ReplacementTransform(eq_py[0][2], eq2[0][2]),
                  ReplacementTransform(eq_py[0][5], eq2[0][1]),
                  ReplacementTransform(eq_py[0][1].copy(), eq2[0][4]),
                  ReplacementTransform(eq_py[0][3].copy(), eq2[0][5]),
                  ReplacementTransform(eq_py[0][2].copy(), eq2[0][6]),
                  ReplacementTransform(eq_py[0][5].copy(), eq2[0][8]),
                  FadeIn(eq2[0][3]),
                  FadeOut(eq_py[0][0], eq_py[0][4]),
#                  gp.animate.shift(LEFT * 0.4),
                  run_time=2)
        self.wait(0.2)

        c0 = eq2[0][0:2].get_center()
        c1 = eq_py[2][0:2].get_center()
        linex1 = Line(c0 + DL * 0.3, c0 + UR * 0.3, stroke_color=RED, stroke_width=5, color=RED).set_z_index(40)
        linex2 = Line(c1 + DL * 0.3, c1 + UR * 0.3, stroke_color=RED, stroke_width=5, color=RED).set_z_index(40)
        self.play(Create(linex1), Create(linex2), run_time=0.6)
        self.wait(0.2)
        self.play(FadeOut(linex1, linex2, eq2[0][:3], eq_py[2][:3]), run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq_py[1], eq3[1]),
                  ReplacementTransform(eq_py[2][3:], eq3[2][:]),
                  ReplacementTransform(eq2[0][3:5] + eq2[0][6:8] + eq2[0][5],
                                       eq3[0][1:3] + eq3[0][3:5] + eq3[0][6]),
                  ReplacementTransform(eq2[0][7].copy(), eq3[0][6]),
                  FadeIn(eq3[0][0], eq3[0][5]),
                  FadeOut(eq2[0][8]),
                  run_time=2)
        self.wait(0.2)
        c2 = eq3[0][4].get_center()
        linex3 = Line(c2 + DL*0.25, c2 + UR*0.25, stroke_color=RED, stroke_width=5, color=RED).set_z_index(40)
        self.play(Create(linex3), run_time=0.6)
        self.wait(0.2)
        eq4_1 = eq4[1].copy().move_to(eq3[1])
        self.play(LaggedStart(AnimationGroup(FadeOut(linex3, eq3[0][3:5], eq3[1]), FadeIn(eq4_1)),
                  FadeOut(eq3[0][0], eq3[0][5]), lag_ratio=0.5), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq3[2][:] + eq3[0][6] + eq3[0][1] + eq4_1,
                                       eq4[2][:2] + eq4[2][4] + eq4[2][3] + eq4[1]),
                  ReplacementTransform(eq3[0][2], eq4[0][0]),
                  FadeIn(eq4[2][2]),
                  run_time=2)

        self.wait(0.5)


class RadiusCalc2(RadiusCalc):
    def construct(self):
        radius = config.frame_y_radius * 1.5
        cdot, surf, line, rightangle, eq = self.get_trig(radius)
        center = cdot.get_center()
        earth, mountain, wojak = self.get_earth(center, radius)
        gp = Group(earth, mountain, VGroup(cdot, surf, line, rightangle))
        gp2 = Group(eq, gp).shift(LEFT)
        wojak.shift(LEFT)

        self.add(gp2, wojak)
        self.wait(0.5)

        theta1 = 18 * DEGREES
        p0 = center + UP * radius
        p1 = center + (UP + LEFT * math.tan(theta1)) * radius
        p5 = center + (UP * math.cos(theta1) + LEFT * math.sin(theta1)) * radius
        line1 = Line(p0, p1, stroke_color=WHITE, stroke_width=5).set_z_index(20)
        line5 = Line(p5, p1, stroke_color=WHITE, stroke_width=5).set_z_index(20)
        line6 = Line(center, p5, stroke_color=LIGHT_BROWN, stroke_width=5).set_z_index(20)

        eq1 = MathTex(r'R{{\approx}}\frac{d_2^2}{2h_2}').set_z_index(30).to_edge(UR, buff=0.7)
        eq2 = MathTex(r'R{{\approx}}\frac{d_1^2}{2h_1}').set_z_index(30).next_to(eq1, DOWN)
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq2[1], coor_mask=RIGHT)
        eq3 = MathTex(r'd_1+d_2{{=}}d').set_z_index(30).next_to(eq2, DOWN).align_to(eq2, RIGHT)
        eq4 = MathTex(r'\frac{d_1^2}{2h_1}{{\approx}}\frac{d_2^2}{2h_2}').set_z_index(30)
        eq4.next_to(eq2[1], ORIGIN, submobject_to_align=eq4[1])
        eq5 = MathTex(r'd_1^2{{\approx}}\frac{h_1}{h_2}d_2^2').set_z_index(30)
        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1])
        eq6 = MathTex(r'd_1{{\approx}}\sqrt{\frac{h_1}{h_2} }d_2').set_z_index(30)
        eq6.next_to(eq5[1], ORIGIN, submobject_to_align=eq6[1]).to_edge(RIGHT, buff=0.2)
        eq7 = MathTex(r'd_2+\sqrt{\frac{h_1}{h_2} }d_2{{\approx}} d').set_z_index(30).to_edge(RIGHT, buff=0.2)
        eq7.next_to(eq3[1], ORIGIN, submobject_to_align=eq7[1], coor_mask=UP)
        eq8 = MathTex(r'd_2{{\approx}}\frac{d}{1+\sqrt{\frac{h_1}{h_2} }').set_z_index(30).next_to(eq1, DOWN).to_edge(RIGHT, buff=0.2)

        p0_1 = cdot.get_center() + UP * radius
        line1_1 = Line(p0_1, p0, stroke_color=WHITE, stroke_width=5).set_z_index(20)
        line1_2 = Line(p0_1, p1, stroke_color=WHITE, stroke_width=5).set_z_index(20)
        self.play(gp2.animate.shift(RIGHT), wojak.animate.next_to(p1, LEFT, buff=0.33),
                  Create(line1_1), Create(line1_2), FadeOut(eq[:2],
                                                            target_position=eq[:2].get_center() + RIGHT), run_time=1.5)
        self.wait(0.5)

        rangle = RightAngle(line[0], line1, length=0.5, stroke_color=WHITE, stroke_width=5, quadrant=(-1, 1)).set_z_index(20)
        eq_d1 = MathTex(r'd_1')[0].set_z_index(30).next_to(line1, UP, buff=0.2)
        eq_d2 = MathTex(r'd_2')[0].set_z_index(30).next_to(line[1], UP, buff=0.2)
        eq_R1 = MathTex(r'R')[0].set_z_index(30).move_to(line6).shift(LEFT * 0.3)
        eq_h1 = MathTex(r'h_1', stroke_width=1.5)[0].set_z_index(30).move_to(line5).shift(LEFT * 0.2)
        eq_h2 = MathTex(r'h_2', stroke_width=1.5)[0].set_z_index(30).move_to(line[2]).shift(DR * 0.25)

        tmpdot = Dot(center).set_opacity(0)

        def f():
            to = tmpdot.get_center()
            v = to - center
            if v[0] * v[0] + v[1] * v[1] <= radius * radius:
                return Line(center, to, stroke_color=LIGHT_BROWN, stroke_width=5).set_z_index(20)
            else:
                return VGroup(line6, Line(p5, to, stroke_color=WHITE, stroke_width=5).set_z_index(20))

        radial = always_redraw(f)
        self.add(radial)
        self.play(tmpdot.animate.move_to(p1), FadeIn(eq_R1), run_time=1.8)
        self.remove(radial)
        self.add(line5, line6)

        self.wait(0.2)
        self.play(Create(rangle), run_time=0.8)
        self.wait(0.2)
        self.play(FadeIn(eq_d1, eq_d2), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq_h1, eq_h2), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq1), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(eq3), run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq1[2].copy(), eq4[2]),
                  ReplacementTransform(eq2[2], eq4[0]),
                  ReplacementTransform(eq2[1], eq4[1]),
                  FadeOut(eq2[0]),
                  run_time=2)
        self.wait(0.2)
        c1 = eq4[0][4].get_center()
        c2 = eq4[2][4].get_center()
        linex1 = Line(c1 + DL*0.2, c1 + UR*0.2, stroke_color=RED, stroke_width=5).set_z_index(40)
        linex2 = Line(c2 + DL*0.2, c2 + UR*0.2, stroke_color=RED, stroke_width=5).set_z_index(40)
        self.play(Create(linex1), Create(linex2), run_time=0.5)
        self.wait(0.2)
        self.play(FadeOut(linex1, linex2, eq4[0][4], eq4[2][4]), run_time=0.6)
        self.wait(0.2)
        self.play(ReplacementTransform(eq4[0][:3] + eq4[0][5:] + eq4[1] + eq4[2][:3] + eq4[2][3] + eq4[2][5:],
                                       eq5[0][:] + eq5[2][:2] + eq5[1] + eq5[2][5:8] + eq5[2][2] + eq5[2][3:5]),
                  FadeOut(eq4[0][3], target_position=eq5[0].get_bottom()),
                  run_time=2)
        self.wait(0.2)
        self.play(FadeOut(eq5[0][1], eq5[2][6]),
                  ReplacementTransform(eq5[1][:] + eq5[0][0] + eq5[0][2] + eq5[2][5] + eq5[2][7] + eq5[2][:5],
                                       eq6[1][:] + eq6[0][0] + eq6[0][1] + eq6[2][7] + eq6[2][8] + eq6[2][2:7]),
                  FadeIn(eq6[2][:2]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq3[0][3:5] + eq3[0][2] + eq3[2],
                                       eq7[0][:2] + eq7[0][2] + eq7[2]),
                  abra.fade_replace(eq3[1], eq7[1]),
                  eq3[0][:2].animate.move_to(eq7[0][3:], coor_mask=RIGHT).move_to(eq7[0][10:], coor_mask=UP),
                  run_time=1.5)
        self.play(ReplacementTransform(eq6[2][:], eq7[0][3:]),
                  FadeOut(eq3[0][:2], eq6[:2]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(eq7.animate.next_to(eq8[1], ORIGIN, submobject_to_align=eq7[1], coor_mask=UP), run_time=1)
        self.play(ReplacementTransform(eq7[0][:2] + eq7[0][2:10] + eq7[2][0] + eq7[1],
                                       eq8[0][:] + eq8[2][3:] + eq8[2][0] + eq8[1]),
                  ReplacementTransform(eq7[0][10:12], eq8[0][:]),
                  FadeIn(eq8[2][2], target_position=eq7[0][0].get_left()),
                  FadeIn(eq8[2][1]),
                  run_time=2)
        self.wait(0.5)
        eq9 = MathTex(r'R {{{{\approx}}}} {}'.format(radius_str1)).set_z_index(30)
        eq9.move_to(eq8).to_edge(RIGHT, buff=0.8)

        eq10 = MathTex(r'R{{\approx}} \frac{' + radius_str1 + r'}{\left(1+\sqrt{\frac{h_1}{h_2} }\right)^2').set_z_index(30)
        eq10.next_to(eq9[1], ORIGIN, submobject_to_align=eq10[1]).to_edge(RIGHT, buff=0.2)

        eq11 = MathTex(r'R{{\approx}} \frac{' + radius_str1 + r'}{\left(1+\sqrt{\frac{' + me_str +
                       r'}{' + height_str + r'} }\right)^2').set_z_index(30)
        eq11.next_to(eq9[1], ORIGIN, submobject_to_align=eq11[1]).to_edge(RIGHT, buff=0.2)

        eq12 = MathTex(r'R{{\approx}} \frac{' + radius_str1 + r'}{' + adjust1_str + r'}').set_z_index(30)
        eq12.next_to(eq9[1], ORIGIN, submobject_to_align=eq12[1]).to_edge(RIGHT, buff=1.2)

        eq13 = MathTex(r'R{{\approx}}' + radius_str2 + r'\,{\rm km}')
        eq13.next_to(eq9[1], ORIGIN, submobject_to_align=eq13[1]).next_to(eq12[2].get_right(), LEFT, submobject_to_align=eq13[2][-3], coor_mask=RIGHT, buff=0)

        eq14 = MathTex(r'R_E{{{{=}}}} {}\,{{\rm km}}'.format(radiusE_str)).set_opacity(30)
        eq14.next_to(eq13, DOWN, buff=0.5).align_to(eq14, LEFT)
        self.play(FadeOut(eq1, eq8), FadeIn(eq9[:3]), run_time=1.5)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(eq9[2][:] + eq9[:2],
                                       eq10[2][:4] + eq10[:2]),
                  FadeIn(eq10[2][4:]), lag_ratio=0.4),
                  run_time=2)
        self.wait(0.2)
        self.play(ReplacementTransform(eq10[:2] + eq10[2][:10] + eq10[2][12] + eq10[2][15:],
                                       eq11[:2] + eq11[2][:10] + eq11[2][11] + eq11[2][15:]),
                  abra.fade_replace(eq10[2][10:12], eq11[2][10:11]),
                  abra.fade_replace(eq10[2][13:15], eq11[2][12:15]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq11[:2] + eq11[2][:5],
                                       eq12[:2] + eq12[2][:5]),
                  abra.fade_replace(eq11[2][5:], eq12[2][5:]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq12[:2],
                                       eq13[:2]),
                  abra.fade_replace(eq12[2][:4], eq13[2][:4]),
                  FadeOut(eq12[2][4:]),
                  FadeIn(eq13[2][4:]),
                  run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(eq14), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(eq13, eq14), run_time=1)
        self.wait(0.1)


class Refraction(RadiusCalc):
    def construct(self):
        radius = config.frame_y_radius * 1.5
        cdot, surf, line, rightangle, eq = self.get_trig(radius)
        center = cdot.get_center()
        earth, mountain, wojak = self.get_earth(center, radius)

        theta1 = 18 * DEGREES
        p0 = center + UP * radius
        p1 = center + (UP + LEFT * math.tan(theta1)) * radius
        p5 = center + (UP * math.cos(theta1) + LEFT * math.sin(theta1)) * radius
        line1 = Line(p0, p1, stroke_color=WHITE, stroke_width=5).set_z_index(20)
        line5 = Line(p5, p1, stroke_color=WHITE, stroke_width=5).set_z_index(20)
        line6 = Line(center, p5, stroke_color=LIGHT_BROWN, stroke_width=5).set_z_index(20)
        rangle = RightAngle(line[0], line1, length=0.5, stroke_color=WHITE, stroke_width=5, quadrant=(-1, 1)).set_z_index(20)
        eq_R1 = MathTex(r'R')[0].set_z_index(30).move_to(line6).shift(LEFT * 0.3)
        eq_d1 = MathTex(r'd_1')[0].set_z_index(30).next_to(line1, UP, buff=0.2)
        eq_d2 = MathTex(r'd_2')[0].set_z_index(30).next_to(line[1], UP, buff=0.2)
        eq_h1 = MathTex(r'h_1', stroke_width=1.5)[0].set_z_index(30).move_to(line5).shift(LEFT * 0.2)
        eq_h2 = MathTex(r'h_2', stroke_width=1.5)[0].set_z_index(30).move_to(line[2]).shift(DR * 0.25)

        wojak.next_to(p1, LEFT, buff=0.33)

        self.add(earth, mountain, wojak, cdot, surf, line, rightangle, line1, line5, line6, rangle,
                 eq[2:], eq_R1, eq_d1, eq_d2, eq_h1, eq_h2)

        self.wait(0.5)
        col1 = BLUE_D
        col2 = ManimColor(col1.to_rgb() * 0.8)
        col3 = ManimColor(col1.to_rgb() * 0.6)
        col4 = ManimColor(col1.to_rgb() * 0.4)
        col5 = ManimColor(col1.to_rgb() * 0.2)
        w1 = 0.35
        a1 = Arc(radius=radius+w1/2, arc_center=center, start_angle=184*DEGREES, angle=-200*DEGREES, color=col1,
                 stroke_width=w1 * 100).set_z_index(0.9)
        a2 = Arc(radius=radius+w1*3/2, arc_center=center, start_angle=184*DEGREES, angle=-200*DEGREES, color=col2,
                 stroke_width=w1 * 100).set_z_index(0.8)
        a3 = Arc(radius=radius+w1*5/2, arc_center=center, start_angle=184*DEGREES, angle=-200*DEGREES, color=col3,
                 stroke_width=w1 * 100).set_z_index(0.7)
        a4 = Arc(radius=radius+w1*7/2, arc_center=center, start_angle=184*DEGREES, angle=-200*DEGREES, color=col4,
                 stroke_width=w1 * 100).set_z_index(0.6)
        a5 = Arc(radius=radius+w1*9/2, arc_center=center, start_angle=184*DEGREES, angle=-200*DEGREES, color=col5,
                 stroke_width=w1 * 100).set_z_index(0.5)
        self.play(FadeIn(a1), run_time=2)
        self.wait(0.5)
        self.play(LaggedStart(FadeIn(a2), FadeIn(a3), FadeIn(a4), FadeIn(a5), lag_ratio=0.2), run_time=2)

        self.wait(0.2)
        theta = 10 * DEGREES
        p_l = p1
        p_r = line[1].get_end()
        theta_l = -theta1
        theta_r = 33*DEGREES
        theta_0 = 10*DEGREES

        def curve_func(theta_0):
            def f(theta):
                x1 = 1/math.cos(theta)
                c = math.cos(theta_0)
                s = math.sin(theta_0)
                x2 = (1-1/c) * (theta-theta_l)/(theta_0-theta_l)
                x3 = (theta-theta_l)*(theta_0-theta)
                dx1dt = s/c/c
                dx2dt = (1-1/c)/(theta_0-theta_l)
                dx3dt = theta_l - theta_0

                return center + (UP * math.cos(theta) + RIGHT * math.sin(theta)) * (x1+x2 - x3*(dx1dt+dx2dt)/dx3dt) * radius

            return f

        theta_val = ValueTracker(0.0)
        lines = VGroup(line[0], eq[2], rightangle, rangle)
        lines_1 = lines.copy()
        lines.set_opacity(0)
        line[0].set_opacity(0.3)

        def g():
            theta_0 = theta_val.get_value()
            f = curve_func(theta_0)
            curved = ParametricFunction(f, (theta_l, theta_r), dt=0.01, stroke_width=5, stroke_color=WHITE)\
                .set_z_index(40)

            return VGroup(curved, lines_1.copy().rotate(-theta_0, about_point=center))

        line1.set_z_index(25).set_opacity(0.5)
        line[1].set_z_index(25).set_opacity(0.5)
        curved = always_redraw(g)

        self.add(curved)
        self.play(theta_val.animate.set_value(8 * DEGREES), run_time=1.5)
        self.remove(curved)
        curved = g()
        self.add(curved)


#        a2 = Arc(radius=radius + w1, arc_center=center, start_angle=184*DEGREES, angle=-188*DEGREES, color=BLUE, stroke_width=5).set_z_index(10)

        self.wait(0.5)


class RefractionCalc(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        eq1 = MathTex(r't{{=}}(R+h)\frac{\theta}{c}'
                      r'{{=}}(R+h)\frac{n\theta}{c_0}'
                      r'{{=}}(R+h)(1-ah)\frac{n_0\theta}{c_0}'
                      r'{{\approx}}(R+h-Rah)\frac{n_0\theta}{c_0}'
                      r'{{\approx}}\left(\frac{R}{1-Ra}+h\right)(1-Ra)\frac{n_0\theta}{c_0}')
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
        eq1[5:7].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[5], coor_mask=RIGHT)
        eq1[7:9].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[7], coor_mask=RIGHT)
        eq1[9:11].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[9], coor_mask=RIGHT)
        eq1.to_edge(UR)

        eq_n = MathTex(r'n{{=}}n_0(1-ah)').next_to(eq1[:4], DOWN)

        eq_R = MathTex(r'R^\prime{{=}}\frac{R}{1-Ra}').next_to(eq_n, DOWN)
        eqR2 = MathTex(r'R^\prime(1-Ra){{=}}R')
        eqR2.next_to(eq_R[1], ORIGIN, submobject_to_align=eqR2[1]).move_to(eq_R, coor_mask=RIGHT)
        eqR3 = MathTex(r'R^\prime-R^\prime Ra{{=}}R')
        eqR3.next_to(eqR2[1], ORIGIN, submobject_to_align=eqR3[1])
        eqR4 = MathTex(r'R+R^\prime Ra{{=}}R^\prime')
        eqR4.next_to(eqR3[1], ORIGIN, submobject_to_align=eqR4[1]).align_to(eq_n, RIGHT)
        eqR5 = MathTex(r'R(1+R^\prime a){{=}}R^\prime')
        eqR5.next_to(eqR3[1], ORIGIN, submobject_to_align=eqR5[1]).align_to(eq_n, RIGHT)
        eqR6 = MathTex(r'R{{=}}\frac{R^\prime}{1+R^\prime a}')
        eqR6.next_to(eqR3[1], ORIGIN, submobject_to_align=eqR6[1]).move_to(eq_n, coor_mask=RIGHT)

        self.add(eq1[:3])
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(eq1[2][:5] + eq1[2][5:],
                                       eq1[4][:5] + eq1[4][6:9]),
                  FadeIn(eq1[4][5], eq1[4][9]), lag_ratio=0.3),
                  run_time=1.5)

        self.wait(0.2)
        self.play(FadeIn(eq_n), run_time=1)
        self.wait(0.2)
        postmp = eq1[:2].get_center()
        eq1.next_to(eq1[4].get_right()+RIGHT*0.2, LEFT, submobject_to_align=eq1[6], coor_mask=RIGHT, buff=0)
        pos = eq1[:2].get_center()
        eq1[:5].shift(postmp-pos)
        self.play(ReplacementTransform(eq1[4][:5] + eq1[4][5] + eq1[4][6:],
                                       eq1[6][:5] + eq1[6][11] + eq1[6][13:]),
                  eq1[:2].animate.move_to(pos),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eq_n[2][2:].copy(), eq1[6][5:11]),
                  FadeIn(eq1[6][12]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq1[6][:4] + eq1[6][7] + eq1[6][1].copy() + eq1[6][8:10] + eq1[6][4],
                                       eq1[8][:4] + eq1[8][4] + eq1[8][5] + eq1[8][6:8] + eq1[8][8]),
                  ReplacementTransform(eq1[6][5], eq1[8][0]),
                  ReplacementTransform(eq1[6][10], eq1[8][8]),
                  abra.fade_replace(eq1[1], eq1[7]),
                  FadeOut(eq1[6][6], target_position=eq1[8][1]),
                  ReplacementTransform(eq1[6][11:], eq1[8][9:]),
                  run_time=1.7)
        self.wait(0.2)
        postmp = (eq1[:1] + eq1[7]).get_center()
        eq1.next_to(eq1[8].get_right()+RIGHT*0.2, LEFT, submobject_to_align=eq1[10], coor_mask=RIGHT, buff=0)
        pos = (eq1[:1] + eq1[7]).get_center()
        (eq1[:1] + eq1[7:9]).shift(postmp-pos)

        self.play(ReplacementTransform(eq1[8][:2] + eq1[8][4:7] + eq1[8][2:4],
                                       eq1[10][:2] + eq1[10][4:7] + eq1[10][7:9]),
                  ReplacementTransform(eq1[8][7:9], eq1[10][8:10]),
                  ReplacementTransform(eq1[8][9:], eq1[10][16:]),
                  ReplacementTransform(eq1[8][4:7].copy(), eq1[10][12:15]),
                  FadeIn(eq1[10][2]),
                  FadeIn(eq1[10][3], target_position=eq1[8][3]),
                  FadeIn(eq1[10][11], target_position=eq1[8][3]),
                  FadeIn(eq1[10][10], eq1[10][15]),
                  (eq1[:1] + eq1[7]).animate.move_to(pos),
                  run_time=2
        )
        self.wait(0.2)
        eq_R1 = eq_R[0].copy()
        self.play(FadeIn(eq_R), run_time=1)
        self.wait(0.2)
        self.play(FadeOut(eq1[10][1:7]),
                  eq_R1.animate.next_to(eq1[10][13], ORIGIN, submobject_to_align=eq_R1[0]).move_to(eq1[10][1:7], coor_mask=RIGHT),
                  run_time=2)
        self.wait(0.2)
        self.play(FadeOut(eq1[10][0], eq1[10][7:], eq1[7], eq1[0], eq_R1), run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eq_R[0][:2] + eq_R[1] + eq_R[2][0] + eq_R[2][2:],
                                       eqR2[0][:2] + eqR2[1] + eqR2[2][0] + eqR2[0][3:7]),
                  FadeOut(eq_R[2][1]),
                  FadeIn(eqR2[0][2], target_position=eq_R[2][2].get_left()),
                  FadeIn(eqR2[0][-1], target_position=eq_R[2][-1]),
                  run_time=1.5)
        self.wait(0.2)
        self.play(ReplacementTransform(eqR2[0][:2] + eqR2[0][:2].copy() + eqR2[0][4] + eqR2[0][5:7] + eqR2[1:],
                                       eqR3[0][:2] + eqR3[0][3:5] + eqR3[0][2] + eqR3[0][5:7] + eqR3[1:]),
                  FadeOut(eqR2[0][2], target_position=eqR3[0][0].get_left()),
                  FadeOut(eqR2[0][-1], target_position=eqR3[0][-1].get_right()),
                  FadeOut(eqR2[0][3], target_position=eqR3[0][0].get_right()),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eqR3[0][:2] + eqR3[2][0] + eqR3[0][3:] + eqR3[1],
                                       eqR4[2][:] + eqR4[0][0] + eqR4[0][2:] + eqR4[1]),
                  abra.fade_replace(eqR3[0][2], eqR4[0][1]),
                  run_time=2)
        self.wait(0.2)
        self.play(ReplacementTransform(eqR4[0][:1] + eqR4[0][1:4] + eqR4[0][5] + eqR4[1:],
                                       eqR5[0][:1] + eqR5[0][3:6] + eqR5[0][6] + eqR5[1:]),
                  ReplacementTransform(eqR4[0][4], eqR5[0][0]),
                  FadeIn(eqR5[0][2], target_position=eqR4[0][0]),
                  FadeIn(eqR5[0][1], target_position=eqR4[0][0].get_left()),
                  FadeIn(eqR5[0][-1], target_position=eqR4[0][-1].get_right()),
                  run_time=1)
        self.wait(0.2)
        self.play(ReplacementTransform(eqR5[0][:1] + eqR5[0][2:7] + eqR5[1] + eqR5[2][:],
                                       eqR6[0][:1] + eqR6[2][3:8] + eqR6[1] + eqR6[2][:2]),
                  FadeOut(eqR5[0][1], target_position=eqR6[2][3:8].get_left()),
                  FadeOut(eqR5[0][-1], target_position=eqR6[2][3:8].get_right()),
                  FadeIn(eqR6[2][2]),
                  run_time=2)


        self.wait(0.5)


class Measure(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = ManimColor(WHITE.to_rgb()*0.3)
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        eq1 = MathTex(r'd={}\,\rm km'.format(distance_str)).set_z_index(10).to_edge(UL)
        eq2 = MathTex(r'h={}\,\rm m'.format(height_str)).set_z_index(10).next_to(eq1, DOWN).align_to(eq1, LEFT)

        box = SurroundingRectangle(eq1, corner_radius=0.1, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0)
        box2 = SurroundingRectangle(VGroup(eq1, eq2), corner_radius=0.1, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0)
        self.add(box, eq1)
        self.wait(0.2)
        self.play(LaggedStart(ReplacementTransform(box, box2), FadeIn(eq2), lag_ratio=0.4), run_time=1.5)
        self.wait(0.5)


class Measure2(Measure):
    def construct(self):
        eq1 = MathTex(r'd={}\,\rm km'.format(distance_str)).set_z_index(10)
        eq2 = MathTex(r'h_2={}\,\rm m'.format(height_str)).set_z_index(10).next_to(eq1, DOWN).align_to(eq1, LEFT)
#        eq2.next_to(eq1[0][1], ORIGIN, submobject_to_align=eq2[0][2], coor_mask=RIGHT)
        eq3 = MathTex(r'h_1={}\,\rm m'.format(me_str)).set_z_index(10).next_to(eq2, DOWN).align_to(eq1, LEFT)
#        eq3.next_to(eq1[0][1], ORIGIN, submobject_to_align=eq3[0][2], coor_mask=RIGHT)
        box = SurroundingRectangle(VGroup(eq1, eq2, eq3).to_edge(DL), stroke_opacity=0, fill_color=BLACK, fill_opacity=0.7,
                                   corner_radius=0.1)
        self.add(box, eq1, eq2)
        self.wait(0.5)
        self.play(FadeIn(eq3), run_time=1)
        self.wait(0.5)

class RadiusNumbers1(Scene):
    def construct(self):
        eq2 = MathTex(r'R_E{{{{=}}}} {}\,{{\rm km}}'.format(radiusE_str))
        eq1 = MathTex(r'R{{\approx}}\frac{d^2}{2h}' +
                      r'{{{{\approx}}}}\frac{{ {}^2}}{{2\cdot 0.{} }}'.format(distance_str, height_str) +
                      r'{{{{\approx}}}} {}\,{{\rm km}}'.format(radius_str1))
        eq1[3:5].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[3], coor_mask=RIGHT)
        eq1[5:7].next_to(eq1[1], ORIGIN, submobject_to_align=eq1[5], coor_mask=RIGHT)
        eq1.next_to(eq2, UP, submobject_to_align=eq1[0], buff=0.5).align_to(eq2, LEFT)
        self.add(eq1[:3])
        self.wait(0.2)
        self.play(ReplacementTransform(eq1[2][1:4],
                                       eq1[4][5:8]),
                  abra.fade_replace(eq1[2][0], eq1[4][:5]),
                  abra.fade_replace(eq1[2][4], eq1[4][9:]),
                  FadeIn(eq1[4][8], target_position=eq1[2][3].get_right()),
                  run_time=1.5)
        self.wait(0.2)
        self.play(FadeOut(eq1[4]), FadeIn(eq1[6]), run_time=2)
        self.wait(0.5)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.5)


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        RadiusCalc().render()
