from manim import *
import numpy as np
import math
import sys
import scipy as sp
from networkx.classes import edges

sys.path.append('../../')
import manimhelper as mh

blue = ManimColor((50, 100, 180))
red = ManimColor(RED.to_rgb() * 0.7)

def scale_to_obj(source: Mobject, target: Mobject):
    return source.scale_to_fit_height(target.height).move_to(target)


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
        line1 = Line(dot1.get_center(), dot2.get_center(), color=YELLOW, stroke_width=8).set_z_index(9)
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
    colors = [blue, red]
    intersect = {'thickness': 0.02, 'shift': 0.02, 'color': GREY,
                 'resolution': 8, 'fill_opacity': 0.7, 'stroke_opacity': 0.8}

    def shapes(self):
        res=[self.res, self.res]
        g = self.g
        convA = convexPolytope3D(self.vectors1, g=g[0], scale=self.scale[0], fill_opacity=0.7, stroke_opacity=0,
                                 resolution=res, fill_color=self.colors[0])
        convB = convexPolytope3D(self.vectors2, g=g[1], scale=self.scale[1], fill_opacity=0.7, stroke_opacity=0,
                                 resolution=res, fill_color=self.colors[1], max_radius=8)
        if self.showA and self.showB:
            intersect = intersectPolytopes(convA, convB, **self.intersect)
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
    # showA = False
    # showB = False
    phi=80*DEGREES
    def __init__(self, *args, **kwargs):
        Intersect3D.__init__(self, *args, **kwargs)
        for v in self.vectors1:
            v[:] = rotate_vector(v, 30*DEGREES, RIGHT+UP)
        for v in self.vectors2:
            v[:] = rotate_vector(v, -10*DEGREES, RIGHT)

    g = [2, 2]
    rtime = 4


class Intersect3DEllipsoidsBoundary(Intersect3DEllipsoids):
    intersect = {'thickness': 0.05, 'shift': 0.04, 'color': YELLOW,
                 'resolution': 16, 'fill_opacity': 1, 'stroke_opacity': 1}
    rtime = 1


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

class Necessary(Intersect2D):
    show_eqs=0
    show_o=True

    def construct(self):
        theta = 30 * DEGREES
        vectors = [
            unitVec2D(theta) / 4,
            unitVec2D(theta + PI / 2)
        ]
        vectors2 = [
            unitVec2D(15 * DEGREES) / 1.5,
            unitVec2D(135 * DEGREES) / 2.4
        ]
        scale = 1.0
        kwargs = {'stroke_opacity': 0, 'fill_opacity': 0.7}

        g1 = 2
        g2 = 4

        u = ValueTracker(0.0)
        v = ValueTracker(0.0)
        dot = Dot(radius=0.2, color=WHITE, fill_opacity=0.6).set_z_index(5)

        def f(t):
            x = unitVec2D(t)
            p = u.get_value()
            shift = LEFT * v.get_value()*2.5
            return x * convexPolytopePoint(x, vectors, g1) * scale * (1-p+p*math.cos(t-theta)**6) + shift

        def g(t):
            x = unitVec2D(t)
            p = u.get_value()
            shift = RIGHT * v.get_value() * 2.5
            return x * convexPolytopePoint(x, vectors2, g2) * scale * (1-p+p*math.sin(t-theta)**6) + shift

        def h():
            setA = ParametricFunction(f, (0, 2 * PI), fill_color=red, **kwargs)
            setB = ParametricFunction(g, (0, 2 * PI), fill_color=blue, **kwargs)
            return VGroup(setA, setB, dot)

        sets = always_redraw(h)
        self.add(sets)
        self.wait(0.1)
        self.play(u.animate.set_value(1.), run_time=2.5)
        self.wait(0.1)
        self.play(u.animate.set_value(0.), run_time=1)
        self.wait(0.1)
        self.play(v.animate.set_value(1.), run_time=2.5)
        self.wait(0.1)
        self.play(v.animate.set_value(0.), run_time=1)
        self.wait()



class GCIStatement(Scene):
    anim = True # put in animation on formula
    do_indep = False # just do independence
    def statement(self):
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
        return gp

    def construct(self):
        txt1, txt2, txt3, txt4 = tuple(self.statement())

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
    colors = [
        ManimColor(RED_D.to_rgb() * 0.5),
        ManimColor(RED_E.to_rgb() * 0.5)
    ]

    def plots(self, display=True, ymax=1.15):
        self.set_camera_orientation(phi=PI/2, theta=-PI/2)

        def p0(x):
            return math.exp(-x * x / 2)

        xmax = 2.5
        ax = Axes(x_range=[-xmax, xmax + 0.2], y_range=[0, ymax], x_length=8, y_length=2*ymax/1.15,
                  axis_config={'color': WHITE, 'stroke_width': 4, 'include_ticks': False,
                               "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "shade_in_3d": True,
                               },
                  #                  shade_in_3d=True,
                  ).set_z_index(1)
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
        if display:
            self.add(ax)
            self.wait(0.2)
            self.play(LaggedStart(AnimationGroup(Create(plt1, rate_func=linear), FadeIn(eq1)),
                                  FadeIn(fill1), lag_ratio=0.5), run_time=1.5)
            self.wait(0.1)

        sq1 = Surface(lambda u, v: u * RIGHT + v * UP, u_range=[-xlen, xlen], v_range=[-xlen, xlen], fill_opacity=0.3,
                      stroke_opacity=0.4, checkerboard_colors=[RED_D, RED_E])

        if display:
            self.remove(ax)
            self.add(ax)
            self.move_camera(phi=70*DEGREES, theta=-120*DEGREES)
        else:
            self.set_camera_orientation(phi=70*DEGREES, theta=-120*DEGREES)

        gp2 = gp1[:-2].copy()
        gp2.set(shade_in_3d=True)
        ax.y_axis.set_z_index(3)

        if display:
            self.play(Rotate(gp2, -90*DEGREES, OUT, about_point=ax_o), FadeIn(sq1))
            self.play(gp1[1:-1].animate.shift(xlen*UP), gp2[1:].animate.shift(xlen*RIGHT))
        else:
            gp2.rotate(-90*DEGREES, about_point=ax_o)
            gp1[1:-1].shift(xlen*UP)
            gp2[1:].shift(xlen*RIGHT)

        def p1(x, y):
            return (RIGHT * x + UP * y) * xlen/xmax + OUT * math.exp(-(x*x+y*y)/2) * ylen
        sq1.set_z_index(4)
        surf1 = Surface(p1, u_range=[-xmax, xmax], v_range=[-xmax, xmax], fill_opacity=0.9,
                      stroke_opacity=0.8, checkerboard_colors=self.colors, stroke_color=WHITE).set_z_index(200, family=True)
        line1 = Line(OUT * ylen, OUT * ylen * 1.12, stroke_width=4, stroke_color=WHITE).set_z_index(300)
        if display:
            self.add(line1)
            self.play(ReplacementTransform(sq1, surf1, rate_func=lambda t: smooth(min(t*2, 1))),
                      FadeIn(eq2, rate_func=lambda t: smooth(min(t*2, 1) - max(t*4 - 3, 0))),
                      FadeOut(eq1, rate_func=lambda t: smooth(max(t*4 - 3, 0))),
                      run_time=4)

        return xmax, xlen, ylen, VGroup(ax, gp2[0], line1)

    def construct(self):
        self.plots()


class LinearComb(GCIStatement):
    def statement(self):
        gp1 = GCIStatement.statement(self)
        txt5 = Tex(r'under any centered normal distribution on $\mathbb R^n$.')
        mh.align_sub(txt5, txt5[0][:5], gp1[3]).move_to(ORIGIN, coor_mask=RIGHT)
        txt2 = gp1[1].copy().align_to(txt5, LEFT)

        return gp1, txt2, txt5


    def construct(self):
        gp1, txt2, txt5 = self.statement()

        red3 = ManimColor((255, 50, 0))
        txt4 = gp1[3]
        line1 = Line(txt4[0][5:16].get_corner(DL), txt4[0][5:16].get_corner(UR),
                     stroke_width=10, stroke_color=red3)
        mat_str = [[r'u_{11}Z_1', r'u_{12}Z_2', r'\cdots', r'u_{1m}Z_m'],
                   [r'u_{21}Z_1', r'u_{22}Z_2', r'\cdots', r'u_{2m}Z_m'],
                   [r'u_{n1}Z_1', r'u_{n2}Z_2', r'\cdots', r'u_{nm}Z_m']]
        eq1_str = ['+'.join(row) for row in mat_str]
        eq1 = MathTex(r'X_1', r'=', eq1_str[0])
        eq2 = MathTex(r'X_2', r'=', eq1_str[1])
        eq3 = MathTex(r'\vdots')
        eq4 = MathTex(r'X_n', r'=', eq1_str[2])

        eq5 = MathTex(r'\begin{pmatrix} X_1 \\ X_2 \\ \vdots \\ X_n\end{pmatrix}', r'=',
                      ''.join([r'\begin{pmatrix}', eq1_str[0], r'\\', eq1_str[1], r'\\ \vdots\vdots\vdots \\', eq1_str[2], r'\end{pmatrix}']),
                      r'\begin{pmatrix} Z_1 \\ Z_2 \\ \vdots \\ Z_m\end{pmatrix}')
        eq6 = MathTex(r'X', r'=', r'UZ')
        eq7 = Tex(r'joint normal', font_size=45, color=RED)
        eq8 = Tex(r'independent standard normal', font_size=45, color=RED)

        # eq5 = MathTex(r'\begin{pmatrix} X_1 \\ X_2 \\ \vdots \\ X_n\end{pmatrix}', r'=',
        #               r'\begin{pmatrix} m_{11}Z_1 & m_{12}Z_2 & \cdots & m_{1n}Z_n\\'
        #               r'm_{21}Z_1 & m_{22}Z_2 & \cdots & m_{2n}Z_n \\'
        #               r'\vdots & \vdots & & \vdots \\'
        #               r'm_{n1}Z_1 & m_{n2}Z_2 & \cdots & m_{nn}Z_n \end{pmatrix}')

        # eq5.next_to(gp1, DOWN, submobject_to_align=eq5[:3])
        mh.align_sub(eq5, eq5[:3], ORIGIN).to_edge(DOWN)
        mh.align_sub(eq1, eq1[0][0], eq5[0][5])
        mh.align_sub(eq2, eq2[0][0], eq5[0][7])
        mh.align_sub(eq4, eq4[0][0], eq5[0][12])
        mh.align_sub(eq1, eq1[1][0], eq5[1], coor_mask=RIGHT)
        eq7.next_to(eq1[0], UP, buff=1)
        mh.align_sub(eq8, eq8[0][-1], eq7[0][-1]).move_to(eq1[2], coor_mask=RIGHT).shift(RIGHT)
        arr1 = Arrow(eq7[0][-6].get_bottom(), eq1[0].get_top(), color=RED, stroke_width=4, buff=0.1)
        arr2 = Arrow(eq8[0][-14].get_bottom(), eq1[2][3].get_top(), color=RED, stroke_width=4, buff=0.1)
        arr3 = Arrow(eq8[0][-14].get_bottom(), eq1[2][9].get_top(), color=RED, stroke_width=4, buff=0.1)
        arr4 = Arrow(eq8[0][-14].get_bottom(), eq1[2][19].get_top(), color=RED, stroke_width=4, buff=0.1)
        mh.align_sub(eq2, eq2[1][0], eq5[1], coor_mask=RIGHT)
        mh.align_sub(eq4, eq4[1][0], eq5[1], coor_mask=RIGHT)
        eq3.move_to(eq5[0][9:12]).move_to(eq2[1], coor_mask=RIGHT)
        eq5[2][47:50].move_to(eq5[2][26:29], coor_mask=RIGHT)
        eq5[2][50:53].move_to(eq5[2][32:35], coor_mask=RIGHT)
        eq5[2][53:56].move_to(eq5[2][42:45], coor_mask=RIGHT)
        mh.align_sub(eq6, eq6[1], eq5[1]).move_to(ORIGIN, coor_mask=RIGHT)
        gp2 = VGroup(*(eq5[2][i:j] for i,j in ((5, 8), (11,14), (17, 20), (21, 24),
                                               (26, 29), (32,35), (38, 41), (42, 45),
                                               (47, 56),
                                               (56, 59), (62,65), (68, 71), (72, 75))))
        gp3 = VGroup(eq5[2][:5], eq5[2][-5:], *gp2[:])

        self.add(gp1)
        self.wait(0.1)
        self.play(Create(line1), run_time=0.8)
        self.wait(0.1)
        self.play(FadeIn(eq1))
        self.play(LaggedStart(FadeIn(eq7, arr1), FadeIn(eq8, arr2, arr3, arr4), lag_ratio=0.3),
                  run_time=1.5)
        self.play(LaggedStart(FadeIn(eq2), FadeIn(eq3), FadeIn(eq4), lag_ratio=0.3))
        self.wait(0.1)
        self.play(mh.rtransform(eq1[0][:], eq5[0][5:7], eq2[0][:], eq5[0][7:9], eq3[0][:], eq5[0][9:12],
                                eq3[0][:].copy(), eq5[2][47:50], eq3[0][:].copy(), eq5[2][50:53],
                                eq3[0][:].copy(), eq5[2][53:56],
                                eq4[0][:], eq5[0][12:14]),
                  mh.rtransform(eq1[2][:], eq5[2][5:26], eq2[2][:], eq5[2][26:47], eq4[2][:], eq5[2][56:77]),
                  FadeOut(eq7, eq8, arr1, arr2, arr3, arr4))
        self.play(FadeIn(eq5[0][:5], eq5[0][-5:], eq5[2][:5], eq5[2][-5:]),
                  ReplacementTransform(eq1[1], eq5[1]),
                  ReplacementTransform(eq2[1], eq5[1]),
                  ReplacementTransform(eq4[1], eq5[1]),
                  )
        self.play(mh.rtransform(eq5[2][8:10], eq5[3][5:7], eq5[2][14:16], eq5[3][7:9], eq5[2][24:26], eq5[3][12:14], eq5[2][16:19].copy(), eq5[3][9:12]),
                  mh.rtransform(eq5[2][29:31], eq5[3][5:7], eq5[2][35:37], eq5[3][7:9], eq5[2][45:47], eq5[3][12:14], eq5[2][37:40].copy(), eq5[3][9:12]),
                  mh.rtransform(eq5[2][59:61], eq5[3][5:7], eq5[2][65:67], eq5[3][7:9], eq5[2][75:77], eq5[3][12:14], eq5[2][67:70].copy(), eq5[3][9:12]),
                  FadeOut(eq5[2][10], eq5[2][16], eq5[2][20]),
                  FadeOut(eq5[2][31], eq5[2][37], eq5[2][41]),
                  FadeOut(eq5[2][61], eq5[2][67], eq5[2][71]),
                  FadeIn(eq5[3][:5], eq5[3][-5:], rate_func=rush_into),
                  run_time=2)
        self.wait(0.1)
#        self.play(mh.stretch_replace(eq5[2], eq6[2][0].copy().set_opacity(0)), run_time=1.5)
        yscale = eq6[2][0].height / gp2.height
        xscale = eq6[2][0].width / gp2.width
        target = gp3.copy().stretch(yscale, 1).stretch(xscale, 0).move_to(eq6[2][0]).set_opacity(0)
        self.play(Transform(gp3, target),
                  FadeIn(eq6),
                  ReplacementTransform(eq5[1], eq6[1]),
                  mh.stretch_replace(eq5[3], eq6[2][1].copy().set_opacity(0)),
                  mh.stretch_replace(eq5[0], eq6[0].copy().set_opacity(0)),
                  mh.fade_replace(eq5[1], eq6[1].copy().set_opacity(0)),
                  run_time=2)
        self.wait(0.1)

        eq6.generate_target().next_to(gp1, DOWN, buff=1)
        eq10 = MathTex(r'U^{-1}A', r'=', r'\left\{z\in\mathbb R^m\colon Uz\in A\right\}')
        eq11 = MathTex(r'U^{-1}B', r'=', r'\left\{z\in\mathbb R^m\colon Uz\in B\right\}')
        eq10.next_to(eq6.target, DOWN)
        mh.align_sub(eq11, eq11[1], eq10[1]).next_to(eq10, DOWN, coor_mask=UP)
        self.play(LaggedStart(MoveToTarget(eq6), FadeIn(eq10, eq11), lag_ratio=0.4), run_time=1.5)
        gp4 = VGroup(eq10, eq11)
        eq12 = Tex(r'convex', color=RED, font_size=45).next_to(gp4, RIGHT, buff=1.4)
        eq13 = Tex(r'also\\ convex', color=RED, font_size=45).next_to(gp4, LEFT, buff=1.4)
        arr5 = Arrow(eq12.get_left() + LEFT*0.1, eq10[2][-2].get_right(), color=RED, stroke_width=4, buff=0)
        arr6 = Arrow(eq12.get_left() + LEFT*0.1, eq11[2][-2].get_right(), color=RED, stroke_width=4, buff=0)
        arr7 = Arrow(eq13.get_right(), eq10[0][0].get_left(), color=RED, stroke_width=4, buff=0.1)
        arr8 = Arrow(eq13.get_right(), eq11[0][0].get_left(), color=RED, stroke_width=4, buff=0.1)
        self.play(FadeIn(arr5, arr6, eq12))
        self.play(FadeIn(arr7, arr8, eq13))
        self.wait(0.1)

        eq14str = [r'\mathbb P(X\in A\cap B)', r'=', r'\mathbb P(Z\in U^{-1}A\cap U^{-1}B)',
                       r'\ge', r'\mathbb P(Z\in U^{-1}A)\mathbb P(Z\in U^{-1}B)',
                       r'=', r'\mathbb P(X\in A)\mathbb P(X\in B)']
        eq14 = MathTex(*eq14str)
        mh.align_sub(eq14, eq14[2:5], ORIGIN).to_edge(DOWN, buff=0.2)
        eq14[0].align_to(eq14[2], RIGHT)
        eq14[-1].align_to(eq14[-3], LEFT)
        eq14[1].rotate(PI/2).move_to(eq14[0]).next_to(eq14[2], UP, coor_mask=UP)
        eq14[-2].rotate(PI/2).move_to(eq14[-1]).next_to(eq14[-3], UP, coor_mask=UP)
        eq14[0].next_to(eq14[1], UP, coor_mask=UP)
        eq14[-1].next_to(eq14[-2], UP, coor_mask=UP)
        gp5 = VGroup(eq6, eq10, eq11, eq12, eq13, arr5, arr6, arr7, arr8)

        eq15 = Tex(r'applying GCI to $Z$', color=BLUE, font_size=40)
        eq15.next_to(eq14[3], UP).move_to(VGroup(eq14[1], eq14[-2]), coor_mask=RIGHT)
        self.play(gp5.animate.next_to(eq14, UP, coor_mask=UP),
                  FadeIn(eq14[:3]), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq14[3:5], eq15))
        self.wait(0.1)
        self.play(FadeIn(eq14[5:]))
        self.wait(0.1)
        self.play(FadeOut(eq14[1:3], eq14[4:6], eq15),
                  eq14[3].animate.shift(mh.diff(eq14[4][0], eq14[-1][0]) * UP))
        self.wait(0.1)
        gp6 = VGroup(eq14[0], eq14[3], eq14[-1])
        self.play(FadeOut(gp5), gp6.animate.shift(UP), run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(txt4[0][5:16], line1))
        self.play(ReplacementTransform(gp1[1], txt2),
                  ReplacementTransform(gp1[3][0][:5], txt5[0][:5]),
                  ReplacementTransform(gp1[3][0][16:], txt5[0][16:]),
                  FadeIn(txt5[0][5:16]))
        self.wait(0.1)
        self.play(FadeOut(gp6))

        self.wait()

