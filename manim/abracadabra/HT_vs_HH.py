from manim import *
import numpy as np
import random


# Global variable with H coin and T coin used throughout
H = LabeledDot(Tex("H", color=BLACK), radius=0.35, color=BLUE).scale(1.5)
T = LabeledDot(Tex("T", color=BLACK), radius=0.35, color=YELLOW).scale(1.5)
empty_coin = LabeledDot(Tex("$T$", color=BLACK), radius=0.35, color=BLACK).scale(1.5)


def set_target_location(A, B):
    A.target.set_x(B.get_x())
    A.target.set_y(B.get_y())


def set_new_location(A, B):
    A.set_x(B.get_x())
    A.set_y(B.get_y())


def animate_flip(coin, final='H', n_flips=1, side_H=None, side_T=None, my_scale=1):
    # RETURNS a list of animations that animate the mobject "coin" being flipped
    # The "final" variable incidicates what you want it to be at the end of the flipping
    # To animate a coin, use a loop to play the animations:

    # for a in animate_flip(coins[i],coin_flips[i]):
    #            self.play(a,run_time=0.2)

    global H, T

    if side_H == None:
        side_H = H

    if side_T == None:
        side_T = T

    full_fc = [side_H.copy().move_to(coin.get_center()), side_T.copy().move_to(coin.get_center())]
    anim_list = []
    for i in range(2):
        coin.generate_target()
        coin.target.stretch(0.01, dim=1)
        # coin.target.color = BLACK
        anim_list.append(MoveToTarget(coin))

        coin.color = BLACK
        coin.generate_target()

        offset = 1 if final == 'H' else 0  # Ensures the coin lands on the side requested
        coin.target = full_fc[(i + offset) % 2]

        anim_list.append(MoveToTarget(coin))
    return anim_list * n_flips


"""
Thumbnail
"""


class thumbnail(Scene):
    def construct(self):

        coin_scale = 2

        # VGroup(Tex("takes \emph{longer} than"),Tex("(on average)")).arrange(DOWN)
        HH = VGroup(H.copy(), H.copy()).scale(coin_scale).arrange(RIGHT)
        HT = VGroup(H.copy(), T.copy()).scale(coin_scale).arrange(RIGHT)

        vs = VGroup(HT.copy(), Tex("vs").scale(4), HH.copy()).arrange(RIGHT)
        off_x = 0.5
        vs[0].shift(off_x * LEFT)
        vs[2].shift(off_x * RIGHT)

        text = Tex("Not the same?!").scale(3.5)

        vg = VGroup(vs, text).arrange(DOWN)

        off_y = 0.4
        vg[0].shift(off_y * UP)
        vg[1].shift(off_y * DOWN)

        thumbnail = True
        if thumbnail:
            self.add(vg)
            return 0

        HH_anim = [None for i in range(2)]
        for i in range(2):
            my_string = 'HH'
            HH_anim[i] = animate_flip(HH[i], final=my_string[i], n_flips=1, side_H=H.copy().scale(2),
                                      side_T=T.copy().scale(2))

        HT_anim = [None for i in range(2)]
        for i in range(2):
            my_string = 'HT'
            HT_anim[i] = animate_flip(HT[i], final=my_string[i], n_flips=1, side_H=H.copy().scale(2),
                                      side_T=T.copy().scale(2))

        # Initial coin flipping sequence
        for i in range(2):
            for a in HT_anim[i]:
                self.play(a, run_time=0.2)

        self.wait(2)


class teaser2(Scene):
    def construct(self):

        coin_scale = 2

        thumbnail = False

        # VGroup(Tex("takes \emph{longer} than"),Tex("(on average)")).arrange(DOWN)

        HH = VGroup(H.copy(), H.copy()).scale(coin_scale).arrange(RIGHT)
        HT = VGroup(H.copy(), T.copy()).scale(coin_scale).arrange(RIGHT)

        vs = VGroup(HT, Tex("vs").scale(4), HH).arrange(RIGHT)
        off_x = 0.5
        vs[0].shift(off_x * LEFT)
        vs[2].shift(off_x * RIGHT)

        text = Tex("Not the same?!").scale(3.5)

        vg = VGroup(vs, text).arrange(DOWN)

        off_y = 0.4
        vg[0].shift(off_y * UP)
        vg[1].shift(off_y * DOWN)

        if thumbnail:
            self.add(vg)
            return 0

        HH_anim = [animate_flip(HH[i], final='HH'[i], n_flips=1, side_H=H.copy().scale(2),
                                      side_T=T.copy().scale(2)) for i in range(2)]

        HT_anim = [ animate_flip(HT[i], final='HT'[i], n_flips=1, side_H=H.copy().scale(2),
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

        new_text = Tex("A Probability Puzzle").scale(2)

        set_new_location(new_text, text)
        self.play(Write(new_text), run_time=1)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in [HH, HT, vs[1], new_text]])

        # self.add(vg)


