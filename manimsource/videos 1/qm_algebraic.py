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
        self.wait()