class GCIStatementXY(LinearComb):
    def construct(self):
        self.statement(animate=True)

    def statement(self, animate=False):
        gp1, txt1, txt2 = LinearComb.statement(self)

        txt3 = Tex(r'For centrally symmetric convex $A\subseteq \mathbb R^m$, $B\subseteq\mathbb R^n$ then')
        mh.align_sub(txt3, txt3[:27], txt1[:27])
        txt4 = MathTex(r'\mathbb P(X\in A, Y\in B)', r'\ge', r'\mathbb P(X\in A)\mathbb P(Y\in B)')
        mh.align_sub(txt4, txt4[1], gp1[2][6]).move_to(ORIGIN, coor_mask=RIGHT)
        txt5 = Tex(r'for any centered jointly normal $X$ in $\mathbb R^m$ and $Y$ in $\mathbb R^n$.')
        mh.align_sub(txt5, txt5[0][6:14], txt2[0][8:16]).align_to(txt3, LEFT)

        if not animate:
            return VGroup(gp1[0], txt3, txt4, txt5)

        self.add(gp1[0], txt1, gp1[2], txt2)

        self.play(mh.rtransform(txt1[0][:28], txt3[0][:28], txt1[0][-9:], txt3[0][-9:]),
                  mh.rtransform(txt1[0][-7:-5].copy(), txt3[0][28:30]),
                  mh.fade_replace(txt1[0][-5].copy(), txt3[0][30]))
        self.wait(0.05)
        # self.play(mh.rtransform(gp1[2][:2], txt4[0][:2], gp1[2][2], txt4[0][4],
        #                         gp1[2][4:6], txt4[0][8:],
        #                         gp1[2][6], txt4[1][0], gp1[2][7:9], txt4[2][:2],
        #                         gp1[2][9:13], txt4[2][4:8], gp1[2][-2:], txt4[2][-2:]),
        #           FadeIn(txt4[0][2:4], shift=mh.diff(gp1[2][2], txt4[0][4])),
        #           FadeIn(txt4[0][5:8], shift=mh.diff(gp1[2][4], txt4[0][8])),
        #           FadeOut(gp1[2][3], shift=mh.diff(gp1[2][4], txt4[0][8])),
        #           FadeIn(txt4[2][2:4], shift=mh.diff(gp1[2][9], txt4[2][4])),
        #           FadeIn(txt4[2][8:10], shift=mh.diff(gp1[2][-2], txt4[2][-2])))
        # self.wait(0.05)
        self.play(FadeOut(gp1[2]))
        self.play(mh.rtransform(txt2[0][5:16], txt5[0][3:14], txt2[0][16:22], txt5[0][21:27],
                                txt2[0][-3:], txt5[0][-3:]),
                  mh.fade_replace(txt2[0][:5], txt5[0][:3]),
                  FadeIn(txt5[0][14:21], shift=mh.diff(txt2[0][15:17], txt5[0][14:21])*RIGHT),
                  FadeOut(txt2[0][22:-3], shift=mh.diff(txt2[0][21], txt5[0][26])*RIGHT),
                  FadeIn(txt5[0][27:-3], target_position=txt2[0][22:-3]))
        self.wait(0.05)
        self.play(FadeIn(txt4[0]))
        self.wait(0.05)
        self.play(FadeIn(txt4[1]))
        self.wait(0.05)
        self.play(FadeIn(txt4[2]))

        txt5_1 = txt5[0][14:27]
        line1 = Line(txt5_1.get_corner(DL), txt5_1.get_corner(DR), color=RED, stroke_width=5)
        self.wait(0.1)
        self.play(Create(line1))
        txt6 = Tex(r'$(X, Y)$ is joint normal').next_to(line1, DOWN, buff=1)
        p0 = line1.get_bottom()
        arr1 = Arrow(txt6[0][9].get_top()*UP + p0*RIGHT, p0, stroke_width=5, color=RED, buff=0.1)
        self.play(FadeIn(arr1, txt6))

        center = txt5.get_bottom()*UP * 0.5 + DOWN * config.frame_y_radius * 0.5
        eq1 = MathTex(r"\mathbb P(X'\in A'\cap B')", r'\ge', r"\mathbb P(X'\in A')\mathbb P(X'\in B')")
        eq1.move_to(center)

        eq2 = Tex(r'where: ', r"$X'=(X,Y)$", r"$A'=A\times\mathbb R^n$", r"$B'=\mathbb R^m\times B$")
        eq2[2].next_to(eq2[1][2], ORIGIN, submobject_to_align=eq2[2][2]).shift(DOWN*0.5)
        eq2[3].next_to(eq2[2][2], ORIGIN, submobject_to_align=eq2[3][2]).shift(DOWN*0.5)
        eq2.next_to(eq1, DOWN)

        eq4 = txt4.copy()
        eq4.next_to(eq1[1], ORIGIN, submobject_to_align=eq4[1])
        self.play(ReplacementTransform(txt4.copy(), eq4), run_time=2)
        self.play(mh.rtransform(eq4[0][:3], eq1[0][:3], eq4[0][3:5], eq1[0][4:6],
                                eq4[0][-2], eq1[0][-3], eq4[0][-1], eq1[0][-1]),
                  FadeIn(eq1[0][3], shift=mh.diff(eq4[0][2], eq1[0][2])),
                  FadeIn(eq1[0][6], shift=mh.diff(eq4[0][4], eq1[0][6])),
                  FadeOut(eq4[0][5:8]),
                  FadeIn(eq2),
                  FadeIn(eq1[0][7]),
                  FadeIn(eq1[0][-2], shift=mh.diff(eq4[0][-2], eq1[0][-3])),
                  mh.rtransform(eq4[1], eq1[1], eq4[2][:3], eq1[2][:3],
                                eq4[2][3:5], eq1[2][4:6], eq4[2][5:8], eq1[2][7:10],
                                eq4[2][9:11], eq1[2][12:14], eq4[2][11], eq1[2][15]
                                ),
                  mh.fade_replace(eq4[2][8], eq1[2][10]),
                  FadeIn(eq1[2][3], shift=mh.diff(eq4[2][2], eq1[2][2])),
                  FadeIn(eq1[2][6], shift=mh.diff(eq4[2][4], eq1[2][5])),
                  FadeIn(eq1[2][11], shift=mh.diff(eq4[2][8], eq1[2][10])),
                  FadeIn(eq1[2][14], shift=mh.diff(eq4[2][10], eq1[2][13])),
                  )
        self.wait(0.1)
        self.play(FadeOut(line1, arr1, eq1, eq2, txt6), run_time=1.5)
        self.wait()

class  GCIConditional(GCIStatementXY):
    def construct(self):
        gp1 = GCIStatementXY.statement(self, animate=False)
        self.add(gp1)
        self.wait(0.1)
        eq1 = gp1[2].copy()

        eq2 = MathTex(r'\frac{\mathbb P(X\in A, Y\in B)}{\mathbb P(Y\in B)}', r'\ge', r'\mathbb P(X\in A)')
        eq3 = MathTex(r'\mathbb P(X\in A\vert Y\in B)', r'\ge', r'\mathbb P(X\in A)')

        self.play(eq1.animate.move_to(gp1.get_bottom()*UP*0.6 + mh.pos(DOWN)*0.4),
                  run_time=1.5)
        mh.align_sub(eq2, eq2[1], eq1[1])
        mh.align_sub(eq3, eq3[1], eq2[1])
        self.play(mh.rtransform(eq1[0][:], eq2[0][:10], eq1[1], eq2[1],
                                eq1[2][:6], eq2[2][:6], eq1[2][6:], eq2[0][11:]),
                  FadeIn(eq2[0][10]),
                  run_time=2)
        self.wait(0.05)
        self.play(mh.rtransform(eq2[0][:5], eq3[0][:5], eq2[0][-4:], eq3[0][-4:],
                                eq2[1:], eq3[1:]),
                  mh.rtransform(eq2[0][6:10], eq3[0][-4:]),
                  mh.fade_replace(eq2[0][5], eq3[0][5]),
                  FadeOut(eq2[0][10:13]),
                  run_time=1.5)
        self.wait()

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



class DensityZ(StandardNormal):
    cov = [1.0, 1.0, 0.7]

    def construct(self):
        xmax = 1.5
        xlen = 6
        zmax = 4
        zlen = 2
        zmaxplot = zmax * 1.2
        c = self.cov
        det = c[0] * c[1] - c[2] * c[2]
        assert det > 0 and c[0] > 0 and c[1] > 0
        c_inv = [c[1]/det, c[0]/det, -c[2]/det]

        xscale = xlen/xmax
        zscale = zlen/zmax
        xadj = 1.05

        ax = ThreeDAxes([0, xmax], [0, xmax], [0, zmax], xlen*xadj, xlen*xadj, zlen*1.1,
                        axis_config={'color': WHITE, 'stroke_width': 2, 'include_ticks': False,
                                     "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                                     "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                                     },
                        )
        op = 0.5
        ax.x_axis.set_stroke(opacity=op)
        ax.x_axis.set_fill(opacity=op)
        ax.y_axis.set_stroke(opacity=op)
        ax.y_axis.set_fill(opacity=op)
        ax.z_axis.set_stroke(opacity=op)
        ax.z_axis.set_fill(opacity=op)
        ax.x_axis.get_tip().set_stroke(opacity=0)
        ax.y_axis.get_tip().set_stroke(opacity=0)
        ax.z_axis.get_tip().set_stroke(opacity=0)
        origin = ax.coords_to_point(0, 0, 0)

        scaley = 0.1
        maxw = 1

        rmin = 0.1


        def prob(u, v):
            a = math.sqrt(u * v)
            b = math.exp(c_inv[2] * a)
            w = math.exp(-0.5*(c_inv[0]*u + c_inv[1]*v)) * (b+1/b) / a
            return w

        err = [0.0]
        zmax2 = zmax * 1.1

        def f(u, v):
            u = math.pow(u/xmax, 2)*xmax
            v = math.pow(v/xmax, 2)*xmax
            w = prob(u, v)

            if w > zmaxplot:
                def f(t):
                    return prob(u *(1-t) + xmax * t, v*(1-t) + xmax * t) - zmaxplot

                t1 = sp.optimize.bisect(f, 0, 1, maxiter=100)
                (u, v) = (u *(1-t1) + xmax * t1, v*(1-t1) + xmax * t1)


            if w > zmaxplot:
                w = zmaxplot

            return origin + (u * RIGHT + v * UP) * xscale + w * OUT * zscale

        x0 = 0.01


        surf = Surface(f, u_range=[x0, xmax], v_range=[x0, xmax], fill_opacity=0.5,
                        stroke_opacity=0.8, checkerboard_colors=self.colors, stroke_color=WHITE,
                       resolution=40, should_make_jagged=True).set_z_index(200)

        for obj in surf.submobjects:
            zvals = [(p[0][2] - origin[2])/zscale for p in obj.get_cubic_bezier_tuples()]
            h = sum(zvals)/4
            # h = max(zvals)
            assert len(zvals) == 4
            z0 = zmax*0.

            op = min(1-(h-z0)/(zmaxplot-z0),1)

            obj.set_opacity(op)
            obj.set_stroke(opacity=op)

        print(err)
#        self.set_camera_orientation(phi=0, theta=-PI/2)
        gp = VGroup(ax, surf)
        self.add(gp)
        theta = PI/2 * 0
        gp.rotate(-PI/2, RIGHT, about_point=origin)
        gp.rotate(-PI/2 - theta, UP, about_point=origin)
        ax.z_axis.rotate(-PI/4+theta, UP, about_point=origin)
        gp.rotate(PI/2*0.2, RIGHT, about_point=origin)
        gp.move_to(ORIGIN)

#        surf.rotate()
#        self.move_camera(phi=70 * DEGREES, theta=-120 * DEGREES)





class JointNormal(StandardNormal):
    times = [0., 1., 4.]
    rate_func=[rate_functions.smooth]

    @staticmethod
    def scalings(t):
        t0 = min(t, 1)
        a = 1 + t0
        b = 1 / (1 + t0 * 0.5)
        if t > 1:
            theta = 45 * DEGREES * (t-1)
        else:
            theta = 0.
        return a, b, theta

    def matrixVals(self, coeffs, t, invert=False):
        a, b, theta = self.scalings(t)
        coeffs[3] = a * b
        c = math.cos(theta)
        s = math.sin(theta)
        if invert:
            a, b, s = 1 / a, 1 / b, -s
        coeffs[0] = a * c * c + b * s * s
        coeffs[1] = b * c * c + a * s * s
        coeffs[2] = 2 * (b - a) * c * s

    def construct(self):
        ymax = 0.15 + 2/1.5
        xmax, xlen, ylen, gp = self.plots(display=False, ymax=ymax)
        self.set_camera_orientation(phi=71 * DEGREES, theta=-110 * DEGREES)
        xax = gp[0].x_axis.set_opacity(0)
        gp[1].y_axis.set_opacity(0)
        # create axis again, due to clipping problems
        line1 = Arrow(xax.get_start() + LEFT*0.2, xax.get_end() + RIGHT*0.3, color=WHITE, stroke_width=4,
                      max_tip_length_to_length_ratio=0.4 * DEFAULT_ARROW_TIP_LENGTH / xlen,
                      ).set_z_index(0).rotate(90*DEGREES, RIGHT, ORIGIN)
        self.add(gp[:2], line1)
        #gp[0].x_axis.shift(IN*0.1)#.rotate(3*DEGREES, UP)

        coeffs = [2, 1, 0, 1]

        def p1(x, y):
            return (RIGHT * x + UP * y) * xlen/xmax + OUT * math.exp(-(coeffs[0] * x*x + coeffs[1]*y*y + coeffs[2]*x*y)/2) * ylen * coeffs[3]

        tval = ValueTracker(self.times[0])

        def f():
            t = tval.get_value()
            self.matrixVals(coeffs, t)

            surf1 = Surface(p1, u_range=[-xmax, xmax], v_range=[-xmax, xmax], fill_opacity=0.9,
                          stroke_opacity=0.8, checkerboard_colors=self.colors, stroke_color=WHITE).set_z_index(200, family=True)
            return surf1

        surf = always_redraw(f)
#        cmat = MathTex(r'C=\begin{pmatrix} 2.0 & 2.0 \\ 2.0 & 2.0 \end{pmatrix}').to_edge(DR)
        self.add(surf)
        for i in range(1, len(self.times)):
            self.play(tval.animate.set_value(self.times[i]), run_time=self.times[i]-self.times[i-1], rate_func=self.rate_func[0])

class XMX(Scene):
    def construct(self):
        eq1 = MathTex(r'X^\prime =MX', stroke_width=1.3, font_size=100).to_edge(DL)
        self.add(eq1)

class JointNormal2(JointNormal):
    times = [0., 8.]
    rate_func = [linear]

    @staticmethod
    def scalings(t):
        a = math.exp(math.sin(t*PI))
        b = 1/math.pow(a, 0.7)
        theta = 0.
        if t > 2.5:
            if t > 3:
                theta = t-2.75
            else:
                theta = (t-2.5)**2

        return a, b, theta

class ConvexTransforms(Intersect3D):
    showB = False
    rtime = 1
    colors = [blue, blue]
    vectors1 = [
        (OUT + RIGHT) * 0.45,
        (IN + RIGHT) * 0.4,
        UP * 0.5 * 0.8 + OUT * 0.2,
        UP*0.5 + RIGHT * 0.5,
    ]
    scale = [0.8, 1.09]

    def construct(self):
        self.set_camera_orientation(phi=self.phi, theta=30 * DEGREES)
        convA, _, _ = self.shapes()

        tval = ValueTracker(0.)
        def f():
            t = tval.get_value()
            set = convA.copy()
            mat = np.identity(3)
            if t < 2:
                mat[0, 1] = (1 - math.cos(t * PI)) * 0.7
            if 1.5 < t < 3.5:
                mat[1, 2] = (1 - math.cos((t-1.5) * PI)) * 0.5
            if 3 < t < 5:
                mat[0, 2] = (1 - math.cos((t-3) * PI)) * 0.5
            if 4 < t < 6:
                mat[1, 0] = (1 - math.cos((t-4) * PI)) * 0.7

            mat[0, 0] = 1 + 0.3 * math.sin(t*PI/3.5)
            mat[1, 1] = 1 + 0.2 * (math.sin((t-1)*PI/5.5) + math.sin(PI/5.5))
            mat[2, 2] = 1 - 0.1 * (math.sin((t-2)*PI/4.5) + math.sin(2*PI/4.5))
            set.apply_matrix(mat)
            direct = unitvec3D(t * PI/2, t * PI/4)
            set.rotate(t * PI/3, direct, ORIGIN)

            return set

        set = always_redraw(f)
        self.add(set)
        self.begin_ambient_camera_rotation(rate=PI /3)
        self.play(tval.animate.set_value(6.), rate_func=linear, run_time=8.)

class MatrixVals(Scene):
    animclass=JointNormal
    def construct(self):
        MathTex.set_default(stroke_width=1.2)
        cmat = MathTex(r'C=\begin{pmatrix} -2.0 & -2.00 \\ -2.0 & -2.00 \end{pmatrix}')[0].to_edge(DR)
        self.add(cmat)
        pts = []
        for i,j in ((3,7), (7, 12), (12, 16), (16, 21)):
            cmat[i:j].set_opacity(0)
            pts.append(cmat[i+2].get_center())

        tval = ValueTracker(0.)
        coeffs = [0, 0, 0, 0]
        jn = self.animclass()

        def f():
            t = tval.get_value()
            jn.matrixVals(coeffs, t, invert=True)
            vals = [coeffs[0], coeffs[2]/2, coeffs[2]/2, coeffs[1]]
            for i in range(len(vals)):
                if -0.00001 < vals[i] <= 0:
                    vals[i] = 0.001
            eq = MathTex(r'{:.1f}'.format(vals[0]), r'{:.1f}'.format(vals[1]),
                         r'{:.1f}'.format(vals[2]), r'{:.1f}'.format(vals[3]))
            for i in range(4):
                j = 1 if vals[i] >= 0 else 2
                eq[i].next_to(pts[i], ORIGIN, submobject_to_align=eq[i][j])
            return eq

        mat = always_redraw(f)
        self.add(mat)
        times = jn.times
        for i in range(1, len(times)):
            self.play(tval.animate.set_value(times[i]), run_time=times[i]-times[i-1], rate_func=jn.rate_func[0])
        self.wait(1)

class DensityFuncsBad(Scene):
    def construct(self):
        eq1 = MathTex(r'p_X(x) = \frac1{(2\pi)^{\frac n2}\lvert C\rvert}\,e^{-\frac12 x^TCx}')
        eq2 = MathTex(r'p_Z(z)=\frac1{(8\pi)^{\frac n2}\lvert C\rvert\sqrt{\lvert z_1\ldots z_n\rvert}}',
                      r'\sum_{\epsilon_1,\ldots,\epsilon_n=\pm1}e^{-\frac12x^TCx}')
        eq3 = Tex(r'where $x=(\epsilon_1\sqrt{z_1},\ldots,\epsilon_n\sqrt{z_n})$')
        eq2.next_to(eq1, DOWN)
        eq3.next_to(eq2[1], DOWN)
        gp = VGroup(eq1, eq2, eq3).move_to(ORIGIN).to_edge(DOWN).set_z_index(1)
        box = SurroundingRectangle(gp, fill_opacity=0.7, fill_color=BLACK, stroke_opacity=0, corner_radius=0.15)

        self.add(box, eq1, eq2, eq3)

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

class Trick(Scene):

    def construct(self):
        eq1 = MathTex(r'X=(X_1^{2\!\!\!\!\!},X_2^{2\!\!\!\!\!},\ldots,X_n^{2\!\!\!\!\!})')[0].set_z_index(1)
        eq2 = MathTex(r'Z=(X_1^{2\!\!\!\!\!},X_2^2,\ldots,X_n^2)')[0].set_z_index(1)
        eq2.next_to(eq1, DOWN).align_to(eq1, LEFT)
        VGroup(eq1[4], eq1[8], eq1[16]).set_opacity(0)
        box1 = SurroundingRectangle(VGroup(eq1, eq2), corner_radius=0.15, fill_color=BLACK, fill_opacity=0.7,
                                    stroke_opacity=0)
        VGroup(eq1, eq2, box1).to_edge(DOWN)
        self.add(eq1, box1)
        self.wait()
        self.play(ReplacementTransform((eq1[1:4] + eq1[5:8] + eq1[9:16] + eq1[17:]).copy(),
                                       eq2[1:4] + eq2[5:8] + eq2[9:16] + eq2[17:]),
                  mh.fade_replace(eq1[0].copy(), eq2[0]),
                  FadeIn(eq2[4], target_position=eq1[4]),
                  FadeIn(eq2[8], target_position=eq1[8]),
                  FadeIn(eq2[16], target_position=eq1[16]),
                  run_time=2)
        self.wait()

class NonconvexZ(Scene):
    def construct(self):
        ax = Axes(x_range=[-1, 1.1], y_range=[-1, 1], x_length=6, y_length=4,
                  axis_config={'color': WHITE, 'stroke_width': 2, 'include_ticks': False,
                               "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "stroke_opacity": 1,
                               },
                  ).set_z_index(2)
        ax.shift(-ax.coords_to_point(0, 0))
        ax2 = ax.copy().set_z_index(4)
        ax2.x_axis.set_stroke(opacity=0.5)
        ax2.y_axis.set_stroke(opacity=0.5)

        eq1 = MathTex(r'X_1', font_size=36).next_to(ax.x_axis.get_right(), UL, buff=0.17).set_z_index(1)
        eq2 = MathTex(r'X_2', font_size=36).next_to(ax.y_axis.get_top(), DR, buff=0.1).set_z_index(1)

        theta = 30*DEGREES
        vectors = [ unitVec2D(theta) * 0.4, unitVec2D(theta+90*DEGREES) * 1.2]
        setA = convexPolytope2D([vectors], g=[2.3], stroke_opacity=0, fill_color=blue, fill_opacity=1).set_z_index(3)
        dotpos = unitVec2D(theta) * 2
        dot1 = Dot(radius=0.12, fill_opacity=0.7).move_to(dotpos).set_z_index(5)
        dot2 = dot1.copy().move_to(dotpos * UL)
        dot3 = dot1.copy().move_to(dotpos * DR)
        dot4 = dot1.copy().move_to(dotpos * DL)
        eq3 = MathTex(r'Z=(X_1^2, X_2^2)', font_size=40).next_to(dot1, UR, buff=0.05).set_z_index(6)

        eqZ = eq3[0][0]
        txt1 = Tex(r'\bf same $Z$', stroke_color=GREY, fill_color=WHITE, stroke_width=1.2, font_size=40).set_z_index(10)
        txt1.move_to(dot1.get_corner(DL) + DOWN * 0.3 + LEFT * 0.85).set_z_index(7).scale(1.3)

        arrcol=YELLOW
        arrop = 0.7
        arr1 = CurvedArrow(dot1.get_corner(UL), dot2.get_corner(UR), stroke_width=6, radius=6, color=arrcol).set_z_index(6)
        arr2 = CurvedArrow(dot1.get_corner(DR), dot3.get_corner(UR), stroke_width=6, radius=-6, color=arrcol).set_z_index(6)
        arr3 = Arrow(dot1.get_corner(DL), dot4.get_corner(UR), stroke_width=6, buff=0, color=arrcol).set_z_index(6)
        box1 = SurroundingRectangle(ax, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0, corner_radius=0.15)
        arr1.set_stroke(opacity=arrop)
        arr1.tip.set_opacity(arrop)
        arr2.set_stroke(opacity=arrop)
        arr2.tip.set_opacity(arrop)
        arr3.set_stroke(opacity=arrop)
        arr3.tip.set_opacity(arrop)
        eqA = MathTex(r'A', stroke_width=1.2, color=blue).move_to(LEFT+UP*0.75).set_z_index(10)

        self.add(box1, ax, ax2, eq1, eq2)
        self.wait(0.1)
        self.play(FadeIn(setA, eqA))
        self.wait(0.1)
        self.play(FadeIn(dot1, eq3))
        self.wait(0.1)
        self.play(ReplacementTransform(dot1.copy(), dot2),
                  ReplacementTransform(dot1.copy(), dot3),
                  run_time=2)
        self.play(ReplacementTransform(dot2.copy(), dot4),
                  ReplacementTransform(dot3.copy(), dot4),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeIn(arr1, arr2, arr3, txt1))
        self.wait()

