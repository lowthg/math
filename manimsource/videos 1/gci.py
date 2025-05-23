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

blue = ManimColor((50, 100, 180))
red = ManimColor(RED.to_rgb() * 0.7)

def unitVec2D(theta):
    return RIGHT * math.cos(theta) + UP * math.sin(theta)

def unitvec3D(u, v):
    return OUT * math.cos(u) + (RIGHT * math.cos(v) + UP * math.sin(v)) * math.sin(u)

def convexPolytopePoint(x, vectors, g=4.0, max_radius=4.0, symmetric=True):
    r = max_radius
    a = 0.

    if symmetric:
        for v in vectors:
            a += math.pow(abs(np.inner(x, v)), g)
    else:
        for v in vectors:
            a += math.pow(max(0., np.inner(x, v)), g)

    a = math.pow(a, 1/g)

    if r * a > 1:
        r = 1/a

    return r


def convexPolytope2D(vectors, g=[4.], max_radius=10.0, scale=1.0, symmetric=True, **kwargs):
    def f(t):
        x = unitVec2D(t)
        return x * min([convexPolytopePoint(x, v, g1, max_radius, symmetric) for v, g1 in zip(vectors, g)]) * scale
    return ParametricFunction(f, (0, 2*PI), **kwargs)


def convexPolytope3D(vectors, g=4., max_radius=4.0, scale=1.0, **kwargs):
    n = len(vectors)
    def f(u, v):
        x = unitvec3D(u, v)
        return x * convexPolytopePoint(x, vectors, g, max_radius) * scale

    conv = Surface(f, u_range=[0, PI], v_range=[-PI, PI], checkerboard_colors=False,
                    **kwargs)

    return conv


def intersectPolytopes(setA, setB, shift=0.0, **kwargs):
    intersect = VGroup()
    subA = setA.submobjects
    subB = setB.submobjects
    n = len(subA)
    assert len(subB) == n
    for i in range(n):
        objA = subA[i]
        objB = subB[i]
        ptsA = [p[0] for p in objA.get_cubic_bezier_tuples()]
        ptsB = [p[0] for p in objB.get_cubic_bezier_tuples()]
        r = [np.linalg.norm(pA) - np.linalg.norm(pB) for pA, pB in zip(ptsA, ptsB)]
        pts = []
        edges = []
        for j, k in ((0, 1), (1, 2), (2, 3), (3, 0)):
            if r[j] > 0 >= r[k] or r[k] > 0 >= r[j]:
                p = r[k] / (r[k] - r[j])
                pt = ptsA[j] * p + ptsA[k] * (1 - p)
                pts.append(pt)
                edges.append(j)

        if len(pts) > 0:
            ptsA = objA.get_cubic_bezier_tuples()
            ptsB = objB.get_cubic_bezier_tuples()
            objA2 = objA.copy()
            objB2 = objB.copy()
            for a, b, c, d in ((0, 1, 2, 3), (1, 2, 3, 0), (2, 3, 0, 1), (3, 0, 1, 2)):
                if (edges[0] == c and edges[1] == a) or (edges[0] == b and edges[1] == a):
                    edges[0], edges[1] = edges[1], edges[0]
                    pts[0], pts[1] = pts[1], pts[0]
                if edges[0] == a and edges[1] == c:
                    objA.set_points_as_corners([ptsA[a][0], pts[0], pts[1], ptsA[d][0]])
                    objB.set_points_as_corners([ptsB[a][0], pts[0], pts[1], ptsB[d][0]])
                    objA2.set_points_as_corners([pts[0], ptsA[b][0], ptsA[c][0], pts[1]])
                    objB2.set_points_as_corners([pts[0], ptsB[b][0], ptsB[c][0], pts[1]])
                    subA[i] = VGroup(objA, objA2)
                    subB[i] = VGroup(objB, objB2)
                if edges[0] == a and edges[1] == b:
                    objA.set_points_as_corners([ptsA[a][0], pts[0], pts[1], ptsA[c][0], ptsA[d][0]])
                    objB.set_points_as_corners([ptsB[a][0], pts[0], pts[1], ptsB[c][0], ptsB[d][0]])
                    objA2.set_points_as_corners([pts[0], ptsA[b][0], pts[1]])
                    objB2.set_points_as_corners([pts[0], ptsB[b][0], pts[1]])
                    subA[i] = VGroup(objA, objA2)
                    subB[i] = VGroup(objB, objB2)

            for j in range(len(pts)):
                pts[j] *= (1 + shift / np.linalg.norm(pts[j]))

            for j in range(0, len(pts), 2):
                intersect += Line3D(pts[j], pts[j + 1], **kwargs)
    return intersect


