"""
Animations for ABRACADABRA! The magic of martingale theory
"""

from manim import *
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
        coins = VGroup(*[VGroup(*[get_coin(face) for face in row]).arrange(RIGHT) for row in sequences]).arrange(DOWN).to_edge(UL)
        for row in coins:
            row.to_edge(LEFT)
            for coin in row:
                animate_flip(self, coin)
            nh = MathTex('N_H={}'.format(len(row)), font_size=60).next_to(coins, RIGHT).set_y(row.get_y())
            self.add(nh)
            self.wait(1)

        self.wait(1)

#SequenceH().construct()

class Teaser2(Scene):
    def construct(self):

        Row = 'TTHHHT'

        RowCoins = [get_coin(face) for face in Row]

        RowImg = VGroup(*RowCoins).arrange(RIGHT)

        for coin in RowImg:
            animate_flip(self, coin)

        self.wait(0.5)

        return

        coin_scale = 2

        # VGroup(Tex("takes \emph{longer} than"),Tex("(on average)")).arrange(DOWN)

        HH = VGroup(H.copy(), H.copy()).scale(coin_scale).arrange(RIGHT)
        HT = VGroup(H.copy(), T.copy()).scale(coin_scale).arrange(RIGHT)

        vs = VGroup(HT, Tex("vs").scale(4), HH).arrange(RIGHT)
        off_x = 0.5
        vs[0].shift(off_x * LEFT)
        vs[2].shift(off_x * RIGHT)

        text = Tex("A Probability Puzzle").scale(2)

        vg = VGroup(vs, text).arrange(DOWN)

        off_y = 0.4
        vg[0].shift(off_y * UP)
        vg[1].shift(off_y * DOWN)


        HH_anim = [animate_flip(HH[i], final='HH'[i], side_H=H.copy().scale(2),
                                      side_T=T.copy().scale(2)) for i in range(2)]

        HT_anim = [ animate_flip(HT[i], final='HT'[i], side_H=H.copy().scale(2),
                                      side_T=T.copy().scale(2)) for i in range(2)]

        # Initial coin flipping sequence
        for i in range(2):
            for a in HT_anim[i]:
                self.play(a, run_time=0.2)

        self.play(Write(vs[1]), run_time=0.5)

        for i in range(2):
            for a in HH_anim[i]:
                self.play(a, run_time=0.2)

        # self.play(FadeOut(vs))
        # self.wait(2)

        self.play(Write(text), run_time=1)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in [HH, HT, vs[1], text]])
