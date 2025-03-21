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


def create_filter(width=1.3, ngaps=10):
    fcol = BLACK
    fcoledge = WHITE
    buff = 0.1
    gap = 0.7
    p1 = RoundedRectangle(width=width, height=width, corner_radius=0.05, stroke_color=fcoledge, stroke_width=2)
    polys = [p1]
    pts = list(p1.points)
    dx = (width - 2 * buff) / (ngaps * gap + (ngaps - 1) * (1 - gap))
    dl, ul = DL * (width / 2 - buff), UL * (width / 2 - buff)
    p2 = Polygram(*[np.array([dl, ul, ul + RIGHT * dx * gap, dl + RIGHT * dx * gap])], fill_opacity=0.5, fill_color=WHITE,
                  stroke_opacity=0)
    for _ in range(ngaps):
        pts.extend(list(p2.points))
        polys.append(p2.copy())
        p2.shift(RIGHT * dx)
    polys.append(Polygram(fill_color=fcol, fill_opacity=1, stroke_opacity=0).set_points(pts))
    return VGroup(*polys)

def arrows():
    arrows = VGroup(Line(start=ORIGIN, end=RIGHT, buff=0, color=RED).add_tip(),
                    Line(start=ORIGIN, end=UP, buff=0, color=GREEN).add_tip(),
                    Line(start=ORIGIN, end=OUT, buff=0, color=BLUE).add_tip())
    return arrows


class RelFreq(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = WHITE
        MathTex.set_default(color=BLACK, stroke_width=1.5, font_size=DEFAULT_FONT_SIZE * 1.08)
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        eq1 = MathTex(r'{\rm Number\ of\ trials} = N')[0]
        eq2 = MathTex(r'{\rm Number\ of\ successes} = M')[0].next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'{\rm Relative\ frequency} = M/N\ge0')[0].next_to(eq2, DOWN).align_to(eq1, LEFT)
        VGroup(eq1, eq2, eq3).to_corner(DR)

        self.wait(0.5)
        self.play(FadeIn(eq1), run_time=1)
        self.play(FadeIn(eq2), run_time=1)
        self.play(FadeIn(eq3[:-2]), run_time=1)
        self.play(FadeIn(eq3[-2:]), run_time=1)
        self.wait(0.5)


class ParticlePaths(Scene):
    bgcolor = GREY

    def __init__(self, *args, **kwargs):
        config.background_color = self.bgcolor
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        scale = 6
        end = ORIGIN + RIGHT * 5
        start = end + LEFT * scale
        radius = 0.5
        dot_rad = DEFAULT_DOT_RADIUS
        end_dot = Dot(color=BLACK, radius=radius, z_index=4).move_to(end)

        np.random.seed(1)

        nsteps = 100
        vol = 2 / math.sqrt(nsteps)
        xvals = np.zeros(nsteps + 1)
        yvals = np.zeros(nsteps + 1)
        times = np.linspace(0, 1, nsteps + 1)

        dot = Dot(color=PURE_BLUE, z_index=3, radius=dot_rad).move_to(start)
        start_dot = dot.copy().set_color(ManimColor(WHITE.to_rgb() * 0.3)).set_z_index(2)
        path_col = BLUE

        def update_dot(dot):
            dot.move_to(crv.get_end())

        dot.add_updater(update_dot)
        self.add(dot, end_dot, start_dot)

        for _ in range(20):
            rands = np.random.normal(0, 1, nsteps*2)
            for i in range(nsteps):
                xvals[i+1] = xvals[i] + rands[i*2] * vol
                yvals[i+1] = yvals[i] + rands[i*2+1] * vol
            xvals -= times * (xvals[-1] - scale)
            yvals -= times * yvals[-1]
            points = [start + RIGHT * xvals[i] + UP * yvals[i] for i in range(nsteps+1)]
            for i in range(1, nsteps+1):
                if np.linalg.norm(points[i] - end) < radius - dot_rad:
                    break
            crv = VMobject(color=path_col, z_index=1).set_points_as_corners(points[:i+1])

            self.play(Create(crv, rate_func=linear), run_time=3)
            crv.set_z_index(1)
            self.play(crv.animate.set_color(ManimColor(path_col.to_rgb() * 0.5 + self.bgcolor.to_rgb()*0.5)),
                      run_time=0.5)

        self.wait(0.5)