class teaser(Scene):
    def construct(self):

        nflip = 3
        colr = [BLUE, YELLOW]

        def create_coins(n):
            coins = VGroup()
            for i in range(n):
                my_H = LabeledDot(Tex('H', color=BLACK), radius=0.35, color=BLUE).scale(1.5)
                coins += my_H
            coins.arrange(RIGHT)
            return coins

        def create_coins_anim(coins_H, coins_T, coins):
            coins_anim = [None for i in range(len(coins))]
            for i in range(len(coins)):
                my_H = LabeledDot(Tex(coins_H[i], color=BLACK), radius=0.35, color=colr[i % 2]).scale(1.5)
                my_T = LabeledDot(Tex(coins_T[i], color=BLACK), radius=0.35, color=colr[(i + 1) % 2]).scale(1.5)
                coins_anim[i] = animate_flip(coins[i], final='T', n_flips=nflip, side_H=my_H, side_T=my_T)
            return coins_anim

        coins1 = create_coins(4)

        coins2 = create_coins(4)
        vg = VGroup(coins1, coins2).arrange(RIGHT)
        vg.shift(2 * UP)
        coins1.shift(0.5 * LEFT)
        coins2.shift(0.5 * RIGHT)
        cflip_time = 0.2

        coins1_anim = create_coins_anim('COIN', 'PROB', coins1)
        for i in range(2 * nflip):
            anim_list = [my_anim[i] for my_anim in coins1_anim]
            self.play(*anim_list, run_time=cflip_time)

        coins2_anim = create_coins_anim('FLIP', 'BLTY', coins2)
        for i in range(2 * nflip):
            anim_list = [my_anim[i] for my_anim in coins2_anim]
            self.play(*anim_list, run_time=cflip_time)

        coins3 = create_coins(6)
        coins3.next_to(coins1, DOWN)
        coins3.set_x(0)
        coins3_anim = create_coins_anim('CASINO', 'MAGIC!', coins3)
        for i in range(2 * nflip):
            anim_list = [my_anim[i] for my_anim in coins3_anim]
            self.play(*anim_list, run_time=cflip_time)

        text = Tex("Are two heads better than one?").scale(1.5)
        # text.next_to(coins2,2*DOWN)
        text.set_x(0)
        text.set_y(0)
        text.shift(DOWN)
        self.play(Write(text))


def random_coin_flip():
    v = random.randint(0,1)
    if v==0:
        return 'H'
    else:
        return 'T'

def random_coins_ends_in(target_seq):
    #target sequence must be length 2
    cflip = ''
    finished = False
    while not finished:
        cflip += random_coin_flip()
        i = len(cflip)-1
        finished = (i >= 1) and (cflip[i] == target_seq[1] and cflip[i-1] == target_seq[0])
    return cflip

def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

print(random_coins_ends_in('HT'))


