from manim import *
import cv2
import math

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
        eq4 = MathTex(r'x=2').to_edge(UP, buff=1)
        eq5 = MathTex(r"\mathbb E[{{W_A}} -& {{W_B}}\vert A]{{\mathbb P(A) }}{{ +}}"
                      r"\\ & \mathbb E[{{W_A}} - {{W_B}}\vert B]{{\mathbb P(B)}} {{=}} 0",
                      font_size=40).next_to(eq4, DOWN).align_to(eq4, UP)

        eq5 = MathTex(r"\mathbb E[{{W_A}} - {{W_B}}\vert A]{{\mathbb P(A) }}{{ +}}"
                      r" \mathbb E[{{W_A}} - {{W_B}}\vert B]{{\mathbb P(B)}} {{=}} 0",
                      font_size=40)
        eq5[7:].next_to(eq5[:7], DOWN, coor_mask=UP, buff=0.208).align_to(eq5[2], LEFT)
        eq5.next_to(eq4, DOWN).align_to(eq4, UP)


        self.add(eq5)
        self.wait(1)
        eq6 = MathTex(r"\mathbb E[{{W_A}} - {{W_B}}\vert A]{{\mathbb P(A)}}{{ = }} "
                      r"\mathbb E[{{W_B}} - {{W_A}}\vert B]{{\mathbb P(B)}}", font_size=40)
        eq6.shift(eq5[0].get_center()-eq6[0].get_center())
        eq6[6:].shift(eq5[7][0].get_center() - eq6[7][0].get_center())
        self.play(ReplacementTransform(eq5[:6] + eq5[-2] + eq5[7] + eq5[8] + eq5[9] + eq5[10] + eq5[11:13],
                                       eq6[:6] + eq6[6] + eq6[7] + eq6[10] + eq6[9] + eq6[8] + eq6[11:13]),
                  FadeOut(eq5[6], eq5[-1]),
                  run_time=2)
        self.wait(1)





if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        Dice().render()


