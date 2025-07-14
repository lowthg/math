from manim import *
import numpy as np
import math
import sys
import scipy as sp
from networkx.classes import edges
from sorcery import switch

sys.path.append('../../')
import manimhelper as mh


class Hilbert(Scene):
    def construct(self):
        fs1 = 120
        fs2 = 80
        fs3 = 60
        eq1 = MathTex(r'\mathcal H', font_size=200)[0]
        eq2 = MathTex(r'\Psi\in\mathcal H', font_size=fs1)[0]
        mh.align_sub(eq2, eq2[-1], eq1[-1], coor_mask = UP).shift(UP*0.2)
        eq3 = MathTex(r'\Phi,\Psi\in\mathcal H', font_size=fs1)[0]
        mh.align_sub(eq3, eq3[-1], eq2[-1], coor_mask = UP)
        eq4 = MathTex(r'\Phi + \Psi\in\mathcal H', font_size=fs1)[0]
        eq4.next_to(eq3, DOWN, buff=0.35)
        eq5 = MathTex(r'a,b\in\mathbb C', font_size=fs1)[0]
        mh.align_sub(eq5, eq5[-2], eq3[-2]).next_to(eq3, RIGHT, coor_mask=RIGHT, buff=1)
        eq3_1 = eq3.copy()
        VGroup(eq3_1, eq5).move_to(ORIGIN, coor_mask=RIGHT)
        eq6 = MathTex(r'a\Phi + b\Psi\in\mathcal H', font_size=fs1)[0]
        mh.align_sub(eq6, eq6[-2], eq4[-2], coor_mask=UP)
        eq7 = MathTex(r'\langle\Phi\vert\Psi\rangle\in\mathbb C', font_size=fs1)[0]
        mh.align_sub(eq7, eq7[-2], eq3[-2], coor_mask=UP)
        eq10 = MathTex(r'\langle\Phi\vert a\Psi_1+b\Psi_2\rangle', r'=',
                       r'a\langle\Phi\vert\Psi_1\rangle + b\langle\Phi\vert\Psi_2\rangle',
                       font_size=fs2).set_z_index(1)
        eq11 = Tex(r'\underline{Linear}', font_size=fs3, color=BLUE).next_to(eq10, UP, buff=0.35)
        eq11[0][-1].set_z_index(0.9).next_to(eq11[0][0], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq11.next_to(eq10[0], UP).align_to(eq10, LEFT)

        eq12 = MathTex(r'\langle\Psi\vert\Phi\rangle', r'=', r'\overline{\langle\Phi\vert\Psi\rangle}', font_size=fs2)
        mh.align_sub(eq12, eq12[1], eq10[1])
        eq13 = Tex(r'\underline{Conjugate symmetry}', font_size=fs3, color=BLUE).next_to(eq10, UP, buff=0.35)
        eq13[0][-1].set_z_index(0.9).next_to(eq13[0][1], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq13.align_to(eq11, LEFT).move_to(eq12, coor_mask=UP)
        eq12.next_to(eq13, RIGHT, coor_mask=RIGHT, buff=0.35)

        eq14 = MathTex(r'\langle a\Phi_1+b\Phi_2\vert\Psi\rangle', r'=',
                       r'\overline{\langle \Psi\vert a\Phi_1+b\Phi_2\rangle}', font_size=fs2)
        eq15 = Tex(r'\underline{Conjugate linear}', font_size=fs3, color=BLUE).next_to(eq14, UP, buff=0.35)
        eq15[0][-1].set_z_index(0.9).next_to(eq15[0][1], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq14.align_to(eq10, LEFT)
        eq15.next_to(eq14[0], UP).align_to(eq10, LEFT)
        VGroup(eq14, eq15).next_to(eq13, DOWN, buff=0.5, coor_mask=UP)
        eq16 = MathTex(r'\langle a\Phi_1+b\Phi_2\vert\Psi\rangle', r'=',
                       r'\overline{a\langle \Psi\vert\Phi_1\rangle+b\langle \Psi\vert\Phi_2\rangle}', font_size=fs2)
        mh.align_sub(eq16, eq16[1], eq14[1])
        eq17 = MathTex(r'\langle a\Phi_1+b\Phi_2\vert\Psi\rangle', r'=',
                       r'\overline{a}\langle\Phi_1\vert\Psi\rangle+\overline{b}\langle\Phi_2\vert\Psi\rangle}', font_size=fs2)
        mh.align_sub(eq17, eq17[1], eq16[1])
        eq18 = Tex(r'(conjugate symmetry)')
        eq18[0][1:-1].set_color(RED)
        eq18.next_to(eq14[2], DOWN)
        eq19 = Tex(r'(linearity)')
        eq19[0][1:-1].set_color(RED)
        eq19.next_to(eq14[2], DOWN)
        mh.align_sub(eq19, eq19[0][0], eq18[0][0], coor_mask=UP)

        eq20 = MathTex(r'\langle\Psi\vert\Psi\rangle', r'>', r'0', r'\ \ \ {\rm if\ }\Psi\not=0', font_size=fs2)
        eq20.next_to(eq14, DOWN, buff=0.35)
        #mh.align_sub(eq12, eq12[1], eq10[1])
        eq21 = Tex(r'\underline{Positive}', font_size=fs3, color=BLUE)
        eq21[0][-1].set_z_index(0.9).next_to(eq21[0][1], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq21.align_to(eq11, LEFT).move_to(eq20, coor_mask=UP)
        eq20.next_to(eq21, RIGHT, coor_mask=RIGHT, buff=0.35)

        # eq10.shift(UP)
        # mh.align_sub(eq10, eq10[0][1], eq3[1], coor_mask=UP)

        self.wait(0.2)
        self.play(FadeIn(eq1, rate_func=linear))
        self.wait(0.1)
        self.play(mh.rtransform(eq1[-1], eq2[-1]),
                  FadeIn(eq2[:2], shift=(eq2[-1].get_left()-eq1[-1].get_left()) * RIGHT),
                  run_time=1.2)
        self.wait(0.1)
        self.play(mh.rtransform(eq2[:], eq3[2:]),
                  FadeIn(eq3[:2], shift=mh.diff(eq2[0], eq3[2])),
                  run_time=0.8)
        self.wait(0.1)
        self.play(mh.rtransform(eq3[0].copy(), eq4[0], eq3[2:].copy(), eq4[2:]),
                  FadeIn(eq4[1], target_position=eq3[:3]),
                  run_time=1.5)
        self.wait(0.1)
        eq3_2 = eq3.copy()
        self.play(LaggedStart(ReplacementTransform(eq3, eq3_1),
                              AnimationGroup(FadeIn(eq5),
                  mh.rtransform(eq4[:2], eq6[1:3], eq4[2:], eq6[4:]),
                  FadeIn(eq6[0], target_position=eq5[0]),
                  FadeIn(eq6[3], target_position=eq5[2])),
                              lag_ratio=0.3),
                  run_time=2)
        eq3 = eq3_2
        self.wait(0.1)
        self.play(FadeOut(eq6, rate_func=linear),
                  ReplacementTransform(eq3_1, eq3),
                  FadeOut(eq5),
                  run_time=1.5)
        self.wait(0.1)
        self.play(mh.rtransform(eq3[0].copy(), eq7[1], eq3[2].copy(), eq7[3], eq3[-2].copy(), eq7[-2]),
                  FadeIn(eq7[0], shift=mh.diff(eq3[0], eq7[1])),
                  FadeIn(eq7[4], shift=mh.diff(eq3[2], eq7[3])),
                  FadeIn(eq7[2], target_position=eq3[:3]),
                  FadeIn(eq7[-1], target_position=eq3[-1]),
                  eq3.animate.shift(UP*2),
                  run_time=1.5)
        self.wait(0.1)
        eq9 = eq10[0]
        # self.play(mh.rtransform(eq3[:2], eq8[:2], eq3[3:], eq8[7:], eq3[2], eq8[2],
        #                         eq3[2].copy(), eq8[5],
        #                         eq7[:3], eq9[:3], eq7[3], eq9[4],
        #                         eq7[3].copy(), eq9[8], eq7[4], eq9[10]),
        #           FadeIn(eq8[3:5], shift=mh.diff(eq3[2], eq8[2])),
        #           FadeIn(eq8[6], shift=mh.diff(eq3[2], eq8[5])),
        #           FadeIn(eq9[3], eq9[5], shift=mh.diff(eq7[3], eq9[4])),
        #           FadeIn(eq9[7], eq9[9], shift=mh.diff(eq7[3], eq9[8])),
        #           FadeIn(eq9[6], target_position=eq7[3]),
        #           FadeOut(eq7[-2:]),
        #           run_time=1)
        self.play(mh.rtransform(eq7[:3], eq9[:3], eq7[3], eq9[4],
                                eq7[3].copy(), eq9[8], eq7[4], eq9[10]),
                  FadeIn(eq9[3], eq9[5], shift=mh.diff(eq7[3], eq9[4])),
                  FadeIn(eq9[7], eq9[9], shift=mh.diff(eq7[3], eq9[8])),
                  FadeIn(eq9[6], target_position=eq7[3]),
                  FadeOut(eq7[-2:]),
                  FadeOut(eq3),
                  FadeIn(eq11),
                  run_time=2)
        self.wait(0.1)
        #self.play(mh.rtransform(eq9, eq10[0]))
        eq9_1 = eq10[0].copy()
        self.play(mh.rtransform(eq9_1[:3], eq10[2][1:4], eq9_1[:3].copy(), eq10[2][9:12],
                                eq9_1[3], eq10[2][0], eq9_1[4:6], eq10[2][4:6],
                                eq9_1[7], eq10[2][8], eq9_1[8:11], eq10[2][12:15],
                                eq9_1[10].copy(), eq10[2][6], eq9_1[6], eq10[2][7]),
                  FadeIn(eq10[1]),
                  run_time=1.8)

        self.wait(0.1)
        self.play(VGroup(eq10, eq11).animate.next_to(eq12, UP, buff=0.35, coor_mask=UP),
                  FadeIn(eq12[0], eq13),
                  run_time=1.5)
        self.wait(0.1)
        eq12_1 = eq12[0].copy()
        self.play(mh.rtransform(eq12_1[0], eq12[2][1], eq12_1[1], eq12[2][4], eq12_1[2], eq12[2][3],
                                eq12_1[3], eq12[2][2], eq12_1[4], eq12[2][5]),
                  FadeIn(eq12[1], eq12[2][0], shift=mh.diff(eq12_1[0], eq12[2][1])),
                  run_time=1.6)
        self.wait(0.1)
        self.play(FadeIn(eq14[0], eq15),
                  run_time=1)
        self.wait(0.1)
        eq14_1 = eq14[0].copy()
        self.play(mh.rtransform(eq14_1[0], eq14[2][1], eq14_1[1:8], eq14[2][4:11],
                                eq14_1[8], eq14[2][3], eq14_1[9], eq14[2][2],
                                eq14_1[10], eq14[2][11]),
                  FadeIn(eq14[1], eq14[2][0], shift=mh.diff(eq14_1[0], eq14[2][1])),
                  FadeIn(eq18),
                  run_time=1.8)
        self.play(mh.rtransform(eq14[:2], eq16[:2], eq14[2][0], eq16[2][0],
                                eq14[2][1:4], eq16[2][2:5], eq14[2][4], eq16[2][1],
                                eq14[2][5:7], eq16[2][5:7], eq14[2][7:9], eq16[2][8:10],
                                eq14[2][9:12], eq16[2][13:16],
                                eq14[2][11].copy(), eq16[2][7], eq14[2][1:4].copy(), eq16[2][10:13]),
                  FadeOut(eq18, rate_func=rush_from),
                  FadeIn(eq19, rate_func=rush_from),
                  run_time=2)
        self.play(mh.rtransform(eq16[:2], eq17[:2], eq16[2][1:3], eq17[2][1:3],
                                eq16[2][3], eq17[2][6], eq16[2][4], eq17[2][5],
                                eq16[2][5:7], eq17[2][3:5], eq16[2][7:9], eq17[2][7:9],
                                eq16[2][9:11], eq17[2][10:12], eq16[2][11], eq17[2][15],
                                eq16[2][12], eq17[2][14], eq16[2][13:15], eq17[2][12:14],
                                eq16[2][15], eq17[2][16]),
                  FadeOut(eq16[2][0]),
                  mh.rtransform(eq17[2][0].copy().move_to(eq16[2][0], coor_mask=UP), eq17[2][0],
                                eq17[2][9].copy().move_to(eq16[2][0], coor_mask=UP), eq17[2][9]),
                  FadeIn(eq18, rate_func=rush_from),
                  FadeOut(eq19, rate_func=rush_from),
                  run_time=1.8)
        self.play(FadeOut(eq18), run_time=0.6)
        self.wait(0.1)
        self.play(FadeIn(eq20, eq21))
        self.wait(0.1)
        eq22 = MathTex(r'\lVert\Psi\rVert', r'=', r'\sqrt{\langle\Psi\vert\Psi\rangle}', font_size=fs2)
        eq22.to_edge(DOWN, buff=0.35).align_to(eq20, LEFT)
        eq23 = Tex(r'\underline{Norm}', font_size=fs3, color=BLUE)
        eq23[0][-1].set_z_index(0.9).next_to(eq23[0][1], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq23.align_to(eq11, LEFT).move_to(eq22, coor_mask=UP)
        # eq20.next_to(eq21, RIGHT, coor_mask=RIGHT, buff=0.35)


        self.play(VGroup(eq10, eq11, eq12, eq13, eq15, eq17, eq20, eq21).animate.to_edge(UP, buff=0.35),
                  FadeIn(eq22, eq23))

        self.wait()

class Pdefinition(Scene):
    box_op = 0.7
    def __init__(self, *args, **kwargs):
        if not config.transparent:
            config.background_color = GREY
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        self.create_eqs(True)

    def create_eqs(self, anim=False)->VGroup:
        fs = DEFAULT_FONT_SIZE * 0.9
        eq3 = MathTex(r'P(A)', r'=', r'\langle\Psi\vert A\vert\Psi\rangle', font_size=fs)
        eq3.to_edge(UR)

        eq15 = Tex(r'\underline{Event: projection $\pi$}', color=BLUE, font_size=fs).set_z_index(1)
        eq15.next_to(eq3, DOWN).align_to(eq3, RIGHT)
        eq3.move_to(eq15, coor_mask=RIGHT)
        box5 = SurroundingRectangle(eq3, fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)

        eq15[0][-1].set_z_index(0.9).next_to(eq15[0][0], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq16 = MathTex(r'{\rm probability}', r'=', r'P(\pi)', font_size=fs)
        eq16.next_to(eq15, DOWN, buff=0.15)
        box6 = SurroundingRectangle(VGroup(eq3, eq15, eq16), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)

        eq23 = MathTex(r"P'(A)", r"=", r"P(\pi A\pi)/P(\pi)", font_size=fs)
        eq23.next_to(eq16, DOWN, buff=0.15)

        box7 = SurroundingRectangle(VGroup(eq3, eq15, eq16, eq23), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)

        eq30 = Tex(r'\underline{unitary transform: $U$}', color=BLUE, font_size=fs).set_z_index(1)
        eq30.next_to(eq23, DOWN)
        eq30[0][-1].set_z_index(0.9).next_to(eq30[0][0], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq31 = MathTex(r"P'(A)", r'=', r"P(U^*AU)", font_size=fs)
        eq31.next_to(eq30, DOWN, buff=0.15)

        gp1 = VGroup(eq3, eq15, eq16, eq23, eq30, eq31)
        box8 = SurroundingRectangle(gp1, fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)
        gp2 = VGroup(*gp1[:], box5, box6, box7, box8)
        gp2.to_edge(UR, buff=0.1)

        if not anim:
            for eq in (eq16, eq23, eq31, eq3):
                eq.set_z_index(1)
            return VGroup(*gp1[:], box8)

        MathTex.set_default(font_size=DEFAULT_FONT_SIZE * 1.1)


        eq1_1 = MathTex(r'{\rm\ expected\ value\ of\ }A', r'=', r'\langle\Psi\vert A\vert\Psi\rangle')
        eq2 = MathTex(r'P(A)', r'=', r'\langle\Psi\vert A\vert\Psi\rangle')
        eq2.move_to(ORIGIN).to_edge(DOWN, buff=1)
        mh.align_sub(eq1_1, eq1_1[1], eq2[1]).move_to(ORIGIN, coor_mask=RIGHT)
        # mh.align_sub(eq3, eq3[1], eq1[1])
        eq4 = MathTex(r'{\rm probability\ amplitude}', r'=', r'\langle\Phi\vert\Psi\rangle')
        mh.align_sub(eq4, eq4[1], eq2[1], coor_mask=UP)

        eq5 = MathTex(r'{\rm probability}', r'=', r'\lvert\langle\Phi\vert\Psi\rangle\rvert^2')
        mh.align_sub(eq5, eq5[1], eq4[1], coor_mask=UP)
        eq6 = MathTex(r'{\rm probability}', r'=', r'\overline{\langle\Phi\vert\Psi\rangle}\,\langle\Phi\vert\Psi\rangle')
        mh.align_sub(eq6, eq6[1], eq5[1], coor_mask=UP)
        eq7 = MathTex(r'{\rm probability}', r'=', r'\langle\Psi\vert\Phi\rangle\,\langle\Phi\vert\Psi\rangle')
        mh.align_sub(eq7, eq7[1], eq6[1], coor_mask=UP)
        eq8 = MathTex(r'\pi_\Phi', r'=', r'\vert\Phi\rangle\langle\Phi\vert')
        mh.align_sub(eq8, eq8[1], eq7[1]).next_to(eq7, DOWN, coor_mask=UP)
        eq9 = MathTex(r'{\rm probability}', r'=', r'P(\pi_\Phi)')
        mh.align_sub(eq9, eq9[1], eq7[1])

        box1 = SurroundingRectangle(VGroup(eq1_1, eq2, eq4, eq6), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)


        eq10 = MathTex(r'\pi_V', r'=', r'{\rm orthogonal\ projection\ onto\ }V')
        mh.align_sub(eq10, eq10[1], eq8[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq11 = MathTex(r'{\rm probability', r'=', r'\lVert\pi_V\Psi\rVert^2')
        mh.align_sub(eq11, eq11[1], eq9[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq12 = MathTex(r'{\rm probability', r'=', r'\langle\pi_V\Psi\vert\pi_V\Psi\rangle')
        mh.align_sub(eq12, eq12[1], eq11[1])
        eq13 = MathTex(r'{\rm probability}', r'=', r'\langle\Psi\vert\pi_V^*\pi_V\vert\Psi\rangle')
        mh.align_sub(eq13, eq13[1], eq12[1])
        eq14 = MathTex(r'{\rm probability}', r'=', r'P(\pi_V)')
        mh.align_sub(eq14, eq14[1], eq13[1])

        box2 = SurroundingRectangle(VGroup(eq8, eq10, eq11), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)

        eq17 = MathTex(r'\Psi^\prime', r'=', r'\pi_V\Psi / \lVert\pi_V\Psi\rVert')
        mh.align_sub(eq17, eq17[1], eq14[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq18 = MathTex(r'P^\prime(A)', r'=', r"\langle\Psi'\vert A\vert\Psi'\rangle")
        mh.align_sub(eq18, eq18[1], eq17[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq19 = MathTex(r'P^\prime(A)', r'=', r"\langle\pi_V\Psi\vert A\vert\pi_V\Psi\rangle/ \lVert\pi_V\Psi\rVert^2")
        mh.align_sub(eq19, eq19[1], eq18[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq20 = MathTex(r'P^\prime(A)', r'=', r"\langle\Psi\vert\pi_V^* A\pi_V\vert\Psi\rangle/ \lVert\pi_V\Psi\rVert^2")
        mh.align_sub(eq20, eq20[1], eq19[1])#.move_to(ORIGIN, coor_mask=RIGHT)
        eq21 = MathTex(r'P^\prime(A)', r'=', r"P(\pi_V A\pi_V)/ \lVert\pi_V\Psi\rVert^2")
        mh.align_sub(eq21, eq21[1], eq20[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq22 = MathTex(r'P^\prime(A)', r'=', r"P(\pi_V A\pi_V)/ P(\pi_V)")
        mh.align_sub(eq22, eq22[1], eq21[1])#.move_to(ORIGIN, coor_mask=RIGHT)

        box3 = SurroundingRectangle(VGroup(eq17, eq18, eq19, eq20, eq21, eq22, eq8), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)

        eq24 = MathTex(r"\Psi'", r'=', r'U\Psi')
        eq25 = Tex(r'unitary transform: $U$', r'=')
        mh.align_sub(eq25, eq25[1], eq22[1], coor_mask=UP)
        mh.align_sub(eq24, eq24[1], eq10[1], coor_mask=UP)
        eq25[0].move_to(ORIGIN, coor_mask=RIGHT)
        eq26 = MathTex(r"P'(A)", r'=', r"\langle\Psi'\vert A\vert\Psi'\rangle")
        mh.align_sub(eq26, eq26[1], eq22[1], coor_mask=UP)
        eq27 = MathTex(r"P'(A)", r'=', r"\langle U\Psi\vert A\vert U\Psi\rangle")
        mh.align_sub(eq27, eq27[1], eq26[1])
        eq28 = MathTex(r"P'(A)", r'=', r"\langle \Psi\vert U^*AU\vert\Psi\rangle")
        mh.align_sub(eq28, eq28[1], eq27[1])
        eq29 = MathTex(r"P'(A)", r'=', r"P(U^*AU)")
        mh.align_sub(eq29, eq29[1], eq28[1])

        for eq in (eq16, eq23, eq31, eq1_1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11, eq12, eq13, eq14,
                   eq17, eq18, eq19, eq20, eq21, eq22, eq24, eq25, eq26, eq27, eq28, eq29):
            eq.set_z_index(1)

        box4 = SurroundingRectangle(VGroup(eq24, eq25[0], eq26, eq28), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)

        # self.add(eq1, box4)
        # self.wait(0.1)
        # self.play(mh.rtransform(eq1.copy(), eq1_1),
        #           FadeIn(box1), run_time=1.5)
        self.add(eq1_1, box1)
        self.wait(0.1)
        shift = mh.diff(eq1_1[0][-1], eq2[0][-2], RIGHT)
        self.play(mh.rtransform(eq1_1[1:], eq2[1:], eq1_1[0][-1], eq2[0][-2]),
                  FadeOut(eq1_1[0][:-1]),
                  FadeIn(eq2[0][:-2], eq2[0][-1], shift=shift),
                  run_time=1.5)
        self.wait(0.1)
        # shift = mh.diff(eq1[0][-1], eq3[0][-2], RIGHT)
        self.play(mh.rtransform(eq2.copy(), eq3),
                  # mh.rtransform(eq1[1:], eq3[1:], eq1[0][-1], eq3[0][-2]),
                  # FadeOut(eq1[0][:-1]),
                  FadeIn(box5, shift=mh.diff(eq2, eq3)),
                  run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq2), FadeIn(eq4), run_time=1.5)
        self.wait(0.1)
        shift = mh.diff(eq4[2][:], eq5[2][1:-2], RIGHT)
        self.play(mh.rtransform(eq4[0][:11], eq5[0][:], eq4[1], eq5[1],
                                eq4[2][:], eq5[2][1:-2]),
                  FadeIn(eq5[2][0], shift=shift),
                  FadeIn(eq5[2][-2:], shift=shift),
                  FadeOut(eq4[0][11:]),
                  run_time=1.2)
        self.wait(0.1)
        shift = mh.diff(eq5[2][1:-2], eq6[2][6:]),
        shift2 = mh.diff(eq5[2][1:-2], eq6[2][1:6])
        self.play(mh.rtransform(eq5[:2], eq6[:2], eq5[2][1:-2], eq6[2][6:]),
                  mh.rtransform(eq5[2][1:-2].copy(), eq6[2][1:6]),
                  FadeOut(eq5[2][0]),
                  FadeOut(eq5[2][-2:], shift=shift),
                  FadeIn(eq6[2][0], shift=shift2),
                  run_time=1)
        self.wait(0.1)
        self.play(mh.rtransform(eq6[:2], eq7[:2], eq6[2][6:], eq7[2][5:],
                                eq6[2][1], eq7[2][0], eq6[2][2], eq7[2][3],
                                eq6[2][3], eq7[2][2], eq6[2][4], eq7[2][1],
                                eq6[2][5], eq7[2][4]),
                  FadeOut(eq6[2][0]),
                  run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(box1, box2, rate_func=rush_from), mh.rtransform(eq7[2][2:8].copy(), eq8[2][:]),
                  FadeIn(eq8[:2]),
                  run_time=1)
        self.wait(0.1)
        eq9_1 = eq9[2][2:4].copy().move_to(eq7[2][2:-2], coor_mask=RIGHT)
        self.play(mh.rtransform(eq8[0][:].copy(), eq9_1),
                  FadeOut(eq7[2][3:-3]),
                  run_time=1.2)
        self.wait(0.1)
        shift = mh.diff(eq7[2][-3], eq9[2][-1])
        shift2 = mh.diff(eq7[2][2], eq9[2][1])
        self.play(mh.rtransform(eq7[:2], eq9[:2], eq9_1, eq9[2][2:4]),
                  FadeOut(eq7[2][:3], shift=shift2),
                  FadeOut(eq7[2][-3:], shift=shift),
                  FadeIn(eq9[2][:2], shift=shift2),
                  FadeIn(eq9[2][-1], shift=shift),
                  run_time=1)
        self.wait()
        self.play(FadeOut(eq8, eq9), FadeIn(eq10, eq11), run_time=1.5)
        self.wait(0.1)
        shift = mh.diff(eq11[2][1:4], eq12[2][5:8], coor_mask=RIGHT)
        self.play(mh.rtransform(eq11[:2], eq12[:2], eq11[2][1:4], eq12[2][1:4],
                                eq11[2][1:4].copy(), eq12[2][5:8]),
                  FadeIn(eq12[2][0], eq12[2][4]),
                  FadeIn(eq12[2][-1], shift=shift),
                  FadeOut(eq11[2][0], eq11[2][-2:]),
                  run_time=1)
        self.wait(0.1)
        shift=mh.diff(eq12[2][1], eq13[2][3])
        self.play(mh.rtransform(eq12[:2], eq13[:2], eq12[2][0], eq13[2][0],
                                eq12[2][1], eq13[2][3], eq12[2][3:5], eq13[2][1:3],
                                eq12[2][2], eq13[2][5], eq12[2][4].copy(), eq13[2][8],
                                eq12[2][5:7], eq13[2][6:8], eq12[2][-2:], eq13[2][-2:]),
                  FadeIn(eq13[2][4], shift=shift),
                  run_time=1)
        self.wait(0.1)
        eq13_1 = eq13[2][6:8].copy().move_to(eq13[2][2:9], coor_mask=RIGHT)
        shift=mh.diff(eq13[2][3], eq13_1[0], )
        self.play(mh.rtransform(eq13[2][6:8], eq13_1),
                  mh.rtransform(eq13[2][3], eq13_1[0], eq13[2][5], eq13_1[1]),
                  FadeOut(eq13[2][4], shift=shift),
                  run_time=1)
        self.wait(0.1)
        shift = mh.diff(eq13[2][-3], eq14[2][-1], coor_mask=RIGHT)
        shift2 = mh.diff(eq13[2][2], eq14[2][1], coor_mask=RIGHT)
        self.play(mh.rtransform(eq13[:2], eq14[:2], eq13_1, eq14[2][2:4]),
                  FadeOut(eq13[2][:3], shift=shift2),
                  FadeOut(eq13[2][-3:], shift=shift),
                  FadeIn(eq14[2][:2], shift=shift2),
                  FadeIn(eq14[2][-1], shift=shift),
                  run_time=1.2)
        self.wait(0.1)
        shift = mh.diff(eq13[2][2], eq16[2][2])
        self.play(FadeIn(eq15),
                  mh.rtransform(eq14[:2], eq16[:2], eq14[2][:3], eq16[2][:3], eq14[2][-1], eq16[2][-1]),
                  FadeOut(eq14[2][3], shift=shift),
                  FadeOut(eq10, box2),
                  ReplacementTransform(box5, box6, rate_func=rush_from),
                  run_time=2)

        self.wait(0.1)
        self.play(FadeIn(box3, eq17[:2], eq17[2][:3], rate_func=linear), run_time=0.8)
        self.wait(0.1)
        self.play(FadeIn(eq17[2][3:], rate_func=linear), run_time=0.8)
        self.wait(0.1)
        self.play(eq17.animate.shift(mh.diff(eq17[1], eq10[1], coor_mask=UP)),
                  FadeIn(eq18),
                  run_time=1.5)
        self.wait(0.1)
        shift1 = mh.diff(eq18[2][1], eq19[2][3], coor_mask=RIGHT)
        shift2 = mh.diff(eq18[2][6], eq19[2][9], coor_mask=RIGHT)
        shift3 = mh.diff(eq17[2][-1], eq19[2][-2])
        self.play(mh.rtransform(eq18[:2], eq19[:2], eq18[2][0], eq19[2][0],
                                eq18[2][3:6], eq19[2][4:7], eq18[2][8], eq19[2][10],
                                eq18[2][1], eq19[2][3], eq18[2][6], eq19[2][9]),
                  mh.rtransform(eq17[2][:3].copy(), eq19[2][1:4]),
                  mh.rtransform(eq17[2][:3].copy(), eq19[2][7:10]),
                  mh.rtransform(eq17[2][3:9].copy(), eq19[2][11:17]),
                  FadeOut(eq18[2][2], shift=shift1),
                  FadeOut(eq18[2][7], shift=shift2),
                  FadeIn(eq19[2][-1], shift=shift3),
                  run_time=1.8)
        self.wait(0.1)
        shift = mh.diff(eq19[2][1], eq20[2][3], coor_mask=RIGHT)
        self.play(mh.rtransform(eq19[:2], eq20[:2], eq19[2][0], eq20[2][0],
                                eq19[2][1], eq20[2][3], eq19[2][2], eq20[2][5],
                                eq19[2][3:5], eq20[2][1:3], eq19[2][5], eq20[2][6],
                                eq19[2][6], eq20[2][9], eq19[2][7:9], eq20[2][7:9],
                                eq19[2][9:], eq20[2][10:]),
                  FadeIn(eq20[2][4], shift=shift),
                  run_time=1.3)
        self.play(FadeOut(eq20[2][4]),
                  eq20[2][5].animate.move_to(eq20[2][8], coor_mask=UP),
                  rate_func=linear,
                  run_time=1)
        self.wait(0.1)
        shift1 = mh.diff(eq20[2][2], eq21[2][1], coor_mask=RIGHT)
        shift2 = mh.diff(eq20[2][9], eq21[2][7], coor_mask=RIGHT)
        self.play(mh.rtransform(eq20[:2], eq21[:2], eq20[2][3], eq21[2][2],
                                eq20[2][5:9], eq21[2][3:7], eq20[2][12:], eq21[2][8:]),
                  FadeOut(eq20[2][:3], shift=shift1),
                  FadeIn(eq21[2][:2], shift=shift1),
                  FadeOut(eq20[2][9:12], shift=shift2),
                  FadeIn(eq21[2][7], shift=shift2),
                  run_time=1.4)
        self.wait(0.1)
        shift1 = mh.diff(eq21[2][9], eq22[2][10], coor_mask=RIGHT)
        shift2 = mh.diff(eq21[2][12], eq22[2][13], coor_mask=RIGHT)
        self.play(mh.rtransform(eq21[:2], eq22[:2], eq21[2][:9], eq22[2][:9],
                                eq21[2][10:12], eq22[2][11:13]),
                  FadeOut(eq21[2][9], shift=shift1),
                  FadeIn(eq22[2][9:11], shift=shift1),
                  FadeOut(eq21[2][12:], shift=shift2),
                  FadeIn(eq22[2][13], shift=shift2),
                  run_time=1.2)
        self.wait(0.1)
        self.play(mh.rtransform(eq22[:2], eq23[:2], eq22[2][:3], eq23[2][:3],
                                eq22[2][4:6], eq23[2][3:5], eq22[2][7:12], eq23[2][5:10],
                                eq22[2][13], eq23[2][10]),
                  FadeOut(eq22[2][3], shift=mh.diff(eq22[2][2], eq23[2][2])),
                  FadeOut(eq22[2][6], shift=mh.diff(eq22[2][5], eq23[2][4])),
                  FadeOut(eq22[2][12], shift=mh.diff(eq22[2][11], eq23[2][9])),
                  FadeOut(eq17),
                  FadeOut(box3),
                  ReplacementTransform(box6, box7, rate_func=rush_from),
                  run_time=2)
        self.wait(0.5)

        self.play(FadeIn(eq24, eq25[0], box4), run_time=1.2)
        self.wait(0.1)
        self.play(FadeOut(eq25[0]), FadeIn(eq26), run_time=1.5)
        self.wait(0.1)
        self.play(mh.rtransform(eq26[:2], eq27[:2], eq26[2][0], eq27[2][0],
                                eq26[2][1], eq27[2][2], eq26[2][3:6], eq27[2][3:6],
                                eq26[2][6], eq27[2][7], eq26[2][8], eq27[2][8]),
                  FadeOut(eq26[2][2], shift=mh.diff(eq26[2][1], eq27[2][2], coor_mask=RIGHT)),
                  FadeOut(eq26[2][7], shift=mh.diff(eq26[2][6], eq27[2][7], coor_mask=RIGHT)),
                  mh.rtransform(eq24[2][:].copy(), eq27[2][1:3]),
                  mh.rtransform(eq24[2][:].copy(), eq27[2][6:8]),
                  run_time=1.3)
        self.wait(0.1)
        self.play(mh.rtransform(eq27[:2], eq28[:2], eq27[2][0], eq28[2][0],
                                eq27[2][1], eq28[2][3], eq27[2][2:4], eq28[2][1:3],
                                eq27[2][4], eq28[2][5], eq27[2][5], eq28[2][7],
                                eq27[2][6], eq28[2][6], eq27[2][7:9], eq28[2][8:10]),
                  FadeIn(eq28[2][4], shift=mh.diff(eq27[2][1], eq28[2][3], coor_mask=RIGHT)),
                  run_time=1.2)
        self.wait(0.1)
        shift1 = mh.diff(eq28[2][2], eq29[2][1], coor_mask=RIGHT)
        shift2 = mh.diff(eq28[2][7], eq29[2][6], coor_mask=RIGHT)
        self.play(mh.rtransform(eq28[:2], eq29[:2], eq28[2][3:7], eq29[2][2:6]),
                  FadeOut(eq28[2][:3], shift=shift1),
                  FadeIn(eq29[2][:2], shift=shift1),
                  FadeOut(eq28[2][7:], shift=shift2),
                  FadeIn(eq29[2][6], shift=shift2),
                  run_time=1.2)
        self.wait(0.1)
        self.play(FadeIn(eq30),mh.rtransform(eq29, eq31), FadeOut(eq24, box4),
                  ReplacementTransform(box7, box8, rate_func=rush_from), run_time=2)

        self.wait()
        return VGroup()


class MixedP(Pdefinition):
    def construct(self):
        eqs = self.create_eqs()
        self.add(eqs)

        fs = DEFAULT_FONT_SIZE * 0.9
        eq8 = MathTex(r'P(A)', r'\!=', r'\!\sum_kp_k\langle\Psi_k\vert A\vert\Psi_k\rangle', font_size=fs).set_z_index(1)
        mh.align_sub(eq8, eq8[1], eqs[0][1]).align_to(eqs[:-1], RIGHT)
        eqs2 = VGroup(eq8, *eqs[1:-1].copy().next_to(eq8, DOWN, buff=0.15))
        box2 = SurroundingRectangle(eqs2, corner_radius=0.15, fill_color=BLACK, fill_opacity=self.box_op,
                                    stroke_opacity=0)
        eqs2 = VGroup(*eqs2[:], box2)


        Tex.set_default(font_size=60)
        MathTex.set_default(font_size=60)

        eq1 = Tex(r'$\Psi = \Psi_1$', ' with probability ', r'$p_1$')
        eq2 = Tex(r'$\Psi = \Psi_2$', ' with probability ', r'$p_2$')
        eq3 = Tex(r'$\Psi = \Psi_3$', ' with probability ', r'$p_3$')
        eq4 = Tex(r'$\vdots$')
        mh.align_sub(eq2, eq2[0][1], eq1[0][1]).next_to(eq1, DOWN, coor_mask=UP)
        mh.align_sub(eq3, eq3[0][1], eq1[0][1]).next_to(eq2, DOWN, coor_mask=UP)
        mh.align_sub(eq4, eq4[0][0], eq1[0][1]).next_to(eq3, DOWN, coor_mask=UP)
        gp1 = VGroup(eq1, eq2, eq3, eq4)
        eq5 = MathTex(r'P(A)', r'=', r'\langle\Psi_1\vert A\vert\Psi_1\rangle \mathbb P(\Psi=\Psi_1)',
                      r' + \langle\Psi_2\vert A\vert\Psi_2\rangle \mathbb P(\Psi=\Psi_2)',
                      r' + \langle\Psi_3\vert A\vert\Psi_3\rangle \mathbb P(\Psi=\Psi_3)',
                      r' + \cdots'
                      )
        eq5[3].next_to(eq5[2], DOWN).align_to(eq5[2], LEFT)
        eq5[4].next_to(eq5[3], DOWN).align_to(eq5[2], LEFT)
        eq5[5].next_to(eq5[4], DOWN).align_to(eq5[2], LEFT)
        eq5.move_to(gp1)
        eq6 = MathTex(r'P(A)', r'=', r'p_1\langle\Psi_1\vert A\vert\Psi_1\rangle',
                      r' + p_2\langle\Psi_2\vert A\vert\Psi_2\rangle',
                      r' + p_3\langle\Psi_3\vert A\vert\Psi_3\rangle',
                      r' + \cdots'
                      )
        mh.align_sub(eq6, eq6[1], eq5[1])
        mh.align_sub(eq6[3], eq6[3][0], eq5[3][0])
        mh.align_sub(eq6[4], eq6[4][0], eq5[4][0])
        mh.align_sub(eq6[5], eq6[5][0], eq5[5][0])
        eq7 = MathTex(r'P(A)', r'=', r'\sum_kp_k\langle\Psi_k\vert A\vert\Psi_k\rangle')
        mh.align_sub(eq7, eq7[1], eq6[1]).move_to(gp1)

        gp2 = VGroup(*gp1[:], eq5, eq6, eq7)
        gp2.set_z_index(1)


        box1 = SurroundingRectangle(gp2, corner_radius=0.15, fill_color=BLACK, fill_opacity=self.box_op,
                                    stroke_opacity=0)
        VGroup(box1, gp2).to_edge(DOWN, buff=0.15)

        self.play(FadeIn(box1, eq1), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq2), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq3), run_time=1)
        self.play(FadeIn(eq4), run_time=1)
        self.wait(0.1)
        eq5_1 = eq5[0].copy().scale(1.5).move_to(eq5)
        self.play(FadeOut(eq1, eq2, eq3, eq4), FadeIn(eq5_1), run_time=1.5)
        self.wait(0.1)
        shift = eq5[0].get_right() - eq5_1.get_right()
        self.play(LaggedStart(AnimationGroup(mh.rtransform(eq5_1, eq5[0]),
                  FadeIn(eq5[1], shift=shift)),
                  FadeIn(eq5[2][:-7]),
                              lag_ratio=0.3),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq5[2][-7:]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq5[3]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq5[4:]), run_time=1)
        self.wait(0.1)

        eq6_1 = eq6[2][:2].copy().move_to(eq5[2][-7], aligned_edge=LEFT, coor_mask=RIGHT)
        eq6_2 = eq6[3][1:3].copy().move_to(eq5[3][-7], aligned_edge=LEFT, coor_mask=RIGHT)
        eq6_3 = eq6[4][1:3].copy().move_to(eq5[4][-7], aligned_edge=LEFT, coor_mask=RIGHT)

        self.play(FadeOut(eq5[2][-7:], eq5[3][-7:], eq5[4][-7:]),
                  FadeIn(eq6_1, eq6_2, eq6_3), rate_func=linear, run_time=1.3)
        self.wait(0.1)
        self.play(mh.rtransform(eq5[:2], eq6[:2], eq5[2][:-7], eq6[2][2:], eq6_1, eq6[2][:2],
                                eq5[3][0], eq6[3][0], eq5[3][1:-7], eq6[3][3:], eq6_2, eq6[3][1:3],
                                eq5[4][0], eq6[4][0], eq5[4][1:-7], eq6[4][3:], eq6_3, eq6[4][1:3],
                                eq5[5], eq6[5]),
                  run_time=1.5)
        self.wait(0.1)
        eq7_1 = eq7[2][3].copy()
        eq7_2 = eq7[2][6].copy()
        eq7_3 = eq7[2][11].copy()
        eq7_4 = eq7_1.copy()
        eq7_5 = eq7_2.copy()
        eq7_6 = eq7_3.copy()
        shift1 = mh.diff(eq6[3][1], eq7[2][2])
        self.play(mh.rtransform(eq6[:2], eq7[:2], eq6[2][0], eq7[2][2], eq6[2][2:4], eq7[2][4:6],
                                eq6[2][5:9], eq7[2][7:11], eq6[2][10], eq7[2][12]),
                  mh.rtransform(eq6[3][1], eq7[2][2], eq6[3][3:5], eq7[2][4:6],
                                eq6[3][6:10], eq7[2][7:11], eq6[3][11], eq7[2][12]),
                  mh.rtransform(eq6[4][1], eq7[2][2], eq6[4][3:5], eq7[2][4:6],
                                eq6[4][6:10], eq7[2][7:11], eq6[4][11], eq7[2][12]),
                  mh.fade_replace(eq6[2][1], eq7[2][3]),
                  mh.fade_replace(eq6[2][4], eq7[2][6]),
                  mh.fade_replace(eq6[2][9], eq7[2][11]),
                  mh.fade_replace(eq6[3][2], eq7_1),
                  mh.fade_replace(eq6[3][5], eq7_2),
                  mh.fade_replace(eq6[3][10], eq7_3),
                  mh.fade_replace(eq6[4][2], eq7_4),
                  mh.fade_replace(eq6[4][5], eq7_5),
                  mh.fade_replace(eq6[4][10], eq7_6),
                  FadeIn(eq7[2][:2], shift=shift1),
                  FadeOut(eq6[3][0], shift=shift1),
                  FadeOut(eq6[4][0], shift=mh.diff(eq6[4][1], eq7[2][4])),
                  FadeOut(eq6[5], shift=mh.diff(eq6[5][1], eq7[2][4])),
                  run_time=2)
        self.remove(eq7_1, eq7_2, eq7_3, eq7_4, eq7_5, eq7_6)
        self.wait(0.1)
        self.play(mh.rtransform(eqs[0][:2], eq8[:2], eqs[0][2][:2], eq8[2][4:6],
                                eqs[0][2][2:6], eq8[2][7:11], eqs[0][2][6], eq8[2][12]),
                  # FadeIn(eq8[2][:2], shift=mh.diff(eqs[0][1], eq8[1])),
                  mh.rtransform(eq7, eq8),
                  mh.rtransform(eqs[1:], eqs2[1:]),
                  FadeOut(box1),
                  run_time=2)

        self.wait()


class Projection(Pdefinition):
    def construct(self):
        Tex.set_default(font_size=DEFAULT_FONT_SIZE*0.9)
        eq1 = Tex(r'\underline{orthogonal projections}', color=BLUE).set_z_index(1)
        eq1[0][-1].next_to(eq1[0][0], DOWN, buff=0.04, coor_mask=UP).set_z_index(0.9).set_color(WHITE)
        eq2 = Tex(r'self-adjoint: $\pi^*=\pi$').set_z_index(1)
        eq2.next_to(eq1, DOWN, buff=0.2)
        eq3 = Tex(r'idempotent: $\pi^2=\pi$').set_z_index(1)
        eq3.next_to(eq2, DOWN, buff=0.2)

        gp1 = VGroup(eq1, eq2, eq3)

        box1 = SurroundingRectangle(gp1, fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)
        VGroup(*gp1[:], box1).to_edge(UL, buff=0.1)

        eq4 = Tex(r'equivalently: $\pi^*\pi=\pi$').set_z_index(1)
        eq4.next_to(eq3, DOWN, buff=0.2)
        box2 = SurroundingRectangle(VGroup(gp1, eq4), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)

        self.add(eq1, eq2, eq3, box1)
        self.wait(0.5)
        self.play(ReplacementTransform(box1, box2, rate_func=rush_from), FadeIn(eq4), run_time=1)

class Unitary(Pdefinition):
    def construct(self):
        Tex.set_default(font_size=DEFAULT_FONT_SIZE*1.1)
        MathTex.set_default(font_size=DEFAULT_FONT_SIZE*1.1)
        eq1 = Tex(r'\underline{unitary transform}', color=BLUE).set_z_index(1)
        eq1[0][-1].next_to(eq1[0][0], DOWN, buff=0.04, coor_mask=UP).set_z_index(0.9).set_color(WHITE)
        eq2 = MathTex(r"\Psi'", r'=', r'U\Psi').set_z_index(1)
        eq2.next_to(eq1, DOWN, buff=0.2)
        eq3 = MathTex(r"U^*U", r'=', r'UU^*', r'=', r'I').set_z_index(1)
        eq3.next_to(eq2, DOWN, buff=0.2)
        eq4 = MathTex(r"\lVert \Psi'\rVert^2", r"=", r"\langle\Psi'\vert\Psi'\rangle")
        eq4.next_to(eq3, DOWN, buff=0.2)
        eq5 = MathTex(r"\lVert \Psi'\rVert^2", r"=", r"\langle U\Psi\vert U\Psi\rangle")
        mh.align_sub(eq5, eq5[1], eq4[1], coor_mask=UP)
        eq6 = MathTex(r"\lVert \Psi'\rVert^2", r"=", r"\langle \Psi\vert U^*U\vert\Psi\rangle")
        mh.align_sub(eq6, eq6[1], eq4[1], coor_mask=UP)
        eq7 = MathTex(r"\lVert \Psi'\rVert^2", r"=", r"\langle \Psi\vert\Psi\rangle")
        mh.align_sub(eq7, eq7[1], eq4[1], coor_mask=UP)
        eq8 = MathTex(r"\lVert \Psi'\rVert^2", r"=", r"\lVert \Psi\rVert^2")
        mh.align_sub(eq8, eq8[1], eq4[1], coor_mask=UP)

        gp1 = VGroup(eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8).set_z_index(1)

        box1 = SurroundingRectangle(gp1, fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)
        VGroup(box1, gp1).to_edge(DOWN, buff=0.2)

        self.add(eq1, eq2, box1)
        self.wait(0.1)
        self.play(FadeIn(eq3))
        self.wait(0.1)
        self.play(FadeIn(eq4))
        self.wait(0.1)
        self.play(mh.rtransform(eq4[:2], eq5[:2], eq4[2][0], eq5[2][0],
                                eq4[2][1], eq5[2][2], eq4[2][3], eq5[2][3],
                                eq4[2][4], eq5[2][5], eq4[2][6], eq5[2][6]),
                  FadeOut(eq4[2][2], shift=mh.diff(eq4[2][1], eq5[2][2])),
                  FadeOut(eq4[2][5], shift=mh.diff(eq4[2][4], eq5[2][5])),
                  ReplacementTransform(eq2[2][:].copy(), eq5[2][1:3]),
                  ReplacementTransform(eq2[2][:].copy(), eq5[2][4:6]),
                  run_time=1.4)
        self.wait(0.1)
        self.play(mh.rtransform(eq5[:2], eq6[:2], eq5[2][0], eq6[2][0],
                                eq5[2][1], eq6[2][3], eq5[2][2], eq6[2][1],
                                eq5[2][3].copy(), eq6[2][2], eq5[2][3], eq6[2][6],
                                eq5[2][4], eq6[2][5], eq5[2][5], eq6[2][7],
                                eq5[2][6], eq6[2][8]),
                  FadeIn(eq6[2][4], shift=mh.diff(eq5[2][1], eq6[2][3], coor_mask=RIGHT)),
                  run_time=1.6)
        self.wait(0.1)
        eq6_1 = mh.align_sub(eq3.copy(), eq3[3], eq6[1])[4].move_to(eq6[2][3:6])
        self.play(ReplacementTransform(eq3[4].copy(), eq6_1),
                  FadeOut(eq6[2][3:6]),
                  run_time=1.2)
        self.wait(0.1)
        self.play(mh.rtransform(eq6[:2], eq7[:2], eq6[2][:3], eq7[2][:3],
                                eq6[2][7:9], eq7[2][3:5]),
                  mh.rtransform(eq6[2][6], eq7[2][2]),
                  FadeOut(eq6_1, shift=mh.diff(eq6_1, eq7[2][2], coor_mask=RIGHT)),
                  run_time=1.4)
        self.wait(0.1)
        shift1 = mh.diff(eq7[2][0], eq8[2][0], coor_mask=RIGHT)
        shift2 = mh.diff(eq7[2][4], eq8[2][2], coor_mask=RIGHT)
        self.play(mh.rtransform(eq7[:2], eq8[:2], eq7[2][1], eq8[2][1]),
                  mh.rtransform(eq7[2][3], eq8[2][1]),
                  FadeOut(eq7[2][0], shift=shift1),
                  FadeIn(eq8[2][0], shift=shift1),
                  FadeOut(eq7[2][4], shift=shift2),
                  FadeIn(eq8[2][2:], shift=shift2),
                  FadeOut(eq7[2][2], shift=mh.diff(eq7[2][2], eq8[2][1], coor_mask=RIGHT)),
                  run_time=1.4)
        self.wait()

class Hamiltonian(Pdefinition):
    def construct(self):
        Tex.set_default(font_size=DEFAULT_FONT_SIZE*1.1)
        MathTex.set_default(font_size=DEFAULT_FONT_SIZE*1.1)

        eq1 = MathTex(r'i\hbar\frac{d}{dt}\Psi = H\Psi')
        eq2 = MathTex(r'\Psi_t', r'=', r'e^{-\frac{iHt}{\hbar} }\Psi_0')
        eq2.next_to(eq1, DOWN)
        eq3 = MathTex(r'P_t(A)', r'=', r'P_0\left(e^{\frac{iHt}{\hbar} }Ae^{-\frac{iHt}{\hbar} }\right)')
        mh.align_sub(eq3, eq3[1], eq2[1], coor_mask=UP)
        eq4 = MathTex(r'\frac{d}{dt}P_t(A)', r'=',
                      r'P_0\left(\frac{d}{dt} \left(e^{\frac{iHt}{\hbar} } Ae^{-\frac{iHt}{\hbar} }\right)\right)')
        mh.align_sub(eq4, eq4[1], eq3[1])
        eq5 = MathTex(r'\frac{d}{dt}P_t(A)', r'=',
                      r'P_0\left(\frac{de^{\frac{iHt}{\hbar} } }{dt} Ae^{-\frac{iHt}{\hbar} } + e^{\frac{iHt}{\hbar} } A\frac{de^{-\frac{iHt}{\hbar} } }{dt}\right)')
        for eq in (eq1, eq2, eq3, eq4, eq5):
            eq.set_z_index(1)
        box1 = SurroundingRectangle(VGroup(eq1, eq2, eq3), fill_color=BLACK, stroke_opacity=0, fill_opacity=self.box_op, corner_radius=0.15)
        VGroup(eq1, eq2, eq3, eq4, eq5, box1).to_edge(DOWN, buff=0.15)

        eq4.move_to(box1, coor_mask=UP)
        mh.align_sub(eq5, eq5[1], eq4[1], coor_mask=UP)
        eq6 = MathTex(r'\frac{d}{dt}P_t(A)', r'=',
                      r'P_0\left(e^{\frac{iHt}{\hbar}{\frac{iH}{\hbar} } } Ae^{-\frac{iHt}{\hbar} } + e^{\frac{iHt}{\hbar} } A^{\frac{-iH}{\hbar} }e^{-\frac{iHt}{\hbar} }\right)')
        eq6[2][9:13].move_to(eq6[1], coor_mask=UP)
        eq6[2][29:34].move_to(eq6[1], coor_mask=UP)
        mh.align_sub(eq6, eq6[1], eq5[1])
        eq7 = MathTex(r'\frac{d}{dt}P_t(A)', r'=', r'\frac{i}{\hbar}',
                      r'P_0\left(e^{\frac{iHt}{\hbar} }(HA-AH)e^{-\frac{iHt}{\hbar} }\right)')
        mh.align_sub(eq7, eq7[1], eq6[1], coor_mask=UP)
        eq8 = MathTex(r'\frac{d}{dt}P_t(A)', r'=', r'\frac{i}{\hbar}',
                      r'P_t\left(HA-AH\right)')
        mh.align_sub(eq8, eq8[1], eq7[1], coor_mask=UP)
        eq9 = MathTex(r'\frac{d}{dt}P_t(A)', r'=', r'\frac{-i}{\hbar}',
                      r'P_t\left(AH-HA\right)')
        mh.align_sub(eq9, eq9[1], eq8[1])
        eq10 = MathTex(r'i\hbar\frac{d}{dt}P_t(A)', r'=', r'P_t\left(AH-HA\right)')
        mh.align_sub(eq10, eq10[1], eq9[1], coor_mask=UP)

        box2_1 = SurroundingRectangle(eq4)
        box2 = RoundedRectangle(height=box1.height, width=box2_1.width, fill_color=BLACK, stroke_opacity=0,
                         fill_opacity=self.box_op, corner_radius=0.15).move_to(box1).move_to(box2_1, coor_mask=RIGHT)
        box3_1 = SurroundingRectangle(eq5)
        box3 = RoundedRectangle(height=box1.height, width=box3_1.width, fill_color=BLACK, stroke_opacity=0,
                         fill_opacity=self.box_op, corner_radius=0.15).move_to(box1).move_to(box3_1, coor_mask=RIGHT)
        box4_1 = SurroundingRectangle(eq6)
        box4 = RoundedRectangle(height=box1.height, width=box4_1.width, fill_color=BLACK, stroke_opacity=0,
                         fill_opacity=self.box_op, corner_radius=0.15).move_to(box1).move_to(box4_1, coor_mask=RIGHT)


        eq1_1 = eq1.copy().move_to(box1, coor_mask=UP)
        self.add(box1, eq1_1)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(eq1_1, eq1), FadeIn(eq2), lag_ratio=0.3),
                  run_time=1.5)
        self.wait(0.1)
        self.play(mh.rtransform(eq2[1], eq3[1], eq2[0][1], eq3[0][1], eq2[2][:7], eq3[2][10:17],
                                eq2[2][0].copy(), eq3[2][3], eq2[2][2:7].copy(), eq3[2][4:9]),
                  mh.fade_replace(eq2[0][0], eq3[0][0], coor_mask=RIGHT),
                  FadeIn(eq3[0][2:], shift=mh.diff(eq2[0][1], eq3[0][1], coor_mask=RIGHT)),
                  FadeOut(eq2[2][7:9]),
                  FadeIn(eq3[2][9]),
                  FadeIn(eq3[2][:3], shift=mh.diff(eq2[1], eq3[1])),
                  FadeIn(eq3[2][-1], shift=(eq3[2][:-1].get_right() - eq2[2].get_right()) * RIGHT),
                  run_time=1.4)
        self.wait(0.1)
        self.play(
            mh.rtransform(eq3[0][:], eq4[0][4:], eq3[1], eq4[1], eq3[2][:2], eq4[2][:2], eq3[2][-1], eq4[2][-1],
                          eq3[2][3:-1], eq4[2][8:-2]),
            mh.stretch_replace(eq3[2][2], eq4[2][2]),
            FadeIn(eq4[0][:4], shift=mh.diff(eq3[0][0], eq4[0][4])),
            FadeIn(eq4[2][3:8], shift=mh.diff(eq3[2][2], eq4[2][8])),
            FadeIn(eq4[2][-2], shift=mh.diff(eq3[2][-1], eq4[2][-2])),
            FadeOut(eq1),
            ReplacementTransform(box1, box2, rate_func=rush_from),
            run_time=1.5
        )
        self.wait(0.1)
        self.play(mh.rtransform(eq4[:2], eq5[:2], eq4[2][:2], eq5[2][:2],
                               eq4[2][3], eq5[2][3], eq4[2][4:7], eq5[2][10:13],
                               eq4[2][8:14], eq5[2][4:10],
                               eq4[2][14:22], eq5[2][13:21]),
                  mh.stretch_replace(eq4[2][-2], eq5[2][-1]),
                  mh.stretch_replace(eq4[2][7], eq5[2][2]),
                  mh.stretch_replace(eq4[2][2], eq5[2][2]),
                  mh.stretch_replace(eq4[2][-1], eq5[2][-1]),
                  mh.rtransform(eq4[2][8:15].copy(), eq5[2][22:29], eq4[2][15:22].copy(), eq5[2][30:37],
                               eq4[2][3].copy(), eq5[2][29], eq4[2][4:7].copy(), eq5[2][37:40]),
                  FadeIn(eq5[2][21], target_position=eq4[2][14]),
                  ReplacementTransform(box2, box3),
                  run_time=2)
        self.wait(0.1)
        self.play(mh.rtransform(eq5[:2], eq6[:2], eq5[2][:2], eq6[2][:2],
                                eq5[2][4:10], eq6[2][3:9], eq5[2][6].copy(), eq6[2][10],
                                eq5[2][8:10].copy(), eq6[2][11:13], eq5[2][13:29], eq6[2][13:29],
                                eq5[2][30:37], eq6[2][34:41], eq5[2][31].copy(), eq6[2][29],
                                eq5[2][33].copy(), eq6[2][31],
                                eq5[2][35:37].copy(), eq6[2][32:34]),
                  mh.stretch_replace(eq5[2][32].copy(), eq6[2][30]),
                  mh.stretch_replace(eq5[2][2], eq6[2][2]),
                  mh.stretch_replace(eq5[2][5].copy(), eq6[2][9]),
                  mh.stretch_replace(eq5[2][-1], eq6[2][-1]),
                  FadeOut(eq5[2][3], eq5[2][10:13], eq5[2][29], eq5[2][37:40]),
                  ReplacementTransform(box3, box4),
                  run_time=1.5)
        self.wait(0.1)
        self.play(mh.rtransform(eq6[0][:], eq7[0][:], eq6[1], eq7[1],
                             eq6[2][:9], eq7[3][:9], eq6[2][-8:], eq7[3][-8:],
                                eq6[2][10], eq7[3][10], eq6[2][13], eq7[3][11],
                                eq6[2][28], eq7[3][13], eq6[2][31], eq7[3][14],
                                eq6[2][29], eq7[3][12],
                                eq6[2][11:13], eq7[2][1:]
                                ),
                  mh.rtransform(eq6[2][14:21], eq7[3][-8:-1], eq6[2][22:28], eq7[3][3:9],
                                eq6[2][32:34], eq7[2][1:]),
                  mh.stretch_replace(eq6[2][2].copy(), eq7[3][9]),
                  mh.stretch_replace(eq6[2][-1].copy(), eq7[3][-9]),
                  mh.stretch_replace(eq6[2][9], eq7[2][0]),
                  mh.fade_replace(eq6[2][21], eq7[3][12]),
                  mh.fade_replace(eq6[2][30], eq7[2][0]),
                  run_time=2)
        self.wait(0.1)
        self.play(mh.rtransform(eq7[:3], eq8[:3], eq7[3][0], eq8[3][0],
                                eq7[3][10:15], eq8[3][3:8]),
                  mh.fade_replace(eq7[3][1], eq8[3][1]),
                  mh.stretch_replace(eq7[3][2], eq8[3][2]),
                  mh.stretch_replace(eq7[3][9], eq8[3][2]),
                  mh.stretch_replace(eq7[3][15], eq8[3][8]),
                  mh.stretch_replace(eq7[3][-1], eq8[3][-1]),
                  FadeOut(eq7[3][3:9], shift=mh.diff(eq7[3][9], eq8[3][2])),
                  FadeOut(eq7[3][16:23], shift=mh.diff(eq7[3][15], eq8[3][8])),
                  run_time=1.7)
        self.wait(0.1)
        self.play(mh.rtransform(eq8[:2], eq9[:2], eq8[2][:], eq9[2][1:],
                                eq8[3][:3], eq9[3][:3], eq8[3][3:5], eq9[3][6:8],
                                eq8[3][5], eq9[3][5], eq8[3][6:8], eq9[3][3:5],
                                eq8[3][-1], eq9[3][-1]),
                  FadeIn(eq9[2][0], shift=mh.diff(eq8[2][0], eq9[2][1])))
        self.wait(0.1)
        self.play(mh.rtransform(eq9[0][:], eq10[0][2:], eq9[1], eq10[1], eq9[3], eq10[2], eq9[2][3], eq10[0][1]),
                  mh.stretch_replace(eq9[2][1], eq10[0][0]),
                  FadeOut(eq9[2][0], shift=mh.diff(eq9[2][1], eq10[0][0])),
                  FadeOut(eq9[2][2], shift=mh.diff(eq9[2][1], eq10[0][0], coor_mask=RIGHT)),
                  run_time=1.7)
        self.wait()


class AliceState(Scene):
    def construct(self):
        Tex.set_default(font_size=55)
        MathTex.set_default(font_size=55)

        eq1 = MathTex(r'P_A(M)', r'=', r'\frac1{\sqrt2}\left(\langle{\rm up}\vert M\vert{\rm up}\rangle +'
                                       r'\langle{\rm down}\vert M\vert{\rm down}\rangle\right)')
        eq2 = MathTex(r'P_B(M)', r'=', r'\frac1{\sqrt2}\left(\langle{\rm left}\vert M\vert{\rm left}\rangle',
                                       r'+\langle{\rm right}\vert M\vert{\rm right}\rangle\right)')
        eq3 = MathTex(r'\vert{\rm left}\rangle', r'=', r'\frac1{\sqrt2}\left(\vert{\rm up}\rangle+\vert{\rm down}\rangle\right)')
        eq4 = MathTex(r'\vert{\rm right}\rangle', r'=', r'\frac1{\sqrt2}\left(\vert{\rm up}\rangle-\vert{\rm down}\rangle\right)')
        eq1.to_edge(UP)
        eq2.next_to(eq1, DOWN)
        eq3.next_to(eq2, DOWN)
        eq4.next_to(eq3, DOWN)
        eq5 = MathTex(r'P_B(M)', r'=', r'\frac1{\sqrt2}\left(\frac12\left(\langle{\rm up}\vert + \langle{\rm down}\vert\right) M\left(\vert{\rm up}\rangle + \vert{\rm down}\rangle\right)',
                                       r'+\frac12\left(\langle{\rm up}\vert - \langle{\rm down}\vert\right) M\left(\vert{\rm up}\rangle - \vert{\rm down}\rangle\right)\right)')
        mh.align_sub(eq5, eq5[1], eq2[1]).shift(LEFT*0.5)
        eq5[3].next_to(eq5[2], DOWN, buff=0.1).align_to(eq5[2], RIGHT)
        eq6 = MathTex(r'P_B(M)', r'=', r'\frac1{2\sqrt2}\left(\left(\langle{\rm up}\vert + \langle{\rm down}\vert\right) M\left(\vert{\rm up}\rangle + \vert{\rm down}\rangle\right)',
                                       r'+\left(\langle{\rm up}\vert - \langle{\rm down}\vert\right) M\left(\vert{\rm up}\rangle - \vert{\rm down}\rangle\right)\right)')
        mh.align_sub(eq6, eq6[1], eq5[1])
        mh.align_sub(eq6[3], eq6[3][0], eq5[3][0])
        #eq6[2][6](eq5[2][6].copy().move_to(eq5[2][6], coor_mask=RIGHT))

        self.add(eq1)
        self.wait(0.1)
        self.play(FadeIn(eq2))
        self.wait(0.1)
        self.play(FadeIn(eq3))
        self.wait(0.1)
        self.play(FadeIn(eq4))
        self.wait(0.1)
        eq2_1 = eq2[2].copy()
        eq3_1 = eq3[2].copy()
        eq4_1 = eq4[2].copy()
        eq5_1 = eq5[2].copy()
        self.play(mh.rtransform(eq2[:2], eq5[:2], eq2[2][:5], eq5[2][:5],
                                eq2[2][12], eq5[2][22], eq2[2][13], eq5[2][24],
                                eq2[2][18], eq5[2][27], eq2[2][6], eq5[2][10],
                                eq2[2][11], eq5[2][13]),
                  mh.rtransform(eq3[2][5:18], eq5[2][23:36]),
                  mh.stretch_replace(eq2[2][5], eq5[2][5]),
                  FadeOut(eq2[2][14:18], target_position=eq5[2][25:27]),
                  FadeOut(eq2[2][7:11], shift=mh.diff(eq2[2][7:11], eq5[2][11:13], coor_mask=RIGHT)),
                  mh.rtransform(eq3_1[5], eq5[2][9], eq3_1[7:9], eq5[2][11:13],
                                eq3_1[10], eq5[2][14], eq3_1[12:16], eq5[2][16:20],
                                eq3_1[17], eq5[2][20], eq3[2][:2], eq5[2][6:8],
                                eq3[2][4], eq5[2][8]),
                  mh.fade_replace(eq3_1[6], eq5_1[10]),
                  mh.fade_replace(eq3_1[9], eq5_1[13]),
                  mh.fade_replace(eq3_1[11], eq5[2][15]),
                  mh.fade_replace(eq3_1[16], eq5[2][21]),
                  FadeOut(eq3[2][2:4], shift=mh.diff(eq3[2][4], eq5[2][8])),
                  FadeOut(eq3[:2]),
                  mh.stretch_replace(eq2[3][-1], eq5[3][-1]),
                  eq2[3][:-1].animate.shift(mh.diff(eq2[3][-2], eq5[3][-3])),
                  run_time=2)
        eq5_1.set_opacity(0)
        self.wait(0.1)
        self.play(mh.rtransform(eq2[3][0], eq5[3][0], eq2[3][1], eq5[3][10],
                                eq2[3][7], eq5[3][15], eq2[3][8], eq5[3][17],
                                eq2[3][9], eq5[3][24], eq2[3][15], eq5[3][29]),
                  FadeOut(eq2[3][2:7], shift=mh.diff(eq2[3][2:7], eq5[3][11:14], coor_mask=RIGHT)),
                  FadeOut(eq2[3][10:15], shift=mh.diff(eq2[3][10:15], eq5[3][25:29], coor_mask=RIGHT)),
                  mh.rtransform(eq4[2][5:18], eq5[3][18:31]),
                  mh.rtransform(eq4_1[5], eq5[3][4], eq4_1[7:9], eq5[3][6:8],
                                eq4_1[10], eq5[3][9], eq4_1[12:16], eq5[3][11:15],
                                eq4_1[17], eq5[3][16], eq4[2][:2], eq5[3][1:3],
                                eq4[2][4], eq5[3][3]),
                  mh.fade_replace(eq4_1[6], eq5[3][5]),
                  mh.fade_replace(eq4_1[9], eq5[3][8]),
                  mh.fade_replace(eq4_1[11], eq5[3][10]),
                  mh.fade_replace(eq4_1[16], eq5[3][15]),
                  FadeOut(eq4[2][2:4], shift=mh.diff(eq4[2][4], eq5[3][3])),
                  FadeOut(eq4[:2]),
                  run_time=2)
        self.wait(0.1)
        self.play(mh.rtransform(eq5[:2], eq6[:2], eq5[2][:2], eq6[2][:2], eq5[2][2:5], eq6[2][3:6],
                                eq5[2][5], eq6[2][6], eq5[2][9:], eq6[2][7:]),
                  mh.rtransform(eq5[2][6:8], eq6[2][:2], eq5[2][8], eq6[2][2]),
                  mh.rtransform(eq5[3][0], eq6[3][0], eq5[3][1:3], eq6[2][:2],
                                eq5[3][3], eq6[2][4], eq5[3][4:], eq6[3][1:]),
                  run_time=1.4)
        self.wait()