my_HH_seq = ['HH', 'HTTTTHH', 'THH', 'HTTTHH', 'HTHH', 'HTTTTHH','HH', 'THTHH', 'THH', 'HTHTHTTHTTTHH', 'HH', 'THTHTHTTHTHH', 'HTHTHH', 'THH', 'TTHTTHTHTTHH', 'THTTTTHTHH', 'TTTTHH', 'HH', 'THH', 'TTHTTHH', 'THH', 'HTTTHH', 'HH', 'HTTHTHTHTTTTHTTTHTTHTHH', 'TTHTHH', 'HH', 'THTHH', 'HTHH', 'HH', 'THTTHTHH', 'TTHH', 'TTHH', 'TTHTHH', 'THTHH', 'HH', 'HTHH',  'TTHH',  'HTTHTTHTHTTHTHH', 'THH', 'TTHH', 'HH', 'TTTHTTTHH', 'TTHTTHH', 'HH', 'THTHTTHTTTHTHTTHTHTTTTHH', 'HH', 'TTHTTTTTTTHTHTHH', 'TTTTHTHH', 'HH', 'HTTHH', 'THH', 'TTHH', 'TTHH', 'HH', 'THH', 'THH', 'TTTHTHTHH', 'HTHH', 'THH', 'TTHH', 'HH', 'THH', 'THTHTTHTHTHH', 'THH', 'THTTHTHTTTHH', 'THTHTHH', 'TTHH', 'TTTTTTTTHH', 'HH',  'THTHTHTHH', 'HTTTTHH', 'TTTHTHH', 'HTTHTHTTTTTTHTHH', 'THTTHTHTHTHTTTTTHH', 'TTHH', 'HTHH', 'HTHH', 'HTHH', 'HH', 'HTTHH', 'THH', 'HH', 'THH', 'THH', 'HTTHTTHH', 'THH', 'THH', 'HH', 'HTTTTHH', 'THTHTTHH', 'TTTHTHTTHH', 'THTTHH', 'TTTHH', 'THTHH', 'TTTHTHTTHH', 'TTHTTHTHH', 'TTTHH', 'HTTTTTHTTHTHTHTHH', 'TTHTHH', 'TTHTTTHTTTHH']
my_HT_seq = ['TTHT', 'HT', 'THT', 'HHHHT', 'TTHHHHT', 'THHT', 'HT',  'THT', 'TTHT', 'HHHHT', 'THT', 'TTTTHHHT','HT', 'HHT', 'TTHHHT', 'HT', 'TTTHT', 'TTTHT','HT', 'THT', 'THHHT', 'HT', 'TTTHT', 'HHHT', 'HT', 'HHT', 'THT', 'HT', 'HHT', 'THT', 'HT', 'THT', 'HT', 'TTTHHHHHT', 'HT', 'TTTTTTHT', 'TTHT', 'HHT', 'TTTHHHT', 'TTTHHHHHT', 'HT', 'TTTTHT', 'THT', 'HT', 'THT',  'HT', 'THT', 'HHHHT', 'TTHHHT', 'THHHHT','TTHT', 'TTHHT', 'HT', 'TTTHHHT', 'HHT', 'TTTHHHT', 'HT', 'THT', 'THT', 'THHHHT', 'TTHHT', 'HT', 'TTTTHHT', 'TTHT', 'HHT', 'HT', 'TTHHHT', 'TTHT', 'HHHHT', 'TTTHHT', 'TTTHHHHT', 'HT', 'THHT', 'HT', 'TTTHHT', 'HHT', 'THT', 'HHT', 'TTHHT', 'HT', 'THHHT', 'TTTHT', 'TTHT', 'THHHT', 'HHT', 'THT', 'HT', 'TTHT', 'HHHT', 'HT',  'THT', 'HT', 'HT', 'TTHT', 'TTHT', 'HT', 'TTTHHT', 'TTHT', 'THHHHHHHHHHT', 'THT', 'HT', 'TTTTTTHT', 'THHHHT', 'HT', 'THT', 'HT', 'THT', 'HT', 'TTTTHHT', 'HHHHT', 'HHT', 'TTHT', 'HT', 'HT', 'TTTHT', 'TTHHT', 'THHHHHT', 'HT', 'TTHHHHT', 'HT', 'HHHHT', 'TTHT', 'THT', 'TTHT', 'THHT', 'TTTTTTHT', 'HHHT', 'TTTTTHT', 'TTTHT', 'HHT', 'HHT', 'TTHHT', 'THT', 'HHT', 'THT', 'HHT', 'THHHHT', 'HT', 'TTTHT', 'HHT', 'HT', 'TTTTTTTHHHHHHT', 'TTHT', 'TTTTTTHT', 'THHHHHHHHT', 'HT', 'THHHT', 'HHT', 'THT', 'HT']
print(len(my_HH_seq))
print(len(my_HT_seq))