class GCIAlt(Scene):
    def create_gci(self, skip=False):
        txt1 = Tex(r'\bf\underline{The Gaussian Correlation Inequality}', color=BLUE)
        txt2 = Tex(r'\bf (Alternative form)}', color=BLUE)
        txt3 = Tex(r'For centered multivariate normal $X_1,X_2,\ldots,X_n$')
        txt4 = Tex(r'and integer $1\le k < n$ then')
        eq1 = MathTex(r'\mathbb P(\lvert X_1\rvert\le 1,\ldots,\lvert X_n\rvert\le 1)',
                      r'\ge',
                      r'\mathbb P(\lvert X_1\rvert\le 1,\ldots,\lvert X_k\rvert\le 1)',
                      r'\mathbb P(\lvert X_{k+1}\rvert\le 1,\ldots,\lvert X_n\rvert\le 1)')
        txt2.next_to(txt1, DOWN)
        txt3.next_to(txt2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.2)
        txt4.next_to(txt3, DOWN).align_to(txt3, LEFT)
        eq1[0].next_to(VGroup(txt3, txt4), DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.6)
        eq1[1].next_to(eq1[0], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
        eq1[2:].next_to(eq1[1], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)

        VGroup(txt1, txt2, txt3, txt4, eq1).move_to(ORIGIN)

        if not skip:
            self.add(txt1, txt2)
            self.wait(0.1)
            self.play(FadeIn(txt3, txt4))
            self.wait(0.1)
            self.play(FadeIn(eq1[0]))
            self.wait(0.1)
            self.play(FadeIn(eq1[1]))
            self.wait(0.1)
            self.play(FadeIn(eq1[2]))
            self.wait(0.1)
            self.play(FadeIn(eq1[3]))
            self.wait(0.1)

        eq2 = MathTex(r'\mathbb P(\lvert X_1\rvert\le r_1,\ldots,\lvert X_n\rvert\le r_n)',
                      r'\ge',
                      r'\mathbb P(\lvert X_1\rvert\le r_1,\ldots,\lvert X_k\rvert\le r_k)',
                      r'\mathbb P(\lvert X_{k+1}\rvert\le r_{k+1},\ldots,\lvert X_n\rvert\le r_n)')
        eq2[0].next_to(eq1[0][0], ORIGIN, submobject_to_align=eq2[0][0]).move_to(eq1[0], coor_mask=RIGHT)
        eq2[2].next_to(eq1[2][0], ORIGIN, submobject_to_align=eq2[2][0], coor_mask=UP)
        eq2[3].next_to(eq1[3][0], ORIGIN, submobject_to_align=eq2[3][0], coor_mask=UP)
        eq2[2:].move_to(eq1[2:], coor_mask=RIGHT)

        to_fade = [eq1[0][7], eq1[0][18], eq1[2][7], eq1[2][18], eq1[3][9], eq1[3][20]]
        if not skip:
            self.play(Transform(eq1[0][:7] + eq1[0][8:18] + eq1[0][19],
                                           eq2[0][:7] + eq2[0][9:19] + eq2[0][21]),
                      Transform(eq1[2][:7] + eq1[2][8:18] + eq1[2][19],
                                           eq2[2][:7] + eq2[2][9:19] + eq2[2][21]),
                      Transform(eq1[3][:9] + eq1[3][10:20] + eq1[3][21],
                                           eq2[3][:9] + eq2[3][13:23] + eq2[3][25]),
                      FadeOut(*to_fade),
                      FadeIn(eq2[0][7:9], eq2[0][19:21], eq2[2][7:9], eq2[2][19:21], eq2[3][9:13], eq2[3][23:25]),
                      run_time=5, rate_func=there_and_back_with_pause)
            self.add(*to_fade)
        self.wait(0.1)
        eq3 = MathTex(r'\mathbb P(\max_i\lvert X_i\rvert\le 1)', r'\ge',
                      r'\mathbb P(\max_{i\le k}\lvert X_i\rvert\le 1)',
                      r'\mathbb P(\max_{i > k}\lvert X_i\rvert\le 1)')
        eq4 = eq3.copy().move_to(ORIGIN).move_to(eq1[1], coor_mask=UP)
        eq3[0].next_to(eq1[0][0], ORIGIN, submobject_to_align=eq3[0][0])#.move_to(eq1[0], coor_mask=RIGHT)
        eq3[1].move_to(eq1[1])
        eq3[2].next_to(eq1[2][0], ORIGIN, submobject_to_align=eq3[2][0]).move_to(eq1[2], coor_mask=RIGHT)
        eq3[3].next_to(eq1[3][0], ORIGIN, submobject_to_align=eq3[3][0])#.move_to(eq1[2], coor_mask=RIGHT)

        i = 4
        j = 6
        k = 6
        if not skip:
            self.play(ReplacementTransform(eq1[0][:2] + eq1[0][2:4] + eq1[0][5:8],
                                           eq3[0][:2] + eq3[0][2+i:4+i] + eq3[0][5+i:8+i]),
                      ReplacementTransform(eq1[0][13:15] + eq1[0][16:20],
                                           eq3[0][2+i:4+i] + eq3[0][5+i:9+i]),
                      mh.fade_replace(eq1[0][4], eq3[0][4+i]),
                      FadeOut(eq1[0][15], target_position=eq3[0][4+i]),
                      FadeOut(eq1[0][8:13]),
                      FadeIn(eq3[0][2:2+i]),
                      ReplacementTransform(eq1[2][:2] + eq1[2][2:4] + eq1[2][5:8],
                                           eq3[2][:2] + eq3[2][2 + j:4 + j] + eq3[2][5 + j:8 + j]),
                      ReplacementTransform(eq1[2][13:15] + eq1[2][16:20],
                                           eq3[2][2 + j:4 + j] + eq3[2][5 + j:9 + j]),
                      mh.fade_replace(eq1[2][4], eq3[2][4 + j]),
                      FadeOut(eq1[2][15], target_position=eq3[2][4 + j]),
                      FadeOut(eq1[2][8:13]),
                      FadeIn(eq3[2][2:2 + j]),
                      ReplacementTransform(eq1[3][:2] + eq1[3][2:4] + eq1[3][7:10],
                                           eq3[3][:2] + eq3[3][2 + k:4 + k] + eq3[3][5 + k:8 + k]),
                      ReplacementTransform(eq1[3][15:17] + eq1[3][18:22],
                                           eq3[3][2 + k:4 + k] + eq3[3][5 + k:9 + k]),
                      mh.fade_replace(eq1[3][4:7], eq3[3][4 + k]),
                      FadeOut(eq1[3][17], target_position=eq3[3][4 + j]),
                      FadeOut(eq1[3][10:15]),
                      FadeIn(eq3[3][2:2 + k]),
                      ReplacementTransform(eq1[1], eq3[1]),
                      run_time=3)
            self.play(ReplacementTransform(eq3, eq4), run_time=2)

        gp1 = VGroup(txt1, txt2, txt3, txt4, eq4)
        gp1.generate_target().to_edge(UP)
        gp1.target[-1].next_to(gp1.target[:-1], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.6, coor_mask=UP)
        if not skip:
            self.play(MoveToTarget(gp1))
        else:
            gp1 = gp1.target
            self.add(gp1)

        return gp1

    def construct(self):
        gp1 = self.create_gci(False)
        eq1 = gp1[-1]

        eq2 = MathTex(r'X^{(1)}=(X_1,\ldots,X_k),\ ', r'X^{(2)}=(X_{k+1},\ldots,X_n)')
        eq2.next_to(eq1, DOWN, buff=1)
        self.play(FadeIn(eq2))

        eq3 = MathTex(r'\mathbb P(\max_i\lvert X_i\rvert\le 1)', r'\ge',
                      r'\mathbb P(\max_i\lvert X^{(1)}_i\rvert\le 1)',
                      r'\mathbb P(\max_i\lvert X^{(2)}_i\rvert\le 1)')
        eq4 = MathTex(r'\Updownarrow').next_to(eq1[1], DOWN)
        eq3.next_to(eq4, DOWN, submobject_to_align=eq3[1])
        self.play(ReplacementTransform((eq1[:2] + eq1[2][:6] + eq1[2][8:10] + eq1[2][10:]).copy(),
                                       eq3[:2] + eq3[2][:6] + eq3[2][6:8] + eq3[2][11:]),
                  ReplacementTransform((eq1[3][:6] + eq1[3][8:10] + eq1[3][10:]).copy(),
                                       eq3[3][:6] + eq3[3][6:8] + eq3[3][11:]),
                  FadeIn(eq3[2][8:11], target_position=eq1[2][9].get_corner(UR)),
                  FadeIn(eq3[3][8:11], target_position=eq1[3][9].get_corner(UR)),
                  eq2.animate.to_edge(DOWN, buff=0.5),
                  FadeIn(eq4),
                  run_time=1.5)

        eq5 = MathTex(r'\mathbb P(X^{(1)}\in A, X^{(2)}\in B)', r'\ge',
                      r'\mathbb P(X^{(1)}\in A)', r'\mathbb P(X^{(2)}\in B)')
        eq6 = MathTex(r'A=[-1,1]^k,\ ', r'B=[-1,1]^{n-k}')
        eq5.next_to(eq3[0][0], ORIGIN, submobject_to_align=eq5[0][0], coor_mask=UP)
        eq6.move_to((eq5.get_bottom() + eq2.get_top())/2, coor_mask=UP)
        eq6.align_to(eq2, LEFT)
        eq5_1 = eq5[2][2:-1].copy().move_to(eq3[2][2:-1], coor_mask=RIGHT)

        self.play(FadeIn(eq6[0]))
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[2][7:11], eq5_1[:4]),
                  FadeOut(eq3[2][2:7], eq3[2][11:-1]),
                  FadeIn(eq5_1[4:]),
                  )
        self.wait(0.1)
        self.play(FadeIn(eq6[1]))
        self.wait(0.1)
        eq5_2 = eq5[3][2:-1].copy().move_to(eq3[3][2:-1], coor_mask=RIGHT)
        self.play(ReplacementTransform(eq3[3][7:11], eq5_2[:4]),
                  FadeOut(eq3[3][2:7], eq3[3][11:-1]),
                  FadeIn(eq5_2[4:]),
                  )
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[0][:2] + eq3[0][-1] + eq3[1],
                                       eq5[0][:2] + eq5[0][-1] + eq5[1]),
                  ReplacementTransform(eq3[2][:2] + eq5_1 + eq3[2][-1],
                                       eq5[2][:2] + eq5[2][2:-1] + eq5[2][-1]),
                  ReplacementTransform(eq3[3][:2] + eq5_2 + eq3[3][-1],
                                       eq5[3][:2] + eq5[3][2:-1] + eq5[3][-1]),
                  FadeOut(eq3[0][2:-1]),
                  FadeIn(eq5[0][2:-1]))
        self.wait(0.1)
        self.play(FadeOut(eq2, eq4, eq5, eq6), run_time=2)
        self.wait(0.1)

        eq7 = MathTex(r'\lvert X_i\rvert\le1', r'\Leftrightarrow X_i^2\le1', r'\Leftrightarrow Z_i\le1')
        eq7.next_to(eq1, DOWN, buff=1)
        for i in range(len(eq7)):
            self.play(FadeIn(eq7[i]))

        # eq8 = MathTex(r'Z_i')[0].align_to(eq1[0][7:9], DOWN)
        # eq8 = [eq8.copy().move_to(eq1[0][6:10]),
        #        eq8.copy().move_to(eq1[2][8:12]),
        #        eq8.copy().move_to(eq1[3][8:12])]
        # self.play(FadeOut(eq1[0][6:8], eq1[0][9]), FadeIn(eq8[0][0]), ReplacementTransform(eq1[0][8], eq8[0][1]),
        #           FadeOut(eq1[2][8:10], eq1[2][11]), FadeIn(eq8[1][0]), ReplacementTransform(eq1[2][10], eq8[1][1]),
        #           FadeOut(eq1[3][8:10], eq1[3][11]), FadeIn(eq8[2][0]), ReplacementTransform(eq1[3][10], eq8[2][1]))

        eq9 = MathTex(r'\mathbb P(\max_i Z_i\le 1)', r'\ge',
                      r'\mathbb P(\max_{i\le k} Z_i\le 1)',
                      r'\mathbb P(\max_{i > k} Z_i\le 1)')
        eq9.next_to(eq1[0][0], ORIGIN, submobject_to_align=eq9[0][0], coor_mask=UP)
        self.play(ReplacementTransform(eq1[0][:6] + eq1[0][10:] + eq1[1] + eq1[2][:8] + eq1[2][12:] + eq1[3][:8] +
                                       eq1[3][12:], # + eq8[0][:] + eq8[1][:] + eq8[2][:],
                                       eq9[0][:6] + eq9[0][8:] + eq9[1] + eq9[2][:8] + eq9[2][10:] + eq9[3][:8] +
                                       eq9[3][10:]), # + eq9[0][6:8] + eq9[2][8:10] + eq9[3][8:10]),
                  ReplacementTransform(eq1[0][8], eq9[0][7]),
                  ReplacementTransform(eq1[2][10], eq9[2][9]),
                  ReplacementTransform(eq1[3][10], eq9[3][9]),
                  FadeOut(eq1[0][6:8], eq1[0][9], eq1[2][8:10], eq1[2][11], eq1[3][8:10], eq1[3][11]),
                  FadeIn(eq9[0][6], eq9[2][8], eq9[3][8]),
                  )
        self.wait(0.1)
        self.play(FadeOut(eq7))


        self.wait()

class EqImageA(Scene):
    eq = 'A'

    def construct(self):
        self.add(MathTex(self.eq, font_size=100, stroke_width=1.5))

class EqImageB(EqImageA):
    eq = 'B'


class EqImagePAB(EqImageA):
    eq = r'\mathbb P(A\cap B)\ge\mathbb P(A)\mathbb P(B)'


class GCIProofForm(Scene):
    def __init__(self, *args, **kwargs):
        if not config.transparent:
            config.background_color = GREY
        Scene.__init__(self, *args, **kwargs)

    def get_eqs(self):
        eq1 = MathTex(r'\mathbb P(X^{(1)}\in A, X^{(2)}\in B)', r'\ge',
                      r'\mathbb P(X^{(1)}\in A)', r'\mathbb P(X^{(2)}\in B)').set_z_index(1)
        eq2 = MathTex(r'X^{(1)}=(X_1,\ldots,X_k),\ ', r'X^{(2)}=(X_{k+1},\ldots,X_n)').set_z_index(1)
        eq2.next_to(eq1, DOWN)
        eq1_1 = eq1[2:].copy().scale(1.1, about_point=eq1[2][5].get_center())
        eq1_0 = eq1[0].copy().scale(1.1, about_point=eq1[0][-6].get_center())
        gp = VGroup(eq1, eq2, eq1_1, eq1_0)
        box1 = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=0.7, corner_radius=0.15, stroke_opacity=0)
        VGroup(gp, box1).to_edge(DOWN, buff=0.1)
        eq3 = MathTex(r'\mathbb P(X^{(1)}\in A, X^{(2)}\in B)', r'\ge',
                      r'\mathbb P_0(X^{(1)}\in A, X^{(2)}\in B)').set_z_index(1)
        eq3.next_to(eq1[1], ORIGIN, submobject_to_align=eq3[1])

        return box1, eq1, eq2, eq3, eq1_1, eq1_0

    def construct(self):
        box1, eq1, eq2, eq3, eq1_1, eq1_0 = self.get_eqs()
        self.add(box1, eq1, eq2)
        self.wait()
        self.play(Transform(eq1[2:], eq1_1), rate_func=there_and_back, run_time=1.9)
        self.play(Transform(eq1[0], eq1_0), rate_func=there_and_back, run_time=1.9)
        self.wait(0.3)
        self.play(ReplacementTransform(eq1[:2] + eq1[2][0] + eq1[2][1:8] + eq1[3][2:],
                                       eq3[:2] + eq3[2][0] + eq3[2][2:9] + eq3[2][10:]),
                  FadeIn(eq3[2][1], eq3[2][9]),
                  FadeOut(eq1[2][8], eq1[3][:2]),
                  run_time=2)
        self.wait()


class CovMatrix(Scene):
    def __init__(self, *args, **kwargs):
        if not config.transparent:
            config.background_color=GREY
        Scene.__init__(self, *args, **kwargs)

    def get_eqs(self, anim=True):
        eq2 = MathTex(r'C=', r'\begin{pmatrix}'
                             r'c_{11} & c_{12} & c_{13} & \cdots & c_{1n} \\'
                             r'c_{21} & c_{22} & c_{23} & \cdots & c_{2n} \\'
                             r'c_{31} & c_{32} & c_{33} & \cdots & c_{3n} \\'
                             r'\vdots & \vdots & \vdots & \ddots & \vdots \\'
                             r'c_{n1} & c_{n2} & c_{n3} & \cdots & c_{nn}'
                             r'\end{pmatrix}').set_z_index(1)
        eq1 = MathTex(r'C = ', r'{\rm Cov}(X)').set_z_index(1)
        eq1.next_to(eq2[0], ORIGIN, submobject_to_align=eq1[0], coor_mask=UP)
        eq3 = MathTex(r'c_{ij}', r'={\rm Cov}(X_i, X_j)', r'=\mathbb E[X_iX_j]').set_z_index(1)
        eq3.next_to(eq2, DOWN * 2)
        eq4 = MathTex(r'C=', r'\begin{pmatrix}'
                             r'C_1 & A \\'
                             r'A^T & C_2'
                             r'\end{pmatrix}').set_z_index(1)
        #        eq4.next_to(eq1[0], ORIGIN, submobject_to_align=eq4[0], coor_mask=UP)
        eq5 = MathTex(r'C_1={\rm Cov}(X^{(1)}),', r'C_2={\rm Cov}(X^{(2)}),',
                      r'A={\rm Cov}(X^{(1)},X^{(2)})').set_z_index(1)
        eq5[2].next_to(eq5[:2], DOWN)
        eq5.move_to(ORIGIN).next_to(eq3[1][0], ORIGIN, submobject_to_align=eq5[0][2], coor_mask=UP)
        box1 = Rectangle(width=2 * config.frame_x_radius, height=2 * config.frame_y_radius, fill_opacity=1,
                         fill_color=BLACK, stroke_opacity=0)
        box2 = SurroundingRectangle(eq2, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0, corner_radius=0.15)
        box3 = SurroundingRectangle(eq4, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0, corner_radius=0.15)
        VGroup(eq4, box3).to_edge(DOWN, buff=0.1)

        if not anim:
            return box3, eq4

        row2 = eq2[1][22:37]
        row3 = eq2[1][37:52]
        col2 = VGroup(eq2[1][10:13], eq2[1][70:73])
        col3 = VGroup(eq2[1][13:16], eq2[1][73:76])
        p1 = (row2.get_corner(DL) + row3.get_corner(UL)) / 2
        p2 = (row2.get_corner(DR) + row3.get_corner(UR)) / 2
        p3 = (col2.get_corner(UR) + col3.get_corner(UL)) / 2
        p4 = (col2.get_corner(DR) + col3.get_corner(DL)) / 2

        eq4_1 = eq4[1][1:3].copy()
        eq4_2 = eq4[1][3].copy()
        eq4_3 = eq4[1][4:6].copy()
        eq4_4 = eq4[1][6:8].copy()

        line1 = Line(p1, p2,
                     stroke_width=4, stroke_opacity=0.5, stroke_color=YELLOW)
        line2 = Line(p3, p4,
                     stroke_width=4, stroke_opacity=0.5, stroke_color=YELLOW)
        line3 = Line((eq4_1.get_corner(UR) + eq4_2.get_corner(UL)) / 2,
                     (eq4_3.get_corner(DR) + eq4_4.get_corner(DL)) / 2,
                     stroke_color=YELLOW, stroke_opacity=0)
        line4 = Line((eq4_1.get_corner(DL) + eq4_3.get_corner(UL)) / 2,
                     (eq4_2.get_corner(DR) + eq4_4.get_corner(UR)) / 2,
                     stroke_color=YELLOW, stroke_opacity=0)
        eq4_1.next_to((p1 + p3) / 2, ORIGIN, submobject_to_align=eq4_1[0], buff=0)
        eq4_2.next_to((p2 + p3) / 2, ORIGIN, submobject_to_align=eq4_2[0], buff=0)
        eq4_3.next_to((p1 + p4) / 2, ORIGIN, submobject_to_align=eq4_3[0], buff=0)
        eq4_4.next_to((p2 + p4) / 2, ORIGIN, submobject_to_align=eq4_4[0], buff=0)

        self.add(box1, eq1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1[0], eq2[0]),
                  FadeOut(eq1[1]), FadeIn(eq2[1], box2),
                  run_time=2)
        self.play(FadeIn(eq3))
        self.wait(0.1)
        self.play(FadeIn(line1, line2))
        self.wait(0.1)
        self.play(FadeIn(eq4_1, eq4_2, eq4_3, eq4_4, eq5),
                  FadeOut(eq2[1][7:82], eq3), run_time=1, rate_func=linear)
        self.wait(0.1)
        self.play(ReplacementTransform(eq2[0][:] + eq4_1 + eq4_2 + eq4_3 + eq4_4,
                                       eq4[0][:] + eq4[1][1:3] + eq4[1][3] + eq4[1][4:6] + eq4[1][6:8]),
                  mh.fade_replace(eq2[1][:7], eq4[1][0]),
                  mh.fade_replace(eq2[1][82:], eq4[1][8:]),
                  ReplacementTransform(line2, line3),
                  ReplacementTransform(line1, line4),
                  ReplacementTransform(box2, box3),
                  FadeOut(eq5, box1),
                  run_time=2)
        self.wait()
        return box3, eq4

    def construct(self):
        box1, eq1 = self.get_eqs(anim=True)
        eq2 = MathTex(r'0', r'0').set_z_index(1)
        eq3 = MathTex(r'tA', r'tA^T').set_z_index(1)
        eq2[0].move_to(eq1[1][3])
        eq2[1].move_to(eq1[1][4])
        eq3[0].next_to(eq1[1][3], ORIGIN, submobject_to_align=eq3[0][1])
        eq3[1].next_to(eq1[1][4:6], ORIGIN, submobject_to_align=eq3[1][1:]).align_to(eq1[1][4], LEFT)
        self.add(box1, eq1)
        self.play(FadeOut(eq1[1][3], eq1[1][4:6]),
                  FadeIn(eq2),
                  rate_func=there_and_back,
                  run_time=2)
        self.add(eq1[1][3], eq1[1][4:6])
        self.wait()
        self.play(ReplacementTransform(eq1[1][3], eq3[0][1]),
                  ReplacementTransform(eq1[1][4:6], eq3[1][1:]),
                  FadeIn(eq3[0][0], eq3[1][0]),
                  run_time=1)
        self.wait(0.1)
        self.play(VGroup(eq1, eq3, box1).animate.to_edge(UR, buff=0.1), run_time=2)
        self.wait()


