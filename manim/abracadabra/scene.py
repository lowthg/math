from manim import *
import cv2
import math
import abracadabra as abra


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation


class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        square.next_to(circle, DOWN, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen


class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        square = Square()  # create a square

        self.play(Create(square))  # show the square on screen
        self.play(square.animate.rotate(PI / 4))  # rotate the square
        self.play(Transform(square, circle))  # transform the square into a circle
        self.play(
            square.animate.set_fill(PINK, opacity=0.5)
        )  # color the circle on screen
        self.play(FadeOut(square))  # fade out animation


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI / 2), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()


class TwoTransforms(Scene):
    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(Transform(a, b))
        self.play(Transform(a, c))
        self.play(FadeOut(a))

    def replacement_transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(ReplacementTransform(a, b))
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(c))

    def construct(self):
        self.transform()
        self.wait(0.5)  # wait for 0.5 seconds
        self.replacement_transform()


class TransformCycle(Scene):
    def construct(self):
        a = Circle()
        t1 = Square()
        t2 = Triangle()
        self.add(a)
        self.wait()
        for t in [t1, t2]:
            self.play(Transform(a, t))


class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello world", font_size=144)
        self.add(text)


class SingleLineColor(Scene):
    def construct(self):
        text = MarkupText(
            f'all in red <span fgcolor="{YELLOW}">except this</span>', color=RED
        )
        self.add(text)


class DifferentWeight(Scene):
    def construct(self):
        import manimpango

        g = VGroup()
        weight_list = dict(
            sorted(
                {
                    weight: manimpango.Weight(weight).value
                    for weight in manimpango.Weight
                }.items(),
                key=lambda x: x[1],
            )
        )
        for weight in weight_list:
            g += Text(weight.name, weight=weight.name, font="Arial")
        self.add(g.arrange(DOWN).scale(0.5))


class MathTeXDemo(Scene):
    def construct(self):
        rtarrow0 = MathTex(r"\xrightarrow{x^6y^8}", font_size=96)
        rtarrow1 = Tex(r"$\xrightarrow{x^6y^8}$", font_size=96)

        self.play(VGroup(rtarrow0, rtarrow1).arrange(DOWN).animate)


