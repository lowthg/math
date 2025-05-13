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


class GCIforms(Scene):
    def construct(self):
        eq1 = MathTex(r'\mu_n(A\cap B)\ge\mu_n(A)\mu_n(B)')
        eq2 = MathTex(r'\mathbb P(X\in A\cap B)\ge\mathbb P(X \in A)\mathbb P(X\in B)')
        eq2.next_to(eq1, DOWN)#.align_to(eq1, LEFT)
        eq3 = MathTex(r'\mathbb P(X\in A, Y\in B)\ge\mathbb P(X \in A)\mathbb P(Y\in B)')
        eq3.next_to(eq2, DOWN)#.align_to(eq1, LEFT)
        eq4 = MathTex(r'\mathbb P(X\in A\vert Y\in B)\ge\mathbb P(X \in A)')
        eq4.next_to(eq3, DOWN)#.align_to(eq1, LEFT)
        eq5 = MathTex(r'\mathbb P(\lvert X_1\rvert\le1,\ldots,\lvert X_n\rvert\le1)\ge\\ \mathbb P(\lvert X_1\rvert\le1,\ldots,\lvert X_m\rvert\le1)\mathbb P(\lvert X_{m+1}\rvert\le1,\ldots,\lvert X_n\rvert\le1)')
        eq5.next_to(eq4, DOWN)#.align_to(eq1, LEFT)
        self.wait(0.1)
        self.play(FadeIn(eq1, eq2, eq3, eq4, eq5), run_time=1)
        self.wait(0.1)


class EqImageA(Scene):
    eq = 'A'

    def construct(self):
        self.add(MathTex(self.eq, font_size=100, stroke_width=1.5))

class EqImageB(EqImageA):
    eq = 'B'


class EqImagePAB(EqImageA):
    eq = r'\mathbb P(A\cap B)\ge\mathbb P(A)\mathbb P(B)'


class SimpleIntersect(ThreeDScene):
    def __init__(self, *args, **kwargs):
        config.background_color=WHITE
        ThreeDScene.__init__(self, *args, **kwargs)

    def construct(self):
        setA = Cube(side_length=2, fill_opacity=0.5, fill_color=BLUE, stroke_color=WHITE, stroke_opacity=0.5, stroke_width=1)
        setB = Octahedron(side_length=2, fill_opacity=0.5, fill_color=RED)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(setA)
        dt = 2
        self.begin_ambient_camera_rotation(rate=PI * 2 / dt)
        self.wait(dt)


class ConvexIntersect(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        #        axes = ThreeDAxes()
        cube = Cube(side_length=3, fill_opacity=0.7, fill_color=BLUE)
        points = [
            [1.93192757, 0.44134585, -1.52407061],
            [-0.93302521, 1.23206983, 0.64117067],
            [-0.44350918, -0.61043677, 0.21723705],
            [-0.42640268, -1.05260843, 1.61266094],
            [-1.84449637, 0.91238739, -1.85172623],
            [1.72068132, -0.11880457, 0.51881751],
            [0.41904805, 0.44938012, -1.86440686],
            [0.83864666, 1.66653337, 1.88960123],
            [0.22240514, -0.80986286, 1.34249326],
            [-1.29585759, 1.01516189, 0.46187522],
            [1.7776499, -1.59550796, -1.70240747],
            [0.80065226, -0.12530398, 1.70063977],
            [1.28960948, -1.44158255, 1.39938582],
            [-0.93538943, 1.33617705, -0.24852643],
            [-1.54868271, 1.7444399, -0.46170734]
        ]
        points = points + [[-x for x in p] for p in points]
        setA = ConvexHull3D(
            *points,
            faces_config = {"stroke_opacity": 0},
            graph_config = {
                "vertex_type": Dot3D,
                "edge_config": {
                    "stroke_color": BLUE,
                    "stroke_width": 2,
                    "stroke_opacity": 0.05,
                }
            }
        )

        dot = Dot3D(color=RED, radius=1).shift(RIGHT*0.5)
        self.set_camera_orientation(phi=60*DEGREES, theta=35*DEGREES)

        self.play(FadeIn(dot))
        self.add(setA)
        self.begin_ambient_camera_rotation(rate=PI * 0.1)
        self.wait(2)


class threed(ThreeDScene):
    def construct(self):
        #by default phi = 0, theta = -90
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

        axes = ThreeDAxes()
        cube = Cube(side_length=3, fill_opacity = 0.25, stroke_color = WHITE, stroke_width = 1)
        self.play(Write(cube))

        self.move_camera(phi = 0, theta = -90*DEGREES)
        self.wait()

        self.begin_ambient_camera_rotation(rate = -70*DEGREES, about = "theta")
        self.begin_ambient_camera_rotation(rate = 40*DEGREES, about = "phi")
        self.play(FadeToColor(cube, RED), run_time = 2)
        self.stop_ambient_camera_rotation(about = "theta")
        self.stop_ambient_camera_rotation(about = "phi")

        self.wait()
        self.play(Write(axes))
        self.move_camera(zoom = 0.8, theta = 30*DEGREES)
        self.wait()

        self.play(Rotate(cube, 360*DEGREES))
        self.wait()

        self.play(cube.animate.shift(RIGHT), cube.animate.scale(0.25))
        self.play(cube.animate.move_to(axes.c2p(4, 0, 0)))
        self.wait()

        self.move_camera(phi=75*DEGREES, theta=-45*DEGREES)
        self.wait()