class Intersect2D(Scene):
    show_eqs=2
    show_A = 1
    show_B = 1
    show_o = False

    def shapeparams(self):
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
        g = [2.5, 3]

        return [vectors, vectors2], g, scale

    def construct(self):
        MathTex.set_default(font_size=120)
        vectors, g, scale = self.shapeparams()

        setA = convexPolytope2D([vectors[0]], g=[g[0]], stroke_opacity=0, fill_color=red, fill_opacity=1, scale=scale).set_z_index(0)
        setB = convexPolytope2D([vectors[1]], g=[g[1]], stroke_opacity=0, fill_color=blue, fill_opacity=1, scale=scale).set_z_index(0)
        setC = convexPolytope2D(vectors, g, fill_color=(red+blue)*0.5, fill_opacity=1, stroke_opacity=0, scale=scale).set_z_index(1)

        if self.show_eqs == 1:
            eq1 = MathTex(r'C_1').move_to((LEFT*2.4 + DOWN*1.17)*scale).set_z_index(2)
            eq2 = MathTex(r'C_2').move_to((LEFT*0.1 + UP*2)*scale).set_z_index(2)
            eq3 = MathTex(r'C_1\cap C_2').set_z_index(2)#.move_to(LEFT*0.1 + UP*2)
        elif self.show_eqs == 2:
            eq1 = MathTex(r'A').move_to((LEFT*2.4 + DOWN*1)*scale).set_z_index(2)
            eq2 = MathTex(r'B').move_to((LEFT*0.1 + UP*2)*scale).set_z_index(2)
            eq3 = MathTex(r'A\cap B').set_z_index(2)#.move_to(LEFT*0.1 + UP*2)
        else:
            eq1 = eq2 = eq3 = VGroup()

        if self.show_A:
            self.add(setA, eq1)
        if self.show_B:
            self.add(setB, eq2)
        if self.show_A and self.show_B:
            self.add(setC, eq3)
        if self.show_o:
            self.add(Dot(radius=0.2, color=WHITE, fill_opacity=0.6).set_z_index(5))


class Convexity(Intersect2D):
    def construct(self):
        vectors, g, scale = self.shapeparams()

        vec1 = [vectors[1]]
        g1 = [g[1]]

        setB = convexPolytope2D(vec1, g=g1, stroke_opacity=0, fill_color=blue, fill_opacity=1, scale=scale).set_z_index(0)

        def f(t):
            x = unitVec2D(t)
            res = x * min([convexPolytopePoint(x, v, g, 4.) for v, g in zip(vec1, g1)]) * scale

            a = PI * 0.85
            b = PI * 1.35
            s, t1 = 1, t
            if b > t - PI > a:
                s, t1 = -1, t - PI
            if b > t + PI > a:
                s, t1 = -1, t + PI
            if b > t1 > a:
                print('s=', s, 't1', t1)
                res += RIGHT * (1 - math.cos((t1 - a) / (b-a) * 2 * PI)) * s * 0.45

            return res

        setC = ParametricFunction(f, (0, 2 * PI), stroke_opacity=0, fill_color=blue, fill_opacity=1)

        self.add(setB)
        self.wait(0.1)
        dot1 = Dot(UP * 1.7 + LEFT*1.55, radius=0.2, fill_color=WHITE).set_z_index(10)
        dot2 = Dot(DOWN*2.4 + LEFT*0.85, radius=0.2, fill_color=WHITE).set_z_index(10)
        self.play(FadeIn(dot1, dot2))
        line1 = Line(dot1, dot2, color=YELLOW, stroke_width=8).set_z_index(9)
        self.play(Create(line1))
        setB2 = setB.copy()
        self.play(Transform(setB, setC))
        self.wait(0.1)
        self.play(Transform(setB, setB2))
        self.wait(0.1)
        self.play(FadeOut(dot2, line1))

        dot3 = Dot(-dot1.get_center(), radius=0.2, fill_color=WHITE).set_z_index(10)
        doto = Dot(ORIGIN, radius=0.2, fill_color=WHITE, fill_opacity=0.6).set_z_index(10)
        line2 = Line(dot1.get_center(), dot3.get_center(), color=YELLOW, stroke_width=8).set_z_index(9)

        self.play(FadeIn(doto, dot3), Create(line2))
        self.wait(0.1)