class AddPackageLatex(Scene):
    def construct(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        tex = Tex(
            r"$\mathscr{H} \rightarrow \mathbb{H}$",
            tex_template=myTemplate,
            font_size=144,
        )
        self.add(tex)

class LaTeXAttributes(Scene):
    def construct(self):
        tex = Tex(r'Hello \LaTeX', color=BLUE, font_size=144)
        self.add(tex)


class LaTeXSubstrings(Scene):
    def construct(self):
        tex = Tex('Hello', r'$\bigstar$', r'\LaTeX', font_size=144).move_to(UP)
        tex2 = MathTex(r'\int_{-\infty}^\infty e^{-\frac12{{x^2}}}\,dx=\sqrt{2\pi}',
                   font_size=80).next_to(tex, DOWN)
        tex.set_color_by_tex('igsta', RED)
        tex2[1].set_color(RED)
        equation = MathTex(
            r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots",
            substrings_to_isolate="x"
        ).next_to(tex2, DOWN)
        equation.set_color_by_tex("x", YELLOW)
        self.add(tex)
        self.add(tex2, equation)
        self.play(tex2[0][2:4].animate.set_color(BLUE))
        self.wait(2)


class IndexLabelsMathTex(Scene):
    def construct(self):
        text = MathTex(r"\binom{2n}{n+2}", font_size=96)

        # index the first (and only) term of the MathTex mob
        self.add(index_labels(text[0]))

        text[0][1:3].set_color(YELLOW)
        text[0][3:6].set_color(RED)
        text[0][6].set_color(BLUE)
        self.add(text)


class Wife(Scene):
    def construct(self):
        wife0 = ImageMobject("wifejak.png")
        wife_happy0 = ImageMobject("wifejak_happy.png")
        wife = ImageMobject(wife0.pixel_array[:320,:,:]).to_edge(LEFT, buff=0.04)
        wife_happy = ImageMobject(wife_happy0.pixel_array[:320,:,:], z_index=2).to_edge(LEFT, buff=0.04)
        wojak0 = ImageMobject("wojak.png")
        wojak_happy0 = ImageMobject("wojak_happy.png")
        wojak = ImageMobject(np.flip(wojak0.pixel_array, 1))
        scale = wife.height/wojak.height*0.95
        wojak.scale(scale).next_to(wife, RIGHT)
        wojak_happy = ImageMobject(np.flip(wojak_happy0.pixel_array, 1)).scale(scale).move_to(wojak)
        self.add(wife, wojak)
        self.wait(2)
        wife.target = wife_happy
        wojak.target = wojak_happy
        self.play(MoveToTarget(wife), run_time=2)
        self.play(MoveToTarget(wojak), run_time=2)
        wojak.generate_target().set_opacity(0)
        wife.generate_target().set_opacity(0)
        self.play(MoveToTarget(wojak, rate_func=lambda t: t * 0.9), run_time=2)
        self.play(MoveToTarget(wife, rate_func=lambda t: t * 0.9), run_time=2)
        self.wait(2)


_dice_faces = None


def get_dice_faces():
    global _dice_faces
    if _dice_faces is None:
        blank = RoundedRectangle(width=2, height=2, fill_color=WHITE, fill_opacity=1, corner_radius=0.2, stroke_color=GREY)
        dot = Dot(radius=0.22, color=BLACK, z_index=1)
        x = RIGHT * 0.54
        y = UP * 0.54

        _dice_faces = []

        for dots in [
            [ORIGIN],
            [-x - y, x + y],
            [-x - y, ORIGIN, x + y],
            [-x - y, -x + y, x + y, x - y],
            [-x - y, -x + y, x + y, x - y, ORIGIN],
            [-x - y, -x, -x + y, x - y, x, x + y]
        ]:
            _dice_faces.append(VGroup(blank.copy(), *[dot.copy().move_to(s) for s in dots]))
    return _dice_faces


def animate_roll(scene, key, pos=ORIGIN, scale=0.3):
    key = int(key) - 1
    rows = [
        [1, 5, 6, 2],
        [2, 4, 5, 3], ##
        [3, 1, 4, 6],  ##
        [4, 2, 3, 5], #
        [5, 6, 2, 1], #
        [6, 5, 1, 2],  ##
    ]

    faces = get_dice_faces()
    f_row = [faces[i-1] for i in rows[key]]

    flag = False
    for i in range(10, -1, -1):
        t = -i * i * 0.045
        c = math.cos(t) * scale
        s = math.sin(t) * scale
#        arr = [f_row[i].copy().apply_matrix([[x, 0], [0, scale]]).move_to(pos + RIGHT * y) for i, x, y in [(0, c, s), (1, s, -c), (2, -c, -s), (3, -s, c)]]
        arr = [f_row[0].copy().apply_matrix([[c, 0], [0, scale]]).move_to(pos + RIGHT * s),
               f_row[1].copy().apply_matrix([[s, 0], [0, scale]]).move_to(pos + LEFT * c),
               f_row[2].copy().apply_matrix([[-c, 0], [0, scale]]).move_to(pos + LEFT * s),
               f_row[3].copy().apply_matrix([[-s, 0], [0, scale]]).move_to(pos + RIGHT * c)]
        if c < 0:
            arr[0].set_opacity(0)
        else:
            arr[2].set_opacity(0)
        if s < 0:
            arr[1].set_opacity(0)
        else:
            arr[3].set_opacity(0)
        if flag:
            for j in range(4):
                f[j].target = arr[j]
            scene.play(*[MoveToTarget(f[j]) for j in range(4)], rate_func=rate_functions.linear, run_time=0.05 * (1 + t / 10))
        else:
            f = arr
            flag = True

    scene.remove(*f[1:])
    return f_row[0]

class Dice(Scene):
    def construct(self):
        faces = VGroup(*get_dice_faces())
        faces.arrange(RIGHT).to_edge(UL)
        self.add(faces)
        """
        rotate angle t about x=z=0
        

        rotate angle t about x=-y, z=0
        (c+1)/2 (c-1)/2  rs
        (c-1)/2 (c+1)/2 rs
          -s     0      c
        
        """


        self.wait(0.1)

        for i in range(1, 7):
            animate_roll(self, i)
            self.wait(0.5)

class Test(Scene):
    def construct(self):
        txt = MathTex(r'\int_{-\infty}^\infty e^{-x^2}\,dx=\sqrt{\pi}')
        self.add(txt)
        self.play(txt.animate.to_edge(DOWN))
        self.play(txt.animate.to_edge(RIGHT).move_to(ORIGIN, coor_mask=UP))
        self.play(txt.animate.to_edge(UP).move_to(ORIGIN, coor_mask=RIGHT))
        self.play(txt.animate.to_edge(LEFT).move_to(ORIGIN, coor_mask=UP))
        self.play(txt.animate.move_to(ORIGIN))
        self.add(txt)


class OddSum(Scene):
    def construct(self):
        n = 10
        fill_color = ManimColor(BLUE.to_rgb() * 0.5)
        dx = 0.36
        rects = []
        for i in range(0, n):
            j = 2*i + 1
            rect = Rectangle(width=dx, height=dx * j, stroke_width=3, stroke_opacity=1, fill_opacity=1,
                             fill_color=fill_color, stroke_color=BLUE).set_z_index(n+2-i)
            if i > 0:
                rect.move_to(rects[0]).shift(RIGHT * i * dx).align_to(rects[0], DOWN)
            rects.append(rect)

        eq = MathTex(r'123\cdots n', font_size=40)[0].next_to(rects[0], DOWN, buff=0.15)
        eq2 = MathTex(r'\bf 135 2n-1', font_size=36, color=PURE_RED, stroke_color=BLACK, stroke_width=1.5)[0].set_z_index(20)
        for i in range(-1, 3):
            eq[i].move_to(rects[i], coor_mask=RIGHT)
            tmp = eq2[i] if i >=0 else eq2[-4:]
            if i >= 0:
                eq2[i].move_to(rects[i]).rotate(90*DEGREES)
            else:
                eq2[-4:].move_to(rects[i].get_bottom()).shift(UP*n/2*dx).rotate(90*DEGREES)
        eq[3:6].move_to((eq[2].get_right()+eq[-1].get_left())/2, coor_mask=RIGHT)

        gp = VGroup(*rects, eq, eq2).move_to(ORIGIN).to_edge(DOWN, buff=0.2)
        self.wait(0.5)
        self.play(FadeIn(rects[0], eq[0], eq2[0]), run_time=0.5)
        print(len(rects))
        for i in range(1, n):
            anims = [ReplacementTransform(rects[i-1].copy().set_z_index(n+2-i), rects[i])]
            if i < 3:
                anims.append(FadeIn(eq[i], eq2[i]))
            elif i == 3:
                anims.append(FadeIn(eq[3:6]))
            elif i == n-1:
                anims.append(FadeIn(eq[-1], eq2[-4:]))

            self.play( *anims, run_time=0.5)

        rect = Rectangle(width=n*dx, height=n*dx, stroke_color=YELLOW, stroke_opacity=1, fill_opacity=0,
                         stroke_width=6).align_to(rects[0], DL).set_z_index(100)
        self.wait(0.2)
        eq3 = MathTex(r'n', color=YELLOW).set_z_index(10).rotate(90*DEGREES).next_to(rect, LEFT, buff=0.2)
        self.play(Create(rect, rate_func=linear), FadeIn(eq3, rate_func=lambda t: max(2*t-1, 0)), run_time=2)
#        for r in gp:
#            self.play(Create(r), run_time=0.5)

        rects1 = []
        rects2 = []
        for i in range(n//2, n):
            j = 2*i+1
            rect1 = Rectangle(width=dx, height=dx * n, stroke_width=3, stroke_opacity=1, fill_opacity=1,
                             fill_color=fill_color, stroke_color=BLUE).set_z_index(2)
            rect2 = Rectangle(width=dx, height=dx * (j-n), stroke_width=3, stroke_opacity=1, fill_opacity=1,
                             fill_color=fill_color, stroke_color=BLUE).set_z_index(2)
            rect1.move_to(rects[i]).align_to(rects[i], DOWN)
            rect2.move_to(rects[i]).align_to(rects[i], DOWN).shift(UP*dx*n)
            self.add(rect1)
            self.remove(rects[i])
            rects1.append(rect1)
            rects2.append(rect2)

        gp = VGroup(*rects2)

        angle = ValueTracker(0.)

        def f():
            t = angle.get_value()
            return gp.copy().rotate(t, about_point=gp.get_corner(DL))

        rect3 = always_redraw(f)
        self.add(rect3)
        self.wait(0.5)

        self.play(angle.animate.set_value(180*DEGREES), run_time=3)

        self.wait(0.5)


class SquareSum(ThreeDScene):
    def create_blocks(self, n, h, gap1):
        colors = [BLUE, TEAL, GREEN, YELLOW_E, RED, PINK, GOLD, MAROON, PURPLE]
        cube = Prism((h, h, h), fill_color=BLUE, stroke_width=1, stroke_color=WHITE, stroke_opacity=1).set_z_index(1.0)

        shifts = []
        shift = 0.0
        for i in range(n):
            tmp = []
            for j in range(i + 1):
                tmp.append(shift)
                shift += h
            shifts.append(tmp)
            shift += gap1

        return VGroup(*[VGroup(*[VGroup(*[VGroup(*[
            cube.copy().shift(UP * shifts[i][k] + RIGHT * shifts[j][l]).set_fill(color=colors[max(i, j)])
            for l in range(j + 1)]) for k in range(i + 1)]) for j in range(n)]) for i in range(n)]).move_to(ORIGIN)

    def do_init(self, n, blocks, skip=False, do_eqns=True):
        h = blocks[0][0][0][0].width
        eq1 = [MathTex(r'\bf {}'.format(i + 1), z_index=100.0)[0].set_z_index(100.0).move_to(blocks[0][i]) for i in range(n)]
        maxh = max([x.height for x in eq1])
        for i in range(n):
            eq1[i].rotate(90 * DEGREES, axis=RIGHT).shift(OUT * (maxh/2 + h/2))

        eq01 = MathTex(r'\bf 2025{{=}}45^2')
        eq02 = MathTex(r'\bf 2025{{=}}(1+2+3+4+5+6+7+8+9)^2').set_z_index(0.0)
        eq03 = MathTex(r'\bf 2025{{=}}1^3+2^3+3^3+4^3+5^3+6^3+7^3+8^3+9^3')
        VGroup(eq01, eq02, eq03).to_edge(UP, buff=1)
        self.add_fixed_in_frame_mobjects(eq01, eq02, eq03)
        self.remove(eq01, eq02, eq03)

        if skip:
            self.add(blocks, *eq1, *eq02)
            return eq02, eq03

        if do_eqns:
            self.play(FadeIn(eq01), run_time=1)
            self.play(abra.fade_replace(eq01[2][:-1], eq02[2][:-1]),
                      ReplacementTransform(eq01[2][-1], eq02[2][-1]),
                      ReplacementTransform(eq01[:2], eq02[:2]),
                      run_time=3)

        row0 = blocks[0].copy().scale(1.7).move_to(ORIGIN).shift(RIGHT*h*5)
        row0.shift(IN*maxh)
        eq2 = [eq1[i].copy().move_to(row0[i]).shift(OUT * (maxh + h)) for i in range(n)]

        gp1 = VGroup(blocks[0], VGroup(*eq1))
        gp2 = VGroup(row0, VGroup(*eq2))

        for i in range(n):
            self.play(FadeIn(gp2[0][i], gp2[1][i]), run_time=0.5)

        self.play(ReplacementTransform(gp2, gp1), run_time=1)

        fps = config.frame_rate

        for i in range(1, n):
            self.add(blocks[i])
            self.wait(1.0/15 + 0.01)

        return eq02, eq03


    def construct(self):
        skip = False
        do_eqns = False

        n = 9
        sum_n = (n*(n+1))//2
        h = 7 / sum_n
        phi = 60*DEGREES
        theta = -110*DEGREES
        self.set_camera_orientation(phi=phi, theta=theta)
#        self.add(Arrow3D(ORIGIN, RIGHT, color=RED), Arrow3D(ORIGIN, UP, color=GREEN), Arrow3D(ORIGIN, OUT, color=YELLOW))

        blocks = self.create_blocks(n, h, h)

        eq1, eq2 = self.do_init(n, blocks, skip=False, do_eqns=do_eqns)

        for i in range(n-1, 0, -1):
            self.wait(0.5)
            pos0 = blocks[0][i][0][0].get_center()
            pos1 = blocks[i][i][0][0].get_center()
            anims = []
            shifts = []
            for j in range(i):
                x = blocks[i][j]
                shifts.append(blocks[i][i][0][-1].get_center() - x[0][-1].get_center())
                x.shift(OUT*h*(i-j)) if skip else anims.append(x.animate.shift(OUT*h*(i-j)))
            self.wait(1) if skip else self.play(*anims, run_time=1)

            anims = []
            for j in range(i):
                blocks[i][j].shift(shifts[j]) if skip else anims.append(blocks[i][j].animate.shift(shifts[j]))
            self.wait(1) if skip else self.play(*anims, run_time=1)

            if skip:
                blocks[i][:i].rotate(90 * DEGREES, axis=OUT, about_point=blocks[i][i].get_center())
                self.wait(1)
            else:
                ang = ValueTracker(0.0)

                def f():
                    x = ang.get_value()
                    return blocks[i][:i].copy().rotate(x, axis=OUT, about_point=blocks[i][i].get_center())

                rot = always_redraw(f)
                self.remove(*blocks[i][:i])
                self.add(rot)
                self.play(ang.animate.set_value(90*DEGREES), run_time=1)
                self.remove(rot)
                self.add(*blocks[i][:i])
                blocks[i][:i].rotate(90 * DEGREES, axis=OUT, about_point=blocks[i][i].get_center())

            anims = []
            shifts = []
            for j in range(i):
                x = blocks[j][i]
                shifts.append(blocks[i][i][0][0].get_center() - x[0][0].get_center())
                x.shift(OUT*h*(j+1)) if skip else anims.append(x.animate.shift(OUT*h*(j+1)))
            self.wait(1) if skip else self.play(*anims, run_time=1)

            t_shift = ValueTracker(0.0)
            def f():
                t = t_shift.get_value()
                res = VGroup(*blocks[i][:i+1].copy()).shift((pos0-pos1)*t)
                sblocks = []
                for j in range(i):
                    p0 = res[i-j-1][-1][0].get_center() + DOWN*h
                    p1 = blocks[j][i][-1][0].get_center()
                    shift = p0-p1
                    shift[1] = min(shift[1], 0.0)
                    sblocks.append(blocks[j][i].copy().shift(shift))

                return VGroup(*res[:], *sblocks)

            shifted = always_redraw(f)
            self.remove(*blocks[i][:i+1], *[blocks[j][i] for j in range(i)])
            self.add(shifted)
            self.play(t_shift.animate.set_value(1.0), run_time=2)
            self.remove(shifted)
            cube = f()
            self.add(cube)

        if not skip and do_eqns:
            self.play(ReplacementTransform(eq1[:2], eq2[:2]),
                      FadeOut(eq1[2][0], eq1[2][-2:]),
                      ReplacementTransform(eq1[2][1:1+2*n:2], eq2[2][0:3*n:3]),
                      ReplacementTransform(eq1[2][2:2+2*(n-1):2], eq2[2][2:3*(n-1):3]),
                      FadeIn(*eq2[2][1:1+3*n:3]),
                      run_time=3)
        self.wait(1)


class SquareSumEq(Scene):
    def __init__(self, *args, **kwargs):
        if config.transparent:
            print("transparent!")
            config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    def construct(self):
        eq01 = MathTex(r'\bf 2025{{=}}45^2')
        eq02 = VGroup(*MathTex(r'\bf 2025{{=}}')[:], MathTex(r'(1+2+3+4+5+6+7+8+9)^2', font_size=28)[0])
        spc = r'\hspace{-0.3em}'
        spc2 = r'\hspace{-0.05em}'
        eq03 = MathTex(r'1^3{0}+{1}2^3{0}+{1}3^3{0}+{1}4^3{0}+{1}5^3{0}+{1}6^3{0}+{1}7^3{0}+{1}8^3{0}+{1}9^3'.format(spc, spc2), font_size=28)[0]
        VGroup(eq01, eq02, eq03).to_edge(UP, buff=1)
        eq02[:2].move_to(ORIGIN, coor_mask=RIGHT)
        eq02[2].move_to(ORIGIN).next_to(eq03[:2], DOWN*1.5, coor_mask=UP)
        eq03.next_to(eq02[2][1], ORIGIN, submobject_to_align=eq03[0])
        eq03.move_to(ORIGIN, coor_mask=RIGHT)

        self.add(eq01)
        self.wait(0.5)
        self.play(abra.fade_replace(eq01[2][:-1], eq02[2][:-1]),
                  ReplacementTransform(eq01[2][-1], eq02[2][-1]),
                  ReplacementTransform(eq01[:2], eq02[:2]),
                  run_time=2)
        self.wait(1)
        eq1 = eq02
        eq2 = eq03
        n = 9
        self.play(FadeOut(eq1[2][0], eq1[2][-2:]),
                  ReplacementTransform(eq1[2][1:1 + 2 * n:2], eq03[0:3 * n:3]),
                  ReplacementTransform(eq1[2][2:2 + 2 * (n - 1):2], eq03[2:3 * (n - 1):3]),
                  FadeIn(*eq03[1:1 + 3 * n:3]),
                  run_time=2)


class SquareSumEq2(Scene):
    def construct(self):
        self.add(MathTex(r'\left(\sum_{k=1}^nk\right)^2=\sum_{k=1}^nk^3'))

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        SquareSum().render()


