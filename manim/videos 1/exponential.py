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
        eq1 = MathTex(r'e^{i\pi}+1=0', font_size=160)[0]
        eq2 = MathTex(r'0\ 1\ {}^i\ \pi\ e', font_size=160)[0]
        eq3 = MathTex(r'e\ {}^i\ \pi\ 1\ 0', font_size=160)[0]
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
        eq3 = MathTex(r'\sqrt{-1}', font_size=70, color=BLUE)[0].next_to(eq1[1], UL, buff=0.8)
        arr1 = Arrow(eq3.get_corner(DR) + DR * 0.1, eq1[1].get_corner(UL), color=RED, buff=0)
        self.play(FadeIn(eq3, arr1), run_time=1)
        self.wait(0.1)
        rad = 0.6
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