#        self.play(setB.animate.scale(-1), run_time=2)

        vec2 = [[
            UP*1.03,
            unitVec2D(-30 * DEGREES)*1.03,
            unitVec2D(210 * DEGREES)*1.03
#            (RIGHT * math.sqrt(3) + DOWN)/2,
#            (LEFT * math.sqrt(3) + DOWN) / 2,
        ]]
        setD = convexPolytope2D(vec2, g=[4.], stroke_opacity=0, fill_color=blue, fill_opacity=1, symmetric=False,
                                scale=2).set_z_index(1)
        setE = setD.copy().set_fill(color=GREY_C).set_z_index(0)
        self.play(ReplacementTransform(setB, setD))
        self.wait(0.1)
        self.add(setE)
        self.play(setD.animate.scale(-1, about_point=ORIGIN), run_time=2)



class Intersect3D(ThreeDScene):
    vectors1 = [
        (OUT + RIGHT) * 0.45,
        (IN + RIGHT * 1.1) * 0.4,
        UP * 0.5 * 0.8 + OUT * 0.2
    ]
    vectors2 = [
        RIGHT * 0.5,
        UP * 0.3,
        OUT * 0.5
    ]
    res = 80
    g = [4.0, 2.0]
    scale=[1.18, 1.09]
    rtime=1
    showA = True
    showB = True
    phi=60*DEGREES

    def shapes(self):
        res=[self.res, self.res]
        g = self.g
        convA = convexPolytope3D(self.vectors1, g=g[0], scale=self.scale[0], fill_opacity=0.7, stroke_opacity=0,
                                 resolution=res, fill_color=blue)
        convB = convexPolytope3D(self.vectors2, g=g[1], scale=self.scale[1], fill_opacity=0.7, stroke_opacity=0,
                                 resolution=res, fill_color=red, max_radius=8)
        if self.showA and self.showB:
            intersect = intersectPolytopes(convA, convB, shift = 0.02, thickness=0.02, color=GREY, resolution=8,
                                           fill_opacity=0.7, stroke_opacity=0.8)
        else:
            intersect = VGroup()
        return convA, convB, intersect

    def construct(self):
        self.set_camera_orientation(phi=self.phi, theta=0*DEGREES)
        convA, convB, intersect = self.shapes()
        if self.showA:
            self.add(convA)
        if self.showB:
            self.add(convB)
        if self.showA and self.showB:
            self.add(intersect)
#        self.add(Arrow3D(ORIGIN, OUT*4, color=WHITE))
#        self.wait(0.2)
        self.begin_ambient_camera_rotation(rate=PI*2/self.rtime)

        self.wait(self.rtime)

class Intersect3DSlab(Intersect3D):
    vectors1 = [
        (OUT + RIGHT*2) * 0.45,
        (IN + RIGHT * 1.1*2) * 0.4,
        UP * 0.5*2 * 0.8 + OUT * 0.2
    ]
    rtime=4

    def shapes(self):
        thickness=1/4
        vectors2 = [unitvec3D(0 * DEGREES, 0) / thickness]
        res=[100, 50]
        du = PI/res[0]
        rmax = 6
        umax = math.floor(math.acos(thickness / rmax)/du)*du
        rmax2 = thickness / math.cos(umax)
        g = self.g
        convA = convexPolytope3D(self.vectors1, g=g[0], scale=self.scale[0], fill_opacity=0.7, stroke_opacity=0, resolution=res, fill_color=blue)
        convB = convexPolytope3D(vectors2, g=g[1], scale=self.scale[1], fill_opacity=0.7, stroke_opacity=0, resolution=res, fill_color=red, max_radius=rmax2)
        for s in convB.submobjects:
            if s.u2 > umax and PI - s.u1 > umax:
                s.set_fill(color=GREY).set_fill(opacity=0.3)
        VGroup(convA, convB).rotate(15*DEGREES, axis=UP)
        intersect = intersectPolytopes(convA, convB, shift = 0.02, thickness=0.02, color=GREY, resolution=8, fill_opacity=0.7, stroke_opacity=0.8)
        newB = Cylinder(radius=6, height=2/3*self.scale[1], color=GREY, stroke_opacity=0, fill_opacity=0.7, fill_color=red, show_ends=True, resolution=20)
        newB.rotate(15*DEGREES, axis=UP)
        return convA, convB, intersect