class ProbvsT(CovMatrix):
    def construct(self):
        eq1_txt=r'\mathbb P_t(X^{(1)}\in A, X^{(2)}\in B)'
        eq1 = MathTex(eq1_txt).set_z_index(1)
        box1 = SurroundingRectangle(eq1, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0, corner_radius=0.15)
        VGroup(eq1, box1).to_edge(DOWN, buff=0.1)
        eq2 = eq1[0][:2].copy().move_to(ORIGIN, coor_mask=RIGHT)
        ax = Axes(x_range=[0, 1.1], y_range=[0, 1.15], x_length=6, y_length=3,
                  axis_config={'color': WHITE, 'stroke_width': 4, 'include_ticks': False,
                               "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  ).set_z_index(1)
        ax.shift(ax.coords_to_point(0.5, 0) * LEFT)


        eq3 = MathTex(r't', font_size=34).next_to(ax.x_axis.get_right(), UL, buff=0.2)

        p0 = ax.coords_to_point(0, 0)
        p1 = ax.coords_to_point(0, 1)
        p2 = ax.coords_to_point(1, 0)
        p3 = ax.coords_to_point(1, 1)
        line1 = DashedLine(p1, p3).set_z_index(1)
        line2 = DashedLine(p2, p3).set_z_index(1)
        eq4 = MathTex(r'1', font_size=34).next_to(p2, DOWN, buff=0.1)
        eq5 = eq4.copy().next_to(p1, LEFT, buff=0.1)
        eq6 = MathTex(r'0', font_size=34).next_to(p0, DOWN, buff=0.1)
        eq7 = eq6.copy().next_to(p0, LEFT, buff=0.1)
        eq8 = MathTex(eq1_txt, font_size=30).set_z_index(1).next_to(ax.y_axis.get_top(), RIGHT, buff=0.1)

        gp = VGroup(ax, eq3, line1, line2, eq4, eq5, eq6, eq7, eq8)
        box2 = SurroundingRectangle(gp, fill_color=BLACK, fill_opacity=0.7, stroke_opacity=0, corner_radius=0.15)
        VGroup(gp, box2).to_edge(DOWN, buff=0.05)

        def f(t):
            return t*t * 0.5 + 0.25

        crv = ax.plot(f, [0, 1], stroke_color=YELLOW)
        dot1 = Dot(radius=0.1, fill_color=YELLOW).move_to(ax.coords_to_point(0, f(0)))
        dot2 = Dot(radius=0.1, fill_color=YELLOW).move_to(ax.coords_to_point(1, f(1)))
        eq9 = MathTex(r'\mathbb P(X^{(1)}\in A)\mathbb P(X^{(2)}\in B)', font_size=28).set_z_index(1)
        eq10 = MathTex(r'\mathbb P(X^{(1)}\in A,X^{(2)}\in B)', font_size=28).set_z_index(1)
        eq9.next_to(dot1, DOWN, buff=0).shift(RIGHT*1.6)
        eq10.next_to(dot2, UP, buff=0).shift(LEFT*1.45)

        self.add(box1, eq2)
        self.wait()
        self.play(LaggedStart(ReplacementTransform(eq2, eq1[0][:2]), FadeIn(eq1[0][2:]),
                  lag_ratio=0.5), run_time=3)
        self.wait(0.1)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq1, eq8),
                  ReplacementTransform(box1, box2)),
                  FadeIn(gp[:-1]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.1)
        self.play(Create(crv), FadeIn(dot1, dot2, eq9, eq10), run_time=2)
        self.wait()


class MGF(Scene):
    linecol = ManimColor(BLUE.to_rgb() * 0.6)

    def get_eqs(self, animate=True):
        p0 = config.frame_x_radius * LEFT/2
        p1 = -p0
        txt1 = Tex(r'for multivariate normal $X$', color=BLUE).move_to(p0)
        txt2 = Tex(r"for $Z_i=\frac12X_i^2$ (Royen's trick)" , color=BLUE).move_to(p1).to_edge(UP, buff=0.1)
        txt1.next_to(txt2[0][0], ORIGIN, submobject_to_align=txt1[0][0], coor_mask=UP)
        eq7 = MathTex(r'\mathbb E[e^{-\lambda\cdot X}]=', r'e^{\frac12\lambda^TC\lambda}').set_z_index(1)
        eq11 = MathTex(r'\mathbb E[e^{-\lambda\cdot Z}]=', r'\lvert 1+\Lambda C\rvert^{-\frac12}').set_z_index(1)
        eq7.next_to(txt1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
        eq11.move_to(p1).next_to(eq7[0][0], ORIGIN, submobject_to_align=eq11[0][0], coor_mask=UP)
        p0 = VGroup(eq7 ,eq11).get_bottom() * UP + DOWN * 0.2
        p1 = p0 + LEFT * config.frame_x_radius
        p2 = p0 + RIGHT * config.frame_x_radius
        p3 = UP * config.frame_y_radius
        box = VGroup(txt1, txt2, Line(p1, p2, color = self.linecol, stroke_width=6),
                     Line(p0, p3, color = self.linecol, stroke_width=6))

        if not animate:
            return eq7, eq11, box
        eq7pos = eq7.get_center()
        eq11pos = eq11.get_center()

        eq1 = Tex(r'Moment Generating Function of $n$-dimensional', r'\\ random vector $X$', color=BLUE)
        eq2 = MathTex(r'{\rm MGF}_X(\lambda)', r'=', r'\mathbb E[e^{-\lambda\cdot X}]')
        eq3 = Tex(r'for $\lambda\in\mathbb R^n$.')
        eq4 = Tex( r'(we suppose finite expectation for $\lambda_i\ge0$)')
        eq1[1].align_to(eq1[0], LEFT)
        eq2.next_to(eq1, DOWN)
        eq3.next_to(eq2, DOWN).align_to(eq1, LEFT)
        eq4.next_to(eq3, DOWN).align_to(eq1, LEFT)
        gp1 = VGroup(eq1, eq2, eq3, eq4).to_edge(UP)
        eq5 = Tex(r'If $X\sim N(0, C)$ ', r'then ',  r'$\lambda\cdot X\sim N(0, \lambda^TC\lambda)$')
        eq5.next_to(eq4, DOWN, buff=1)
        eq6 = MathTex(r'\mathbb E[e^{-\lambda\cdot X}]=', r'e^{\frac12{\rm Var}(\lambda\cdot X)}')
        eq6.next_to(eq5, DOWN)
        eq7.next_to(eq6[0][-1], ORIGIN, submobject_to_align=eq7[0][-1])

        self.add(gp1)
        self.play(FadeIn(eq5[0]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq5[1:]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq6[0]), run_time=1)
        self.play(FadeIn(eq6[1]), run_time=1)
        self.play(ReplacementTransform(eq6[1][:4] + eq6[0], eq7[1][:4] + eq7[0]),
                  FadeOut(eq6[1][4:]), FadeIn(eq7[1][4:]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(eq7.animate.next_to(eq5[2][0].get_corner(DL), UR, submobject_to_align=eq7[0][0], buff=0),
                  FadeOut(eq5[2]), run_time=1.5)
        eq5[2].set_opacity(0)
        self.play(VGroup(eq5, eq7).animate.next_to(eq4, DOWN, coor_mask=UP))

        eq8 = Tex(r'If $Z=\frac12(X_1^2,\ldots,X_n^2)$', r' then ', r'$\lambda\cdot Z=\frac12X^T\Lambda X$').next_to(eq5, DOWN).align_to(eq5, LEFT)
        eq8_1 = Tex(r'If $Z=(X_1^2,\ldots,X_n^2)$')
        eq8_1.next_to(eq8[0][0], ORIGIN, submobject_to_align=eq8_1[0][0])

        eq9 = MathTex(r'\Lambda = \begin{pmatrix}'
                      r'\lambda_1 & 0 & \cdots & 0\\'
                      r'0 & \lambda_2 & \cdots & 0\\'
                      r'\vdots & \vdots & \ddots & \vdots\\'
                      r'0 & 0 & \cdots & \lambda_n'
                      r'\end{pmatrix}', font_size=40)
        eq9.next_to(eq8, DOWN * 0.8, coor_mask=UP)
        eq10 = MathTex(r'\mathbb E[e^{-\lambda\cdot Z}]=', r'\mathbb E[e^{-\frac12X^T\Lambda X}]')
        eq10.next_to(eq8[2][0].get_corner(DL), UR, submobject_to_align=eq10[0][0], buff=0)
        eq11.next_to(eq10[0][0], ORIGIN, submobject_to_align=eq11[0][0])


        self.play(FadeIn(eq8_1))
        self.play(ReplacementTransform(eq8_1[0][:4] + eq8_1[0][4:], eq8[0][:4] + eq8[0][7:]),
                  FadeIn(eq8[0][4:7]))
        self.wait(0.1)
        self.play(FadeIn(eq8[1:]), run_time=1.5)
        self.play(FadeIn(eq9), run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq8[2][:3] + eq8[2][4:7] + eq8[2][8:10] + eq8[2][3],
                                       eq10[0][4:7] + eq10[1][4:7] + eq10[1][8:10] + eq10[0][-1]),
                  FadeIn(eq10[0][:3], eq10[0][7:-1], eq10[1][:3], eq10[1][11:]),
                  FadeIn(eq10[0][3], target_position=eq8[2][0].get_left()),
                  FadeIn(eq10[1][3], target_position=eq8[2][5].get_left()),
                  mh.stretch_replace(eq8[2][7], eq10[1][7]),
                  mh.stretch_replace(eq8[2][10], eq10[1][10]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq10[0], eq11[0]),
                  ReplacementTransform(eq10[1][9], eq11[1][3]),
                  FadeOut(eq10[1][:9], eq10[1][10:]),
                  FadeIn(eq11[1][:3], eq11[1][4:]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(FadeOut(eq1, eq2, eq3, eq4, eq5[:2], eq8[:2], eq9),
                  eq7.animate.move_to(eq7pos),
                  eq11.animate.move_to(eq11pos),
                  FadeIn(box),
                  run_time=2)

        self.wait()
        return eq7, eq11, box

    def construct(self):
        self.add(*self.get_eqs())


class MGFDiff(MGF):
    eqstr = [r'\frac{d}{dt}\mathbb E[f(X)]', r'=',
             r'\frac12\sum_{i,j}{\dot C_{ij} }\, \mathbb E[\partial_i\partial_j f(X)]']

    def get_eqs(self):
        eq1, eq2, box = MGF.get_eqs(self, animate=False)
        eq0 = MathTex(*self.eqstr, font_size=DEFAULT_FONT_SIZE*0.9).set_z_index(1)
        eq0.next_to(eq1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
        p0 = eq0.get_bottom() * UP + DOWN * 0.2
        p1 = p0 + LEFT * config.frame_x_radius
        p2 = p0 + RIGHT * config.frame_x_radius
        p3 = UP * config.frame_y_radius
        box2 = VGroup(*box[:2], Line(p1, p2, color = self.linecol, stroke_width=6),
                     Line(p0, p3, color = self.linecol, stroke_width=6))

        return eq1, eq2, eq0, box, box2

    def construct(self):
        eq1, eq2, eq0, box, box2 = self.get_eqs()
#        self.add(eq1, eq2, eq0, box2)
#        self.wait()
#        eq0 = MathTex(*self.eqstr, font_size=DEFAULT_FONT_SIZE*0.9).set_z_index(1)
#        eq0.next_to(eq1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
        p0 = eq0.get_bottom() * UP + DOWN * 0.2
        p1 = p0 + LEFT * config.frame_x_radius
        p2 = p0 + RIGHT * config.frame_x_radius
        p3 = UP * config.frame_y_radius
        box2 = VGroup(*box[:2], Line(p1, p2, color = self.linecol, stroke_width=6),
                     Line(p0, p3, color = self.linecol, stroke_width=6))


        self.add(box, eq1, eq2)
        self.wait(0.1)

        eq11 = MathTex(*self.eqstr).set_z_index(1)
        eq3 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot X}]', r'=',
                      r'\frac{d}{dt}e^{\frac12\lambda^TC\lambda}').set_z_index(1)
        eq3.next_to(eq11[1].get_center()/2, ORIGIN, submobject_to_align=eq3[1], coor_mask=RIGHT)
        eq3.move_to(box.get_bottom()*0.6 + config.frame_y_radius*DOWN*0.4, coor_mask=UP)
        eq4 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot X}]', r'=',
                      r'\frac12\lambda^T{\dot C}\lambda\, e^{\frac12\lambda^TC\lambda}').set_z_index(1)
        eq4.next_to(eq3[1], ORIGIN, submobject_to_align=eq4[1])
        eq5 = Tex(r'(writing $\dot C$ for $dC/dt$)').set_z_index(1).next_to(eq4[2], DOWN)
        eq6 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot X}]', r'=',
                      r'\frac12\lambda^T{\dot C}\lambda\, \mathbb E[e^{-\lambda\cdot X}]').set_z_index(1)
        eq6.next_to(eq4[1], ORIGIN, submobject_to_align=eq6[1])
        eq7 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot X}]', r'=',
                      r'\frac12\sum_{i,j}\lambda_i{\dot C_{ij} }\lambda_j\, \mathbb E[e^{-\lambda\cdot X}]').set_z_index(1)
        eq7.next_to(eq6[1], ORIGIN, submobject_to_align=eq7[1])
        eq8 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot X}]', r'=',
                      r'\frac12\sum_{i,j}{\dot C_{ij} }\, \mathbb E[\lambda_i\lambda_j e^{-\lambda\cdot X}]').set_z_index(1)
        eq8.next_to(eq7[1], ORIGIN, submobject_to_align=eq8[1])
        eq9 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot X}]', r'=',
                      r'\frac12\sum_{i,j}{\dot C_{ij} }\, \mathbb E[\partial_i\partial_j e^{-\lambda\cdot X}]').set_z_index(1)
        eq9.next_to(eq8[1], ORIGIN, submobject_to_align=eq9[1])
        eq10 = Tex(r'(writing $\partial_i$ for $\partial/\partial X_i$)').set_z_index(1).next_to(eq9[2], DOWN)
        eq11.next_to(eq9[1], ORIGIN, submobject_to_align=eq11[1])
        eq12 = Tex(r'Invertability of MGF/Laplace transforms:\\ can replace $e^{-\lambda\cdot X}$ by $f(X)$', color=BLUE).set_z_index(1)
        eq12.next_to(eq11[2], UP, coor_mask=UP)
        pos1 = eq9[0][6:11].get_bottom()
        pos2 = eq9[2][-6:-1].get_bottom()
        arr1 = Arrow(pos1 + DOWN*1.7, pos1, color=RED, stroke_width=10)
        arr2 = Arrow(pos2 + DOWN*1.7, pos2, color=RED, stroke_width=10)


        self.play(LaggedStart(ReplacementTransform((eq1[0][:-1]+eq1[0][-1] + eq1[1][:]).copy(),
                                       eq3[0][4:] + eq3[1][0] + eq3[2][4:]),
                  FadeIn(eq3[0][:4], eq3[2][:4]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq3[2][4:] + eq3[2][5:7].copy() + eq3[2][8:10].copy()
                                       + scale_to_obj(eq4[2][6].copy(), eq3[2][10])
                                       + eq3[2][11].copy() + scale_to_obj(eq4[2][2].copy(), eq3[2][7]),
                                       eq4[2][8:] + eq4[2][:2] + eq4[2][3:5]
                                       + eq4[2][6]
                                       + eq4[2][7] + eq4[2][2]),
                  FadeOut(eq3[2][:4]),
                  FadeIn(eq4[2][5], target_position=eq3[2][10].get_top()),
                  run_time=2
                  )
        self.play(FadeIn(eq5))
        self.play(ReplacementTransform(eq4[2][:8], eq6[2][:8]),
                  FadeOut(eq4[2][8:]),
                  FadeIn(eq6[2][8:]),
                  run_time=2)
        self.play(ReplacementTransform(eq6[2][:3] + eq6[2][3] + eq6[2][5:7] + eq6[2][7] + eq6[2][8:],
                                       eq7[2][:3] + eq7[2][7] + eq7[2][9:11] + eq7[2][13] + eq7[2][15:]),
                  FadeOut(eq6[2][4], target_position=eq7[2][7].get_corner(UR)),
                  FadeIn(eq7[2][8], target_position=eq6[2][3].get_corner(DR)),
                  FadeIn(eq7[2][11:13], target_position=eq6[2][5:7].get_corner(DR)),
                  FadeIn(eq7[2][14], target_position=eq6[2][7].get_corner(DR)),
                  FadeIn(eq7[2][3:7]),
                  FadeOut(eq5),
                  run_time=2)
        self.play(ReplacementTransform(eq7[2][:7] + eq7[2][9:13] + eq7[2][15:17] + eq7[2][17:]
                                       + eq7[2][7:9] + eq7[2][13:15],
                                       eq8[2][:7] + eq8[2][7:11] + eq8[2][11:13] + eq8[2][17:]
                                       + eq8[2][13:15] + eq8[2][15:17]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq8[2][:13] + eq8[2][14] + eq8[2][16] + eq8[2][17:],
                                       eq9[2][:13] + eq9[2][14] + eq9[2][16] + eq9[2][17:]),
                  FadeOut(eq8[2][13], eq8[2][15]),
                  FadeIn(eq9[2][13], eq9[2][15]))
        self.play(FadeIn(eq10))
        self.wait(0.1)
        self.play(FadeIn(eq12, arr1, arr2), FadeOut(eq10))
        self.wait(0.1)
        self.remove(eq3[0][10], eq9[2][21])
        self.play(ReplacementTransform(eq3[0][:6] + eq3[0][-1] + scale_to_obj(eq11[0][8].copy(), eq3[0][10]) + eq3[1],
                                       eq11[0][:6] + eq11[0][-1] + eq11[0][8] + eq11[1]),
                  ReplacementTransform(eq9[2][:17] + eq9[2][-1] + scale_to_obj(eq11[2][19].copy(), eq9[2][21]),
                                       eq11[2][:17] + eq11[2][-1] + eq11[2][19]),
                  FadeOut(eq3[0][6:10]),
                  FadeIn(eq11[0][6:8] + eq11[0][9]),
                  FadeOut(eq9[2][17:21]),
                  FadeIn(eq11[2][17:19], eq11[2][20]),
                  run_time=1.5)
        self.play(ReplacementTransform(box, box2),
                  ReplacementTransform(eq11, eq0),
                  FadeOut(eq12),
                  FadeOut(arr1, arr2, rate_func=rush_from),
                  run_time=2)
        self.wait()


class MGFDiffExample(MGFDiff): # overly complex
    def construct(self):
        skip = False
        eq1, eq2, eq3, _, box = MGFDiff.get_eqs(self)
        box2 = SurroundingRectangle(box, fill_opacity=0.4, fill_color=BLACK, stroke_opacity=0, buff=0.05).set_z_index(10)
        eq4 = MathTex(r'f', r'=', r'I([-1, 1]^n)')
        eq5 = MathTex(r'f(X)', r'=', r'I(X\in[-1, 1]^n)')
        eq5_1 = MathTex(r'f(X)', r'=', r'I(\max_i \lvert X_i\rvert\le1)')
        eq6 = MathTex(r'\mathbb E[f(X)]', r'=', r'\mathbb E[I(\max_i \lvert X_i\rvert\le1)]')
        eq7 = MathTex(r'\mathbb E[f(X)]', r'=', r'\mathbb P(\max_i \lvert X_i\rvert\le1)')
        eq8 = MathTex(r'\frac{d}{dt}\mathbb P(\max_i \lvert X_i\rvert\le1)', r'=', r'\frac{d}{dt}\mathbb E[f(X)]')
        eq9str = [r'\frac{d}{dt}\mathbb P(\max_i\lvert X_i\rvert\le1)', r'=', r'\frac12\sum_{i,j}\dot C_{ij}\mathbb E[\partial_i\partial_jf(X)]']
        eq9 =  MathTex(*eq9str)
        eq10 = MathTex(*eq9str, font_size=35).next_to(box, DOWN).to_edge(LEFT, buff=0.1)
        eq4.move_to(box.get_bottom()*0.6 + config.frame_y_radius*DOWN*0.4, coor_mask=UP)
        box3 = SurroundingRectangle(eq10, fill_opacity=0.4, fill_color=BLACK, stroke_opacity=0, buff=0).set_z_index(1)
        mh.align_sub(eq5, eq5[1], eq4[1])
        mh.align_sub(eq5_1, eq5_1[1], eq4[1])
        mh.align_sub(eq6, eq6[1], eq5[1])
        mh.align_sub(eq7, eq7[1], eq6[1])
        mh.align_sub(eq7[2], eq7[2][1], eq6[2][3])
        mh.align_sub(eq8, eq8[1], eq7[1])
        mh.align_sub(eq9, eq9[1], eq8[1])
        br2 = BraceLabel(eq8[0][:], r'{\rm exactly\ what\ we\ need}\\ {\rm to\ show\ is\ positive!', label_constructor=mh.mathlabel_ctr2, font_size=40,
                         brace_config={'color': RED}).set_z_index(2)
        br3 = BraceLabel(eq9[2][7:], r'{\rm is\ this\ positive?', label_constructor=mh.mathlabel_ctr2, font_size=50,
                         brace_config={'color': RED}).set_z_index(2)

        br4 = br3.copy().scale(eq10.width/eq9.width).shift(eq10[2].get_center() - eq9[2].get_center()).set_opacity(0)

        if not skip:
            self.add(eq1, eq2, eq3, eq4, box, box2)
            self.wait(0.1)
            self.play(ReplacementTransform(eq4[0][:1] + eq4[1] + eq4[2][:2] + eq4[2][2:],
                                           eq5[0][:1] + eq5[1] + eq5[2][:2] + eq5[2][4:]),
                      FadeIn(eq5[0][1:], target_position=eq4[0].get_right()),
                      FadeIn(eq5[2][2:4]),
                      run_time=1.5)
            self.wait(0.1)
            self.play(ReplacementTransform(eq5[:2] + eq5[2][:2] + eq5[2][-1],
                                           eq5_1[:2] + eq5_1[2][:2] + eq5_1[2][-1]),
                      FadeOut(eq5[2][2:-1]),
                      FadeIn(eq5_1[2][2:-1]),
                      run_time=1.5)
            self.wait(0.1)
            self.play(ReplacementTransform(eq5_1[0][:] + eq5_1[1] + eq5_1[2][:],
                                           eq6[0][2:-1] + eq6[1] + eq6[2][2:-1]),
                      FadeIn(eq6[0][:2], eq6[0][-1], eq6[2][:2], eq6[2][-1]),
                      run_time=1.5)
            self.wait(0.1)
            self.play(ReplacementTransform(eq6[:2] + eq6[2][3:-1],
                                           eq7[:2] + eq7[2][1:]),
                      mh.fade_replace(eq6[2][0], eq7[2][0]),
                      FadeOut(eq6[2][1], target_position=eq7[2][1]),
                      FadeOut(eq6[2][2], target_position=eq7[2][1]),
                      FadeOut(eq6[2][-1], target_position=eq7[2][-1]),
                      run_time=1)
            self.wait(0.1)
            self.play(ReplacementTransform(eq7[0][:] + eq7[1] + eq7[2][:],
                                           eq8[2][4:] + eq8[1] + eq8[0][4:]),
                      run_time=2)
            self.play(FadeIn(eq8[0][:4], eq8[2][:4]),
                      FadeIn(br2),
                      run_time=1.5)
            self.wait(0.1)
            self.play(ReplacementTransform(eq8[:2] + eq3[2].copy().set_z_index(20),
                                           eq9[:2] + eq9[2]),
                      FadeOut(eq8[2]), run_time=2)
            self.wait(0.1)
            self.play(
                ReplacementTransform(br2.brace, br3.brace),
                mh.fade_replace(br2.label, br3.label),
                run_time=2)
            self.wait(0.1)
            self.play(ReplacementTransform(eq9, eq10),
                      ReplacementTransform(br3, br4),
                      run_time=2)
            self.play(FadeIn(box3), rate_func=linear)
        else:
            self.add(eq10, box3)

        eq11 = MathTex(r'\dot C', r'=', r'\begin{pmatrix}'
                                   r'C_1 & tA \\ tA^T & C_2\end{pmatrix}').set_z_index(2)
        eq12 = MathTex(r'0', r'0')
        eq13 = MathTex(r'\dot C', r'=', r'\begin{pmatrix}'
                                   r'I_m & tI_m \\ tI_m & I_m\end{pmatrix}').set_z_index(2)
        eq11.to_edge(LEFT).move_to((eq10.get_bottom() + DOWN * config.frame_y_radius)/2, coor_mask=UP)
        mh.align_sub(eq11[2][1:3], eq11[2][1], eq11[2][6], coor_mask=RIGHT)
        mh.align_sub(eq11[2][3:5], eq11[2][4], eq11[2][8], coor_mask=RIGHT)
        eq13[2][1:3].move_to(eq13[2][7:9], coor_mask=RIGHT)
        mh.align_sub(eq13, eq13[1], eq11[1])
        eq12[0].move_to(eq11[2][1])
        eq12[1].move_to(eq11[2][8])

        self.play(LaggedStart(ReplacementTransform(eq10[2][8].copy().set_z_index(2), eq11[0][1]),
                  FadeIn(eq11[1:]), lag_ratio=0.4),
                  run_time=2.5)
        tofade = [eq11[2][1:4], eq11[2][5], eq11[2][8:10]]
        self.play(FadeIn(eq11[0][0], eq12), FadeOut(*tofade),
                  rate_func=linear)
        self.wait(0.1)
        VGroup(*tofade).set_opacity(0)
        self.play(ReplacementTransform(eq11[0][1:] + eq11[1] + eq11[2][0] + eq11[2][-1],
                                       eq13[0][1:] + eq13[1] + eq13[2][0] + eq13[2][-1]),
                  FadeOut(eq12, eq11[2][4], eq11[2][6:8], eq11[0][0]),
                  FadeIn(eq13[2][1:-1]),
                  run_time=2)
        self.wait(0.1)
        eq12[0].move_to(eq13[2][1:3])
        eq12[1].move_to(eq13[2][9:11])
        tofade = [eq13[2][1:4], eq13[2][6], eq13[2][9:-1]]
        self.play(FadeIn(eq13[0][0], eq12),
                  FadeOut(*tofade), rate_func=linear)
        VGroup(*tofade).set_opacity(0)
        self.wait(0.1)
        self.play(FadeOut(eq10))
        self.wait(0.1)
        self.play(FadeOut(eq12, eq13), rate_func=linear)
        self.remove(box3)

        eq14 = MathTex(r'\int\limits_{\partial A\cap\partial B}p(x)\cot(\theta)\,dx')
        eq15 = Tex(r'angle between $\partial A$ and $\partial B$', font_size=40)
        eq14.move_to(eq13).to_edge(LEFT)
        eq15.to_edge(DL).shift(RIGHT*0.3)
        arr = Arrow(eq15.get_top(), eq14[0][-4].get_bottom(), buff=0.2)
        gp2 =  VGroup(eq14, eq15, arr).move_to(eq4)
        mh.align_sub(gp2, eq14, eq4.get_center() * UP + LEFT * config.frame_x_radius/2)

        self.play(FadeIn(eq14))
        self.play(FadeIn(eq15, arr))
        self.wait(0.1)
        self.play(FadeOut(eq14, eq15, arr), rate_func=linear)
        self.wait(0.1)
        self.play(FadeOut(box2), rate_func=linear)
        self.wait(0.1)



class MGFDiffExample2(MGFDiff): # overly complex
    def construct(self):
        eq1, eq2, eq3, _, box = MGFDiff.get_eqs(self)
        box2 = SurroundingRectangle(box, fill_opacity=0.4, fill_color=BLACK, stroke_opacity=0, buff=0).set_z_index(10)
        eq4 = MathTex(r'f', r'=', r'I(A\times B)')
        eq6 = MathTex(r'\mathbb E[f(X)]', r'=', r'\mathbb E[I(X\in A\times B)]')
        eq7 = MathTex(r'\mathbb E[f(X)]', r'=', r'\mathbb P(X\in A\times B)')
        eq8 = MathTex(r'\frac{d}{dt}\mathbb P(X\in A\times B)', r'=', r'\frac{d}{dt}\mathbb E[f(X)]')
        eq9 = MathTex(r'\frac{d}{dt}\mathbb P(X\in A\times B)', r'=', r'\frac12\sum_{i,j}\dot C_{ij}\mathbb E[\partial_i\partial_jf(X)]')
        eq4.move_to(box.get_bottom()*0.6 + config.frame_y_radius*DOWN*0.4, coor_mask=UP)
        mh.align_sub(eq6, eq6[1], eq4[1])
        mh.align_sub(eq7, eq7[1], eq6[1])
        mh.align_sub(eq7[2], eq7[2][1], eq6[2][3])
        mh.align_sub(eq8, eq8[1], eq7[1])
        mh.align_sub(eq9, eq9[1], eq8[1])
        br1 = BraceLabel(eq6[2][4:-2], r'{\rm equivalently:\ }X^{(1)}\in A,X^{(2)}\in B', label_constructor=mh.mathlabel_ctr2, font_size=40,
                         brace_config={'color': RED})
        br2 = BraceLabel(eq8[0][:], r'{\rm exactly\ what\ we\ need}\\ {\rm to\ show\ is\ positive!', label_constructor=mh.mathlabel_ctr2, font_size=40,
                         brace_config={'color': RED})
        br3 = BraceLabel(eq9[2][7:], r'{\rm is\ this\ positive?', label_constructor=mh.mathlabel_ctr2, font_size=50,
                         brace_config={'color': RED})

        eq10 = Tex(r'\underline{\bf Hypercubes}', color=BLUE, font_size=40)
        eq11 = Tex(r'{\rm (sufficient\ to\ prove\ the\ GCI)}', color=BLUE, font_size=40)
        eq12 = Tex(r'$A=[-1,1]^k, B=[-1,1]^{n-k}$', color=BLUE, font_size=40)
        eq13 = Tex(r'$f(x)=I(\max_i\lvert x_i\rvert\le1)$', font_size=40).set_z_index(2)
        gp1 = VGroup(eq10, eq11, eq12, eq13).arrange(direction=DOWN, center=True, buff=0.15)
        gp1.next_to(eq9[0], DOWN, buff=0.15).align_to(eq9[1], RIGHT)

        eq14 =  MathTex(r'\frac{d}{dt}\mathbb P(\max_i\lvert X_i\rvert\le1)', r'=', r'\frac12\sum_{i,j}\dot C_{ij}\mathbb E[\partial_i\partial_jf(X)]')
        mh.align_sub(eq14, eq14[1], eq9[1]).set_z_index(2)

        self.add(eq1, eq2, eq3, eq4, box, box2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4[0][:] + eq4[1] + eq4[2][:2] + eq4[2][2:],
                                       eq6[0][:1] + eq6[1] + eq6[2][2:4] + eq6[2][6:-1]),
                  FadeIn(eq6[0][1:], target_position=eq4[0].get_right()),
                  FadeIn(eq6[2][4:6]),
                  run_time=1.5)
        self.play(FadeIn(br1))
        self.wait(0.1)
        self.play(FadeIn(eq6[2][:2], eq6[2][-1]), run_time=1)
        self.play(ReplacementTransform(eq6[:2] + eq6[2][3:-1],
                                       eq7[:2] + eq7[2][1:]),
                  mh.fade_replace(eq6[2][0], eq7[2][0]),
                  FadeOut(eq6[2][1], target_position=eq7[2][1]),
                  FadeOut(eq6[2][2], target_position=eq7[2][1]),
                  FadeOut(eq6[2][-1], target_position=eq7[2][-1]),
                  run_time=1)
        self.wait(0.1)
        self.play(ReplacementTransform(eq7[0][:] + eq7[1] + eq7[2][:],
                                       eq8[2][4:] + eq8[1] + eq8[0][4:]),
                  br1.animate.shift(eq8[0][4:].get_center() - eq7[2][:].get_center()),
                  run_time=2)
        self.play(FadeIn(eq8[0][:4], eq8[2][:4]),
#                  FadeIn(br2),
                  ReplacementTransform(br1.brace, br2.brace),
                  mh.fade_replace(br1.label, br2.label),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq8[:2] + eq3[2].copy().set_z_index(20),
                                       eq9[:2] + eq9[2]),
                  FadeOut(eq8[2]), run_time=2)
        self.wait(0.1)
        self.play(
            ReplacementTransform(br2.brace, br3.brace),
            mh.fade_replace(br2.label, br3.label),
            run_time=2)
        self.wait(0.1)
        self.play(FadeIn(gp1[:-1]))
        self.play(FadeIn(gp1[-1]))
        self.wait(0.1)
        self.play(ReplacementTransform(eq9[1:] + eq9[0][:6] + eq9[0][-1],
                                       eq14[1:] + eq14[0][:6] + eq14[0][-1]),
                  FadeOut(eq9[0][6:-1]),
                  ReplacementTransform((eq13[0][7:12] + eq13[0][13:-1]).copy(),
                                       eq14[0][6:11] + eq14[0][12:-1]),
                  mh.fade_replace(eq13[0][12].copy(), eq14[0][11]),
                  run_time=2)

        self.wait()


