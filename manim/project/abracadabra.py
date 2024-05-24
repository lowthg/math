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
        self.play(ReplacementTransform(eq6[0], eq7[0]),
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

        explicit_calc = False
        alt_calc = True
        initial_anim = False

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


            class label_ctr(Text):
                def __init__(self, text, font_size):
                    Text.__init__(self, text, font_size=font_size, color=RED)
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
            #eq8.align_to(txt2, LEFT).shift(RIGHT)

            self.play(ReplacementTransform(eq7[0], eq8[0]),
                      ReplacementTransform(eq7[2], eq8[1]),
                      ReplacementTransform(eq7[3][0], eq8[2][0]),
                      ReplacementTransform(eq7[1][0], eq8[2][2]),
                      FadeIn(eq8[2][1]),
                      run_time=2)


            self.wait(1)


            return

            txt4 = MathTex(r'{{=}}& {{1}}{{\,\mathbb P(X_1={\rm H})}}\\'
                           r'&+{{(1+\mathbb E[N_H])}}\,\mathbb P(X_1={\rm T})',
                           font_size=font_size)
            txt4.shift(txt3[1].get_center() - txt4[0].get_center())
            txt4_1 = txt4[2].copy()
            txt4_2 = txt4[5].copy()
            txt4_1.shift((txt3[3].get_center() - txt4_1.get_center()) * np.array([1, 0, 0]))
            txt4_2.shift((txt3[6].get_center() - txt4_2.get_center()) * np.array([1, 0, 0]))
            self.wait(0.5)
            self.play(FadeOut(txt3[3]), FadeIn(txt4_1), FadeOut(txt3[6]), FadeIn(txt4[5]), run_time=2)
            self.wait(0.5)