class Intersect3DEllipsoids(Intersect3D):
    vectors1 = [
        OUT * 0.3,
        RIGHT * 0.45,
        UP * 0.8,
    ]
    showB = False
    phi=80*DEGREES
    def __init__(self, *args, **kwargs):
        Intersect3D.__init__(self, *args, **kwargs)
        for v in self.vectors1:
            v[:] = rotate_vector(v, 30*DEGREES, RIGHT+UP)
        for v in self.vectors2:
            v[:] = rotate_vector(v, -10*DEGREES, RIGHT)

    g = [2, 2]
    rtime = 4


class Intersect3DEllipsoid(Intersect3D):
    rtime=4
#    res=40
    vectors1 = [
        (OUT * 0.8 + RIGHT*1.1) * 0.45,
        (IN * 0.8 + RIGHT * 1.1*1.1) * 0.4,
        UP * 0.5 * 0.8 + OUT * 0.2 * 0.8
    ]


class Intersect3DGeneral(Intersect3D):
    rtime = 4
    res=100
    g = [4, 3]
    vectors1 = [
        (OUT * 0.8 + RIGHT*1.1) * 0.45,
        (IN * 0.8 + RIGHT * 1.1*1.1) * 0.4,
        UP * 0.5 * 0.8 + OUT * 0.2 * 0.8
    ]
    vectors2 = [
        (OUT * 0.2 + LEFT*0.1)*1,
        (OUT * 0.2 + UP * 0. + RIGHT * -0.17)*1.02,
        RIGHT * 0.45 + UP * 0.1 + OUT * 0.1,
        UP * 0.7,

    ]
    def __init__(self, *args, **kwargs):
        Intersect3D.__init__(self, *args, **kwargs)
        for v in self.vectors1:
            v[1] *= 0.95
            v[:] = rotate_vector(v, 30 * DEGREES, OUT+DOWN)
            v[1] *= 1
        for v in self.vectors2:
            v[2] *= 1.1
            v[1] *= 1
            v[:] = rotate_vector(v, 50*DEGREES, RIGHT)


class GCIStatement(Scene):
    anim = True # put in animation on formula
    do_indep = False # just do independence

    def construct(self):
        txt1 = Tex(r'\bf\underline{The Gaussian Correlation Inequality}', color=BLUE)
        txt2 = Tex(r'For centrally symmetric convex $A,B\subseteq\mathbb R^n$ then')
        txt3 = MathTex(r'\mathbb P(A\cap B)\ge\mathbb P(A)\mathbb P(B)')[0]
        txt4 = Tex(r'under the standard normal distribution on $\mathbb R^n$.')

        txt2.next_to(txt1, DOWN)
        txt3.next_to(txt2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.2)
        txt4.next_to(txt3, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.2)
        gp = VGroup(txt1, txt2, txt3, txt4)
        txt2.align_to(gp, LEFT)
        txt4.align_to(gp, LEFT)
        gp.move_to(ORIGIN).to_edge(UP)
        txt3[0][:6].set(stroke_width=2, family=True)

        if not self.do_indep:
            self.add(txt1, txt2, txt3, txt4)
            if self.anim:
                self.wait()
                txtbig = txt3.copy()
                for x in txtbig:
                    x.set(stroke_width=2)
                txtbig[:6].scale(1.2, about_point=txt3[3].get_center())
                txtbig[6:7].scale(1.2)
                txtbig[7:].scale(1.2, about_point=txt3[8].get_center())
    #            self.play(txt3[:6].animate.scale(1.2).set(stroke_width=4), rate_func=rate_functions.there_and_back, run_time=2)
                self.play(Transform(txt3[:6], txtbig[:6]), rate_func=rate_functions.there_and_back, run_time=2)
                self.play(Transform(txt3[6:7], txtbig[6:7]), rate_func=rate_functions.there_and_back, run_time=2)
                self.play(Transform(txt3[7:], txtbig[7:]), rate_func=rate_functions.there_and_back, run_time=2)
                self.wait()
        if self.do_indep:
            txt5 = Tex(r'\underline{$A, B$ independent}', stroke_width=1.7).to_edge(LEFT, buff=0.6)
            txt6 = MathTex(r'\mathbb P(A\cap B)=\mathbb P(A)\mathbb P(B)', stroke_width=1.5)[0]
            txt6.next_to(txt5, DOWN, buff=0.3).align_to(txt5, LEFT)
            self.add(txt5)
            self.wait()
            self.play(ReplacementTransform(txt3.copy(), txt6), run_time=2)
            self.wait()