class intro(Scene):
    def construct(self):
        max_n = 9
        pause_len = 10
        long_pause_len = 25
        counts_HH = np.zeros(max_n)  # [0 for _ i n range(max_n)]
        counts_HT = np.zeros(max_n)  # [0 for _ i n range(max_n)]
        over_HH = 0
        over_HT = 0

        avg_HH = 0
        avg_HT = 0

        chart_width = 5.65
        chart_HH = BarChart(
            values=np.zeros(max_n),
            bar_names=[2, 3, 4, 5, 6, 7, 8, 9, '10+'],
            y_range=[0, 1, 0.25],
            bar_colors=[BLUE for _ in range(max_n)],
            y_length=1.5,
            x_length=chart_width,
            x_axis_config={"font_size": 36},
            y_axis_config={}
        )

        chart_HT = BarChart(
            values=np.zeros(max_n),
            bar_names=[2, 3, 4, 5, 6, 7, 8, 9, '10+'],
            y_range=[0, 1, 0.25],
            bar_colors=[YELLOW for _ in range(max_n)],
            y_length=1.5,
            x_length=chart_width,
            x_axis_config={"font_size": 36},
            y_axis_config={}
        )

        chart_HT.to_edge(RIGHT)
        chart_HH.to_edge(LEFT)

        t_s = 1.2
        c_s = 0.5
        n_s = 1.2
        # Tex("Flips to").scale(t_s),
        title_HT = VGroup(H.copy().scale(c_s), T.copy().scale(c_s), Tex(r": Avg $\approx$").scale(t_s),
                          Tex("0.00").scale(n_s)).arrange(RIGHT)
        title_HH = VGroup(H.copy().scale(c_s), H.copy().scale(c_s), Tex(r": Avg $\approx$").scale(t_s),
                          Tex("0.00").scale(n_s)).arrange(RIGHT)
        title_HT.next_to(chart_HT, 0.5 * UP)
        title_HH.next_to(chart_HH, 0.5 * UP)

        title_HH.set_x(chart_HH.get_x())
        title_HT.set_x(chart_HT.get_x())

        off_x = 0.5
        title_HH.shift(off_x * RIGHT)
        title_HT.shift(off_x * RIGHT)

        N_flips = VGroup(Tex("Trial"), Tex(r"$\#99$")).arrange(DOWN)
        N_flips.to_corner(DR)
        N_flips.shift(0.5 * UP)

        # self.add(title_HT,title_HH)
        # self.add(chart_HT)
        # self.add(chart_HH)
        # self.add(N_flips)
        # return 0

        n_trials = 100

        make_random_coins = False

        if make_random_coins:
            HH_finished = False
            while not HH_finished:
                finished = False
                while not finished:
                    coin_flip_seq_HH = [random_coins_ends_in('HH') for i in range(5)]
                    finished = not checkIfDuplicates([len(c) for c in coin_flip_seq_HH])
                coin_flip_seq_HH.extend([random_coins_ends_in('HH') for i in range(n_trials - 5)])

                HH_avg = sum(map(len, coin_flip_seq_HH)) / len(coin_flip_seq_HH)
                HH_finished = abs(HH_avg - 6.0) < 0.25

            HT_finished = False
            while not HT_finished:
                finished = False
                while not finished:
                    coin_flip_seq_HT = [random_coins_ends_in('HT') for i in range(5)]
                    finished = not checkIfDuplicates([len(c) for c in coin_flip_seq_HT])
                coin_flip_seq_HT.extend([random_coins_ends_in('HT') for i in range(n_trials - 5)])

                HT_avg = sum(map(len, coin_flip_seq_HT)) / len(coin_flip_seq_HT)
                HT_finished = abs(HT_avg - 4.0) < 0.25
        else:
            coin_flip_seq_HH = my_HH_seq
            coin_flip_seq_HT = my_HT_seq

        # coin_flip_seq_HH = ['THTHH','HTHH','TTTTHH','THH','HH']
        # coin_flip_seq_HT = ['HT','TTH','THHHT','THHT','TTTTTHT']

        print(coin_flip_seq_HH)
        print(coin_flip_seq_HT)

        flip_time = 0.2

        for i_flip, (coin_flips_HH, coin_flips_HT) in enumerate(zip(coin_flip_seq_HH, coin_flip_seq_HT)):