class EMField(ThreeDScene):
    def __init__(self, *args, **kwargs):
        config.background_color = BLUE
        ThreeDScene.__init__(self, *args, *kwargs)

    def construct(self):

        dy = 1

        n = 120
        x_vals = np.linspace(-13*PI, 3*PI, n)
        dx = (x_vals[-1] - x_vals[0]) / (n - 1)
        rdir = RIGHT /(x_vals[-1]+dx/2) * 9
        x_axis = Line(rdir * (x_vals[0]-dx/2), rdir * (x_vals[-1] + dx/2))
        Ecol = BLUE
        Bcol = RED

        rectE = Rectangle(width=dx * 0.8 * rdir[0], height=1, fill_color=Ecol, fill_opacity=1, stroke_opacity=0).shift(UP/2).rotate(PI/2,RIGHT, ORIGIN)
        rectB = Rectangle(width=dx * 0.8 * rdir[0], height=1, fill_color=Bcol, fill_opacity=1, stroke_opacity=0).shift(UP/2)
        txtE = MathTex(r'\bf E', color=Ecol, stroke_color=WHITE, stroke_width=1).rotate(PI/2, RIGHT).next_to(OUT * 1, OUT).set_z_index(300)
        txtB = MathTex(r'\bf B', color=Bcol, stroke_color=WHITE, stroke_width=1).next_to(DOWN * 1, DOWN).set_z_index(300)

        for i in range(n):
            if x_vals[i] > 0:
                break
        ilabel = i
        ipolar = ilabel - 5
        p = RIGHT * x_vals[ipolar]

        field = VGroup(VGroup(*[rectE.copy().shift(RIGHT*x_vals[i] + UP/2).set_z_index(i+2) for i in range(n)]),
                       VGroup(*[rectB.copy().shift(RIGHT*x_vals[i] + UP/2).set_z_index(i+2) for i in range(n)]), txtE, txtB,
                       VGroup(Arrow(p, p + OUT * 2, color=BLUE, buff=0, z_index=ipolar+2), Arrow(p, p + IN * 2, color=BLUE, buff=0)).set_opacity(0))
        angles = np.zeros(n)

        self.set_camera_orientation(phi=80*DEGREES, theta=-20*DEGREES)
        self.add(x_axis)

        c = 4
        starttime = 0.0
        endtime = 20 * PI / c
        starttime = 13 * PI / c
        endtime = 32 * PI / c

        starttime = 0.0
        endtime = 33.0
        tpolar = [14.9]
        rottime = 23
        fieldtime = 12


        time = ValueTracker(starttime)

        def wavefun(x):
            if x + fieldtime*c > 0:
                return 0.0, 0.0
            return math.sin(x) * (1.0 - math.exp(-((x+fieldtime*c)/PI)**2)), -max(min(0.0, ((x+rottime*c)/PI) * 15), -90) * DEGREES

        def f():
            t = time.get_value()
            for i in range(n):
                x = x_vals[i]
                y, angle = dy * wavefun(x - c * t)
                if abs(y) < 0.001:
                    y = 0.001
                p = rdir * x
                field[0][i].rotate(-angles[i], RIGHT, p)
                field[1][i].rotate(-angles[i], RIGHT, p)
                field[0][i].stretch_to_fit_depth(y).move_to(p).shift(OUT*y/2)
                field[1][i].stretch_to_fit_height(y).move_to(p).shift(DOWN*y/2)
                field[0][i].rotate(angle, RIGHT, p)
                field[1][i].rotate(angle, RIGHT, p)
                if t > tpolar[0]:
                    op = min((t - tpolar[0]) * 1, 1)
                    if op == 1:
                        tpolar[0] = 1e10
                    field[4].set_opacity(op)
                if i == ilabel:
                    field[2].rotate(angle - angles[i], RIGHT, p)
                    field[3].rotate(angle - angles[i], RIGHT, p)
                if i == ipolar:
                    field[4].rotate(angle - angles[i], RIGHT, p)
                angles[i] = angle
            return field

        field = always_redraw(f)
        self.add(field)
        self.wait(0.5)
        self.play(time.animate(rate_func=linear).set_value(endtime), run_time=endtime - starttime)


