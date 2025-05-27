from manim import *
import numpy as np
import math
import sys
import scipy.interpolate

sys.path.append('../abracadabra/')
# noinspection PyUnresolvedReferences
import abracadabra as abra

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

    def shapes(self):
        res=[self.res, self.res]
        g = self.g
        convA = convexPolytope3D(self.vectors1, g=g[0], scale=self.scale[0], fill_opacity=0.7, stroke_opacity=0,
                                 resolution=res, fill_color=self.colors[0])
        convB = convexPolytope3D(self.vectors2, g=g[1], scale=self.scale[1], fill_opacity=0.7, stroke_opacity=0,
                                 resolution=res, fill_color=self.colors[1], max_radius=8)
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
                  abra.fade_replace(eq1[0].copy(), eq2[0]),
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
                      abra.fade_replace(eq1[0][4], eq3[0][4+i]),
                      FadeOut(eq1[0][15], target_position=eq3[0][4+i]),
                      FadeOut(eq1[0][8:13]),
                      FadeIn(eq3[0][2:2+i]),
                      ReplacementTransform(eq1[2][:2] + eq1[2][2:4] + eq1[2][5:8],
                                           eq3[2][:2] + eq3[2][2 + j:4 + j] + eq3[2][5 + j:8 + j]),
                      ReplacementTransform(eq1[2][13:15] + eq1[2][16:20],
                                           eq3[2][2 + j:4 + j] + eq3[2][5 + j:9 + j]),
                      abra.fade_replace(eq1[2][4], eq3[2][4 + j]),
                      FadeOut(eq1[2][15], target_position=eq3[2][4 + j]),
                      FadeOut(eq1[2][8:13]),
                      FadeIn(eq3[2][2:2 + j]),
                      ReplacementTransform(eq1[3][:2] + eq1[3][2:4] + eq1[3][7:10],
                                           eq3[3][:2] + eq3[3][2 + k:4 + k] + eq3[3][5 + k:8 + k]),
                      ReplacementTransform(eq1[3][15:17] + eq1[3][18:22],
                                           eq3[3][2 + k:4 + k] + eq3[3][5 + k:9 + k]),
                      abra.fade_replace(eq1[3][4:7], eq3[3][4 + k]),
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
                  abra.fade_replace(eq2[1][:7], eq4[1][0]),
                  abra.fade_replace(eq2[1][82:], eq4[1][8:]),
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
        eq9 = MathTex('\mathbb P(X^{(1)}\in A)\mathbb P(X^{(2)}\in B)', font_size=28).set_z_index(1)
        eq10 = MathTex('\mathbb P(X^{(1)}\in A,X^{(2)}\in B)', font_size=28).set_z_index(1)
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
        self.play(ReplacementTransform(eq8[2][:3] + eq8[2][4:11] + eq8[2][3],
                                       eq10[0][4:7] + eq10[1][4:11] + eq10[0][-1]),
                  FadeIn(eq10[0][:3], eq10[0][7:-1], eq10[1][:3], eq10[1][11:]),
                  FadeIn(eq10[0][3], target_position=eq8[2][0].get_left()),
                  FadeIn(eq10[1][3], target_position=eq8[2][5].get_left()),
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
        eq0 = MathTex(*self.eqstr, font_size=DEFAULT_FONT_SIZE*0.9).set_z_index(1)
        eq0.next_to(eq1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
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
        self.play(FadeIn(eq12))
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
                  FadeOut(eq10),
                  run_time=1.5)
        self.play(ReplacementTransform(box, box2),
                  ReplacementTransform(eq11, eq0),
                  FadeOut(eq12),
                  run_time=2)
        self.wait()


class MGFDiffZ(MGFDiff):
    eqstr1 = [r'\frac{d}{dt}\mathbb E[f(Z)]', r'=',
                      r'\sum_{S}c_S\,\mathbb E[(-\partial)^Sf(\tilde Z)]']
    eqstr2 = [r'where ', r'$c_S=-\frac12\frac{d}{dt}\lvert C_S\rvert$']

    def construct(self):
        eq1, eq2, eq3, _, box = self.get_eqs()
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
                  abra.fade_replace(eq4[2][11], eq5[2][11]),
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
                  abra.fade_replace(eq12[2][19], eq15[2][9]),
                  FadeIn(eq15[2][4:8], shift=shift2),
                  FadeIn(eq15[2][10], target_position=eq12[2][19].get_corner(DR)),
                  FadeIn(eq15[2][11], shift=shift2),
                  run_time=2)
        self.wait(0.1)
        self.play(LaggedStart(ReplacementTransform(eq15[0][:] + eq15[1] + eq15[2][1:-4] + eq15[2][-4:],
                                       eq16[0][4:] + eq16[1] + eq16[2][1:-8:] + eq16[2][-4:]),
                  AnimationGroup(FadeIn(eq16[0][:4] ,eq16[2][-8:-4]),
                                 abra.fade_replace(eq15[2][0], eq16[2][0])),
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
                  abra.fade_replace(eq18[2][21], eq19[2][23]),
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
        self.play(FadeIn(eq23), FadeOut(eq20, eq21))
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
                  run_time=2)
        self.wait()


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True, 'fps': 15}):
        JointNormal().render()