#            if i_flip >= 1:
#                return 0

            if i_flip == 4:
                # Rescale the bar charts after 5 flips

                chart_bak_HH = BarChart(
                    values=counts_HH / (np.sum(counts_HH) + over_HH),
                    bar_names=[2, 3, 4, 5, 6, 7, 8, 9, '10+'],  # range(2,max_n+2),
                    y_range=[0, 0.34, 0.25],
                    bar_colors=[BLUE for _ in range(max_n)],
                    y_length=1.5,
                    x_length=chart_width,
                    x_axis_config={"font_size": 36},
                    y_axis_config={}
                )

                chart_bak_HT = BarChart(
                    values=counts_HT / (np.sum(counts_HT) + over_HT),
                    bar_names=[2, 3, 4, 5, 6, 7, 8, 9, '10+'],
                    y_range=[0, 0.34, 0.25],
                    bar_colors=[YELLOW for _ in range(max_n)],
                    y_length=1.5,
                    x_length=chart_width,
                    x_axis_config={"font_size": 36},
                    y_axis_config={}
                )

                set_new_location(chart_bak_HH, chart_HH)
                set_new_location(chart_bak_HT, chart_HT)
                self.play(ReplacementTransform(chart_HT, chart_bak_HT), ReplacementTransform(chart_HH, chart_bak_HH))
                chart_HH = chart_bak_HH
                chart_HT = chart_bak_HT

            n = max(len(coin_flips_HH), len(coin_flips_HT))
            c_scale = 1
            coins_HH = VGroup(
                *[H.copy().scale(c_scale) if c == 'H' else T.copy().scale(c_scale) for c in coin_flips_HH]).arrange(
                RIGHT)
            coins_HT = VGroup(
                *[H.copy().scale(c_scale) if c == 'H' else T.copy().scale(c_scale) for c in coin_flips_HT]).arrange(
                RIGHT)

            # coins.next_to(step2,4*DOWN) #shift(UP*0.5)
            coins_HH.to_corner(UL)
            coins_HT.to_corner(DL)

            # coins_HT.shift(0.5*DOWN)
            # coins_HH.shift(DOWN)

            # coins.set_y(0)
            # flip_anim_cutoff = 4

            if i_flip < 4:
                coin_flip_animations_HH = [None for i in range(n)]
                coin_flip_animations_HT = [None for i in range(n)]

                for i in range(len(coin_flips_HH)):
                    coin_flip_animations_HH[i] = animate_flip(coins_HH[i], coin_flips_HH[i])

                for i in range(len(coin_flips_HT)):
                    coin_flip_animations_HT[i] = animate_flip(coins_HT[i], coin_flips_HT[i])

                if i_flip == 0:

                    for i in range(len(coin_flips_HH)):
                        for a_HH in coin_flip_animations_HH[i]:
                            self.play(a_HH, run_time=flip_time)
                            # pass
                    for i in range(len(coin_flips_HT)):
                        for a_HT in coin_flip_animations_HT[i]:
                            self.play(a_HT, run_time=flip_time)
                            # pass

                if i_flip > 0:
                    for i in range(min(len(coin_flips_HH), len(coin_flips_HT))):
                        for a_HH, a_HT in zip(coin_flip_animations_HH[i], coin_flip_animations_HT[i]):
                            self.play(a_HH, a_HT, run_time=flip_time)
                            # pass

                    if len(coin_flips_HH) > len(coin_flips_HT):
                        for i in range(len(coin_flips_HT), len(coin_flips_HH)):
                            for a_HH in coin_flip_animations_HH[i]:
                                self.play(a_HH, run_time=flip_time)
                                # pass
                    elif len(coin_flips_HT) > len(coin_flips_HH):
                        for i in range(len(coin_flips_HH), len(coin_flips_HT)):
                            for a_HT in coin_flip_animations_HT[i]:
                                self.play(a_HT, run_time=flip_time)
                                # pass

            box_HH = SurroundingRectangle(VGroup(coins_HH[-2], coins_HH[-1]), color=BLUE, buff=SMALL_BUFF)
            box_HT = SurroundingRectangle(VGroup(coins_HT[-2], coins_HT[-1]), color=YELLOW, buff=SMALL_BUFF)

            N_HT = Tex(f"$N_{{HT}}={len(coin_flips_HT)}$", color=YELLOW)
            N_HT.next_to(box_HT, UP)

            N_HH = Tex(f"$N_{{HH}}={len(coin_flips_HH)}$", color=BLUE)
            N_HH.next_to(box_HH, DOWN)

            if len(coin_flips_HH) - 2 < max_n:
                counts_HH[len(coin_flips_HH) - 2] += 1
            else:
                counts_HH[-1] += 1

            if len(coin_flips_HT) - 2 < max_n:
                counts_HT[len(coin_flips_HT) - 2] += 1
            else:
                counts_HT[-1] += 1

            avg_HT += (len(coin_flips_HT) - avg_HT) / (i_flip + 1)
            avg_HH += (len(coin_flips_HH) - avg_HH) / (i_flip + 1)

            title_HT[-1].target = Tex(f"{avg_HT:.2f}", color=YELLOW).scale(n_s)
            title_HH[-1].target = Tex(f"{avg_HH:.2f}", color=BLUE).scale(n_s)
            set_target_location(title_HT[-1], title_HT[-1])
            set_target_location(title_HH[-1], title_HH[-1])

            N_flips[1].target = Tex(f"$\#{i_flip + 1}$")
            set_target_location(N_flips[1], N_flips[1])

            chart_bak_HH = chart_HH.copy()
            chart_bak_HH.change_bar_values(counts_HH / (np.sum(counts_HH) + over_HH))
            chart_bak_HT = chart_HT.copy()
            chart_bak_HT.change_bar_values(counts_HT / (np.sum(counts_HT) + over_HT))

            if i_flip > 0 and i_flip < 4:
                flip_time = (4 - i_flip) / 4 * 0.1
                move_to_target_list = [title_HT[-1], title_HH[-1], N_flips[1]]
                self.play(Write(box_HH), Write(N_HH), Write(box_HT), Write(N_HT),
                          *[MoveToTarget(mob) for mob in move_to_target_list],
                          ReplacementTransform(chart_HT, chart_bak_HT), ReplacementTransform(chart_HH, chart_bak_HH))
                chart_HH = chart_bak_HH
                chart_HT = chart_bak_HT
                self.play(FadeOut(box_HH), FadeOut(N_HH), FadeOut(box_HT), FadeOut(N_HT), FadeOut(coins_HH),
                          FadeOut(coins_HT))

            # elif i_flip > 4:
            #    flip_time = 0.02
            #    self.play(FadeOut(coins_HH),FadeOut(coins_HT),MoveToTarget(title_HT[-1]),MoveToTarget(title_HH[-1]),ReplacementTransform(chart_HT,chart_bak_HT),ReplacementTransform(chart_HH,chart_bak_HH))
            #    chart_HH = chart_bak_HH
            #    chart_HT = chart_bak_HT

            elif i_flip >= 4:
                flip_time = 0.02

                if i_flip < 50:
                    r_time = 0.25 + 0.1 * (50 - i_flip) / 50
                else:
                    r_time = 0.25

                fade_mob_list = [coins_HH, coins_HT, box_HT, box_HH, N_HT, N_HH]
                move_to_target_list = [title_HT[-1], title_HH[-1], N_flips[1]]

                self.play(*[FadeIn(mob, run_time=r_time) for mob in fade_mob_list])
                self.play(*[FadeOut(mob, run_time=r_time) for mob in fade_mob_list],
                          *[MoveToTarget(mob, run_time=r_time) for mob in move_to_target_list],
                          ReplacementTransform(chart_HT, chart_bak_HT, run_time=r_time),
                          ReplacementTransform(chart_HH, chart_bak_HH, run_time=r_time))
                chart_HH = chart_bak_HH
                chart_HT = chart_bak_HT



            elif i_flip == 0:

                coin_scale = 1
                q_scale = 1
                flip_time = 0.1

                self.play(Write(box_HH), Write(N_HH))

                self.wait(1)
                self.play(Write(box_HT), Write(N_HT))
                self.wait(pause_len)

