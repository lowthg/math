"""
Animations for ABRACADABRA! The magic of martingale theory
"""

from manim import *
import numpy as np
import math
import random

# Global variable with H coin and T coin used throughout
H = LabeledDot(Text("H", color=BLACK, font='Helvetica', weight=SEMIBOLD), radius=0.35, color=BLUE).scale(1.5)
T = LabeledDot(Text("T", color=BLACK, font='Helvetica', weight=SEMIBOLD), radius=0.35, color=YELLOW).scale(1.5)


class label_ctr(Text):
    def __init__(self, text, font_size):
        Text.__init__(self, text, font_size=font_size, color=RED)

def label_ctrMU(text, font_size):
    return MarkupText(text, font_size=font_size, color=RED)

def get_coin(face='H'):
    global H, T
    if face == 'H':
        return H.copy()
    elif face == 'T':
        return T.copy()
    raise Exception('invalid argument {}'.format(face))


def set_new_location(A, B):
    A.set_x(B.get_x())
    A.set_y(B.get_y())


def animate_flip(scene: Scene, coin, rate=0.1, nflips=1):
    """
    RETURNS a list of animations that animate the mobject "coin" being flipped
    The "final" variable incidicates what you want it to be at the end of the flipping
    To animate a coin, use a loop to play the animations:

    for a in animate_flip(coins[i],coin_flips[i]):
            self.play(a,run_time=0.2)

    """

    global H, T

    final = coin.submobjects[0].text

    offset = 1 if final == 'H' else 0  # Ensures the coin lands on the side requested

    scale = coin.radius/H.radius

    full_fc = [H.copy().move_to(coin.get_center()).scale(scale), T.copy().move_to(coin.get_center()).scale(scale)]

    rate_fn = lambda t: 1 - math.cos(math.pi * t * 0.95 / 2)

    for i in range(2*nflips):
        scene.play(coin.animate(rate_func=rate_fn, remover=True).stretch(0.0, dim=1), run_time=rate)
        coin = full_fc[(i + offset) % 2].copy()
        scene.play(coin.animate(rate_func=lambda t: rate_fn(1-t)).stretch(0.0, dim=1), run_time=rate)

    return coin


class MonkeyType(Scene):
    """
    Intro - Monkey typing the infinite monkey theorem
    """
    def construct(self):
        monkey = ImageMobject("Chimpanzee_seated_at_typewriter.jpg").scale(0.7).to_edge(DR, buff=0.1)
        ft = Text("THE INFINITE MONKEY THEOREM", font="Courier New", weight=SEMIBOLD, color=BLUE, font_size=30)\
            .to_edge(UP, buff=1).shift(LEFT).set_opacity(0)
        bodytext = "\tA monkey hitting keys at random on a\n"\
                   "typewriter keyboard, for an infinite amount\n"\
                   "of time, will almost surely type any given\n"\
                   "text, including the complete\n"\
                   "works of William Shakespeare."
        ft2 = Text(bodytext, font="Courier New", font_size=30, line_spacing=1.2).set_opacity(0)

        ias = ft2.text.find('almost')

        ft2.next_to(ft, DOWN, buff=0.5)

        self.add(monkey)

        self.add(ft, ft2)

        if True:
            for x in ft:
                self.wait(0.12)
                x.set_opacity(1)

            for x in ft2:
                self.wait(0.12)
                x.set_opacity(1)
        else:
            ft.set_opacity(1)
            ft2.set_opacity(1)
            self.wait(1)

        self.play(ft2[ias:ias+10].animate.set(color="#E02A20").set_style(stroke_width=1.2))
        self.play(ft.animate.set_opacity(0), ft2[:ias].animate.set_opacity(0), ft2[ias+10:].animate.set_opacity(0),
                  monkey.animate.set_opacity(0), run_time=3)
        self.play(ft2.animate.set(font_size=100).shift(RIGHT*2.6))
        self.wait(1)


class SequenceH(Scene):
    @staticmethod
    def sequences(n=5):
        for i in range(n):
            row = ''
            while len(row) < 1 or row[-1] != 'H':
                row += random.choice(['H', 'T'])
            print(row)

    def construct(self):
        sequences = [
            'TH',
            'TTTH',
            'H',
            'TTH'
        ]
        coins = VGroup(*[
            VGroup(*[get_coin(face) for face in row]).arrange(RIGHT) for row in sequences
        ]).arrange(DOWN).to_edge(UL)
        for row in coins:
            row.to_edge(LEFT).shift(RIGHT)

        for row in coins:
            self.wait(0.5)
            for coin in row:
                animate_flip(self, coin)
            self.wait(0.5)
            nh = MathTex('N_H={}'.format(len(row)), font_size=80).next_to(coins, RIGHT, buff=1).set_y(row.get_y())
            self.play(FadeIn(nh))
            self.wait(0.5)

        eq1 = MathTex(r'\mathbb E[N_H]=2', font_size=80).to_edge(DOWN, buff=1.2)
        self.play(FadeIn(eq1))
        self.wait(1)