class MGFDiffZ(MGFDiff):
    eqstr1 = [r'\frac{d}{dt}\mathbb E[f(Z)]', r'=',
                      r'\sum_{S}c_S\,\mathbb E[(-\partial)^Sf(\tilde Z)]']
    eqstr2 = [r'where ', r'$c_S=-\frac12\frac{d}{dt}\lvert C_S\rvert$']

    def get_eqs(self, animate=False):
        eq1, eq2, eq3, _, box = MGFDiff.get_eqs(self)

        eq30 = MathTex(*self.eqstr1, font_size=DEFAULT_FONT_SIZE*0.9)
        eq30.next_to(eq2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
        eq31 = Tex(*self.eqstr2, font_size=DEFAULT_FONT_SIZE)
        eq31.next_to(eq30, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0)

        p0 = eq31.get_bottom() * UP + DOWN * 0.2
        p1 = p0 + LEFT * config.frame_x_radius
        p2 = p0 + RIGHT * config.frame_x_radius
        p3 = UP * config.frame_y_radius
        box2 = VGroup(*box[:2], Line(p1, p2, color = self.linecol, stroke_width=6),
                     Line(p0, p3, color = self.linecol, stroke_width=6))

        if not animate:
            return eq1, eq2, eq3, eq30, eq31, box2

        self.add(eq1, eq2, eq3, box)

        self.wait(0.1)
        eq4 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'\frac{d}{dt}\lvert 1+\Lambda C\rvert^{-\frac12}')
        eq4.move_to(box.get_bottom()*0.65 + config.frame_y_radius*DOWN*0.35, coor_mask=UP)
        eq5 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'-\frac12\lvert 1+\Lambda C\rvert^{-\frac32}\frac{d}{dt}\lvert 1+\Lambda C\rvert')
        eq5.next_to(eq4[1], ORIGIN, submobject_to_align=eq5[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq6 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'-\frac12\mathbb E[e^{-\lambda\cdot Z}]^3\frac{d}{dt}\lvert 1+\Lambda C\rvert')
        eq6.next_to(eq5[1], ORIGIN, submobject_to_align=eq6[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq7 = Tex(r'setting $\tilde Z = Z + Z^\prime + Z^{\prime\prime}$', r'\\ (sum of independent copies of $Z$)')
        eq7.next_to(eq6, DOWN)
        eq8 = MathTex(r'\mathbb E[e^{-\lambda\cdot\tilde Z}]', r'=',
                      r'\mathbb E[e^{-\lambda\cdot Z}e^{-\lambda\cdot Z^\prime}e^{-\lambda\cdot Z^{\prime\prime}}]')
        eq8.next_to(eq7, DOWN)
        eq9 = MathTex(r'\mathbb E[e^{-\lambda\cdot\tilde Z}]', r'=',
                      r'\mathbb E[e^{-\lambda\cdot Z}]\mathbb E[e^{-\lambda\cdot Z^\prime}]\mathbb E[e^{-\lambda\cdot Z^{\prime\prime}}]')
        eq9.next_to(eq8[1], ORIGIN, submobject_to_align=eq9[1])#.move_to(ORIGIN, coor_mask=RIGHT)
        eq10 = MathTex(r'\mathbb E[e^{-\lambda\cdot\tilde Z}]', r'=',
                       r'\mathbb E[e^{-\lambda\cdot Z}]^3')
        eq10.next_to(eq9[1], ORIGIN, submobject_to_align=eq10[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq11 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'-\frac12\mathbb E[e^{-\lambda\cdot\tilde Z}]\frac{d}{dt}\lvert 1+\Lambda C\rvert')
        eq11.next_to(eq6[1], ORIGIN, submobject_to_align=eq11[1])#.move_to(ORIGIN, coor_mask=RIGHT)

        eq12 = MathTex(r'\lvert 1+\Lambda C\rvert', r'=',
                       r'1+\sum_{\emptyset\not=S\subseteq\{1,\ldots,n\}}\lvert(\Lambda C)_S\rvert')
        eq12.next_to(eq11, DOWN, coor_mask=UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.5)
        eq15 = MathTex(r'\lvert 1+\Lambda C\rvert', r'=',
                       r'1+\sum_{S}(\Pi_{i\in S}\lambda_i)\lvert C_S\rvert')
        eq15.next_to(eq12[1], ORIGIN, submobject_to_align=eq15[1]).align_to(eq12, RIGHT)
        eq16 = MathTex(r'\frac{d}{dt}\lvert 1+\Lambda C\rvert', r'=',
                       r'0+\sum_{S}(\Pi_{i\in S}\lambda_i)\frac{d}{dt}\lvert C_S\rvert')
        eq16.next_to(eq15[1], ORIGIN, submobject_to_align=eq16[1])
        eq17 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'-\frac12\mathbb E[e^{-\lambda\cdot\tilde Z}]\sum_{S}(\Pi_{i\in S}\lambda_i)\frac{d}{dt}\lvert C_S\rvert')
        eq17.next_to(eq11[1], ORIGIN, submobject_to_align=eq17[1])#.move_to(ORIGIN, coor_mask=RIGHT)
        eq17.next_to(eq16[2][-1], ORIGIN, submobject_to_align=eq17[2][-1], coor_mask=RIGHT)

        eq18 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'-\frac12\sum_{S}\frac{d}{dt}\lvert C_S\rvert\,\mathbb E[(\Pi_{i\in S}\lambda_i)e^{-\lambda\cdot\tilde Z}]')
        eq18.next_to(eq17[1], ORIGIN, submobject_to_align=eq18[1])
        eq19 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'-\frac12\sum_{S}\frac{d}{dt}\lvert C_S\rvert\,\mathbb E[(\Pi_{i\in S}(-\partial_i))e^{-\lambda\cdot\tilde Z}]')
        eq19.next_to(eq18[1], ORIGIN, submobject_to_align=eq19[1])
        eq20 = Tex(r'writing $\partial_i$ for $\partial/\partial \tilde Z_i$').set_z_index(1).next_to(eq19[2], DOWN)
        eq21 = Tex(r'and ', r'$(-\partial)^S$', r' for $\Pi_{i\in S}(-\partial_i)$').set_z_index(1).next_to(eq20, DOWN)

        eq22 = MathTex(r'\frac{d}{dt}\mathbb E[e^{-\lambda\cdot Z}]', r'=',
                      r'-\frac12\sum_{S}\frac{d}{dt}\lvert C_S\rvert\,\mathbb E[(-\partial)^Se^{-\lambda\cdot\tilde Z}]')
        eq22.next_to(eq19[1], ORIGIN, submobject_to_align=eq22[1])
        eq23 = Tex(r'Invertability of MGF/Laplace transforms:\\ can replace $e^{-\lambda\cdot Z}$ by $f(Z)$', color=BLUE).set_z_index(1)
        eq23.next_to(eq22[2], UP, coor_mask=UP, buff=0.05)
        pos1 = eq22[0][6:11].get_bottom()
        pos2 = eq22[2][-7:-1].get_bottom()
        arr1 = Arrow(pos1 + DOWN*1.7, pos1, color=RED, stroke_width=10)
        arr2 = Arrow(pos2 + DOWN*1.7, pos2, color=RED, stroke_width=10)
        eq24 = MathTex(r'\frac{d}{dt}\mathbb E[f(Z)]', r'=',
                      r'-\frac12\sum_{S}\frac{d}{dt}\lvert C_S\rvert\,\mathbb E[(-\partial)^Sf(\tilde Z)]')
        eq24.next_to(eq22[1], ORIGIN, submobject_to_align=eq24[1])
        eq25 = MathTex(*self.eqstr1)
        eq25.next_to(eq24[2][4], ORIGIN, submobject_to_align=eq25[2][0])
        eq26 = Tex(*self.eqstr2).next_to(eq25, DOWN)

        self.play(LaggedStart(ReplacementTransform((eq2[0][:-1]+eq2[0][-1] + eq2[1][:]).copy(),
                                       eq4[0][4:] + eq4[1][0] + eq4[2][4:]),
                  FadeIn(eq4[0][:4], eq4[2][:4]), lag_ratio=0.5),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4[:2] + eq4[2][:4] + eq4[2][4:10] + eq4[2][10:13].copy()
                                       + scale_to_obj(eq5[2][3].copy(), eq4[2][13])
                                       + eq4[2][10] + eq4[2][12:14] + eq4[2][4:10].copy(),
                                       eq5[:2] + eq5[2][14:18] + eq5[2][4:10] + eq5[2][:3]
                                       + eq5[2][3]
                                       + eq5[2][10] + eq5[2][12:14] + eq5[2][18:]),
                  mh.fade_replace(eq4[2][11], eq5[2][11]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq5[:2] + eq5[2][:4] + eq5[2][11] + eq5[2][14:],
                                       eq6[:2] + eq6[2][:4] + eq6[2][12] + eq6[2][13:]),
                  FadeOut(eq5[2][4:11], eq5[2][12:14]),
                  FadeIn(eq6[2][4:12]),
                  run_time=2)
        self.wait(0.1)
        self.play(LaggedStart(FadeIn(eq7), FadeIn(eq8), lag_ratio=0.4), run_time=2)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(eq8[:2] + eq8[2][:7] + eq8[2][7:13] + eq8[2][13:21],
                                       eq9[:2] + eq9[2][:7] + eq9[2][10:16] + eq9[2][19:27]),
                  FadeIn(eq9[2][7:10], eq9[2][16:19]),
                              lag_ratio=0.4),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeOut(eq9[2][15], eq9[2][24:26]))
        self.wait(0.1)
        self.play(ReplacementTransform(eq9[:2] + eq9[2][:8],
                                       eq10[:2] + eq10[2][:8]),
                  ReplacementTransform(eq9[2][8:15] + eq9[2][16],
                                       eq10[2][:7] + eq10[2][7]),
                  ReplacementTransform(eq9[2][17:24] + eq9[2][26],
                                       eq10[2][:7] + eq10[2][7]),
                  FadeIn(eq10[2][-1], target_position=eq9[2][16].get_corner(UR)),
                  run_time=2)
        self.play(ReplacementTransform(eq6[:2] + eq10[0][:].copy() + eq6[2][:4] + eq6[2][13:],
                                       eq11[:2] + eq11[2][4:13] + eq11[2][:4] + eq11[2][13:]),
                  FadeOut(eq6[2][4:13]),
                  FadeOut(eq7, eq10),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq12[:2]))
        self.wait(0.1)
        self.play(FadeIn(eq12[2]))
        self.wait(0.1)
        shift = eq15[2][3].get_center() - eq12[2][6].get_center()
        shift2 = (eq15[2][9].get_center() - eq12[2][19].get_center()) * RIGHT
        self.play(ReplacementTransform(eq12[:2] + eq12[2][:3] + eq12[2][6]
                                       + eq12[2][17] + eq12[2][20] + eq12[2][22:24]
                                       + eq12[2][22].copy(),
                                       eq15[:2] + eq15[2][:3] + eq15[2][3]
                                       + eq15[2][12] + eq15[2][13] + eq15[2][14:16]
                                       + eq15[2][8]),
                  FadeOut(eq12[2][3:6], shift=shift),
                  FadeOut(eq12[2][7:17], shift=shift),
                  FadeOut(eq12[2][18], target_position=eq15[2][12]),
                  FadeOut(eq12[2][21], target_position=eq15[2][15]),
                  mh.fade_replace(eq12[2][19], eq15[2][9]),
                  FadeIn(eq15[2][4:8], shift=shift2),
                  FadeIn(eq15[2][10], target_position=eq12[2][19].get_corner(DR)),
                  FadeIn(eq15[2][11], shift=shift2),
                  run_time=2)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(eq15[0][:] + eq15[1] + eq15[2][1:-4] + eq15[2][-4:],
                                       eq16[0][4:] + eq16[1] + eq16[2][1:-8:] + eq16[2][-4:]),
                  AnimationGroup(FadeIn(eq16[0][:4] ,eq16[2][-8:-4]),
                                 mh.fade_replace(eq15[2][0], eq16[2][0])),
                              lag_ratio=0.4),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq11[:2] + eq11[2][:13] + eq16[2][2:].copy(),
                                       eq17[:2] + eq17[2][:13] + eq17[2][13:]),
                  FadeOut(eq11[2][13:]),
                  run_time=1.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq17[:2] + eq17[2][:4] + eq17[2][13:15],
                                       eq18[:2] + eq18[2][:4] + eq18[2][4:6]),
                  ReplacementTransform(eq17[2][-8:], eq18[2][6:14]),# path_arc=-PI/6),
                  ReplacementTransform(eq17[2][4:6] + eq17[2][6:13],
                                       eq18[2][14:16] + eq18[2][24:31]),# path_arc=-PI/6),
                  ReplacementTransform(eq17[2][15:23], eq18[2][16:24]),
                  FadeOut(eq16, rate_func=lambda t: smooth(min(1,t*2))),
                  run_time=2.5)
        self.wait(0.1)
        self.play(ReplacementTransform(eq18[:2] + eq18[2][:21] + eq18[2][23:] + eq18[2][22],
                                       eq19[:2] + eq19[2][:21] + eq19[2][26:] + eq19[2][24]),
                  mh.fade_replace(eq18[2][21], eq19[2][23]),
                  FadeIn(eq19[2][22], target_position=eq18[2][21]),
                  FadeIn(eq19[2][25], target_position=eq18[2][23].get_left()),
                  FadeIn(eq19[2][21], target_position=eq18[2][21].get_left()),
                  run_time=1)
        self.play(LaggedStart(FadeIn(eq20), FadeIn(eq21), lag_ratio=0.5), run_time=2)
        self.wait(0.1)
        eq22_1 = eq21[1][:].copy()
        self.play(#eq22_1.animate.next_to(eq19[2][16], RIGHT, buff=0).move_to(eq22[2][16:21], coor_mask=UP),#.move_to(eq19[2][17:26]),
                  ReplacementTransform(eq22_1, eq22[2][16:21]),
                  FadeOut(eq19[2][16:27]),
                  run_time=1.5)
        self.play(ReplacementTransform(eq19[:2] + eq19[2][:16] + eq19[2][27:],
                                       eq22[:2] + eq22[2][:16] + eq22[2][21:]))
        self.wait(0.1)
        self.play(FadeIn(eq23, arr1, arr2), FadeOut(eq20, eq21))
        self.wait(0.1)
        self.play(ReplacementTransform(eq22[0][:6] + eq22[0][-1] + eq22[0][-2] + eq22[1],
                                       eq24[0][:6] + eq24[0][-1] + eq24[0][-3] + eq24[1]),
                  ReplacementTransform(eq22[2][:21] + eq22[2][-1] + eq22[2][-3:-1],
                                       eq24[2][:21] + eq24[2][-1] + eq24[2][-4:-2]),
                  FadeOut(eq22[0][6:10]),
                  FadeIn(eq24[0][6:8], eq24[0][-2]),
                  FadeOut(eq22[2][21:25]),
                  FadeIn(eq24[2][21:23], eq24[2][-2]),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq24[:2] + eq24[2][4:6] + eq24[2][14:],
                                       eq25[:2] + eq25[2][:2] + eq25[2][4:]),
                  FadeIn(eq25[2][2:4], shift=(eq24[2][11].get_center()-eq25[2][2].get_center())*LEFT),
                  ReplacementTransform(eq24[2][:4] + eq24[2][6:14],
                                       eq26[1][3:7] + eq26[1][7:]),
                  FadeIn(eq26[0], eq26[1][:3]),
                  FadeOut(eq23),
                  FadeOut(arr1, arr2, rate_func=rush_from),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq25, eq30),
                  ReplacementTransform(eq26, eq31),
                  ReplacementTransform(box, box2),
                  run_time=2)
        self.wait()
        return eq1, eq2, eq3, eq30, eq31, box2

    def construct(self):
        self.get_eqs(animate=True)