class StandardNormal(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=PI/2, theta=-PI/2)

        def p0(x):
            return math.exp(-x*x/2)

        xmax = 2.5
        ax = Axes(x_range=[-xmax, xmax + 0.2], y_range=[0, 1.15], x_length=8, y_length=2,
                  axis_config={'color': WHITE, 'stroke_width': 4, 'include_ticks': False,
                               "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "shade_in_3d": True,
                               },
#                  shade_in_3d=True,
                  ).set_z_index(1)


#        ax.x_axis.set(shade_in_3d=True)
        ax[0].submobjects[0].set(shade_in_3d=True)
        ax_o = ax.coords_to_point(0, 0)
        ax.shift(-ax_o)
        ax_o=ORIGIN
        xlen = ax.coords_to_point(xmax, 0)[0] - ax_o[0]
        ylen = ax.coords_to_point(0, 1)[1] - ax_o[1]

        plt1 = ax.plot(p0, x_range=[-xmax, xmax], color=BLUE, shade_in_3d=True).set_z_index(2)
        fill1 = ax.get_area(plt1, color=BLUE, opacity=0.5, shade_in_3d=True).set_z_index(2)
        eq1 = MathTex(r'p(x)=\frac1{\sqrt{2\pi}}e^{-\frac12x^2}', font_size=35, shade_in_3d=True)[0]
        eq2 = MathTex(r'{p(x,y)=\frac1{2\pi}e^{-\frac12(x^2+y^2)}}', font_size=35, color=WHITE, stroke_width=1.7, stroke_color=WHITE, shade_in_3d=True)[0]

        eq1.set_z_index(3).move_to(ax.coords_to_point(-xmax, 1.1), UL)
        eq2.set_z_index(3).move_to(ax.coords_to_point(-xmax, 1), UL)

        gp1 = VGroup(ax, plt1, fill1, eq1, eq2).rotate(PI/2, axis=RIGHT, about_point=ax_o)
        eq2.shift(DOWN*xlen/2)
        self.add(ax)
        self.wait(0.2)
        self.play(LaggedStart(AnimationGroup(Create(plt1, rate_func=linear), FadeIn(eq1)),
                              FadeIn(fill1), lag_ratio=0.5), run_time=1.5)
        self.wait(0.1)

        sq1 = Surface(lambda u, v: u * RIGHT + v * UP, u_range=[-xlen, xlen], v_range=[-xlen, xlen], fill_opacity=0.3,
                      stroke_opacity=0.4, checkerboard_colors=[RED_D, RED_E])
        self.remove(ax)
        self.add(ax)

        self.move_camera(phi=70*DEGREES, theta=-120*DEGREES)
        gp2 = gp1[:-2].copy()
        gp2.set(shade_in_3d=True)
        self.play(Rotate(gp2, -90*DEGREES, OUT, about_point=ax_o), FadeIn(sq1))
        ax.y_axis.set_z_index(3)
        self.play(gp1[1:-1].animate.shift(xlen*UP), gp2[1:].animate.shift(xlen*RIGHT))

        def p1(x, y):
            return (RIGHT * x + UP * y) * xlen/xmax + OUT * math.exp(-(x*x+y*y)/2) * ylen
        sq1.set_z_index(4)
        colors = [
            ManimColor(RED_D.to_rgb()*0.5),
            ManimColor(RED_E.to_rgb() * 0.5)
        ]
        surf1 = Surface(p1, u_range=[-xmax, xmax], v_range=[-xmax, xmax], fill_opacity=0.9,
                      stroke_opacity=0.8, checkerboard_colors=colors, stroke_color=WHITE).set_z_index(200, family=True)
        line1 = Line(OUT * ylen, OUT * ylen * 1.12, stroke_width=4, stroke_color=WHITE).set_z_index(300)
        self.add(line1)
        self.play(ReplacementTransform(sq1, surf1, rate_func=lambda t: smooth(min(t*2, 1))),
                  FadeIn(eq2, rate_func=lambda t: smooth(min(t*2, 1) - max(t*4 - 3, 0))),
                  FadeOut(eq1, rate_func=lambda t: smooth(max(t*4 - 3, 0))),
                  run_time=4)