class GeometricMean(Scene):
    def explicit_calc(self, top: VMobject, font_size=60):
        eq1 = MathTex(r'\mathbb P(N_H > n){{=}}\mathbb P({{{\rm first\ }n{\rm\ tosses\ are\ T}}})',
                      font_size=font_size).next_to(top, DOWN, buff=1).align_to(top, LEFT)
        self.play(FadeIn(eq1), run_time=0.5)

        eq2 = MathTex(r'{{=}}\mathbb P({{1^{\rm st}{\rm\ is\ T}}},{{2^{\rm nd}{\rm\ is\ T}}},\ldots,{{n^{\rm th}{\rm\ is\ T}}})',
                      font_size=font_size)
        eq2.shift(eq1[1].get_center()-eq2[0].get_center())
        self.wait(0.5)
        self.play(ReplacementTransform(eq1[1:3], eq2[0:2]),
                  run_time=0.5)
        self.play(FadeOut(eq1[3:5]),
                  FadeIn(eq2[2:8]),
                  run_time=2)
        self.wait(0.5)

        eq3 = MathTex(r'{{=}}\mathbb P({{1^{\rm st}{\rm\ is\ T}}})\mathbb P({{2^{\rm nd}{\rm\ is\ T}}})\cdots\mathbb P({{n^{\rm th}{\rm\ is\ T}}})',
                      font_size=font_size)
        eq3.shift(eq2[0].get_center()-eq3[0].get_center())

        txt1 = Text(r'Independence!', color=RED, font_size=font_size).next_to(eq3, DOWN).align_to(eq3[1])
        self.add(txt1)
        self.play(ReplacementTransform(eq2[0:3], eq3[0:3]),
                  ReplacementTransform(eq2[4], eq3[4]),
                  ReplacementTransform(eq2[6:8], eq3[6:8]),
                  FadeOut(eq2[3], eq2[5]),
                  FadeIn(eq3[3], eq3[5]),
                  run_time=2)
        self.remove(txt1)

        self.wait(0.5)

        eq4 = MathTex(r'\mathbb P(N_H > n){{=}}(1-p)^n', font_size=font_size)
        eq4.shift(eq3[0].get_center() - eq4[1].get_center())

        eq4_1 = eq4[2][0:5].copy()
        eq4_2 = eq4[2][0:5].copy()
        eq4_3 = eq4[2][0:5].copy()
        eq4_1.shift([(eq3[2].get_center() - eq4_1.get_center())[0], 0, 0])
        eq4_2.shift([(eq3[4].get_center() - eq4_2.get_center())[0], 0, 0])
        eq4_3.shift([(eq3[6].get_center() - eq4_3.get_center())[0], 0, 0])

        self.play(FadeOut(eq3[1][0], eq3[2], eq3[3][1], eq3[4], eq3[5][4], eq3[6]),
                  ReplacementTransform(eq3[1][1], eq4_1[0]),
                  ReplacementTransform(eq3[3][0], eq4_1[-1]),
                  ReplacementTransform(eq3[3][2], eq4_2[0]),
                  ReplacementTransform(eq3[5][0], eq4_2[-1]),
                  ReplacementTransform(eq3[5][-1], eq4_3[0]),
                  ReplacementTransform(eq3[7][0], eq4_3[-1]),
                  FadeIn(eq4_1[1:-1], eq4_2[1:-1], eq4_3[1:-1]),
                  run_time=2)

        self.wait(0.5)

        self.play(ReplacementTransform(eq3[0], eq4[1]),
                  ReplacementTransform(eq4_1[0:5], eq4[2][0:5]),
                  ReplacementTransform(eq4_2[0:5], eq4[2][0:5]),
                  ReplacementTransform(eq4_3[0:5], eq4[2][0:5]),
                  FadeOut(eq3[5][1:-2]),
                  FadeIn(eq4[2][-1]),
                  ReplacementTransform(eq1[0], eq4[0]),
                  run_time=2)

        self.wait(0.5)

        txt2 = Text(r'Geometric distribution!', color=RED, font_size=font_size).next_to(eq4, DOWN).move_to(ORIGIN, coor_mask=np.array([1,0,0]))
        self.play(FadeIn(txt2), run_time=0.1)
        self.wait(1)
        self.play(FadeOut(txt2), run_time=0.1)
        self.wait(0.5)

        self.play(eq4.animate.next_to(top, DOWN).align_to(top, LEFT))

        self.wait(1)

        eq5 = MathTex(r'\mathbb E[N_H]{{=}}{{\sum_{m=0}^\infty}}m{{\mathbb P(N_H = m)}}', font_size=font_size)\
            .next_to(eq4, DOWN).align_to(eq4, LEFT)
        self.play(FadeIn(eq5), run_time=0.5)
        self.wait(0.5)

        eq6 = MathTex(r'{{=}}{{\sum_{m=0}^\infty}}\sum_{n=0}^{m-1}{{\mathbb P(N_H = m)}}', font_size=font_size)
        eq6.shift(eq5[1].get_center() - eq6[0].get_center())

        self.play(ReplacementTransform(eq5[2], eq6[1]),
                 # ReplacementTransform(eq5[3], eq6[2]),
                  ReplacementTransform(eq5[3][0], eq6[2][0]),
                  FadeIn(eq6[2][1:]),
                  ReplacementTransform(eq5[4], eq6[3]),
                  run_time=2)
        self.wait(0.5)
        eq7 = MathTex(r'{{=}}{{\sum_{n=0}^\infty}}\sum_{m=n+1}^\infty{{\mathbb P(N_H = m)}}', font_size=font_size)
        eq7.shift(eq6[0].get_center() - eq7[0].get_center())
        self.play(ReplacementTransform(eq5[1], eq7[0]),
                  ReplacementTransform(eq6[2][3:], eq7[1][1:]),
                  ReplacementTransform(eq6[2][:3], eq7[1][:1]),
                  ReplacementTransform(eq6[1][:4], eq7[2][:4]),
                  ReplacementTransform(eq6[1][4:], eq7[2][4:]),
                  ReplacementTransform(eq6[3], eq7[3]),
                  run_time=2)
        self.wait(0.5)
        eq8 = MathTex(r'{{=}}{{\sum_{n=0}^\infty}}{{\mathbb P(N_H > n)}}', font_size=font_size)
        eq8.shift(eq7[0].get_center() - eq8[0].get_center())
        self.play(ReplacementTransform(eq7[:2], eq8[:2]),
                  FadeOut(eq7[2]),
                  ReplacementTransform(eq7[3], eq8[2]),
                  run_time=2)
        self.wait(0.5)

        eq9 = MathTex(r'{{=}}{{\sum_{n=0}^\infty}}{{(1-p)^n}}', font_size=font_size)
        eq9.shift(eq8[0].get_center() - eq9[0].get_center())
        self.play(ReplacementTransform(eq8[:2], eq9[:2]),
                  ReplacementTransform(eq4[2].copy(), eq9[2]),
                  FadeOut(eq8[2]),
                  run_time=2)
        self.wait(0.5)

        eq10 = MathTex(r'={{\frac{1}{1-(1-p)}}}', font_size=font_size)
        eq10.shift(eq9[0].get_center() - eq10[0].get_center())
        txt2 = Text(r'Geometric series!', color=RED, font_size=font_size).next_to(eq10, RIGHT, buff=1)
        self.add(txt2)
        self.play(FadeOut(eq9[1:2], eq9[2][-1]),
                  FadeIn(eq10[1][:4]),
                  ReplacementTransform(eq9[2][:-1], eq10[1][4:]),
                  ReplacementTransform(eq9[0], eq10[0]),
                  run_time=2)
        self.remove(txt2)
        self.wait(0.5)

        eq11 = MathTex(r'={{\frac{1}{1-(1+p)}}}', font_size=font_size)
        eq11.shift(eq10[0].get_center() - eq11[0].get_center())
        self.play(ReplacementTransform(eq10[0], eq11[0]),
                  ReplacementTransform(eq10[1][:4], eq11[1][:4]),
                  ReplacementTransform(eq10[1][5:8], eq11[1][5:8]),
                  FadeOut(eq10[1][4], eq10[1][8]),
                  run_time=0.5)

        eq12 = MathTex(r'={{\frac{1}{1-1+p}}}', font_size=font_size)
        eq12.shift(eq11[0].get_center() - eq12[0].get_center())
        self.play(ReplacementTransform(eq11[0], eq12[0]),
                  ReplacementTransform(eq11[1][:4], eq12[1][:4]),
                  ReplacementTransform(eq11[1][5:8], eq12[1][4:7]),
                  run_time=1)
        self.wait(0.5)

        l1 = Line(LEFT*0.4, RIGHT*0.4, color=BLUE, stroke_width=10).move_to(eq12[1][2]).rotate(0.8)
        l2 = Line(LEFT*0.4, RIGHT*0.4, color=BLUE, stroke_width=10).move_to(eq12[1][4]).rotate(0.8)
        self.play(FadeIn(l1, l2))
        self.wait(0.5)

        self.play(FadeOut(l1, l2, eq12[1][2:5]), run_time=1)
        self.wait(0.5)

        eq13 = MathTex(r'\mathbb E[N_H]{{=}}\frac1p', font_size=font_size)
        eq13.shift(eq12[0].get_center() - eq13[1].get_center())
        self.play(ReplacementTransform(eq5[0], eq13[0]),
                  ReplacementTransform(eq12[0], eq13[1]),
                  ReplacementTransform(eq12[1][:2], eq13[2][:2]),
                  ReplacementTransform(eq12[1][6], eq13[2][2]),
                  FadeOut(eq12[1][5]),
                  run_time=1)
        self.wait(2)

        return [eq4, eq13]

    def construct(self):
        font_size = 60

        explicit_calc = True
        alt_calc = True
        initial_anim = True

        coins = VGroup(*[get_coin(face) for face in 'TTTTH']).arrange(RIGHT).to_edge(UP)

        if initial_anim:
            self.wait(0.1)
            for coin in coins:
                animate_flip(self, coin)

        txt0 = VGroup(Tex(r'Biased coin with $\mathbb P({\rm H})=p$', font_size=font_size),
                      Tex(r'$N_H=$ number of tosses to get H', font_size=60))\
            .arrange(DOWN, center=False, aligned_edge=LEFT).to_edge(UL).shift(DOWN*1.4)

        if initial_anim:
            self.play(FadeIn(txt0[0]), run_time=1)
            self.play(FadeIn(txt0[1]), run_time=1)
        else:
            self.add(coins, txt0)

        if explicit_calc:
            explicit_obj = self.explicit_calc(txt0)
            if alt_calc:
                self.play(FadeOut(*explicit_obj), run_time=1)

        if alt_calc:
            txt1 = Text(r'Markov/recursive method', color=RED, font_size=font_size).next_to(txt0, DOWN).shift(DOWN)\
                .move_to(ORIGIN, coor_mask=np.array([1, 0, 0]))
            self.play(FadeIn(txt1), run_time=0.5)
            self.wait(1)
            self.play(FadeOut(txt1), run_time=0.5)

            txt2 = Tex(r'$X =$ first coin flip', font_size=font_size).next_to(txt0, DOWN).align_to(txt0, LEFT)
            self.play(FadeIn(txt2), run_time=0.5)

            eq1 = MathTex(r'\mathbb E[N_H]{{=}} 1 + {{\mathbb E[N_H-1\vert X={\rm T}]}}\mathbb P(X={\rm T})',
                          font_size=font_size).next_to(txt2, DOWN).align_to(txt2, LEFT)
            self.wait(0.5)
            self.play(FadeIn(eq1), run_time=0.5)

            br1 = BraceLabel(eq1[2][0], r'First flip', label_constructor=label_ctr, font_size=40,
                             brace_config={'color': RED})
            br2 = BraceLabel(eq1[3][2:6], r'Additional tosses in case first is not H',
                             label_constructor=label_ctr, font_size=40, brace_config={'color': RED})

            self.play(FadeIn(br1), run_time=0.5)
            self.wait(1)
            self.play(FadeOut(br1), run_time=0.5)
            self.play(FadeIn(br2), run_time=0.5)
            self.wait(1)
            self.play(FadeOut(br2), run_time=0.5)

            eq2 = MathTex(r'\mathbb E[N_H-1\vert X={\rm T}]={{\mathbb E[N_H]}}',
                          font_size=font_size).next_to(eq1, DOWN).align_to(eq1, LEFT)
            self.play(FadeIn(eq2), run_time=0.5)

            txt3 = Text(r'Markov property!', color=RED, font_size=font_size).next_to(eq2, DOWN, buff=0.5)
            self.play(FadeIn(txt3), run_time=0.5)
            self.wait(1)
            self.play(FadeOut(txt3), run_time=0.5)

            eq3 = eq2[1].copy()
            self.play(FadeOut(eq1[3]),
                      eq3.animate.move_to(eq1[3]),
                      run_time=1)

            eq4 = MathTex(r'{{=}} 1 + {{\mathbb E[N_H]}}\mathbb P(X={\rm T})',
                          font_size=font_size)
            eq4.shift(eq1[1].get_center()-eq4[0].get_center())

            self.play(ReplacementTransform(eq1[1:3], eq4[0:2]),
                      ReplacementTransform(eq3, eq4[2]),
                      ReplacementTransform(eq1[4], eq4[3]),
                      FadeOut(eq2),
                      run_time=1)

            eq5 = MathTex(r'{{=}} 1 + {{\mathbb E[N_H]}}(1-p)',
                          font_size=font_size)
            eq5.shift(eq4[0].get_center()-eq5[0].get_center())

            self.play(ReplacementTransform(eq4[0:3], eq5[0:3]),
                      FadeOut(eq4[3]),
                      FadeIn(eq5[3]),
                      run_time=2)
            self.wait(0.5)

            eq6 = MathTex(r'{{\mathbb E[N_H]}}-{{\mathbb E[N_H]}}{{(1-p)}}={{1}}', font_size=font_size)
            eq6.shift(eq5[0].get_center()-eq6[4].get_center())
            eq6.align_to(txt2, LEFT)

            self.play(ReplacementTransform(eq1[0], eq6[0]),
                      ReplacementTransform(eq5[1][1], eq6[1][0]),
                      ReplacementTransform(eq5[2:4], eq6[2:4]),
                      ReplacementTransform(eq5[0], eq6[4]),
                      ReplacementTransform(eq5[1][0], eq6[-1][0]),
                      FadeOut(txt2),
                      run_time=2)

            self.wait(0.5)

            l1 = Line(LEFT * 0.8, RIGHT * 0.8, color=BLUE, stroke_width=10).move_to(eq6[0]).rotate(0.6)
            l2 = Line(LEFT * 0.4, RIGHT * 0.4, color=BLUE, stroke_width=10).move_to(eq6[3][1]).rotate(0.8)
            self.play(FadeIn(l1, l2), run_time=0.5)
            self.wait(0.5)
            self.play(FadeOut(l1, l2, eq6[0], eq6[3][1]), run_time=1)
            self.play(FadeOut(eq6[1], eq6[3][2], eq6[3][0], eq6[3][4]), run_time=0.5)

            eq7 = MathTex(r'{{\mathbb E[N_H]}}p{{=}}1', font_size=font_size)
            eq7.shift(eq6[4].get_center()-eq7[2].get_center())
            eq7.align_to(txt2, LEFT).shift(RIGHT)

            self.play(ReplacementTransform(eq6[2], eq7[0]),
                      ReplacementTransform(eq6[3][3], eq7[1]),
                      ReplacementTransform(eq6[4], eq7[2]),
                      ReplacementTransform(eq6[5], eq7[3]),
                      run_time=1)
            self.wait(0.5)
            eq8 = MathTex(r'{{\mathbb E[N_H]}}{{=}}\frac1p', font_size=font_size)
            eq8.shift(eq7[2].get_center()-eq8[1].get_center())
            eq8.align_to(eq7, LEFT)

            self.play(ReplacementTransform(eq7[0], eq8[0]),
                      ReplacementTransform(eq7[2], eq8[1]),
                      ReplacementTransform(eq7[3][0], eq8[2][0]),
                      ReplacementTransform(eq7[1][0], eq8[2][2]),
                      FadeIn(eq8[2][1]),
                      run_time=2)


            self.wait(1)

            return


