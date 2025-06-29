from manim import *
import numpy as np
import math
import sys
import scipy as sp
from networkx.classes import edges
from sorcery import switch

sys.path.append('../../')
import manimhelper as mh


class Pdefinition(Scene):
    def construct(self):
        eq1 = MathTex(r'{\rm\ expected\ value\ of\ }A', r'=', r'\langle\Psi\vert A\vert\Psi\rangle')
        eq1.to_edge(UR)

        eq15 = Tex(r'\underline{Event: projection $\pi$}', color=BLUE).set_opacity(1)
        eq15.next_to(eq1, DOWN).align_to(eq1, RIGHT)
        eq15[0][-1].set_opacity(0.9).next_to(eq15[0][0], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq16 = MathTex(r'{\rm probability}', r'=', r'P(\pi)')
        eq16.next_to(eq15, DOWN)
        eq23 = MathTex(r"P'(A)", r"=", r"P(\pi A\pi)/P(\pi)")
        eq23.next_to(eq16, DOWN)
        eq30 = Tex(r'\underline{unitary transform: $U$}', color=BLUE).set_opacity(1)
        eq30.next_to(eq23, DOWN)
        eq30[0][-1].set_opacity(0.9).next_to(eq30[0][0], DOWN, buff=0.04, coor_mask=UP).set_color(WHITE)
        eq31 = MathTex(r"P'(A)", r'=', r"P(U^*AU)")
        eq31.next_to(eq30, DOWN)

        eq1_1 = eq1.copy()
        eq2 = MathTex(r'P(A)', r'=', r'\langle\Psi\vert A\vert\Psi\rangle')
        eq2.move_to(ORIGIN).to_edge(DOWN, buff=1)
        mh.align_sub(eq1_1, eq1_1[1], eq2[1])
        eq3 = eq2.copy()
        mh.align_sub(eq3, eq3[1], eq1[1])
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

        self.add(eq1)
        self.wait(0.1)
        self.play(mh.rtransform(eq1.copy(), eq1_1), run_time=1.5)
        self.wait(0.1)
        shift = mh.diff(eq1_1[0][-1], eq2[0][-2], RIGHT)
        self.play(mh.rtransform(eq1_1[1:], eq2[1:], eq1_1[0][-1], eq2[0][-2]),
                  FadeOut(eq1_1[0][:-1], shift=shift),
                  FadeIn(eq2[0][:-2], eq2[0][-1], shift=shift),
                  run_time=1.5)
        self.wait(0.1)
        shift = mh.diff(eq1[0][-1], eq3[0][-2], RIGHT)
        self.play(mh.rtransform(eq2.copy(), eq3),
                  mh.rtransform(eq1[1:], eq3[1:], eq1[0][-1], eq3[0][-2]),
                  FadeOut(eq1[0][:-1], shift=shift),
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
        self.play(mh.rtransform(eq7[2][2:8].copy(), eq8[2][:]),
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
                  FadeOut(eq10),
                  run_time=2)

        self.wait(0.1)
        self.play(FadeIn(eq17[:2], eq17[2][:3], rate_func=linear), run_time=0.8)
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
                  run_time=2)
        self.wait(0.5)

        self.play(FadeIn(eq24, eq25[0]), run_time=1.2)
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
        self.play(FadeIn(eq30),mh.rtransform(eq29, eq31), FadeOut(eq24), run_time=2)

        self.wait()