#                return 0

                HH = VGroup(H.copy(), H.copy()).scale(coin_scale).arrange(RIGHT)
                HT = VGroup(H.copy(), T.copy()).scale(coin_scale).arrange(RIGHT)

                Q1 = VGroup(Tex("\emph{Q}:"), HH.copy(), Tex(" vs. ").scale(1.2), HT.copy(), Tex("?")).scale(
                    q_scale).arrange(RIGHT)

                self.play(Write(Q1))
                self.wait(pause_len)

                chart_HH = chart_bak_HH
                chart_HT = chart_bak_HT
                title_HH[-1] = title_HH[-1].target
                title_HT[-1] = title_HT[-1].target
                N_flips[1] = N_flips[1].target

                self.play(FadeOut(Q1), FadeIn(chart_HT), FadeIn(chart_HH), FadeIn(title_HT), FadeIn(title_HH),
                          FadeIn(N_flips))
                self.play(FadeOut(coins_HH), FadeOut(box_HH), FadeOut(N_HH), FadeOut(coins_HT), FadeOut(box_HT),
                          FadeOut(N_HT))

        self.wait(long_pause_len)
        defn = Tex(r"$\mathbb{E}[N_{\text{target}}]$ := \text{Average number of coinflips until target}")
        defn.to_corner(UL)
        defn.set_x(0)

        # VGroup(Tex("takes \emph{longer} than"),Tex("(on average)")).arrange(DOWN)
        HH = VGroup(H.copy(), H.copy()).scale(coin_scale).arrange(RIGHT)
        HT = VGroup(H.copy(), T.copy()).scale(coin_scale).arrange(RIGHT)

        Q1 = VGroup(Tex("\emph{Q}:"), HH.copy(), Tex(" vs. ").scale(1.2), HT.copy(), Tex("?")).scale(q_scale).arrange(
            RIGHT)
        Q1.next_to(defn, 2 * DOWN)
        Q1.set_x(0)
        off_y = 2
        chart_HT.generate_target()
        chart_HH.generate_target()
        chart_HT.target.shift(off_y * DOWN)
        chart_HH.target.shift(off_y * DOWN)

        title_HT.generate_target()
        title_HT.target.shift(off_y * DOWN)

        title_HH.generate_target()
        title_HH.target.shift(off_y * DOWN)

        title_HT[-1].generate_target()
        title_HT[-1].target.shift(off_y * DOWN)

        title_HH[-1].generate_target()
        title_HH[-1].target.shift(off_y * DOWN)

        a_list = [MoveToTarget(mob) for mob in [chart_HT, chart_HH, title_HT, title_HH, title_HH[-1], title_HT[-1]]]
        self.play(Write(Q1), *a_list, FadeOut(N_flips))
        self.wait(pause_len)

        # boxHH_text = Tex("Lose",color=RED)
        boxHH = SurroundingRectangle(Q1[1], color=RED, buff=SMALL_BUFF)
        HH_text = VGroup(Tex("Takes 6 flips", substrings_to_isolate="6"), Tex("on average")).scale(1.2).arrange(DOWN)
        HH_text[0].set_color_by_tex("6", RED)
        HH_text.next_to(boxHH, DOWN)
        # boxHH_text.next_to(boxHH,UP)

        # boxHT_text = Tex("Win",color=GREEN)
        boxHT = SurroundingRectangle(Q1[3], color=GREEN, buff=SMALL_BUFF)
        HT_text = VGroup(Tex("Takes 4 flips", substrings_to_isolate="4"), Tex("on average")).scale(1.2).arrange(DOWN)
        HT_text[0].set_color_by_tex("4", GREEN)
        HT_text.next_to(boxHT, DOWN)
        # boxHT_text.next_to(boxHT,UP)

        boxHH_text = Tex("Slow", color=RED)
        boxHT_text = Tex("Fast", color=GREEN)
        boxHH_text.next_to(boxHH, UP)
        boxHT_text.next_to(boxHT, UP)

        Q1[0].target = Tex("\emph{A}:")
        set_target_location(Q1[0], Q1[0])
        # Q1[2].target = Tex("$>$").scale(1.2)
        # set_target_location(Q1[2],Q1[2])
        Q1[4].target = Tex("!")
        set_target_location(Q1[4], Q1[4])

        # MoveToTarget(Q1[2])
        #
        self.play(MoveToTarget(Q1[0]), MoveToTarget(Q1[4]), Write(boxHH), Write(boxHT), Write(boxHH_text),
                  Write(boxHT_text))
        self.wait(long_pause_len)

        # FadeOut(plots),
        self.play(Write(HH_text), Write(HT_text))
        self.wait(pause_len)

        fade_out_list = [chart_HT, chart_HH, title_HT, title_HH, title_HH[-1], title_HT[-1], boxHT_text, boxHH_text]
        self.play(Write(defn), *[FadeOut(mob) for mob in fade_out_list])
        self.wait(pause_len)