class MartingaleH(Scene):
    """
    Time to get H
    """
    def get_door(self, z_index=0):
        door_back = ImageMobject('doorway.png', z_index=z_index).scale(0.6).to_edge(UR)
        a = door_back.pixel_array.copy()
        m,n,p = a.shape
        for i in range(m):
            for j in range(int(n/2)):
                a[i, j, 3] = 0

        door_front = ImageMobject(a, z_index=z_index+3).scale(0.6).to_edge(UR)
        door_hide=Rectangle(width=1, height=2, fill_opacity=1, fill_color=BLACK, stroke_opacity=0, z_index=z_index+2).\
            next_to(door_front, RIGHT, buff=-0.1)
        return Group(door_back, door_hide, door_front)

    def initial_setup(self):
        rules_size = 40
        rules = VGroup(
            Tex(r'\underline{Coin Toss Game Rules}', font_size=rules_size),
            Tex(r'Before flip: Place your stake', font_size=rules_size),
            Tex(r'If T comes up: Receive nothing, losing the stake', font_size=rules_size),
            Tex(r'If H comes up: Receive stake multiplied by $1/p$', font_size=rules_size),
        ).arrange(DOWN, center=False, aligned_edge=LEFT).to_edge(UL)
        rules.shift(rules.get_center() * np.array([-1, 0, 0]))

        for rule in rules:
            self.play(FadeIn(rule), run_time=0.5)
            self.wait(1)
        self.wait(1)

        box = SurroundingRectangle(rules, color=RED, corner_radius=0.1)
        self.play(FadeIn(box), run_time=0.5)

        eq1 = MathTex(r'{\rm Expected\ profit} {{=}} -S + \frac{S}{p}\mathbb{P}(H)', font_size=60)
        eq1.next_to(rules, DOWN, buff=1)

        self.play(FadeIn(eq1), run_time=1)
        self.wait(1)

        br1 = BraceLabel(eq1[2][:2], r'Initial stake', label_constructor=label_ctr, font_size=40,
                         brace_config={'color': RED})
        br2 = BraceLabel(eq1[2][3:6], r'Winnings if H comes up', label_constructor=label_ctr, font_size=40,
                         brace_config={'color': RED})
        br3 = BraceLabel(eq1[2][6:], '   Probability of H\n(independent of stake)', label_constructor=label_ctr, font_size=40,
                         brace_config={'color': RED})

        self.play(FadeIn(br1), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(br1), run_time=0.5)
        self.play(FadeIn(br2), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(br2), run_time=0.5)
        self.play(FadeIn(br3), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(br3), run_time=0.5)

        eq2 = MathTex(r'\frac{S}{p}p', font_size=60)
        eq2.shift(eq1[2][4].get_center() - eq2[0][1].get_center())

        self.wait(1)
        self.play(FadeOut(eq1[2][6:]), FadeIn(eq2[0][3]), run_time=1)
        self.wait(1)

        l1 = Line(LEFT*0.4, RIGHT*0.4, color=BLUE, stroke_width=10).move_to(eq1[2][5]).rotate(0.5)
        l2 = Line(LEFT*0.4, RIGHT*0.4, color=BLUE, stroke_width=10).move_to(eq2[0][3]).rotate(0.5)
        self.play(FadeIn(l1, l2), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(l1, l2, eq1[2][5], eq2), run_time=0.5)

        eq3 = MathTex(r'{{=}}-S+S', font_size=60)
        eq3.shift(eq1[1].get_center()-eq3[0].get_center())
        self.play(FadeOut(eq1[2][4]), run_time=0.5)
        self.play(ReplacementTransform(eq1[2][:4], eq3[1][:4]),
                  run_time=1)

        l3 = Line(LEFT*0.6, RIGHT*0.6, color=BLUE, stroke_width=10).move_to(eq3[1][1]).rotate(0.8)
        l4 = Line(LEFT*0.6, RIGHT*0.6, color=BLUE, stroke_width=10).move_to(eq3[1][3]).rotate(0.8)
        self.play(FadeIn(l3, l4))
        self.wait(2)
        self.play(FadeOut(l3, l4, eq3[1][0:2], eq3[1][3]), run_time=0.5)
        self.wait(1)

        eq4 = MathTex(r'{{=}}0', font_size=60)
        eq4.shift(eq1[1].get_center()-eq4[0].get_center())
        self.play(FadeIn(eq4[1]), FadeOut(eq3[1][2]), run_time=1)

        txt1 = Tex(r'$\Rightarrow$\ Fair game!!!', font_size=60, color=RED).next_to(eq4, RIGHT, buff=0.2)
        self.play(FadeIn(txt1), run_time=1)
        self.wait(2)
        self.play(FadeOut(eq1[0:2], eq4, txt1), run_time=1)

        strat = VGroup(
            Tex(r'\underline{Strategy}', font_size=rules_size),
            Tex(r'Stake \$1 before each toss', font_size=rules_size),
            Tex(r'If T comes up: continue playing', font_size=rules_size),
            Tex(r'If H comes up: quit the game', font_size=rules_size),
        ).arrange(DOWN, center=False, aligned_edge=LEFT).next_to(rules, DOWN, buff=1)
        #rules.shift(rules.get_center() * np.array([-1, 0, 0]))

        for rule in strat:
            self.play(FadeIn(rule), run_time=0.5)
            self.wait(1)
        self.wait(2)

        self.play(FadeOut(strat), run_time=1)

        return box

    def play_game(self, flips='TTTH'):
        door = self.get_door(z_index=1)
        door.to_edge(DR).shift(UP*1.4)
        wojak0 = ImageMobject("wojak.png")
        wojak_happy0 = ImageMobject("wojak_happy.png")
        wojak = ImageMobject(np.flip(wojak0.pixel_array, 1), z_index=2).scale(0.2).move_to(door[1])
        wojak_happy = ImageMobject(np.flip(wojak_happy0.pixel_array, 1), z_index=3).scale(0.2)
        wojak.shift(LEFT*4.5)
        wojak_pos = wojak.get_center()
        wojak.align_to(door, RIGHT)

        self.play(FadeIn(door), run_time=1)
        self.play(wojak.animate.move_to(wojak_pos), run_time=1.5)
        self.play(FadeOut(door), run_time=1)

        t1 = MobjectTable([[Text(r'$0', color=RED, font_size=40)], [Text(r'$0', color=GREEN, font_size=40)]],
                   row_labels=[Text('Paid', font_size=40), Text('Won', font_size=40)],
                   include_outer_lines=True)
        t1.to_edge(DR).shift(UP*1.2)

        t2 = MobjectTable([[Text(r'$0', font_size=40)]],
                          row_labels=[Text('Stake', font_size=40)],
                          include_outer_lines=True,
                          z_index=2)
        t2.to_edge(DL)
        t2.align_to(t1, UP)

        self.play(FadeIn(t1, t2), run_time=2)

        self.wait(1)

        coin = ImageMobject('coin.png', z_index=1).scale(0.1)

        coins = VGroup(*[get_coin(face) for face in flips]).arrange(RIGHT).to_edge(DL).shift(UP*0.5)

        paid = 0
        winnings = 2

        for i, flip in enumerate(flips):
            coin.move_to(wojak).shift(LEFT * 0.3)
            eq5 = Text(r'$1', font_size=40)
            eq5.shift(t2[0][1][0].get_center() - eq5[0].get_center())
            paid += 1
            eq6 = Text(r'${}'.format(paid), font_size=40, color=RED)
            eq6.shift(t1[0][1][0].get_center() - eq6[0].get_center())
            self.play(coin.animate(rate_func=lambda t: t).move_to(t2[0][1:].get_right()), run_time=1)
            self.play(ReplacementTransform(t2[0][1][0], eq5[0]),
                      ReplacementTransform(t1[0][1][0], eq6[0]),
                      FadeOut(t1[0][1][1], t2[0][1][1:], coin),
                      FadeIn(eq5[1:], eq6[1:]),
                      run_time=0.5)
            t1[0][1] = eq6
            t2[0][1] = eq5
            coins[i] = animate_flip(self, coins[i])
            eq7 = Text(r'$0', font_size=40)
            eq7.shift(t2[0][1][0].get_center() - eq7[0].get_center())
            if flip == 'T':
                self.wait(1)
                self.play(ReplacementTransform(t2[0][1][0], eq7[0]),
                          FadeOut(t2[0][1][1:]),
                          FadeIn(eq7[1:]),
                          run_time=0.5)
            else:
                wojak_happy.move_to(wojak)
                self.add(wojak_happy)
                self.remove(wojak)
                self.wait(1)
                coin2 = coin.copy()
                coin2.shift(RIGHT*0.3).set_z_index(0)
                coin_win = Group(coin, coin2)
                eq8 = Text(r'${}'.format(winnings), font_size=40, color=GREEN)
                eq8.shift(t1[0][3][0].get_center()-eq8[0].get_center())
                self.play(ReplacementTransform(t2[0][1][0], eq7[0]),
                          FadeOut(t2[0][1][1:]),
                          FadeIn(eq7[1:]),
                          coin_win.animate(rate_func=linear).move_to(wojak),
                          run_time=1)
                self.play(FadeOut(coin_win),
                          FadeOut(t1[0][3][1:]),
                          FadeIn(eq8[1:]),
                          ReplacementTransform(t1[0][3][0], eq8[0]),
                          run_time=0.8)
                t1[0][3] = eq8

            t2[0][1] = eq7

        self.wait(1)
        eq9 = Text(r'Profit = Winnings  - Paid', font_size=60).to_edge(DL).shift(UP*0.8)
        eq9_1 = Text(r'${}'.format(winnings), font_size=60, color=GREEN).move_to(eq9[6:14])
        eq9_2 = Text(r'${}'.format(paid), font_size=60, color=RED).move_to(eq9[15:])
        self.play(FadeOut(coins, t2), run_time=2)
        self.play(FadeIn(eq9), run_time=1)
        self.wait(1)
        self.play(FadeOut(eq9[6:14]),
                  ReplacementTransform(t1[0][3].copy(), eq9_1),
                  run_time=2)
        self.play(FadeOut(eq9[15:]),
                  ReplacementTransform(t1[0][1].copy(), eq9_2),
                  run_time=2)
        self.wait(1)
        eq10 = Text(r'= -${}'.format(paid-winnings), font_size=60)
        eq10.shift(eq9[5].get_center()-eq10[0].get_center())
        self.play(FadeOut(eq9_1, eq9_2, eq9[14]),
                  FadeIn(eq10[1:]),
                  run_time=2)
        return [eq10[1:], eq9[:6], wojak_happy, t1]

    def do_calc(self, box):
        eq_size=50
        txt1 = Tex(r'\underline{General case', font_size=eq_size).to_edge(LEFT).align_to(box, DOWN).shift(RIGHT+DOWN)
        self.play(FadeIn(txt1), run_time=1)
        eq1 = MathTex(r'{{{\rm Winnings}}}={{\frac1p}}', font_size=eq_size).next_to(txt1, DOWN).align_to(txt1, LEFT)
        self.play(FadeIn(eq1), run_time=1)
        txt2 = Text(r'from final H', font_size=eq_size, color=RED).next_to(eq1, RIGHT, buff=1)
        self.play(FadeIn(txt2), run_time=1)
        eq2 = MathTex(r'{{{\rm Paid}}}={{N_H}}', font_size=eq_size).next_to(eq1, DOWN).align_to(txt1, LEFT)
        self.play(FadeIn(eq2), run_time=1)
        txt3 = Text(r'from stakes', font_size=eq_size, color=RED).next_to(eq2, RIGHT, buff=1)
        self.play(FadeIn(txt3), run_time=1)
        eq3 = MathTex(r'{{{\rm Profit}}}={{{\rm Winnings}}}-{{{\rm Paid}}}', font_size=eq_size).move_to(eq2).align_to(txt1, LEFT)
        eq3.shift((eq2.get_left()-eq1.get_left())*np.array([0, 1, 0]))
        self.play(FadeIn(eq3), run_time=1)

        eq4 = MathTex(r'{{{\rm Profit}}}={{\frac1p}}-{{N_H}}', font_size=eq_size)
        eq4.shift(eq3[1][0].get_center()-eq4[1].get_center())
        eq5 = eq4.copy().next_to(txt1, DOWN).align_to(txt1, LEFT)
        eq4[2].shift((eq3[2].get_center()-eq4[2].get_center())*np.array([1,0,0]))
        eq4[3].shift((eq3[3].get_center()-eq4[3].get_center())*np.array([1,0,0]))
        eq4[4].shift((eq3[4].get_center()-eq4[4].get_center())*np.array([1,0,0]))
        self.play(ReplacementTransform(eq1[2].copy(), eq4[2]), FadeOut(eq3[2]), run_time=2)
        self.play(ReplacementTransform(eq2[2].copy(), eq4[4]), FadeOut(eq3[4]), run_time=2)
        self.wait(2)
        self.play(FadeOut(eq1, eq2, txt2, txt3), run_time=1)
        self.play(ReplacementTransform(eq3[:2], eq5[:2]),
                  ReplacementTransform(eq3[3], eq5[3]),
                  ReplacementTransform(eq4[2], eq5[2]),
                  ReplacementTransform(eq4[4], eq5[4]),
                  run_time=2)
        self.wait(1)
        eq6 = MathTex(r'\mathbb E[{{{\rm Profit}}}]{{=}}0', font_size=eq_size).next_to(eq5, DOWN).align_to(eq5, LEFT)
        eq6.shift(DOWN*0.2)
        self.play(FadeIn(eq6), run_time=0.5)
        txt4 = Text(r'Fair game!', color=RED, font_size=eq_size).next_to(eq6, RIGHT).shift(RIGHT)
        self.play(FadeIn(txt4), run_time=1)
        eq7 = MathTex(r'\mathbb E\left[{{\frac1p-N_H}}\right]{{=}}0', font_size=eq_size)
        eq7.shift(eq6[0][0].get_center()-eq7[0][0].get_center())
        self.wait(1)
        self.play(ReplacementTransform(eq6[0], eq7[0]),
                  ReplacementTransform(eq6[2:], eq7[2:]),
                  FadeOut(eq6[1], txt4),
                  FadeIn(eq7[1]),
                  run_time=2)
        self.wait(1)
        eq8 = MathTex(r'\frac1p-\mathbb E\left[{{N_H}}\right]{{=}}0', font_size=eq_size)
        eq8.shift(eq7[0][0].get_center()-eq8[0][4].get_center())
        eq8.align_to(eq7, LEFT)
        self.play(ReplacementTransform(eq7[1][:4], eq8[0][:4]),
                  ReplacementTransform(eq7[0][:], eq8[0][4:]),
                  ReplacementTransform(eq7[1][4:], eq8[1][:]),
                  ReplacementTransform(eq7[2:], eq8[2:]),
                  run_time=2)
        self.wait(1)
        eq9 = MathTex(r'\frac1p=\mathbb E\left[{{N_H}}\right]', font_size=eq_size)
        eq9.shift(eq8[0][4].get_center()-eq9[0][4].get_center())
        eq9.align_to(eq8, LEFT)
        self.play(ReplacementTransform(eq8[0][:3], eq9[0][:3]),
                  ReplacementTransform(eq8[3][0], eq9[0][3]),
                  ReplacementTransform(eq8[0][4:], eq9[0][4:]),
                  ReplacementTransform(eq8[1:3], eq9[1:3]),
                  FadeOut(eq8[4], eq8[0][3]),
                  run_time=2)
        self.wait(1)
        eq10 = MathTex(r'\mathbb E\left[{{N_H}}\right]=\frac1p', font_size=eq_size)
        eq10.shift(eq9[0][4].get_center()-eq10[0][0].get_center())
        eq10.align_to(eq9, LEFT)
        self.play(ReplacementTransform(eq9[0][4:], eq10[0][:]),
                  ReplacementTransform(eq9[1], eq10[1]),
                  ReplacementTransform(eq9[2][0], eq10[2][0]),
                  ReplacementTransform(eq9[0][3], eq10[2][1]),
                  ReplacementTransform(eq9[0][:3], eq10[2][2:]),
                  run_time=2)
        self.wait(2)

    def construct(self):
        if True:
            box = self.initial_setup()
        else:
            box = Rectangle(width=2, height=2).to_edge(UP)

        if True:
            r = self.play_game(flips='TTTH')
            self.wait(2)
            self.play(FadeOut(*r), run_time=2)

        if True:
            self.do_calc(box)


