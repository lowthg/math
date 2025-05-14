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


def unitVec2D(theta):
    return RIGHT * math.cos(theta) + UP * math.sin(theta)

def convexPolytopePoint(x, vectors, g=4.0, max_radius=4.0):
    r = max_radius
    a = 0.

    for v in vectors:
        a += math.pow(abs(np.inner(x, v)), g)

    a = math.pow(a, 1/g)

    if r * a > 1:
        r = 1/a

    return r


def convexPolytope2D(vectors, g=4., max_radius=10.0, scale=1.0, **kwargs):
    def f(t):
        x = unitVec2D(t)
        return x * min([convexPolytopePoint(x, v, g, max_radius) for v, g in zip(vectors, g)]) * scale
    return ParametricFunction(f, (0, 2*PI), **kwargs)

def convexPolytope3D(vectors, g=4., max_radius=4.0, scale=1.0, **kwargs):
    n = len(vectors)
    weights = np.ones(n) / n
    def f(u, v):
        x = OUT * math.cos(u) + (RIGHT * math.cos(v) + UP * math.sin(v)) * math.sin(u)
        return x * convexPolytopePoint(x, vectors, g, max_radius) * scale

    conv = Surface(f, u_range=[0, PI], v_range=[-PI, PI], checkerboard_colors=False,
                    **kwargs)

    return conv


class Intersect2D(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color=GREY
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        theta = 25*DEGREES
        scale=1.2
        vectors = [
            unitVec2D(theta)/4,
            unitVec2D(theta+PI/2)
        ]
        vectors2 = [
            unitVec2D(15*DEGREES) / 1.5,
            unitVec2D(135*DEGREES) / 2.4
        ]
        blue = ManimColor((50, 100, 180))
        red = ManimColor(RED.to_rgb()*0.7)
        g = [2.5, 3]
        setA = convexPolytope2D([vectors], g=[g[0]], stroke_opacity=0, fill_color=red, fill_opacity=1, scale=scale).set_z_index(0)
        setB = convexPolytope2D([vectors2], g=[g[1]], stroke_opacity=0, fill_color=blue, fill_opacity=1, scale=scale).set_z_index(0)
        setC = convexPolytope2D([vectors, vectors2], g, fill_color=(red+blue)*0.5, fill_opacity=1, stroke_opacity=0, scale=scale).set_z_index(1)
        eq1 = MathTex(r'C_1', font_size=80).move_to((LEFT*2.4 + DOWN*1.17)*scale).set_z_index(2)
        eq2 = MathTex(r'C_2', font_size=80).move_to((LEFT*0.1 + UP*2)*scale).set_z_index(2)
        eq3 = MathTex(r'C_1\cap C_2', font_size=80).set_z_index(2)#.move_to(LEFT*0.1 + UP*2)
        self.add(setA, setB, setC, eq1, eq2, eq3)


class Intersect3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=0*DEGREES)

        vectors = [
            (OUT + RIGHT)*0.45,
            (IN + RIGHT*1.1) * 0.4,
            UP * 0.5 + OUT * 0.2,
            #            RIGHT * 0.5 + UP * 0.15,
#            UP * 0.7,
#            OUT * 0.4 + UP * 0.1,
#            (RIGHT + UP) * 0.2,
        ]
        vectors2 = [
            RIGHT * 0.5,
            UP * 0.3,
            OUT * 0.5
        ]
        res=100

        convA = convexPolytope3D(vectors, g=4.0, scale=1.18, fill_opacity=0.8, stroke_opacity=0, resolution=[res, res], fill_color=BLUE)
        convB = convexPolytope3D(vectors2, g=2.0, scale=0.79, fill_opacity=0.8, stroke_opacity=0, resolution=[res, res], fill_color=RED, max_radius=8)



        self.add(convA, convB)
        self.add(Arrow3D(ORIGIN, OUT*4, color=WHITE))
        self.wait(0.2)
        self.begin_ambient_camera_rotation(rate=PI * 0.5)

        self.wait(1)


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