class MGFDiffZExample(MGFDiffZ):
    def construct(self):
        eq1, eq2, eq3, eq4, eq5, box1 = MGFDiffZ.get_eqs(self, animate=False)
        box2 = SurroundingRectangle(box1, fill_opacity=0.4, fill_color=BLACK, stroke_opacity=0, buff=0.05).set_z_index(1)


        pos1 = box1.get_bottom()
        eq6 = MathTex(r'f', r'=', r'I([-1,1]^3)')
        eq7 = MathTex(r'f(z)', r'=', r'I(\max_i\lvert z_i\rvert\le1)')
        eq9 = MathTex(r'\frac{d}{dt}\mathbb P(\max Z_i\le 1)', r'=', r'\frac{d}{dt}\mathbb E[f(Z)]')
        eq10 = MathTex(r'\frac{d}{dt}\mathbb P(\max Z_i\le 1)', r'=', r'\sum_Sc_S\mathbb E[(-\partial)^Sf(\tilde Z)]')
        eq11 = Tex(r'$(-\partial)^Sf(\tilde Z)$', r' is positive?')


        eq9.to_edge(LEFT, buff=0.1)
        eq6.move_to(eq9, coor_mask=RIGHT)
        mh.align_sub(eq7, eq7[1], eq6[1])
        eq9.next_to(eq7, DOWN)
        VGroup(eq6, eq7, eq9).move_to(pos1 * 0.6 + config.frame_y_radius * DOWN * 0.4, coor_mask=UP)
        mh.align_sub(eq10, eq10[1], eq9[1])
        eq11.next_to(eq10, DOWN)
        mh.align_sub(eq11, eq11[1][-9:-1], eq10[2][-11:-1], coor_mask=RIGHT)

        arr1 = Arrow(eq11[1][-9:-1].get_top(), eq10[2][-11:-1].get_bottom(),
                     stroke_width=6, color=RED, buff=0, max_stroke_width_to_length_ratio=10)

        eq12 = eq7.copy().next_to(box1, DOWN).to_edge(LEFT, buff=0.15)
        eq13 = eq11.copy().next_to(eq12, DOWN).align_to(eq12, LEFT)

        self.add(eq1, eq2, eq3, eq4, eq5, box1, box2)
        self.add(eq6)
        self.wait(0.1)
        self.play(LaggedStart(AnimationGroup(ReplacementTransform(eq6[0][:1] + eq6[1] + eq6[2][:2] + eq6[2][-1],
                                       eq7[0][:1] + eq7[1] + eq7[2][:2] + eq7[2][-1]),
                  FadeIn(eq7[0][1:], shift=eq7[0][0].get_center() - eq6[0][0].get_center())),
                  AnimationGroup(FadeOut(eq6[2][2:-1]),
                  FadeIn(eq7[2][2:-1], rate_func=linear)), lag_ratio=0.3),
                  run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq9[0][4:], eq9[1], eq9[2][4:]))
        self.wait(0.1)
        self.play(FadeIn(eq9[0][:4], eq9[2][:4]))
        self.wait(0.1)
        self.play(ReplacementTransform(eq9[:2] + eq4[2].copy().set_z_index(2),
                                       eq10[:2] + eq10[2]),
                  FadeOut(eq9[2]),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq11, arr1, rate_func=linear))
        self.wait(0.1)
        self.play(Transform(eq7, eq12), Transform(eq11, eq13),
                  FadeOut(arr1, eq10, rate_func = lambda t: min(1, t*3)),
                  run_time=2)
        # self.play(ReplacementTransform(eq10[2][-11:-1].copy(), eq11[0][:]),
        #           FadeIn(eq11[1]),
        #           run_time=2)

        self.wait(0.1)
        self.play(FadeOut(eq7, eq11, rate_func=linear))
        self.wait()


class MGFDiffZDeterminants(MGFDiffZ):
    def get_eqs(self):
        eq1, eq2, eq3, eq4, eq5, box1 = MGFDiffZ.get_eqs(self, animate=False)
        box2 = SurroundingRectangle(box1, fill_opacity=0.4, fill_color=BLACK, stroke_opacity=0, buff=0.05).set_z_index(1)
        eq9 = Tex(r'\underline{Is $\lvert C_S\rvert$ decreasing in $t$?}', color=BLUE, stroke_width=1.1)
        eq9.next_to(box1.get_bottom(), DOWN, buff=0.15)
        return eq1, eq2, eq3, eq4, eq5, box1, box2, eq9

    def construct(self):
        eq1, eq2, eq3, eq4, eq5, box1, box2, eq9 = self.get_eqs()

        pos1 = box1.get_bottom() * 0.6 + mh.pos(DOWN) * 0.4

        eq6 = MathTex(r'c_S', r'=', r'-\frac12\frac{d}{dt}\lvert C_S\rvert').set_z_index(2)
        eq7 = Tex(r'Is $c_S$ positive?')
        eq8 = Tex(r'\underline{Is $\lvert C_S\rvert$ decreasing in $t$?}')
        eq8[0][-1].set_opacity(0)

        eq6.move_to(pos1)
        eq7.next_to(eq6, DOWN)
        eq8.next_to(eq7, DOWN)

        eq10 = MathTex(r'C_S', r'=', r'{\rm Cov}(X_S)')
        eq11 = MathTex(r'p_{X_S}(x)', r'=', r'\frac{1}{\sqrt{2\pi\lvert C_S\rvert}}e^{-\frac12 x^TC_S^{-1}x')
        eq12 = MathTex(r'\mathbb P(X_S\in A)', r'\approx', r'p_{X_S}(0){\rm volume}(A)')
        eq13 = MathTex(r'\mathbb P(X_S\in A)', r'\approx', r'\frac{ {\rm volume}(A)}{\sqrt{2\pi\lvert C_S\rvert} }')
        eq10.move_to(pos1)
        eq11.next_to(eq10, DOWN)
        mh.align_sub(eq12, eq12[1], eq10[1]).to_edge(RIGHT)
        mh.align_sub(eq13, eq13[1], eq12[1]).move_to(eq12, coor_mask=RIGHT)

        xlen = 2
        ax = Axes(x_range=[-1, 1], y_range=[-1, 1], x_length=xlen, y_length=xlen,
                  axis_config={'color': WHITE, 'stroke_width': 3, 'include_ticks': False,
                               "include_tip": False
                               },
                  ).set_z_index(1)

        ax.to_edge(DR, buff=0.1).move_to(eq12 ,coor_mask=RIGHT).shift(LEFT)
        lines = []
        lineargs = {'stroke_width': 1, 'stroke_color': WHITE, 'stroke_opacity': 0.3, 'dash_length': 0.01, 'dashed_ratio': 0.3}
        coords = [1/3, 2/3]
        coords = [0.2, 0.4, 0.6, 0.8]
        for x in coords + [-y for y in coords]:
            lines.append(DashedLine(ax.coords_to_point(-1, x), ax.coords_to_point(1, x), **lineargs).set_z_index(1))
            lines.append(DashedLine(ax.coords_to_point(x, -1), ax.coords_to_point(x, 1), **lineargs).set_z_index(1))
        set1 = Rectangle(width=xlen*0.2, height=xlen*0.2, fill_color=RED, stroke_color=RED,
                         fill_opacity=0.8, stroke_opacity=1).set_z_index(2)
        set1.move_to(ax.coords_to_point(0, 0))
        eq14 = MathTex(r'A', color=RED).next_to(set1, UR, buff=0.05).set_z_index(2)
        box3 = SurroundingRectangle(ax, fill_color=ManimColor(WHITE.to_rgb()*0.1), fill_opacity=1,
                                    stroke_color=GREY, stroke_opacity=1, stroke_width=2, buff=-0.0)
        eq15 = Tex('tiny set', font_size=20).move_to(ax.coords_to_point(2, -0.5))
        arr1 = Arrow(eq15.get_left(), ax.coords_to_point(0.2, -0.1), stroke_width=2, buff=0.05,
                     max_tip_length_to_length_ratio=0.1)

        crv1 = mh.circle_eq(eq13[0])
        eq16 = Tex(r'increasing', color=RED, font_size=40).next_to(eq13[0].get_corner(UR), UP, buff=0.3)
        crv2 = mh.circle_eq(eq13[2][-1]).shift(LEFT*0.2)
        eq17 = Tex(r'decreasing', color=RED, font_size=40).next_to(crv2, DOWN, buff=0.15)

        self.add(eq1, eq2, eq3, eq4, eq5, box1, box2)

        gp1 = VGroup(eq4, eq5[1])
        gp1.set_z_index(2).set_opacity(0.6)
        self.play(gp1.animate.set_opacity(1))
        eq5_1 = eq5[1].copy()
        self.play(ReplacementTransform(eq5_1[:2] + eq5_1[2] + eq5_1[7:] + eq5_1[3],
                                       eq6[0][:] + eq6[1][0] + eq6[2][4:] + eq6[2][0]),
                  mh.stretch_replace(eq5_1[4:7], eq6[2][1:4]),
                  run_time=2)
        self.wait(0.1)
        self.play(FadeIn(eq7))
        self.wait(0.1)
        self.play(FadeIn(eq8))
        self.wait(0.1)
        self.play(ReplacementTransform(eq8[0], eq9[0]),
                  FadeOut(eq6, eq7),
                  gp1.animate.set_opacity(0.6),
                  run_time=2)
#        self.add(eq9, index_labels(eq9[0]))
        self.wait(0.1)
        self.play(FadeIn(eq10))
        self.wait(0.1)
        self.play(FadeIn(eq11))
        self.wait(0.1)
        self.play(VGroup(eq10, eq11).animate.to_edge(LEFT),
                  FadeIn(eq12, ax, set1, eq14, box3, eq15, arr1, *lines),
                  run_time=2)
        self.wait(0.1)
        self.play(ReplacementTransform(eq12[:2] + eq12[2][-9:],
                                       eq13[:2] + eq13[2][:9]),
                  FadeOut(eq12[2][:-9]),
                  FadeIn(eq13[2][9:]),
                  run_time=2)
        self.wait(0.1)
        self.play(Create(crv1), run_time=1)
        self.play(FadeIn(eq16), run_time=0.5)
        self.wait(0.1)
        self.play(Create(crv2), run_time=1)
        self.play(FadeIn(eq17), run_time=0.5)
        self.wait()