class Pairs(Scene):
    def construct(self):
        tosses = 'TTHTHHTHHH'
        coins = VGroup(*[get_coin(face).scale(0.8) for face in tosses]).arrange(RIGHT).to_edge(UP)
        self.add(coins)
        n = len(tosses) - 1
        box = None
        prev_eq = coins
        eqns = []
        for i in range(n):
            new_box = SurroundingRectangle(VGroup(coins[i], coins[i + 1]), color=RED, corner_radius=0.2, stroke_width=6)
            pair = tosses[i:i+2]
            eq = MathTex('P_{}={{\\rm {}{} }}'.format(i+1, *pair), font_size=50).next_to(prev_eq, DOWN)
            if i == 0:
                box = new_box
                self.play(FadeIn(box))
                eq.to_edge(LEFT).next_to(coins, DOWN, coor_mask=UP)
            else:
                self.play(box.animate.move_to(new_box), run_time=0.5)
                eq.next_to(eqns[-1], DOWN).align_to(eqns[-1], LEFT)
            self.wait(0.4)
            self.play(FadeIn(eq), run_time=0.4)
            self.wait(0.4)
            eqns.append(eq)
        self.play(FadeOut(box))

        eqs1 = VGroup(
            MathTex(r'N_{HH}=6', font_size=60),
            MathTex(r'N^P_{HH}=5', font_size=60),
            MathTex(r'N_{HT}=4', font_size=60),
            MathTex(r'N^P_{HT}=3', font_size=60),
        ).arrange_in_grid(rows=2, buff=(1, 0.5)).next_to(eqns[0], RIGHT, buff=1).next_to(coins, DOWN, coor_mask=UP, buff=1)

        box = SurroundingRectangle(coins[:6], color=RED, corner_radius=0.2, stroke_width=6)
        self.play(FadeIn(box, eqs1[0]), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(box), run_time=0.5)
        box = SurroundingRectangle(VGroup(*[X[0][-2:] for X in eqns[:5]]), color=RED, corner_radius=0.2, stroke_width=6)
        self.play(FadeIn(box, eqs1[1]), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(box), run_time=0.5)
        box = SurroundingRectangle(coins[:4], color=RED, corner_radius=0.2, stroke_width=6)
        self.play(FadeIn(box, eqs1[2]), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(box), run_time=0.5)
        box = SurroundingRectangle(VGroup(*[X[0][-2:] for X in eqns[:3]]), color=RED, corner_radius=0.2, stroke_width=6)
        self.play(FadeIn(box, eqs1[3]), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(box), run_time=0.5)
        self.wait(1)

        eq2 = MathTex(r'N_{XY}=N^P_{XY}+1', font_size=60).align_to(eqs1, UP+LEFT).shift(RIGHT)
        self.play(FadeOut(eqs1), FadeIn(eq2), run_time=2)

        eq3 = MathTex(r'\mathbb P(HH){{=}}{{\mathbb P(H)}}{{\mathbb P(H)}}', font_size=60).next_to(eq2, DOWN).align_to(eq2, LEFT)
        self.wait(1)
        self.play(FadeIn(eq3), run_time=0.5)
        eq4 = MathTex(r'={{(1/2)}}{{(1/2)}}', font_size=60)
        eq4.shift(eq3[1][0].get_center()-eq4[0][0].get_center())
        self.play(FadeOut(eq3[2][0], eq3[2][2], eq3[3][0], eq3[3][2]),
                  FadeIn(eq4[1][1:4], eq4[2][1:4]),
                  ReplacementTransform(eq3[2][1], eq4[1][0]),
                  ReplacementTransform(eq3[2][3], eq4[1][4]),
                  ReplacementTransform(eq3[3][1], eq4[2][0]),
                  ReplacementTransform(eq3[3][3], eq4[2][4]),
                  run_time=1)
        self.wait(1)
        eq5 = MathTex(r'{{\mathbb P(HH)}}={{1/4}}', font_size=60)
        eq5.shift(eq4[0][0].get_center()-eq5[1][0].get_center())
        self.play(FadeOut(eq4[1][0], eq4[1][4], eq4[2][0], eq4[2][4]),
                  ReplacementTransform(eq4[1][1:3], eq5[2][0:2]),
                  ReplacementTransform(eq4[2][1:3], eq5[2][0:2]),
                  FadeOut(eq4[1][3], target_position=eq5[2][2]),
                  FadeOut(eq4[2][3], target_position=eq5[2][2]),
                  FadeIn(eq5[2][2]),
                  ReplacementTransform(eq3[0], eq5[0]),
                  run_time=1)
        self.wait(1)

        eq6 = MathTex(r'\mathbb E[N_{HH}]{{=}}{{\mathbb E[N^P_{HH}]}}+1', font_size=60).next_to(eq5, DOWN).align_to(eq5, LEFT)
        self.play(FadeIn(eq6), run_time=1)
        self.wait(1)

        eq7 = MathTex(r'\approx{{\frac1{\mathbb P(HH)} }}', font_size=60)
        eq7.shift(eq6[1][0].get_center()-eq7[0][0].get_center())
        eq7[1].move_to(eq6[2], coor_mask=RIGHT)
        self.play(FadeOut(eq6[2]),
                  FadeIn(eq7[1]),
                  ReplacementTransform(eq6[1][0], eq7[0][0]),
                  run_time=2)
        self.wait(1)

        eq8 = MathTex(r'\approx{{\frac1{1/4} }}', font_size=60)
        eq8.shift(eq7[0][0].get_center()-eq8[0][0].get_center())
        eq8[1][2:].move_to(eq7[1][2:], coor_mask=RIGHT)
        self.play(FadeOut(eq7[1][2:]),
                  ReplacementTransform(eq5[2][:].copy(), eq8[1][2:]),
                  run_time=2)
        self.wait(1)

        eq9 = MathTex(r'\approx{{4}}', font_size=60)
        eq9.shift(eq7[0][0].get_center()-eq9[0][0].get_center())
        eq9[1].move_to(eq7[1][1], coor_mask=RIGHT)
        self.play(FadeOut(eq7[1][:2], eq8[1][2:4]),
                  ReplacementTransform(eq8[1][4], eq9[1][0]),
                  run_time=2)
        self.wait(1)

        eq10 = MathTex(r'{{\mathbb E[N_{HH}]}}\approx{{5}}\ ?', font_size=60)
        eq10.shift(eq7[0][0].get_center()-eq10[1][0].get_center())
        self.play(FadeOut(eq6[3], target_position=eq10[2]),
                  FadeOut(eq9[1], target_position=eq10[2]),
                  FadeIn(eq10[2]),
                  ReplacementTransform(eq7[0], eq10[1]),
                  ReplacementTransform(eq6[0], eq10[0]),
                  run_time=1)
        self.wait(1)
        self.play(FadeIn(eq10[3]), run_time=0.5)

        eq11 = MathTex(r'{{\mathbb E[N_{HT}]}}\approx{{5}}\ ?', font_size=60).next_to(eq10, DOWN).align_to(eq10, LEFT)
        self.play(FadeIn(eq11), run_time=1)
        self.wait(1)

        box = SurroundingRectangle(VGroup(eqns[0][0][-1], eqns[1][0][-1]), color=RED, corner_radius=0.27, stroke_width=6)
        box.move_to(eqns[0][0][-2:], coor_mask=RIGHT)
        box.height *= 1.3
        box.width *= 0.8
        box.rotate(-0.5)
        self.play(FadeIn(box), run_time=0.5)
        for i in range(1, n-1):
            self.wait(1)
            self.play(box.animate.move_to((eqns[i][0][-2:].get_center()+eqns[i+1][0][-2:].get_center())/2), run_time=0.4)
        self.wait(1)
        self.play(FadeOut(box), run_time=0.5)

        self.wait(1)

        eq12 = MathTex(r'\mathbb P(P_n=P_{n+1}=HT) = 0 {{ < \mathbb P(HT)^2}}', font_size=60) \
                    .next_to(eq11, DOWN).next_to(eqns[0], RIGHT, coor_mask=RIGHT, buff=1)
        self.play(FadeIn(eq12[0]), run_time=0.5)
        self.wait(1)
        self.play(FadeIn(eq12[1]), run_time=0.5)
        self.wait(1)

        eq13 = MathTex(r'\mathbb P(P_n=P_{n+1}=HH){{=}}\mathbb P(HHH)^3', font_size=60)\
            .next_to(eq12, DOWN).align_to(eq12, LEFT)
        self.play(FadeIn(eq13[0:2], eq13[2][:-1]), run_time=0.5)
        self.wait(1)

        eq14 = MathTex(r'{{=}}\mathbb P(H)^3', font_size=60)
        eq14.shift(eq13[1].get_center()-eq14[0].get_center())
        self.play(ReplacementTransform(eq13[2][:3], eq14[1][:3]),
                  ReplacementTransform(eq13[2][3], eq14[1][2]),
                  ReplacementTransform(eq13[2][4], eq14[1][2]),
                  ReplacementTransform(eq13[2][5], eq14[1][3]),
                  FadeIn(eq14[1][4], target_mobject=eq13[2][-1]),
                  run_time=1)
        self.wait(1)

        eq15 = MathTex(r'{{=}}(1/2)^3', font_size=60)
        eq15.shift(eq13[1].get_center()-eq15[0].get_center())
        self.play(ReplacementTransform(eq14[1][1], eq15[1][0]),
                  ReplacementTransform(eq14[1][3:], eq15[1][4:]),
                  FadeOut(eq14[1][2], eq14[1][0]),
                  FadeIn(eq15[1][1:4]),
                  run_time=1
                  )
        self.wait(1)

        eq16 = MathTex(r'{{=}}1/8 {{ > \mathbb P(HH)^2 }}', font_size=60)
        eq16.shift(eq13[1].get_center()-eq16[0].get_center())
        self.play(ReplacementTransform(eq15[1][1:3], eq16[1][0:2]),
                  FadeOut(eq15[1][0], eq15[1][4:]),
                  FadeOut(eq15[1][3], target_mobject=eq16[1][2]),
                  FadeIn(eq16[1][2]),
                  run_time=1)
        self.wait(1)
        self.play(FadeIn(eq16[2]), run_time=0.5)
        self.wait(1)

if __name__ == "__main__":
#    MartingaleH().construct()
    print(SequenceH.sequences(10))