class PhotonMeasure(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        photon = Dot(radius=0.2, z_index=3)
        pcol = BLUE
        pcol2 = ManimColor(GREY.to_rgb())
        len = 1.5
        ver = DoubleArrow(DOWN*len, UP*len, color=BLUE, z_index=2, buff=0)
        hor = DoubleArrow(LEFT*len, RIGHT*len, color=BLUE, z_index=2, buff=0)

        theta = 35 * DEGREES
        tdir = (UP*math.cos(theta) + LEFT*math.sin(theta)) * len
        pthet = DoubleArrow(-tdir, tdir, color=BLUE, z_index=2, buff=0).set_z_index(2)
        pthet2 = pthet.copy().rotate(90 * DEGREES)
        lthet = Line(-tdir, tdir, color=WHITE, z_index=1)
        arc = Arc(start_angle=90 * DEGREES, angle=theta, radius=len * 0.7, z_index=1)
        eq_thet = MathTex(r'\theta', z_index=1)[0].move_to((UP*math.cos(theta/2) + LEFT*math.sin(theta/2)) * len * 0.5)
        top = lthet.get_end()
        dotted1 = DashedLine(top, top * RIGHT, color=GREY, z_index=1)
        dotted2 = DashedLine(top, top * UP, color=GREY, z_index=1)
        eq_cos = MathTex(r'\cos\theta', font_size=30, z_index=1).rotate(PI/2).next_to(top*UP/2, RIGHT, buff=0.1)
        eq_sin = MathTex(r'\sin\theta', font_size=30, z_index=1).next_to(top*RIGHT/2+LEFT*0.1, DOWN, buff=0.1)

        eq_ver = MathTex(r'\Psi_V', font_size=30, z_index=1).next_to(ver.get_end(), UR, buff=0)
        eq_hor = MathTex(r'\Psi_H', font_size=30, z_index=1).next_to(hor, LEFT, buff=0.1)
        eq_pthet = MathTex(r'\Psi_\theta=\cos\theta\Psi_V', font_size=30, z_index=1).next_to(top, UP, buff=0.1).align_to(eq_hor, LEFT).shift(LEFT*0.3)
        eq_pthet1 = MathTex(r'+\sin\theta\Psi_H', font_size=30, z_index=1).next_to(eq_pthet, DOWN, buff=0.1).align_to(eq_pthet, LEFT).shift(RIGHT*0.1)
        eqs = VGroup(eq_ver, eq_hor, eq_pthet, eq_pthet1)

        mob = VGroup(ver, hor, eqs, eq_ver)
        width = 2 * (photon.get_center() - mob.get_left())[0]
        height = 2 * (mob.get_top() - photon.get_center())[1]
        rect = RoundedRectangle(width=width + 0.2, height=height + 0.2, corner_radius=0.3, stroke_color=WHITE,
                                stroke_opacity=0, fill_opacity=0.8, fill_color=BLACK, z_index=0)
        VGroup(rect, photon, ver, hor, lthet, arc, eq_thet, dotted1, dotted2, eq_cos, eq_sin, eqs, pthet, pthet2).to_corner(DL)

        eq1 = MathTex(r'\mathbb P({\rm polarization }=\theta)=\cos^2\theta', stroke_width=1.5)
        eq2 = MathTex(r'\mathbb P({\rm polarization }=\theta+90^\circ)=\sin^2\theta', stroke_width=1.5).next_to(eq1, DOWN).align_to(eq1, LEFT)
        VGroup(eq1, eq2).next_to(rect, RIGHT).to_edge(DOWN)

        self.add(rect, photon)
        self.wait(0.5)
        self.play(FadeIn(ver), run_time=1)
        self.wait(0.5)
        self.play(ver.animate.set_color(pcol2), FadeIn(hor), run_time=1)
        self.wait(0.5)
        self.play(ver.animate.set_color(pcol), hor.animate.set_color(pcol2), run_time=0.5)
        self.play(FadeIn(lthet, arc, eq_thet), run_time=0.5)
        self.play(FadeIn(dotted1, dotted2, eq_cos, eq_sin), run_time=1)
        self.play(FadeIn(eqs), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(pthet, eq1), FadeOut(lthet), ver.animate.set_color(pcol2), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(eq2, pthet2), pthet.animate.set_color(pcol2), run_time=1)

        self.wait(0.5)


class Experiment(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = GREY
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        eqAB = MathTex(r'\mathbb P(A=B)=\frac14', stroke_width=1.5)
        eqAC = MathTex(r'\mathbb P(A=C)=\frac14', stroke_width=1.5).next_to(eqAB, DOWN).align_to(eqAB, LEFT)
        eqBC = MathTex(r'\mathbb P(B=C)=\frac14', stroke_width=1.5).next_to(eqAC, DOWN).align_to(eqAC, LEFT)
        VGroup(eqAB, eqAC, eqBC).to_edge(UR)

        len=0.8
        left_buff = DEFAULT_MOBJECT_TO_EDGE_BUFFER * 0.5

        eqA = MathTex(r'A', stroke_width=1.5, z_index=1)
        dot = Dot(radius=0.15, z_index=3).next_to(eqA, RIGHT)
        arr = DoubleArrow(dot.get_center()+DOWN * len, dot.get_center()+UP * len, color=BLUE, z_index=2, buff=0).set_z_index(2)
        photon = VGroup(arr, dot)
        filt = create_filter().next_to(photon, RIGHT)

        expA = VGroup(*[eqA, photon, filt]).to_edge(UP).to_edge(LEFT, buff=left_buff)

        pB = photon.copy().rotate(60 * DEGREES)
        p = pB[1].get_center()
        arc = Arc(arc_center=p, start_angle=90 * DEGREES, angle=60 * DEGREES, radius=len, z_index=1)
        l1 = DashedLine(p, p + UP * len, z_index=1)
        q = p + (UP * math.sqrt(3) + LEFT * 0.95) * len/2 * 0.75
        eq = MathTex(r'60^\circ', font_size=30, stroke_width=1, z_index=1).move_to(q)
        pB.add(arc, l1, eq)

        pC = photon.copy().rotate(-60 * DEGREES)
        p = pC[1].get_center()
        arc = Arc(arc_center=p, start_angle=90 * DEGREES, angle=-60 * DEGREES, radius=len, z_index=1)
        l1 = DashedLine(p, p + UP * len, z_index=1)
        q = p + (UP * math.sqrt(3) + RIGHT) * len/2 * 0.75
        eq = MathTex(r'60^\circ', font_size=30, stroke_width=1, z_index=1).move_to(q)
        pC.add(arc, l1, eq)

        expB = VGroup(MathTex(r'B', stroke_width=1.5, z_index=1),
                     pB,
                     filt.copy().rotate(60 * DEGREES)).arrange(RIGHT).next_to(expA, DOWN).to_edge(LEFT, buff=left_buff)

        expC = VGroup(MathTex(r'C', stroke_width=1.5, z_index=1),
                     pC,
                     filt.copy().rotate(-60 * DEGREES)).arrange(RIGHT).next_to(expB, DOWN).to_edge(LEFT, buff=left_buff)

        expA[1].move_to(expB[1], coor_mask=RIGHT)
        expA[2].move_to(expB[2], coor_mask=RIGHT)

        self.wait(0.5)
        self.play(FadeIn(expA[2]), run_time=0.5)
        self.play(FadeIn(expA[0]), run_time=0.5)
        self.play(FadeIn(expA[1]), run_time=0.5)
        self.wait(0.5)

        p = expB[1][:2].rotate(-60 * DEGREES)
        q = expB[2].rotate(-60 * DEGREES)

        self.play(ReplacementTransform((expA[1][:2] + expA[2]).copy(), p + q), run_time=2)
        self.add(expB[1][3])

        r = VGroup(p,q)
        c = p[1].get_center()
        angle = [0]
        exp = expB

        def f(r):
            end = exp[1][2].get_end() - c
            theta = math.atan(-end[0]/end[1])
            r[0].rotate(theta - angle[0])
            r[1].rotate(theta - angle[0])
            angle[0] = theta

        r.add_updater(f)
        self.add(r)
        self.play(Create(expB[1][2]), FadeIn(expB[1][4], rate_func=rate_functions.ease_in_cubic), run_time=1)
        r.remove_updater(f)

        self.wait(0.5)
        self.play(FadeIn(expB[0], run_time=0.5))
        self.wait(0.5)

        self.play(FadeIn(eqAB), run_time=1)
        self.wait(0.5)


        p = expC[1][:2].rotate(60 * DEGREES)
        q = expC[2].rotate(60 * DEGREES)

        t1 = expB[1][:2].copy()
        t2 = expB[2].copy()
        t = ValueTracker(0.0)
        t0 = [0.0]
        mob = VGroup(t1, t2)
        shift1 = p.get_center() - t1.get_center()
        shift2 = q.get_center() - t2.get_center()

        def g(mob):
            t1 = t.get_value()
            dt = t1 - t0[0]
            t0[0] = t1
            mob[1].shift(shift2 * dt).rotate(-60 * DEGREES * dt)
            mob[0].shift(shift1 * dt).rotate(-60 * DEGREES * dt)

        mob = mob.add_updater(g)
        self.add(mob)
        self.play(t.animate.set_value(1), run_time=2)
        self.remove(mob)
        self.add(expC[1][3])

        r = VGroup(p,q)
        c = p[1].get_center()
        angle = [0]
        exp = expC

        r.add_updater(f)
        self.add(r)
        self.play(Create(expC[1][2]), FadeIn(expC[1][4], rate_func=rate_functions.ease_in_cubic), run_time=1)
        r.remove_updater(f)

        self.wait(0.5)
        self.play(FadeIn(expC[0], run_time=0.5))
        self.wait(0.5)

        self.play(FadeIn(eqAC), run_time=1)
        self.wait(0.5)

        pos = expC[1][1].get_center() * 2 - expB[1][1].get_center()
        p1 = expB[1].copy()
        p2 = expC[1].copy()
        self.play(p1.animate.next_to(pos, ORIGIN, submobject_to_align=p1[1]),
                  p2.animate.next_to(pos, ORIGIN, submobject_to_align=p2[1]),
                  run_time=2)
        self.wait(0.5)
        eq120 = MathTex(r'120^\circ', font_size=30, stroke_width=1, z_index=1).move_to(p1[1].get_center() + UP * len * 0.7)

        self.play(FadeOut(p1[3], p2[3]),
                  FadeOut(p1[4], target_position=eq120),
                  FadeOut(p2[4], target_position=eq120),
                  FadeIn(eq120),
                  run_time=1)

        self.wait(0.5)
        arc = Arc(arc_center=p1[1].get_center(), radius=len, start_angle=150 * DEGREES, angle=60 * DEGREES)
        eq60 = MathTex(r'60^\circ', font_size=30, stroke_width=1, z_index=1).next_to(p1[1].get_center() + LEFT * len * 0.9, buff=0)
        self.play(Create(arc), FadeIn(eq60, rate_func=rate_functions.ease_in_cubic), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(eqBC), run_time=1)
        self.wait(0.5)

        MathTex.set_default(z_index=1, stroke_width=1.5)
        ineq1 = MathTex(r'{{\mathbb P(A=B{\rm\ or\ }A=C{\rm\ or\ }B=C)}}', stroke_width=1.5)
        ineq2 = MathTex(r'\le{{\mathbb P(A=B)}}+{{\mathbb P(A=C)}}+{{\mathbb P(B=C)}}', stroke_width=1.5).next_to(ineq1, DOWN)
        ineq2.set_z_index(1)
        gp = VGroup(ineq1, ineq2).to_edge(DR)
        rect1 = SurroundingRectangle(gp, fill_opacity=0.5, fill_color=BLACK, stroke_opacity=0, corner_radius=0.3)
        self.add(rect1)
        self.play(FadeIn(ineq1, ineq2), run_time=1)
        self.wait(0.5)
        eq1 = MathTex(r'\le{{\frac14}}{{\frac14}}{{\frac14}}', stroke_width=1.5)
        eq1.next_to(ineq2[0], ORIGIN, submobject_to_align=eq1[0])
        eq1[1].move_to(ineq2[1], coor_mask=RIGHT)
        eq1[2].move_to(ineq2[3], coor_mask=RIGHT)
        eq1[3].move_to(ineq2[5], coor_mask=RIGHT)
        rect1_1 = SurroundingRectangle(VGroup(ineq1, eq1), fill_opacity=0.5, fill_color=BLACK, stroke_opacity=0, corner_radius=0.3)
        self.play(FadeIn(eq1[1:]), FadeOut(ineq2[1], ineq2[3], ineq2[5]), ReplacementTransform(rect1, rect1_1), run_time=1)
        self.wait(0.5)
        eq2 = MathTex(r'\le\frac34', stroke_width=1.5)[0].set_z_index(1)
        eq2.next_to(ineq2[0][0], ORIGIN, submobject_to_align=eq2[0])
        eq2[1:].move_to(eq1[2][:], coor_mask=1)
        self.play(ReplacementTransform(eq1[2][1:], eq2[2:]),
                  ReplacementTransform(eq1[1][1:], eq2[2:]),
                  ReplacementTransform(eq1[3][1:], eq2[2:]),
                  FadeOut(eq1[2][0], target_position=eq2[1]),
                  FadeOut(eq1[1][0], target_position=eq2[1]),
                  FadeOut(eq1[3][0], target_position=eq2[1]),
                  FadeOut(ineq2[2][0], target_position=eq2[2]),
                  FadeOut(ineq2[4][0], target_position=eq2[2]),
                  FadeIn(eq2[1]),
                  ineq2[0].animate.next_to(eq2[1:], LEFT, coor_mask=RIGHT),
                  run_time=2
                  )
        self.wait(0.5)
        self.play(FadeOut(ineq1, ineq2[0], eq2[1:]), run_time=1)
        self.remove(rect1_1)
        self.wait(0.5)
        eq3_1 = MathTex(r'\mathbb P(A=B=C)=')[0].set_z_index(1)
        eq3_2 = MathTex(r'\frac12\left(\mathbb P(A=B)+\mathbb P(B=C)+\mathbb P(C=A)-1\right)')[0]\
            .set_z_index(1).next_to(eq3_1, DOWN)
        gp = VGroup(eq3_1, eq3_2).to_edge(DR)
        rect2 = SurroundingRectangle(gp, fill_opacity=0.5, fill_color=BLACK, stroke_opacity=0, corner_radius=0.3)
        self.add(rect2)
        self.play(FadeIn(eq3_1, eq3_2), run_time=1)
        self.wait(0.5)
        eq4 = MathTex(r'\left(\frac14\frac14\frac14\right)', stroke_width=1.5)[0]
        eq4.next_to(eq3_2[1], ORIGIN, submobject_to_align=eq4[2])
        eq4[0].move_to(eq3_2[3], coor_mask=RIGHT)
        eq4[1:4].move_to(eq3_2[4:10], coor_mask=RIGHT)
        eq4[4:7].move_to(eq3_2[11:17], coor_mask=RIGHT)
        eq4[7:10].move_to(eq3_2[18:24], coor_mask=RIGHT)
        eq4[10].move_to(eq3_2[-1], coor_mask=RIGHT)
        self.play(FadeOut(eq3_2[3:10], eq3_2[11:17], eq3_2[18:24], eq3_2[-1]), FadeIn(eq4), run_time=1)
        self.wait(0.5)
        eq5 = MathTex(r'=-\frac18', stroke_width=1.5)[0]
        eq5.next_to(eq3_1[-1], ORIGIN, submobject_to_align=eq5[0])
        eq6 = eq5.copy()
        eq6.next_to(eq4[5], ORIGIN, submobject_to_align=eq6[3])
        self.play(FadeOut(eq4[1:4], target_position=eq6[2:]),
                  FadeOut(eq4[4:7], target_position=eq6[2:]),
                  FadeOut(eq4[7:10], target_position=eq6[2:]),
                  FadeOut(eq4[0], target_position=eq6[2:]),
                  FadeOut(eq4[10], target_position=eq6[2:]),
                  FadeOut(eq3_2[:3], target_position=eq6[2:]),
                  FadeOut(eq3_2[-2], target_position=eq6[2:]),
                  FadeOut(eq3_2[10], target_position=eq6[3]),
                  FadeOut(eq3_2[17], target_position=eq6[3]),
                  ReplacementTransform(eq3_2[-3], eq6[1]),
                  FadeIn(eq6[2:]),
                  run_time=2)
        self.wait(0.5)
        rect3 = SurroundingRectangle(eq5[1:] + eq3_1, fill_opacity=0.5, fill_color=BLACK, stroke_opacity=0)
        self.play(ReplacementTransform(eq6[1:], eq5[1:]),
                  ReplacementTransform(rect2, rect3), run_time=1)
        self.wait(0.5)


class AliceBob(ThreeDScene):
    cube_rad = 0.8
    phot_h = cube_rad * 0.8  # starting photon distance
    center = IN * 2
    filt_h = 4  # filter distance
    photon_dist = 8  # distance beyond filters
    filt_time = 0.8  # time for photon to reach filter
    phi_photon = 15 * DEGREES
    phi_filter = 5 * DEGREES
    photon_speed = 5.

    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE

        # photon emission params
        fps = config.frame_rate
        nframes1 = int((self.filt_h - self.phot_h) * fps / self.photon_speed)
        self.speed = (self.filt_h - self.phot_h)/(nframes1 + 0.5)
        self.photon_time1 = nframes1 / fps + 0.001
        self.photon_dist1 = self.filt_h - self.phot_h - self.speed * 0.5
        photon_nframes2 = int((self.photon_dist - self.filt_h) / self.speed + 0.5)
        self.photon_dist2 = photon_nframes2 * self.speed
        self.photon_time2 = photon_nframes2 / fps + 0.001
        self.axes_photon = [DOWN * math.cos(self.phi_photon) + LEFT * math.sin(self.phi_photon),
                            DOWN * math.cos(self.phi_photon) + RIGHT * math.sin(self.phi_photon)]

        rad = 0.06
        p = []
        max_r = 7.
        f = lambda r: 1/r**2
        for r in np.linspace(1.0, max_r, 15)[::-1]:
            u = f(r)
            if u > 0.02:
                p.append(Dot3D(radius=rad*r, fill_opacity=u, stroke_opacity=0, fill_color=WHITE, z_index=1))
        p = VGroup(*p)
        arr = VGroup(Arrow3D(ORIGIN, OUT*0.7, color=BLUE, z_index=1), Arrow3D(ORIGIN, IN*0.7, color=BLUE, z_index=2))
        pA = VGroup(arr.set_z_index(1), p.set_z_index(2))
        self.photons = VGroup(pA, pA.copy())

        # filter params
        self.axes_filter = [DOWN * math.cos(self.phi_filter) + LEFT * math.sin(self.phi_filter),
                            DOWN * math.cos(self.phi_filter) + RIGHT * math.sin(self.phi_filter)]

        filt = create_filter(width=1.8).set_z_index(10).shift(self.center).rotate(90 * DEGREES, axis=RIGHT)
        filtA = filt.copy().shift(DOWN*self.filt_h).rotate(self.phi_filter, IN)
        filtB = filt.shift(UP*self.filt_h).rotate(self.phi_filter, OUT)
        self.filters = VGroup(filtA, filtB)
        self.filter_angle = (0., 0.)


        ThreeDScene.__init__(self, *args, *kwargs)

    def emit_photons(self, passthru=(True, True), angle=0., filter=True):
        pA, pB = self.photons.copy()
        pA.move_to(self.center + DOWN * self.phot_h)
        pB.move_to(self.center + UP * self.phot_h)
        if angle is None:
            pA[0].set_opacity(0)
            pB[0].set_opacity(0)
            angle = 0.
        else:
            if angle != 0.:
                pA.rotate(angle, self.axes_photon[0])
                pB.rotate(angle, self.axes_photon[1])

        self.filters.set_z_index(0)
        self.add(pA, pB)
        self.play(pA.animate(rate_func=linear).shift(DOWN * self.photon_dist1),
                  pB.animate(rate_func=linear).shift(UP * self.photon_dist1),
                  run_time=self.photon_time1)
        self.filters.set_z_index(50)
        pA.shift(DOWN * self.speed)
        pB.shift(UP * self.speed)
        pA[0].set_opacity(1)
        pB[0].set_opacity(1)
        if not passthru[0]:
            pA.set_opacity(0)
        if not passthru[1]:
            pB.set_opacity(0)
        if filter:
            angle2 = self.filter_angle
            if angle2[0] - angle != 0.:
                pA.rotate(angle2[0] - angle, axis=self.axes_photon[0])
            if angle2[1] - angle != 0.:
                pB.rotate(angle2[1] - angle, axis=self.axes_photon[1])
        else:
            angle2 = (angle, angle)

        self.play(pA.animate(rate_func=linear).shift(DOWN * self.photon_dist2),
                  pB.animate(rate_func=linear).shift(UP * self.photon_dist2),
                  run_time=self.photon_time2)
        if angle2[0] != 0.:
            pA.rotate(-angle2[0], self.axes_photon[0])
        if angle2[1] != 0.:
            pA.rotate(-angle2[1], self.axes_photon[1])
        self.remove(pA, pB)

    def set_filters(self, angle=(0., 0.), run_time=1.):
        t = ValueTracker(0.0)
        t0 = [0.0]
        thetaA = angle[0] - self.filter_angle[0]
        thetaB = angle[1] - self.filter_angle[1]

        def f(mob):
            t1 = t.get_value()
            dt = t1 - t0[0]
            if thetaA * dt != 0.:
                mob[0].rotate(thetaA * dt, axis=self.axes_filter[0])
            if thetaB * dt != 0.:
                mob[1].rotate(thetaB * dt, axis=self.axes_filter[1])
            t0[0] = t1
            return mob

        self.filters.add_updater(f)
        self.play(t.animate.set_value(1.), run_time=run_time)
        self.filters.remove_updater(f)
        self.filter_angle = angle

    def construct(self):
        skip = False
        self.camera.light_source_start_point = 4 * DOWN + 2 * LEFT - 10 * OUT
        self.camera.light_source = Point(self.camera.light_source_start_point)

        m1 = Cube(side_length=self.cube_rad * 2, fill_opacity=1, fill_color=GREY, stroke_opacity=1, stroke_color=WHITE,
                  stroke_width=1).set_z_index(103)
        m2 = Cylinder(radius=0.5, height=1.9, direction=UP, fill_opacity=1, fill_color=BLACK, stroke_opacity=0,
                      stroke_width=1, stroke_color=WHITE, checkerboard_colors=[BLACK],
                      resolution=(1, 32), show_ends=True).set_z_index(102)
        m3 = Cylinder(radius=0.49, height=2, direction=UP, fill_opacity=1, fill_color=BLACK,
                      stroke_opacity=0, checkerboard_colors=[GREY],
                      resolution=(1, 32), show_ends=True).set_z_index(101)
        Tex.set_default(color=DARK_BLUE, font_size=20, stroke_width=1.5)
        txt = VGroup(Tex(r'\b Entanglement'), Tex(r'\b Generator')).arrange(DOWN, buff=0.15)\
            .rotate(90*DEGREES, RIGHT).rotate(90*DEGREES, OUT).shift(RIGHT*self.cube_rad+OUT*self.cube_rad*0.05).set_z_index(105)

        machine = VGroup(m1, m2, m3, txt).move_to(self.center)

        self.set_camera_orientation(phi=80*DEGREES, theta=0*DEGREES)

        self.add(machine)

        self.wait(0.5)
        if not skip:
            self.emit_photons(filter=False)
            self.emit_photons(angle=90 * DEGREES, filter=False)

        self.play(FadeIn(self.filters), run_time=0.5)
        self.wait(0.1)

        if not skip:
            self.set_filters((60 * DEGREES, 60 * DEGREES))
            self.wait(0.1)
            self.set_filters((-60 * DEGREES, -60 * DEGREES))
            self.wait(0.1)
            self.set_filters()
            self.wait(0.1)

        if not skip:
            self.emit_photons((True, True))
            self.emit_photons((False, False), angle=90 * DEGREES)

        if not skip:
            self.set_filters((60 * DEGREES, 60 * DEGREES))
            self.emit_photons((True, True), angle=None)

        if not skip:
            self.set_filters((-60 * DEGREES, -60 * DEGREES))
            self.emit_photons((False, False), angle=None)

        if not skip or True:
            self.set_filters((0 * DEGREES, 60 * DEGREES))
            self.emit_photons((False, True), angle=None)

        if not skip:
            self.set_filters((60 * DEGREES, -60 * DEGREES))
            self.emit_photons((True, False), angle=None)

        if not skip:
            self.set_filters((-60 * DEGREES, 0 * DEGREES))
            self.emit_photons((True, True), angle=None)

        self.set_filters((-60 * DEGREES, 0 * DEGREES))
        self.wait(0.1)
        self.set_filters((0 * DEGREES, 60 * DEGREES))
        self.emit_photons((True, False), angle=None)

        print('done!')

        self.wait(0.1)


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "fps": 15, "preview": True}):
        AliceBob().render()