class VectorX(Scene):
    def construct(self):
        eq1 = MathTex(r'X = (X_1,X_2,\ldots, X_n)', stroke_width=1.3)[0]
        eq1[0].set(stroke_width=1.5)
        self.add(eq1)

class DensityX(Scene):
    stroke_width=1.3
    def eq1(self):
        return MathTex(r'p_X(x_1,\ldots,x_n) {{=}} (2\pi)^{-\frac n2} {{e^{-\frac12(x_1^2+\cdots+x_n^2) } }}', stroke_width=self.stroke_width)

    def construct(self):
        self.add(self.eq1())


class DensityGeneral(DensityX):
    stroke_width = 1.2

    def construct(self):
        eq1 = self.eq1()
        MathTex.set_default(stroke_width=self.stroke_width)
        self.add(eq1)
        self.wait()
        eq2 = MathTex(r'p_X(x){{=}}\frac1{(2\pi)^{\frac n2}\lvert C\rvert }\, {{e^{-\frac12x^Tx} } }}')
        eq2.next_to(eq1[1], ORIGIN, submobject_to_align=eq2[1]).align_to(eq1, LEFT)
        eq2[2][2:9].move_to(eq2[2], coor_mask=RIGHT)
#        eq2[0][:3].move_to(eq1[0][:3], coor_mask=RIGHT)
        eq2_1 = eq2[0][3].copy().move_to(eq1[0][3:-1], coor_mask=RIGHT)
        eq2_2 = eq2[3][5:].copy().move_to(eq1[3][6:-1], coor_mask=RIGHT)
        self.play(FadeOut(eq1[0][3:-1], eq1[3][6:-1]), FadeIn(eq2_1, eq2_2), rate_func=linear)
        self.play(ReplacementTransform(eq1[0][:3] + eq2_1 + eq1[0][-1] + eq1[1] + eq1[3][:5] + eq2_2 +
                                       eq1[2][:4] + eq1[2][5:8],
                                       eq2[0][:3] + eq2[0][3] + eq2[0][-1] + eq2[1] + eq2[3][:5] + eq2[3][5:] +
                                       eq2[2][2:6] + eq2[2][6:9]),
                  FadeOut(eq1[3][5], target_position=eq2[3][5].get_left()),
                  FadeOut(eq1[3][-1], target_position=eq2[3][-1].get_right()),
                  FadeOut(eq1[2][4], target_position=eq2[2][7]),
                  FadeIn(eq2[2][:2], target_position=eq1[2][:8].get_top() + eq2[2][:2].height/2*UP),
                  run_time=2)
        eq3 = MathTex(r'p_X(x){{=}}\frac1{(2\pi)^{\frac n2}\lvert C\rvert }\, {{e^{-\frac12x^TC^{-1}x} } }}')
        eq3.next_to(eq2[1], ORIGIN, submobject_to_align=eq3[1]).align_to(eq2, LEFT)
        self.play(ReplacementTransform(eq2[:2] + eq2[2][:-3] + eq2[3][:7] + eq2[3][-1],
                                       eq3[:2] + eq3[2][:-3] + eq3[3][:7] + eq3[3][-1]),
                  FadeIn(eq3[2][-3:], eq3[3][-4:-1]))
        self.add(eq3)

        self.wait()



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


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True, 'fps': 15}):
        StandardNormal().render()