class MGFDiffZDeterminants2(MGFDiffZDeterminants):
    def construct(self):
        eq1, eq2, eq3, eq4, eq5, box1, box2, eq6 = self.get_eqs()

        skip = False

        self.add(eq1, eq2, eq3, eq4, eq5, box1, box2, eq6)
        pos1 = box1.get_bottom() * 0.5 + mh.pos(DOWN) * 0.5
        pos2 = (eq6.get_bottom() * 0.5 + mh.pos(DOWN) * 0.5) * UP
        c_str = r'\begin{pmatrix} C_1 & tA \\ tA^T & C_2 \end{pmatrix}'
        cs_str = r"\begin{pmatrix} C'_1 & tA' \\ tA'^T & C'_2 \end{pmatrix}"
        m_str = r'\begin{pmatrix} U & 0 \\ 0 & V \end{pmatrix}'
        mt_str = r'\begin{pmatrix} U^T & 0 \\ 0 & V^T \end{pmatrix}'
        c2_str = r"\begin{pmatrix} I_k & tA' \\ tA'^T & I_{n-k}\end{pmatrix}"
        n_str = r"\begin{pmatrix} I_k & -tA' \\ 0 & I_{n-k}\end{pmatrix}"
        nt_str = r"\begin{pmatrix} I_k & 0 \\ -tA'^T & I_{n-k}\end{pmatrix}"
        eq7 = MathTex(r'C', r'=', c_str).move_to(pos1)
        eq8 = MathTex(r'C_S', r'=', cs_str).move_to(pos1)
        eq9 = Tex(r'where ', r"$C'_1, C'_2, A'$", r' are submatrices of ', r'$C_1, C_2, A$')
        eq10 = Tex(r"Choose matrices $U,V$ such that $UC'_1U^T=I_k$ and $VC'_2V^T=I_{n-k}$",
                   font_size=40)
        eq11 = MathTex(r'{\rm set\ }', r'M', r'=', m_str)
        eq12 = MathTex(r'MC_SM^T', r'=', m_str, cs_str, mt_str)
        eq13 = MathTex(r"\begin{pmatrix} UC'_1 & tUA' \\ tVA'^T & VC'_2 \end{pmatrix}")[0]
        eq14 = MathTex(r"\begin{pmatrix} UC'_1U^T & tUA'V^T \\ tVA'^TU^T & VC'_2V^T \end{pmatrix}")[0]
        eq15 = MathTex(r'MC_SM^T', r'=', c2_str)
        eq16 = Tex(r"replace $UA'V^T$ by $A'$ (just a renaming of variables)")
        eq18 = Tex(r"subtract $tA'$ times the second row from the first")
        eq19 = MathTex(r"{\rm by\  multiplying\ with\ }", r'N=', n_str)
        eq20 = MathTex(r'NMC_SM^T', r'=', n_str, c2_str)
        eq21 = MathTex(r'NMC_SM^T', r'=', n_str,
                       r"\begin{pmatrix} I_k - tA'tA'^T & tA' - tA'I_{n-k} \\ "
                       r"tA'^T & I_{n-k} \end{pmatrix}")
        eq22 = MathTex(r'NMC_SM^TN^T', r'=',
                       r"\begin{pmatrix} I_k - t^2A'A'^T & 0 \\ "
                       r"tA'^TI_{n-k}-tA'^T & I_{n-k} \end{pmatrix}", nt_str)
        eq23 = MathTex(r'NMC_SM^TN^T', r'=',
                       r"\begin{pmatrix} I_k - t^2A'A'^T & 0 \\ "
                       r"0 & I_{n-k} \end{pmatrix}", r'={\rm Cov}(NMX_S)')
        eq24 = MathTex(r'\lvert NMC_SM^TN^T\rvert', r'=', r"\lvert I_k-t^2A'A'^T\rvert").next_to(eq23[:3], DOWN)
        eq25 = MathTex(r'\lvert N\rvert\,\lvert M\rvert\,\lvert C_S\rvert\,\lvert M^T\rvert\,\lvert N^T\rvert',
                       r'=', r"\lvert I_k-t^2A'A'^T\rvert").next_to(eq23[:3], DOWN)
        eq26 = MathTex(r'\lvert N\rvert^2\,\lvert M\rvert^2\,\lvert C_S\rvert',
                       r'=', r"\lvert I_k-t^2A'A'^T\rvert").next_to(eq23[:3], DOWN)
        eq27 = MathTex(r'\lvert N\rvert^2\,\lvert M\rvert^2\,\lvert C_S\rvert',
                       r'=', r"\prod_i(1-t^2\alpha_i^2)").next_to(eq23[:3], DOWN)

        # eq7.next_to(eq6, DOWN)
        mh.align_sub(eq8, eq8[1], eq7[1])
        eq9.next_to(eq8, DOWN)
        eq10.next_to(eq8, DOWN)
        # eq11.next_to(eq10, DOWN)
        mh.align_sub(eq11, eq11[1:], eq10, direction=DOWN)
        gp1 = VGroup(eq8.copy(), eq10.copy(), eq11).move_to(pos2)
        mh.align_sub(eq12, eq12[1], gp1[0][1]).move_to(ORIGIN, coor_mask=RIGHT)
        mh.align_sub(eq13, eq13[0], eq12[3][0])
        mh.align_sub(eq14, eq14[-1], eq13[-1])
        mh.align_sub(eq15, eq15[1], eq12[1])
        mh.align_sub(eq15, eq15[2][0], eq14[0], coor_mask=RIGHT)
        eq16.next_to(eq15, DOWN).move_to(ORIGIN, coor_mask=RIGHT)
        eq18.next_to(eq15, DOWN).move_to(ORIGIN, coor_mask=RIGHT)
        eq19.next_to(eq18, DOWN)
        mh.align_sub(eq20, eq20[1], eq15[1]).move_to(ORIGIN, coor_mask=RIGHT)
        mh.align_sub(eq21, eq21[1], eq20[1]).move_to(ORIGIN, coor_mask=RIGHT)
        eq21[3][22:26].align_to(eq21[3][1], LEFT)
        eq21[3][26:30].align_to(eq21[3][11], LEFT)
        mh.align_sub(eq22, eq22[1], eq21[1]).move_to(ORIGIN, coor_mask=RIGHT)
        mh.align_sub(eq23, eq23[1], eq22[1])
        eq23.next_to(ORIGIN, ORIGIN, submobject_to_align=eq23[:3], coor_mask=RIGHT)
        eq24.next_to(eq23[:-1], DOWN)
        mh.align_sub(eq25, eq25[1], eq24[1])
        mh.align_sub(eq26, eq26[1], eq25[1])
        mh.align_sub(eq27, eq27[1], eq26[1])
        br1 = BraceLabel(eq27[0][:8], r" {\rm no\ dependence\ on\ }t"
                                      r"\ (=\lvert C'_1C'_2\rvert^{-1})",
                         label_constructor=mh.mathlabel_ctr, font_size=40,
                         brace_config={'color': RED}).set_z_index(2)
        br2 = BraceLabel(eq27[2][2:], r"{\rm nonnegative,\ decreasing\ on\ }0\le t\le 1",
                         label_constructor=mh.mathlabel_ctr, font_size=40,
                         brace_config={'color': RED}).set_z_index(2)

        if not skip:
            self.wait(0.1)
            self.play(FadeIn(eq7), rate_func=linear)
            self.wait(0.1)
            self.play(ReplacementTransform(eq7[0][:1] + eq7[1] + eq7[2][:2] + eq7[2][2:5] + eq7[2][5:7] +
                                           eq7[2][7:9] + eq7[2][9:],
                                           eq8[0][:1] + eq8[1] + eq8[2][:2] + eq8[2][3:6] + eq8[2][7:9] +
                                           eq8[2][10:12] + eq8[2][13:]),
                      FadeIn(eq8[0][1]),
                      FadeIn(eq8[2][2], eq8[2][6], eq8[2][9], eq8[2][12]))
            self.wait(0.1)
            self.play(FadeIn(eq9))
            self.wait(0.1)
            self.play(FadeOut(eq9))
            self.wait(0.1)
            self.play(FadeIn(eq10))
            self.wait(0.1)
            self.play(FadeIn(gp1[2], target_position=eq11),
                      Transform(eq8, gp1[0]),
                      Transform(eq10, gp1[1]))
            eq11 = gp1[2]
            self.wait(0.1)
            self.play(ReplacementTransform(eq8[0][:] + eq8[1] + eq8[2],
                                           eq12[0][1:3] + eq12[1] + eq12[3]),
                      FadeIn(eq12[0][0], eq12[0][3:], shift=mh.diff(eq8[0][:], eq12[0][1:3])),
                      FadeIn(eq12[2], eq12[4], shift=mh.diff(eq8[2], eq12[3])),
                      run_time=2)
            self.wait(0.1)
            self.play(
                ReplacementTransform(
                    eq12[3][-1:] + eq12[3][0] + eq12[3][1:5] + eq12[3][5:8] + eq12[3][8:11] + eq12[3][11:14],
                    eq13[-1:] + eq13[0] + eq13[2:6] + eq13[7:10] + eq13[11:14] + eq13[15:18]
                ),
                eq12[4].animate.shift(mh.diff(eq12[3][-1], eq13[-1])),
                run_time=1.5)
            self.play(
                ReplacementTransform(
                    eq12[2][1:2] + eq12[2][1].copy() + eq12[2][4] + eq12[2][4].copy(),
                    eq13[1:2] + eq13[6] + eq13[10] + eq13[14]
                ),
                FadeOut(eq12[2][0], eq12[2][2:4], eq12[2][-1], shift=mh.diff(eq12[3][0], eq13[0])),
                run_time=2
            )
            self.wait(0.1)
            self.play(
                ReplacementTransform(
                    eq13[:5] + eq13[5:9] + eq13[9:14] + eq13[14:18] + eq13[18],
                    eq14[:5] + eq14[7:11] + eq14[13:18] + eq14[20:24] + eq14[26]
                ),
                run_time=1)
            self.play(
                ReplacementTransform(
                    eq12[4][1:3] + eq12[4][1:3].copy() + eq12[4][5:7] + eq12[4][5:7].copy(),
                    eq14[5:7] + eq14[18:20] + eq14[11:13] + eq14[24:26]
                ),
                FadeOut(eq12[4][0], eq12[4][3:5] + eq12[4][-1]),
                run_time=2)
            self.play(ReplacementTransform(eq12[:2], eq15[:2]), run_time=1.5)
            self.wait(0.1)
            eq15_1 = eq15.copy().move_to(ORIGIN, coor_mask=RIGHT)
            mh.align_sub(eq15[2][1:6], eq15[2][4], eq14[9])
            eq15[2][1:3].move_to(eq14[1:7], coor_mask=RIGHT)
            mh.align_sub(eq15[2][6:14], eq15[2][7], eq14[15])
            eq15[2][10:14].move_to(eq14[20:26], coor_mask=RIGHT)
            self.play(FadeOut(eq14[1:7], eq14[20:26]),
                      FadeIn(eq15[2][1:3], eq15[2][10:14]))
            self.wait(0.1)
            self.play(FadeOut(eq10, eq11), FadeIn(eq16), run_time=1.5)
            self.wait(0.1)
            self.play(FadeOut(eq14[8], eq14[11:13], eq14[14], eq14[18:20]),
                      mh.rtransform(eq14[7], eq15[2][3], eq14[9:11], eq15[2][4:6],
                                    eq14[13], eq15[2][6], eq14[15:18], eq15[2][7:10]),
                      )
            self.play(mh.rtransform(eq14[0], eq15[2][0].move_to(eq15_1[2][0]),
                                    eq14[-1], eq15[2][-1].move_to(eq15_1[2][-1])),
                      mh.transform(eq15[2][1:-1], eq15_1[2][1:-1], eq15[:2], eq15_1[:2]),
                      run_time=1.5)
            self.wait()
            self.play(FadeOut(eq16), FadeIn(eq18))
            self.play(FadeIn(eq19))
            self.wait(0.1)
            self.play(mh.rtransform(eq15[0][:], eq20[0][1:], eq15[1], eq20[1], eq15[2], eq20[3]),
                      FadeIn(eq20[0][0], shift=mh.diff(eq15[0][:], eq20[0][1:])),
                      FadeIn(eq20[2], shift=mh.diff(eq15[2], eq20[3])),
                      run_time=1.5)
            self.wait(0.1)
            self.play(mh.rtransform(eq20[:3], eq21[:3], eq20[3][:3], eq21[3][:3], eq20[3][-1], eq21[3][-1],
                                    eq20[3][3:6], eq21[3][11:14], eq20[3][6:10], eq21[3][22:26],
                                    eq20[3][10:14], eq21[3][26:30]),
                      run_time=1.5)
            self.play(mh.rtransform(eq21[2][3:7], eq21[3][3:7], eq21[3][22:26].copy(), eq21[3][7:11],
                                    eq21[2][3:7].copy(), eq21[3][14:18], eq21[3][26:30].copy(), eq21[3][18:22]),
                      FadeOut(eq21[2][:3], eq21[2][7:]),
                      run_time=2)
            eq21_1 = mh.align_sub(eq22[2][1:11].copy(), eq22[2][1], eq21[3][1])
            eq21_2 = eq22[2][11].copy().move_to(eq21[3][12], aligned_edge=DOWN)
            self.wait(0.1)
            self.play(mh.rtransform(eq21[3][1:5], eq21_1[:4], eq21[3][5:7], eq21_1[5:7],
                                    eq21[3][8:11], eq21_1[7:10]),
                      ReplacementTransform(eq21[3][7], eq21_1[3]),
                      FadeIn(eq21_1[4]),
                      )
            self.wait(0.1)
            self.play(FadeOut(eq21[3][11:14]),
                      FadeOut(eq21[3][14], target_position=eq21[3][12]),
                      FadeOut(eq21[3][15:22], shift=mh.diff(eq21[3][15], eq21[3][11])),
                      FadeIn(eq21_2))
            self.wait(0.1)
            self.play(mh.rtransform(eq21[0][:], eq22[0][:-2], eq21[1], eq22[1],
                                    eq21[3][0], eq22[2][0], eq21_1, eq22[2][1:11],
                                    eq21_2, eq22[2][11],
                                    eq21[3][22:26], eq22[2][12:16],
                                    eq21[3][26:], eq22[2][25:]))
            self.wait(0.1)
            self.play(FadeIn(eq22[0][-2:], eq22[3]), run_time=1.5)
            self.wait(0.1)
            self.play(mh.rtransform(
                eq22[2][25:29].copy(), eq22[2][16:20],
                eq22[3][4:9], eq22[2][20:25]),
                FadeOut(eq22[3][:4], eq22[3][9:]),
            run_time=2)
            self.wait(0.1)
            eq22_1 = eq22[2][12:25]
            eq22_2 = eq23[2][12].copy().move_to(eq21_1, coor_mask=RIGHT)
            self.play(FadeOut(eq22_1[:8], shift=mh.diff(eq22_1[1], eq22_2, coor_mask=RIGHT)),
                      FadeOut(eq22_1[8], shift=mh.diff(eq22_1[8], eq22_2, coor_mask=RIGHT)),
                      FadeOut(eq22_1[9:], shift=mh.diff(eq22_1[10], eq22_2, coor_mask=RIGHT)),
                      FadeIn(eq22_2),
                      run_time=1.5)
            self.wait(0.1)
            self.play(mh.rtransform(eq22[:2], eq23[:2], eq22[2][:12], eq23[2][:12],
                                    eq22[2][25:], eq23[2][13:], eq22_2, eq23[2][12]),
    #                  mh.fade_replace(eq22[2][12:25], eq23[2][12]),
            run_time=2)
            self.wait(0.1)
            self.play(FadeOut(eq18, eq19))
            self.wait(0.1)
            self.play(FadeIn(eq24),
                      run_time=1)
            self.wait(0.1)
            self.play(mh.rtransform(
                eq24[0][:2], eq25[0][:2], eq24[0][2], eq25[0][4],
                eq24[0][3:5], eq25[0][7:9], eq24[0][5:7], eq25[0][11:13],
                eq24[0][7:], eq25[0][15:], eq24[1:], eq25[1:]
            ),
            FadeIn(eq25[0][2], shift=mh.diff(eq24[0][1], eq25[0][1])),
            FadeIn(eq25[0][3], eq25[0][5], shift=mh.diff(eq24[0][2], eq25[0][4])),
            FadeIn(eq25[0][6], eq25[0][9], shift=mh.diff(eq24[0][3], eq25[0][7])),
            FadeIn(eq25[0][10], eq25[0][13], shift=mh.diff(eq24[0][5], eq25[0][11])),
            FadeIn(eq25[0][14], shift=mh.diff(eq24[0][7], eq25[0][15])))
            self.wait(0.1)
            self.play(mh.rtransform(
                eq25[0][:3], eq26[0][:3], eq25[0][3:6], eq26[0][4:7], eq25[0][6:10], eq26[0][8:12],
                eq25[1:], eq26[1:]
            ), mh.rtransform(
                eq25[0][10:12], eq26[0][4:6], eq25[0][13], eq26[0][6],
                eq25[0][14:16], eq26[0][:2], eq25[0][17], eq26[0][2]
            ), FadeOut(eq25[0][12], shift=mh.diff(eq25[0][11], eq26[0][5])),
            FadeOut(eq25[0][16], shift=mh.diff(eq25[0][15], eq26[0][1])),
            FadeIn(eq26[0][3], shift=mh.diff(eq25[0][2], eq26[0][2])),
            FadeIn(eq26[0][7], shift=mh.diff(eq25[0][5], eq26[0][6])))
            self.wait(0.1)
            self.play(FadeIn(br1))
            self.wait(0.1)
            eq23.generate_target().to_edge(RIGHT)
            eq23[3].set_opacity(0)
            self.add(eq23)
            self.play(MoveToTarget(eq23), run_time=1.5)
            self.wait(0.1)
            self.play(mh.rtransform(eq26[:2], eq27[:2], eq26[2][3:6], eq27[2][4:7]
                                    ),
                      mh.fade_replace(eq26[2][0], eq27[2][2]),
                      mh.fade_replace(eq26[2][1], eq27[2][3], coor_mask=RIGHT),
                      FadeOut(eq26[2][2], shift=mh.diff(eq26[2][1], eq27[2][3])),
                      FadeOut(eq26[2][6:8], shift = mh.diff(eq26[2][6], eq27[2][7], coor_mask=RIGHT)),
                      FadeIn(eq27[2][7:10], shift=mh.diff(eq26[2][6], eq27[2][7], coor_mask=RIGHT)),
                      FadeOut(eq26[2][8:11], shift = mh.diff(eq26[2][8], eq27[2][7], coor_mask=RIGHT)),
                      mh.fade_replace(eq26[2][11], eq27[2][10], coor_mask=RIGHT),
                      FadeIn(eq27[2][:2], shift=mh.diff(eq26[2][0], eq27[2][2], coor_mask=RIGHT)),
                      #                  FadeOut(eq26[2][6:8], shift=mh.diff(eq26[2][6], eq27[2][9], coor_mask=RIGHT)),
    #                  mh.fade_replace(eq26[2][8:10], eq27[2][7:9], coor_mask=RIGHT),
                      run_time=1.5)
        else:
            self.add(eq27, eq23, br1)

        # \\ {\rm equals\ }$\lvert C'_1C'_2\rvert^{-1}$
        # {\rm no\ dependence\ on\ }$t$

        self.wait(0.1)
        self.play(FadeOut(br1), FadeIn(br2))

        ax = Axes(x_range=[0, 1.4], y_range=[0, 1.2], x_length=4, y_length=2.1,
                  axis_config={'color': WHITE, 'stroke_width': 3, 'include_ticks': False,
                               "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                               "include_tip": True
                               },
                  ).set_z_index(1).to_edge(DL, buff=0.2).shift(UP*0.1)

        line1 = DashedLine(ax.coords_to_point(1, 0), ax.coords_to_point(1, 1), color=WHITE, stroke_opacity=0.7)
        line2 = DashedLine(ax.coords_to_point(0, 1), ax.coords_to_point(1, 1), color=WHITE, stroke_opacity=0.7)
        lab1 = MathTex(r't', font_size=40).next_to(ax.x_axis.get_end(), UL, buff=0.15)
        lab2 = MathTex(r'1-t^2\alpha^2', font_size=40).next_to(ax.y_axis.get_end(), RIGHT, buff=0.2)
        lab3 = MathTex(r'1', font_size=35).next_to(ax.coords_to_point(1, 0), DOWN, buff=0.05)
        lab4 = MathTex(r'1', font_size=35).next_to(ax.coords_to_point(0, 1), LEFT, buff=0.05)

        plt = ax.plot(lambda t: 1 - (t/1.2)**2, [0, 1.25], stroke_color=YELLOW, stroke_width=4)
        self.play(FadeIn(ax, line1, line2, lab1, lab2, lab3, lab4))
        self.play(Create(plt), run_time=1, rate_func=linear)

        self.wait()

def indicator_func(r, h=1.):
    """
    smoothed indicator of [-1,1], height h
    """
    beta = PI/r
    scale = h / (2 * r)

    def f(t):
        s = 1 - abs(t)
        if s >= r:
            return h
        elif s <= -r:
            return 0.
        return (s + r + math.sin(s*beta)/beta) * scale
    return f


def indicator_func_diff(r, h=1.):
    """
    differentiated smoothed indicator of [-1,1] of height h
    derivative max value is h/r
    """
    beta = PI/r
    scale = h / (2 * r)

    def f(t):
        s, u = (1 - t, 1) if t > 0 else (1 + t, -1)
        if -r < s < r:
            return (1 + math.cos(s*beta)) * scale * u
        else:
            return 0.
    return f


red1 = ManimColor((255, 50, 0))

class Diff1D(Scene):
    """
    derivatives of f(x)=I([-1,1])
    """
    r = 0.2
    name = r'x'
    scale = 1.
    right_only=False

    def do_anim(self, r=0.2, name=r'x', scale=1., right_only=False):
        xmax = 1 + r * 2
        ymax = 1.2
        label_size = 35 * scale
        eq_size = 40 * scale

        ax = Axes(x_range=[-xmax, xmax + 0.2, 1], y_range=[0, ymax], x_length=8 * scale, y_length=2.5 * scale,
                  axis_config={'color': WHITE, 'stroke_width': 4, 'include_ticks': False,
                               "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH * scale,
                               "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH * scale,
                               "tick_size": 0.1 * scale
                               },
                  x_axis_config={'include_ticks': True}
                  ).set_z_index(1)

        pt1 = ax.coords_to_point(0, 0)
        pt2 = ax.coords_to_point(1, 0)
        pt3 = ax.coords_to_point(-1, 0)
        buff = 0.15 * scale
        eq1 = MathTex(r'0', font_size=label_size).next_to(pt1, DOWN, buff=buff)
        eq2 = MathTex(r'1', font_size=label_size).next_to(pt2, DOWN, buff=buff)
        eq3 = MathTex(r'-1', font_size=label_size)
        eq3.next_to(pt3, DOWN, buff=buff, submobject_to_align=eq3[0][1])
        eq4 = MathTex(r'{{ {} }}_1'.format(name), font_size=label_size).next_to(ax.x_axis.get_right(), UL, buff=0.2 * scale)
        dx = 0.01
        rval = ValueTracker(0.001)

        xmin = 0. if right_only else -xmax

        def smooth_anim():
            f = indicator_func(rval.get_value())
            plt = ax.plot(f, [xmin, xmax, dx], color=BLUE, use_smoothing=False, stroke_width=6).set_z_index(1)
            return plt

        plt2 = always_redraw(smooth_anim)
        eqf = MathTex(r'f({})'.format(name), r' ({\rm smoothed})', font_size=eq_size)
        eqdf = MathTex(r'-\partial_1f({})'.format(name), font_size=eq_size)
        # eqf[1].next_to(eqf[0], DOWN).align_to(eqf[0], LEFT)
        eqf.next_to(ax.y_axis.get_top(), RIGHT, buff=0.2*scale, aligned_edge=UP).shift(UP*0.2*scale)
        eqdf.next_to(ax.y_axis.get_top(), RIGHT, buff=0.2*scale, aligned_edge=UP).shift(UP*0.05*scale)

        self.add(ax, eq1, eq2, eq3, eq4, plt2, eqf[0])
        self.wait(0.1)
        self.play(rval.animate.set_value(r), FadeIn(eqf[1]), run_time=2.5)
        self.remove(plt2)
        plt2 = smooth_anim()
        self.add(plt2)
        r = rval.get_value()
        self.wait(0.1)

        f = indicator_func_diff(r, r * 1.1)
        plt3 = ax.plot(f, [xmin, xmax, dx], colorscale=[(red1, -0.5), (BLUE, 0)], use_smoothing=False, stroke_width=6).set_z_index(1)
        self.play(FadeOut(plt2, eqf), FadeIn(plt3, eqdf), run_time=1, rate_func=linear)
        self.wait()

    def construct(self):
        self.do_anim(r=self.r, name=self.name, scale=self.scale, right_only=self.right_only)


class Diff1DZ(Diff1D):
    """"
    derivatives of f(z) = I([-1,1])
    """
    name = r'z'


class Diff1DZPos(Diff1DZ):
    """
    derivatives of f(z) = I([-1,1]) restricted to z > 0
    """
    right_only = True


class Diff2D(ThreeDScene):
    r = 0.2
    scale = 1.0
    name = r'x'
    right_only=False
    ver=0

    def do_anim(self, r=0.2, scale=1., name=r'x', right_only=False, ver=0):
        xmax = 1 + r * 2
        zmax = 1.2
        label_size = 35 * scale
        eq_size = 40 * scale
        xrange = [-xmax, xmax]
        xrange2 = [-xmax*1.1, xmax*1.1]
        xlen = 8
        zlen = 2.5 * scale

        if right_only:
            xrescale = (xrange2[1] - xrange2[0]*0.3)/(xrange2[1] - xrange2[0])
            xrange2[0] *= 0.3
            xlen *= xrescale

        ax = ThreeDAxes(xrange2, xrange2, [-0.03, zmax, 1], xlen, xlen, zlen,
                        axis_config={'color': WHITE, 'stroke_width': 2, 'include_ticks': False,
                                     "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH * scale,
                                     "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH * scale,
                                     "stroke_width": 6
                                     },
                        )
        origin = ORIGIN
        ax.shift(origin - ax.coords_to_point(0, 0, 0))
        VGroup(ax.x_axis[:], ax.y_axis[:]).shift(IN*0.05*scale)

        gp = Group(ax)
        ax.z_axis.rotate(110*DEGREES, OUT, origin)
        gp.rotate(90*DEGREES, LEFT, origin)
        gp.rotate(110 * DEGREES, DOWN, origin)
        gp.rotate(15*DEGREES, RIGHT, origin)
#        gp.rotate(-90*DEGREES, RIGHT, origin)
#        gp.rotate(40*DEGREES, UP, origin)
#        gp.rotate(-10*DEGREES, RIGHT, origin)
        dx = ax.coords_to_point(1, 0, 0) - origin
        dy = ax.coords_to_point(0, 1, 0) - origin
        dz = ax.coords_to_point(0, 0, 1) - origin
        eqx = MathTex(r'{{ {} }}_1'.format(name), font_size=label_size).move_to(ax.x_axis.get_end() + dx*0.2)
        eqy = MathTex(r'{{ {} }}_2'.format(name), font_size=label_size).move_to(ax.y_axis.get_end() + dy*0.2)
        eqz1 = MathTex(r'f({})'.format(name), font_size=eq_size).move_to(ax.z_axis.get_end() + RIGHT*0.15*scale, aligned_edge=LEFT)
        eqz2 = MathTex(r'-\partial_2f({})'.format(name), font_size=eq_size).move_to(ax.z_axis.get_end() + RIGHT*0.15*scale, aligned_edge=LEFT)
        eqz3 = MathTex(r'\partial_1\partial_2f({})'.format(name), font_size=eq_size).move_to(ax.z_axis.get_end() + RIGHT*0.15*scale, aligned_edge=LEFT)

        f = indicator_func(r)
        f1 = indicator_func_diff(r, r * 1.2)

        def g(u, v):
            return f(u) * f(v)

        def g1(u,v):
            return f(u) * f1(v)

        def g2(u, v):
            return f1(u) * f1(v)

        blue2 = ManimColor(blue.to_rgb()*0.5 + WHITE.to_rgb()*0.5)
        if right_only:
            xrange[0] = 0.
        surf1 = ax.plot_surface(g, xrange, xrange, fill_opacity=0.7, resolution=50, colorscale=[blue, blue2])
        surf2 = ax.plot_surface(g1, xrange, xrange, fill_opacity=0.7, resolution=50, colorscale=[(red, -0.1), (blue,0), (blue2,1)])
        surf3 = ax.plot_surface(g2, xrange, xrange, fill_opacity=0.7, resolution=100, colorscale=[(red, -0.1), (blue,0), (blue2,1)])

        self.add(ax, eqx, eqy, surf1, eqz1)
        if ver == 0:
            self.wait()
        elif ver == 1:
            return
        self.remove(surf1, eqz1)
        self.add(surf2, eqz2)
        if ver == 0:
            self.wait()
        elif ver == 2:
            return
        self.remove(surf2, eqz2)
        self.add(surf3, eqz3)
        if ver == 0:
            self.wait()

    def construct(self):
        self.do_anim(r=self.r, scale=self.scale, name=self.name, right_only=self.right_only, ver=self.ver)


class Diff3D(ThreeDScene):
    name = r'x'
    show_labels = True
    right_only = False
    ver = 0
    frame_scale = 2

    def do_surrounds(self):
        eq1, eq2, eq3, eq4, eq5, box = MGFDiffZ().get_eqs()

        self.add(eq1, eq2, eq3, eq4, eq5, box)

        eq6 = MathTex(r'f(z)', r'=', r'I(z\in[-1,1]^3) ', r'=', r' I(\max_i\lvert z_i\rvert\le 1)').next_to(box, DOWN)
        eq6.to_edge(LEFT)
        eq6[3:].next_to(eq6[:3], DOWN).align_to(eq6[1], LEFT)
        self.play(FadeIn(eq6[:3]))
        self.wait(0.1)
        self.play(FadeIn(eq6[3:]))

    def do_anim(self, name=r'x', show_labels=True, right_only=False, ver=0):
        self.camera.frame_height *= self.frame_scale
        self.camera.frame_width *= self.frame_scale
        xmax = 1.5
        xrange = [-xmax, xmax]
        scale = 1.4
        origin = DOWN * 1.8 + RIGHT * 0.5
        xlen = 2 * xmax * scale

        if right_only:
            xrescale = (xrange[1] - xrange[0]*0.3)/(xrange[1] - xrange[0])
            xrange[0] *= 0.3
            xlen *= xrescale

        ax = ThreeDAxes(xrange, xrange, xrange, xlen, xlen, xlen,
                        axis_config={'color': WHITE, 'stroke_width': 4, 'include_ticks': False,
                                     "tip_width": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                                     "tip_height": 0.5 * DEFAULT_ARROW_TIP_LENGTH,
                                     "shade_in_3d": True,
                                     },
                        )
#        ax.y_axis.rotate(45*DEGREES, UP)
        ax.shift(-ax.coords_to_point(0, 0, 0))
        ax.z_axis.rotate(90*DEGREES, OUT)
        cube_args = {'fill_opacity': 0.7, 'fill_color': blue, 'stroke_opacity': 1, 'stroke_color': BLUE, 'stroke_width': 2}
        if right_only:
            cube = Cube(side_length=scale, **cube_args).shift((RIGHT + UP + OUT)*scale/2)
        else:
            cube = Cube(side_length=2 * scale, **cube_args)
        dotx = Dot().shift(RIGHT * scale)
        doty = Dot().shift(UP * scale)
        dotz = Dot().shift(OUT * scale)

        gp = VGroup(ax, cube, dotx, doty, dotz)
        gp.shift(origin)
        gp.rotate(-40*DEGREES, UP, origin)
        gp.rotate(10*DEGREES, RIGHT, origin)
        px = dotx.get_center()
        py = doty.get_center()
        pz = dotz.get_center()
        dirx = px - origin
        diry = py - origin
        dirz = pz - origin
        eqx = MathTex(r'{}_1'.format(name)).set_z_index(10).move_to(origin + dirx * (xmax + 0.3))
        eqy = MathTex(r'{}_2'.format(name)).set_z_index(10).move_to(origin + diry * xmax, aligned_edge=UP).shift(RIGHT*0.4)
        eqz = MathTex(r'{}_3'.format(name)).set_z_index(10).move_to(origin + dirz * (xmax + 0.3), aligned_edge=UP).shift(RIGHT*0.4)
        p1 = origin + 0.2 * dirx + 0.5 * diry+0.2 * dirz
#        p2 = origin + RIGHT * scale * 2.5 + OUT * scale*1 + UP * scale * 0.6
        p2 = p1 + dirx * 1 + RIGHT
        eq1 = MathTex(r'f({})=1'.format(name), font_size=40, stroke_width=1.3).next_to(p2, RIGHT, buff=0)
        arr = Arrow3D(p2, p1, fill_color=RED, resolution=(10, 8),
                     thickness=0.02)

        p1 = origin + dirx * 1.1 + 0.5 *(diry + dirz)
        p2 = p1 + RIGHT * 2
        p3 = origin - dirx * 0.99 + 0.5*(diry+dirz)
        p4 = p3 + dirz * 1 + OUT * 0.8 + RIGHT * 2.8 + DOWN

        arr2 = Arrow3D(p2, p1, fill_color=RED, resolution=(10, 8),
                     thickness=0.02).set_z_index(5)
        arr2_1 = Arrow3D(p4, p3, fill_color=RED, resolution=(10, 8),
                     thickness=0.02)
        eq7 = MathTex(r'(-\partial_1)f({})'.format(name), r'=\delta({}_1-1)'.format(name), font_size=35, stroke_width=1.3).next_to(p2, RIGHT)
#        eq7[1].next_to(eq7[0], DOWN, buff=0.2).align_to(eq7[0], LEFT)
        eq7_1 = MathTex(r'-\partial_1f({})'.format(name),
                        r'=-\delta({}_1+1)'.format(name), font_size=35, stroke_width=1.3)
        eq7_1.next_to(p4, DOWN, aligned_edge=UP, buff=0.2, submobject_to_align=eq7_1[0]).shift(RIGHT*0.4)
#        eq7_1[1].next_to(eq7_1[0], DOWN, buff=0.2).align_to(eq7_1[0], LEFT)

        blue2 = ManimColor(blue.to_rgb()*0.5 + GREEN.to_rgb()*0.5)

        face1 = cube[3].copy().set_fill(color=blue2, opacity=1)
        face2 = cube[2].copy().set_fill(color=RED, opacity=1)

        edge1 = Line(origin+dirx+diry-dirz, origin+dirx+diry+dirz, stroke_width=10, color=blue2, stroke_opacity=1).set_z_index(3)
        if right_only:
            edge1 = Line(origin+dirx+diry, origin+dirx+diry+dirz, stroke_width=6, color=blue2, stroke_opacity=1).set_z_index(3)
        edge2 = Line(origin-dirx-diry-dirz, origin-dirx-diry+dirz, stroke_width=10, color=blue2, shade_in_3d=True).set_z_index(0)
        edge3 = Line(origin+dirx-diry-dirz, origin+dirx-diry+dirz, stroke_width=10, color=RED, shade_in_3d=True).set_z_index(0)
        edge4 = Line(origin-dirx+diry-dirz, origin-dirx+diry+dirz, stroke_width=10, color=RED, shade_in_3d=True).set_z_index(3)
        p3 = origin + dirx + diry + dirz*0.5+RIGHT*0.1
        p4 = p3 + RIGHT*1.5
        eq8 = MathTex(r'\partial_2\partial_1f({})'.format(name), r'=\delta({}_2-1)\delta({}_1-1)'.format(name, name), font_size=35, stroke_width=1.3)
        eq8.next_to(p4, RIGHT, submobject_to_align=eq8[0])
#        eq8[1].next_to(eq8[0], DOWN, buff=0.1).align_to(eq8[0], LEFT)
        arr3 = Arrow3D(p4, p3, resolution=(10, 8),
                       thickness=0.02).set_z_index(5)
        p5 = origin + dirx * 1.05 - diry + dirz*0.0
        p6 = p5 + RIGHT*1.2 + UP*0.0
        eq8_1 = MathTex(r'\partial_2\partial_1f({})'.format(name), r'=-\delta({}_2+1)\delta({}_1-1)'.format(name, name), font_size=35, stroke_width=1.3)
        eq8_1.next_to(p6, RIGHT)
#        eq8_1[1].next_to(eq8_1[0], DOWN, buff=0.1).align_to(eq8_1[0], LEFT)
        arr3_1 = Arrow3D(p6, p5, resolution=(10, 8),
                       thickness=0.02).set_z_index(10)

        co1=Dot3D(radius=0.08, stroke_color=blue2, color=blue2, fill_opacity=1).move_to(origin+dirx+diry+dirz).set_z_index(4)
        co2=Dot3D(radius=0.08, color=RED, fill_opacity=1).move_to(origin-dirx+diry+dirz).set_z_index(4)
        co3=Dot3D(radius=0.08, color=RED, fill_opacity=1).move_to(origin+dirx-diry+dirz).set_z_index(4)
        co4=Dot3D(radius=0.08, color=RED, fill_opacity=1).move_to(origin+dirx+diry-dirz).set_z_index(4)
        co5=Dot3D(radius=0.08, color=blue2, fill_opacity=1).move_to(origin+dirx-diry-dirz).set_z_index(4)
        co6=Dot3D(radius=0.08, color=blue2, fill_opacity=1).move_to(origin-dirx+diry-dirz).set_z_index(4)
        co7=Dot3D(radius=0.08, color=blue2, fill_opacity=1).move_to(origin-dirx-diry+dirz).set_z_index(4)
        co8=Dot3D(radius=0.08, color=PURE_RED, fill_opacity=1).move_to(origin-dirx-diry-dirz).set_z_index(0)

        p5=origin+dirx+diry+dirz+OUT*0.1
        p6=p5+DOWN*0.1+RIGHT*2
        eq9=MathTex(r'-\partial_3\partial_2\partial_1f({})'.format(name),
                    r'=\delta({}_3-1)\delta({}_2-1)\delta({}_1-1)'.format(name, name, name), font_size=35, stroke_width=1.3).next_to(p6, RIGHT, buff=0.15)
        arr4 = Arrow3D(p6, p5 + RIGHT*0.1, resolution=(10, 8),
                       thickness=0.02).set_z_index(5)
        p7=origin+dirx-diry+dirz+OUT*0.1
        p8=p7+UP*0.2+RIGHT*2
        eq9_1=MathTex(r'-\partial_3\partial_2\partial_1f({})'.format(name),
                    r'=-\delta({}_3+1)\delta({}_2-1)\delta({}_1-1)'.format(name, name, name), font_size=35, stroke_width=1.3).next_to(p8, RIGHT, buff=0.15).shift(UP*0.05).set_z_index(100)
        arr4_1 = Arrow3D(p8, p7 + RIGHT * 0.1, resolution=(10, 8),
                       thickness=0.02).set_z_index(5)

        self.add(ax, cube, eqx, eqy, eqz)
        if show_labels:
            self.add(eq1, arr)
        if ver == 0:
            self.wait()
        elif ver == 1:
            return

        cube.set_opacity(cube_args['fill_opacity'] * 0.7)
        if right_only:
            self.add(face1)
        else:
            self.add(face1, face2)
        if show_labels:
            self.remove(eq1, arr)
            self.add(arr2, eq7)
            if not right_only:
                self.add(arr2_1, eq7_1)
        if ver == 0:
            self.wait()
        elif ver == 2:
            return
        VGroup(face1, face2).set_fill(opacity=0.5)
        if right_only:
            self.add(edge1)
        else:
            self.add(edge1, edge2, edge3, edge4)
        if show_labels:
            self.remove(arr2, eq7, arr2_1, eq7_1)
            self.add(arr3, eq8)
            if not right_only:
                self.add(arr3_1, eq8_1)
        if ver == 0:
            self.wait()
        elif ver == 3:
            return
        VGroup(edge1, edge2, edge3, edge4).set_opacity(0.5)
        if right_only:
            self.add(co1)
        else:
            self.add(co1, co2, co3, co4, co5, co6, co7, co8)

        if show_labels:
            self.remove(arr3, eq8, arr3_1, eq8_1)
            self.add(eq9, arr4)
            if not right_only:
                self.add(eq9_1, arr4_1)

        if ver == 0:
            self.wait()

    def construct(self):
        # self.do_surrounds()
#        cam = ThreeDCamera(default_distance=10)
#        cam.pixel_array

        self.do_anim(name=self.name, show_labels=self.show_labels, right_only=self.right_only, ver=self.ver)


class Diff2Dv1(Diff2D):
    """
    image of f(x) = I([-1,1]^2)
    """
    ver=1


class Diff2Dv2(Diff2D):
    """
    image of df for f(x) = I([-1,1]^2)
    """
    ver = 2


class Diff2Dv3(Diff2D):
    """
    image of d2f for f(x) = I([-1,1]^2)
    """
    ver = 3


class Diff2DZv1(Diff2Dv1):
    """
    image of f(z) = I([-1,1]^2)
    """
    name = r'z'


class Diff2DZv2(Diff2DZv1):
    """
    image of df for f(z) = I([-1,1]^2)
    """
    ver = 2


class Diff2DZv3(Diff2DZv1):
    """
    image of d2f for f(z) = I([-1,1]^2)
    """
    ver = 3


class Diff2DZPosv1(Diff2DZv1):
    """
    image of f(z) = I([-1,1]^2) on z > 0
    """
    right_only = True


class Diff2DZPosv2(Diff2DZPosv1):
    """
    image of df for f(z) = I([-1,1]^2) on z > 0
    """
    ver = 2


class Diff2DZPosv3(Diff2DZPosv1):
    """
    image of d2f for f(z) = I([-1,1]^2) on z > 0
    """
    ver = 3


class Diff3Dv1(Diff3D):
    """
    image of f(x) = I([-1,1]^3)
    """
    ver = 1


class Diff3Dv2(Diff3D):
    """
    image of df for f(x) = I([-1,1]^3)
    """
    ver = 2


class Diff3Dv3(Diff3D):
    """
    image of d2f for f(x) = I([-1,1]^3)
    """
    ver = 3


class Diff3Dv1_NL(Diff3Dv1):
    """
    image of f(x) = I([-1,1]^3), no labels
    """
    show_labels = False


class Diff3Dv2_NL(Diff3Dv1_NL):
    """
    image of df for f(x) = I([-1,1]^3), no labels
    """
    ver = 2


class Diff3Dv3_NL(Diff3Dv1_NL):
    """
    image of d2f for f(x) = I([-1,1]^3), no labels
    """
    ver = 3


class Diff3DZv1(Diff3Dv1):
    """
    image of f(z) = I([-1,1]^3)
    """
    name = r'z'


class Diff3DZv2(Diff3DZv1):
    """
    image of df for f(z) = I([-1,1]^3)
    """
    ver = 2


class Diff3DZv3(Diff3DZv1):
    """
    image of d2f for f(z) = I([-1,1]^3)
    """
    ver = 3


class Diff3DZv4(Diff3DZv1):
    """
    image of d3f for f(z) = I([-1,1]^3)
    """
    ver = 4


class Diff3DZv1_NL(Diff3DZv1):
    """
    image of f(z) = I([-1,1]^3), no labels
    """
    show_labels = False


class Diff3DZv2_NL(Diff3DZv1_NL):
    """
    image of df for f(z) = I([-1,1]^3), no labels
    """
    ver = 2


class Diff3DZv3_NL(Diff3DZv1_NL):
    """
    image of d2f for f(z) = I([-1,1]^3), no labels
    """
    ver = 3


class Diff3DZv4_NL(Diff3DZv1_NL):
    """
    image of d3f for f(z) = I([-1,1]^3), no labels
    """
    ver = 4


class Diff3DZPosv1(Diff3DZv1):
    """
    image of f(z) = I([-1,1]^3), on z > 0
    """
    right_only = True


class Diff3DZPosv2(Diff3DZPosv1):
    """
    image of df for f(z) = I([-1,1]^3), on z > 0
    """
    ver = 2


class Diff3DZPosv3(Diff3DZPosv1):
    """
    image of d2f for f(z) = I([-1,1]^3), on z > 0
    """
    ver = 3


class Diff3DZPosv4(Diff3DZPosv1):
    """
    image of d3f for f(z) = I([-1,1]^3), on z > 0
    """
    ver = 4


class SubMatrix(Scene):
    def construct(self):
        line1 = MGFDiff().get_eqs()[4][-2]
        eq1 = MathTex(r'A', r'=', r'\begin{pmatrix}'
                      r'a_{11} & a_{12} & a_{13} & a_{14} \\ '
                      r'a_{21} & a_{22} & a_{23} & a_{24} \\ '
                      r'a_{31} & a_{32} & a_{33} & a_{34} \\ '
                      r'a_{41} & a_{42} & a_{43} & a_{44}'
                      r'\end{pmatrix}').set_z_index(10)
        eq2 = MathTex(r'S = \{2, 4\}')
        eq3 = Tex(r'{\bf Submatrices}\\ (example)', color=BLUE)
        pos1 = line1.get_center()/2 + UP * config.frame_y_radius/2
        eq1.move_to(pos1)
        eq3.next_to(eq1, LEFT, buff=1, submobject_to_align=eq3[0])
        eq2.next_to(eq3, DOWN, buff=0.25)
        VGroup(eq2, eq3).move_to(pos1, coor_mask=UP)
        VGroup(eq1, eq2, eq3).move_to(ORIGIN, coor_mask=RIGHT)
        eq4 = MathTex(r'A_S', r'=', r'\begin{pmatrix}'
                      r'a_{22} & a_{24} \\ '
                      r'a_{42} & a_{44}'
                      r'\end{pmatrix}').set_z_index(10)
        mh.align_sub(eq4, eq4[1], eq1[1])

        row2 = eq1[2][16:28]
        row4 = eq1[2][40:52]
        col2 = eq1[2][7:10] + eq1[2][43:46]
        col4 = eq1[2][13:16] + eq1[2][49:52]
        row1b = eq4[2][1:7]
        row2b = eq4[2][7:13]
        col1b = eq4[2][1:4] + eq4[2][7:10]
        col2b = eq4[2][4:7] + eq4[2][10:13]

        color = ManimColor(WHITE.to_rgb() * 0.5)
        buff = 0.07
        opacity = 0.5
        rec1 = SurroundingRectangle(row2, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        rec2 = SurroundingRectangle(row4, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        rec3 = SurroundingRectangle(col2, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        rec4 = SurroundingRectangle(col4, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        recs1 = VGroup(rec1, rec2, rec3, rec4)
        rec5 = SurroundingRectangle(row1b, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        rec6 = SurroundingRectangle(row2b, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        rec7 = SurroundingRectangle(col1b, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        rec8 = SurroundingRectangle(col2b, stroke_opacity=0, fill_opacity=opacity, fill_color=color, buff=buff)
        recs2 = VGroup(rec5, rec6, rec7, rec8).set_opacity(0)

        self.add(eq1, eq2, eq3, line1)
        self.wait(0.1)
        self.play(FadeIn(recs1), rate_func=linear)
        self.play(FadeOut(eq1[2][4:19], eq1[2][22:25], eq1[2][28:43], eq1[2][46:49], rate_func=linear),
                  ReplacementTransform(eq1[0][0], eq4[0][0]),
                  FadeIn(eq4[0][1], shift=eq4[0][0].get_center() - eq1[0][0].get_center(), rate_func=linear),
                  run_time=1.5
                  )
        self.wait(0.1)
        self.play(ReplacementTransform(VGroup(eq1[1], *[eq1[2][i:i+3] for i in (19, 25, 43, 49)]),
                                       VGroup(eq4[1], *[eq4[2][i:i+3] for i in (1, 4, 7, 10)])),
                  mh.stretch_replace(eq1[2][:4], eq4[2][0]),
                  mh.stretch_replace(eq1[2][-4:], eq4[2][-1]),
                  ReplacementTransform(recs1, recs2),
                  run_time=2.5)

        self.wait()

class ZGZ(Scene):
    def construct(self):
        eq1 = MathTex(r'Z_i\ge0', font_size=80)
        self.add(eq1)


class AvgB(Scene):
    def construct(self):
        eq = MathTex(r'\int_0^1\lvert B_t\rvert\,dt')
        self.add(eq)

class AvgBAbs(Scene):
    def construct(self):
        eq = MathTex(r'\Big\lvert\int_0^1 B_t\,dt\Big\rvert')
        self.add(eq)


class AvgRMS(Scene):
    def construct(self):
        eq = MathTex(r'\sqrt{\int_0^1 B^2_t\,dt}')
        self.add(eq)


class Measure(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            config.background_color = WHITE
        Scene.__init__(self, *args, **kwargs)

    def construct(self):
        fs = 50
        MathTex.set_default(font_size=fs)
        eq1 = MathTex(r'{\rm Heights:\ }', r'X_1, X_2, X_3,\ldots,X_n', font_size=fs)
        eq4 = MathTex(r'{\rm Weights:\ }', r'Y_1, Y_2, Y_3,\ldots,Y_n', font_size=fs)

        eq2 = MathTex(r'\hat\mu_X = (X_1+X_2+\cdots+X_n)/n', font_size=fs)
        eq3 = MathTex(r'I_X=[\hat\mu_X-2.58\sigma_X, \hat\mu_X+2.58\sigma_X]', font_size=fs)
        eq5 = MathTex(r'\mathbb P(\mu_X\in I_X)=0.99')
        eq6 = MathTex(r'I_Y=[\hat\mu_Y-2.58\sigma_Y, \hat\mu_Y+2.58\sigma_Y]', font_size=fs)

        eq2.next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3.next_to(eq2, DOWN).align_to(eq2, LEFT)
        VGroup(eq1, eq2, eq3, eq4).to_edge(DL, buff=0.6).next_to(mh.pos((-0.83, -0.2)), DR, buff=0)
        eq5.next_to(eq3, DOWN).align_to(eq3, LEFT)
        mh.align_sub(eq4, eq4[0][-1], eq1[0][-1])
        eq4.move_to(eq2, coor_mask=UP)
        eq6.next_to(eq3, DOWN).align_to(eq3, LEFT)

        eq1_1 = eq1[1][:2].copy().to_edge(DR, buff=0.8).move_to(mh.pos((0.82, -0.2)))
        eq1_2 = eq1[1][3:5].copy().to_edge(DR, buff=0.8).move_to(mh.pos((0.82, -0.2)))
        eq1_3 = eq1[1][6:8].copy().to_edge(DR, buff=0.8).move_to(mh.pos((0.82, -0.2)))
        eq1_1_1 = eq1_1.copy()
        eq1_2_1 = eq1_2.copy()
        eq1_3_1 = eq1_3.copy()

        self.add(eq1[0])
        self.wait(0.1)
        self.play(FadeIn(eq1_1), run_time=0.7)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1_1, eq1[1][:2]),
                  FadeIn(eq1[1][2], rate_func=rush_into), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq1_2), run_time=0.7)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1_2, eq1[1][3:5]),
                  FadeIn(eq1[1][5], rate_func=rush_into), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq1_3), run_time=0.7)
        self.wait(0.1)
        self.play(ReplacementTransform(eq1_3, eq1[1][6:8]),
                  FadeIn(eq1[1][8], rate_func=rush_into), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq1[1][9:]))
        self.wait(0.1)
        self.play(FadeIn(eq2))
        self.wait(0.1)
        self.play(FadeIn(eq3))
        self.wait(0.1)
        self.play(FadeIn(eq5))


        eq4_1 = eq4[1][:2].copy().to_edge(DR, buff=0.8).move_to(mh.pos((0.80, -0.9)))
        eq4_2 = eq4[1][3:5].copy().to_edge(DR, buff=0.8).move_to(mh.pos((0.80, -0.9)))
        eq4_3 = eq4[1][6:8].copy().to_edge(DR, buff=0.8).move_to(mh.pos((0.80, -0.9)))
        self.wait(0.1)
        self.play(FadeIn(eq4[0]), FadeOut(eq2, eq1[1], eq3, eq5))
        self.wait(0.1)
        self.play(FadeIn(eq1_1_1, eq4_1), run_time=0.7)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4_1, eq4[1][:2]),
                  ReplacementTransform(eq1_1_1, eq1[1][:2]),
                  FadeIn(eq1[1][2], eq4[1][2], rate_func=rush_into), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq1_2_1, eq4_2), run_time=0.7)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4_2, eq4[1][3:5]),
                  ReplacementTransform(eq1_2_1, eq1[1][3:5]),
                  FadeIn(eq1[1][5], eq4[1][5], rate_func=rush_into), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq1_3_1, eq4_3), run_time=0.7)
        self.wait(0.1)
        self.play(ReplacementTransform(eq4_3, eq4[1][6:8]),
                  ReplacementTransform(eq1_3_1, eq1[1][6:8]),
                  FadeIn(eq1[1][8], eq4[1][8], rate_func=rush_into), run_time=1.5)
        self.wait(0.1)
        self.play(FadeIn(eq4[1][9:], eq1[1][9:]))
        self.play(FadeIn(eq6, eq3))
        self.wait(0.1)
        MathTex.set_default(font_size=DEFAULT_FONT_SIZE*1.2)
        eq7 = MathTex(r'\mathbb P(\mu_X\in I_X, \mu_Y\in Y)', r'\ge',
                      r'\mathbb P(\mu_X\in I_X)\mathbb P(\mu_Y\in Y)')
        eq7.move_to(VGroup(eq6, eq3)).align_to(eq1, LEFT)
        eq8 = MathTex(r'\ge', r'0.9801')
        mh.align_sub(eq8, eq8[0], eq7[1])
        self.play(FadeOut(eq3, eq6), FadeIn(eq7[0]))
        self.wait(0.1)
        self.play(FadeIn(eq7[1:]))
        self.wait(0.1)
        self.play(FadeOut(eq7[2]), FadeIn(eq8[1]))

        self.wait()

class XNorm(Measure):
    def construct(self):
        eq = MathTex(r'X_i\sim N(\mu_X, \sigma^2_X)')
        self.add(eq)

class XX2(Scene):
    def construct(self):
        eq=MathTex(r'X\to X^2', font_size=100, stroke_width=5)
        self.add(eq)


if __name__ == "__main__":
    with tempconfig({"quality": "high_quality", "preview": True, 'fps': 15}):
        DensityZ().render()