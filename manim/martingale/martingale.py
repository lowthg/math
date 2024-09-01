from manim import *
import numpy as np
import math
import random
import csv
import datetime
import sys
sys.path.append('../project/')
# noinspection PyUnresolvedReferences
import abracadabra as abra


class ElectionOdds(Scene):
    def construct(self):
        dates = []
        days = []
        vals = []
        inames = [1, 2, 16]
        jnames = [0, 1, 2]
        colours = [BLUE, RED, BLUE_B]
        with open('2024ElectionOdds.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            cols = None
            for row in reader:
                if cols is None:
                    cols = row
                    names = [row[i] for i in inames]
                    print(names)
                    print(row)
                else:
                    elts = row[0].split('/')
                    date = datetime.date(int(elts[2]), int(elts[1]), int(elts[0]))
                    dates.append(date)
                    days.append((date - dates[0]).days)
                    vals.append([1/float(row[i]) for i in inames])
                    pass

            ax = Axes(x_range=[0, days[-1]], y_range=[0, 1.2], z_index=2,
                      axis_config={'color': WHITE, 'stroke_width': 5, 'include_ticks': False, 'tick_size': 0.05},
                      )
            line1 = Line(ax.coords_to_point(0, 1), ax.coords_to_point(days[-1], 1), stroke_width=5, stroke_color=GREY, z_index=0)

            txt_year = Tex('2024', font_size=30).move_to(ax.coords_to_point((datetime.date(2024, 1, 1) - dates[0]).days, -0.14))

            months=[]
            ticks = []
            for (year, imonth, month) in [(2023, 12, 'December'), (2024, 1, 'January'), (2024, 2, 'February'),
                                          (2024, 3, 'March'), (2024, 4, 'April'), (2024, 5, 'May'),
                                          (2024, 6, 'June'), (2024, 7, 'July'), (2024, 8, 'August')]:
                tex = Tex(month, font_size=25)
                x = (datetime.date(year, imonth, 1) - dates[0]).days
                pos = ax.coords_to_point(x, -0.13)
                tex.move_to(pos, coor_mask=RIGHT)
                tex.next_to(pos, UP, submobject_to_align=tex[0][0], coor_mask=UP)
                months.append(tex)
                ticks.append(ax.x_axis.get_tick(x).next_to(ax.coords_to_point(0, 0), DOWN, buff=0, coor_mask=UP))

            txt_0 = Tex(r'0\%', font_size=30).next_to(ax.coords_to_point(0, 0), LEFT, buff=0.1)
            txt_100 = Tex(r'100\%', font_size=30).next_to(ax.coords_to_point(0, 1), LEFT, buff=0.2)

            legend = []
            for j, k in [(0, 0), (1, 1), (2, 2)]:
                tex = Tex(names[j].split(' ')[-1], font_size=40, color=colours[j])
                pos = ax.coords_to_point(15, 0.9 - k * 0.12)
                tex.next_to(pos, RIGHT, submobject_to_align=tex[0][0], buff=0.1)
                legend.append(tex)
                legend.append(Line(pos + LEFT * 0.5, pos, stroke_width=5, stroke_color=colours[j]))

            self.add(ax, line1, txt_year, *months, txt_0, txt_100, *legend, *ticks)

            for i in range(len(days)):
                points = [ax.coords_to_point(days[i], vals[i][j]) for j in jnames]
                if i > 0:
                    lines = []
                    for j in jnames:
                        lines.append(Line(oldpoints[j], points[j], stroke_color=colours[j], stroke_width=5, z_index=0))
                        lines.append(Dot(oldpoints[j], color=colours[j], radius=0.025, z_index=0))
                    creates = [Create(line, rate_func=linear) for line in lines]
                    self.play(*creates, run_time=2.1/30)

                oldpoints = points


class OneHead(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = WHITE
        Scene.__init__(self, *args, *kwargs)

    seq = 'TTTH'

    def construct(self):
        Tex.set_default(font_size=50)
        r = Rectangle(width=1, height=0.9, stroke_opacity=0, z_index=0, fill_opacity=1,
                      fill_color=BLACK)
        r0 = Rectangle(width=1.5, height=0.9, stroke_opacity=0, z_index=0, fill_opacity=1,
                      fill_color=BLACK)
        r1 = Rectangle(width=1.5, height=0.9, stroke_opacity=0, z_index=0, fill_opacity=1,
                      fill_color=BLACK)
        n = len(self.seq)
        t = MobjectTable([[r0.copy()] + [r.copy() for _ in range(n)] + [r1.copy()] for _ in range(2)],
#                         row_labels=[Tex('Stake'), Tex('Won')],
                          include_outer_lines=True,
                          v_buff=0, h_buff=0).to_edge(DOWN, buff=0.25)
        stake = Tex('Stake', z_index=1, color=GREEN).move_to(t[0][0])
        won = Tex('Won', z_index=1, color=RED).move_to(t[0][n+2])

        self.add(t, stake, won)
        t_elts = [t, stake, won]

        dy = t[0][0].get_center() - t[0][n+2].get_center()

        for i in range(n):
            pos = t[0][i+1].get_center() + dy * 1.2
            self.wait(0.2)
            eq1 = MathTex(r'\$1', z_index=1).move_to(t[0][i+1])
            self.play(FadeIn(eq1), run_time=0.25)
            t_elts.append(eq1)
            coin = abra.get_coin(self.seq[i]).scale(0.8).move_to(pos)
            self.wait(0.2)
            abra.animate_flip(self, coin)
            txt = r'\$0' if self.seq[i] == 'T' else r'\$2'
            eq2 = MathTex(txt, z_index=1).move_to(t[0][n+3+i])
            self.wait(0.2)
            t_elts.append(eq2)
            self.play(FadeIn(eq2), run_time=0.25)

        self.wait(0.2)

        total = Tex(r'Total').move_to(t[0][n+1].get_center() + dy)
        t_elts.append(total)
        self.play(FadeIn(total), run_time=0.3)
        self.wait(0.2)
        stake_t = MathTex(r'\$N').move_to(t[0][n+1])
        t_elts.append(stake_t)
        self.play(FadeIn(stake_t), run_time=0.3)
        self.wait(0.2)
        won_t = MathTex(r'\$2').move_to(t[0][2*n+3])
        t_elts.append(won_t)
        self.play(FadeIn(won_t), run_time=0.3)
        self.wait(0.2)

        eq3 = MathTex(r'2-N', stroke_width=1.5).next_to(t, RIGHT, buff=1)
        self.play(ReplacementTransform(won_t[0][1].copy(), eq3[0][0]), run_time=2)
        self.wait(0.2)
        self.play(ReplacementTransform(stake_t[0][1].copy(), eq3[0][2]),
                  FadeIn(eq3[0][1], target_position=stake_t[0][0]),
                         run_time=2)

        self.wait(1)
        self.play(FadeOut(*t_elts), run_time=0.5)
        eq4 = MathTex(r'\mathbb E[2-N]=0', stroke_width=1.5)[0].move_to(t)
        self.play(ReplacementTransform(eq3[0][:], eq4[2:5]), run_time=2)
        self.wait(0.2)
        self.play(FadeIn(eq4[:2] + eq4[5:]), run_time=2)
        self.wait(0.2)
        eq5 = MathTex(r'\mathbb E[N]=2', stroke_width=1.5)[0].move_to(t)
        eq5.next_to(eq4[-2], ORIGIN, submobject_to_align=eq5[-2], coor_mask=UP)
        self.play(ReplacementTransform(eq4[:2] + eq4[2] + eq4[4:7], eq5[:2] + eq5[5] + eq5[2:5]),
                  FadeOut(eq4[3], target_position=eq5[0]),
                  FadeOut(eq4[-1], target_position=eq5[-1]),
                  run_time=3)
        self.wait(0.2)


class CoinSeq(Scene):
    seq = ['HTHTHH', 'TTHHT']

    def construct(self):
        n = len(self.seq)
        coins = [[abra.get_coin(seq[i]).scale(0.8) for i in range(len(seq))] for seq in self.seq]
        gp = VGroup(*[VGroup(*row).arrange(RIGHT) for row in coins]).arrange(DOWN, center=False, aligned_edge=LEFT)
        for c1 in coins:
            for c2 in c1:
                self.wait(0.1)
                abra.animate_flip(self, c2)
            rect = SurroundingRectangle(VGroup(*c1[-2:]), color=GREEN, fill_opacity=0, stroke_width=6, corner_radius=0.2, buff=0.067)
            self.play(FadeIn(rect), run_time=0.2)
        self.wait(0.1)


class MartingaleDef(Scene):
    skip = False
    graph_only = False

    def build_graph(self, skip=None):
        if skip is None:
            skip = self.skip

        nt = 10

        # construct axes
        ax = Axes(x_range=[0, nt], y_range=[-5, 5],
                  axis_config={'color': BLUE, 'stroke_width': 5, 'include_ticks': False},
                  )

        labels = ax.get_axis_labels(x_label=MathTex(r't'), y_label=MathTex(r'X_t'))

        ax.x_axis.generate_target()
        ax.x_axis.target.add_ticks()
        if not skip:
            self.play(LaggedStart(Write(ax), Write(ax.x_axis.target.submobjects[1], run_time=0.4), lag_ratio=0.5), run_time=3)
            self.add(ax.x_axis.target)
            self.remove(ax.x_axis)
        ax.x_axis = ax.x_axis.target
        if not skip:
            self.play(LaggedStart(Write(labels[0]), Write(labels[1]), lag_ratio=0.5), run_time=1)

        y_vals = [0.4, 2, -0.2, -0.5, -2, -1.6, -4, -1, 1, 0.5, 3.5]
        n = len(y_vals)
        points = [ax.coords_to_point(x, y_vals[x]) for x in range(11)]
        dot = Dot(points[0], fill_color=YELLOW, z_index=2)
        plot = VGroup(dot)
        x_labels = [MathTex(r'X_0').next_to(points[0], UL)]
        if not skip:
            self.play(FadeIn(dot, x_labels[0]), run_time=0.2)
        for x in range(1, n):
            dot = Dot(points[x], fill_color=YELLOW, z_index=2)
            line = Line(points[x-1], points[x], stroke_width=5)
            x_labels.append(MathTex(r'X_{{{}}}'.format(x)).next_to(points[x], UP))
            if not skip:
                self.play(FadeIn(dot, x_labels[x]), Create(line, rate_func=linear), run_time=0.5)
            plot.add(line, dot)

        # show process terms
        x_procstr = r'{{,}}'.join(['X_{{{}}}'.format(x) for x in range(n)] + [r'\ldots'])
        eq1 = MathTex(x_procstr).to_edge(DOWN)
        anim = [ReplacementTransform(x_labels[x][0].copy(), eq1[2*x]) for x in range(n)]
        if not skip:
            self.play(*anim, run_time=2)
            self.play(FadeIn(eq1[1::2], eq1[-1]), run_time=2)

        chart = VGroup(ax.x_axis, ax.y_axis, plot, *labels, *x_labels)
        chart.generate_target().scale(0.6).to_edge(UP, buff=0)
        self.wait(0.5)
        self.play(MoveToTarget(chart), eq1.animate.next_to(chart.target, DOWN), run_time=2)

        return chart, eq1, y_vals, ax

    def build_def(self, eq1, walk=False, skip=None):
        if skip is None:
            skip = self.skip
        eq2 = MathTex(r'\mathbb E[X_{n+1}\vert X_0,X_1,\ldots,X_n]=X_n')[0].next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex(r'\mathbb E[\lvert X_n\rvert] < \infty')[0] \
            .next_to(eq2, DOWN).align_to(eq2, LEFT)
        if not skip:
            self.wait(0.5)
            self.play(FadeIn(eq2), run_time=1)
            self.wait(0.5)
            self.play(FadeIn(eq3), run_time=1)
            self.wait(0.5)
        shift = LEFT.copy()
        if walk and not skip:
            shift+=eq2.get_left()*RIGHT
            self.play(eq3.animate.to_edge(LEFT, buff=0.1), eq2.animate.to_edge(LEFT, buff=0.1), run_time=2)
            pos = np.array([-0.68579769, -0.56742171, 0.])
            walkelt = self.walk(pos, skip=False)
            self.wait(0.5)
            shift -= eq2.get_left()*RIGHT
            self.play(FadeOut(*walkelt), run_time=1)
            self.play(VGroup(eq2, eq3).animate.shift(shift), run_time=2)
            shift *= 0
            self.wait(0.5)


        eq4 = MathTex(r'\mathcal F_n=\sigma(X_0,X_1,\ldots,X_n)')[0].next_to(eq3, DOWN).align_to(eq2, LEFT)
        if not skip:
            self.play(FadeIn(eq4), run_time=1)
            self.wait(0.5)

        eq5 = MathTex(r'\mathbb E[X_{n+1}\vert \mathcal F_n]=X_n')[0]
        eq5.next_to(eq2[-3], ORIGIN, submobject_to_align=eq5[-3]).align_to(eq2, LEFT)

        if not skip:
            self.play(FadeOut(eq2[7:-4]), ReplacementTransform(eq4[:2].copy(), eq5[-6:-4]),
                      run_time=2)
            self.play(ReplacementTransform(eq2[-4:], eq5[-4:]),
                      ReplacementTransform(eq2[:7], eq5[:7]), run_time=1)

        eq6 = MathTex(r'\mathcal F_0\subseteq\mathcal F_1\subseteq\mathcal F_2\subseteq\mathcal F_3\subseteq\cdots') \
            .next_to(eq4, DOWN).align_to(eq2, LEFT)

        if not skip:
            self.wait(0.5)
            self.play(FadeIn(eq6), run_time=1)

        mart_eqs = VGroup(eq5, eq3, eq6)
        if not skip:
            self.wait(0.5)
            line = Line(eq4.get_left(), eq4.get_right()+RIGHT*0.05, stroke_width=5, color=RED)
            self.play(FadeIn(line), run_time=1)
            self.wait(0.5)
            self.play(FadeOut(eq4, line), run_time=2)
        pos = mart_eqs.get_center()
        if not skip:
            self.play(mart_eqs.animate.arrange(direction=DOWN, center=False, aligned_edge=LEFT)\
                      .move_to(pos, coor_mask=UP).shift(shift), run_time=2)
        else:
            mart_eqs.arrange(direction=DOWN, center=False, aligned_edge=LEFT)\
                .move_to(pos, coor_mask=UP).shift(shift)
        box = SurroundingRectangle(mart_eqs, color=DARK_BLUE, corner_radius=0.1, stroke_width=5)
        if skip:
            self.add(eq5, eq3, eq6, box)
        else:
            self.play(FadeIn(box), run_time=1)
            self.wait(0.5)
            eq1 = MathTex(r'\mathbb E[X_m\vert\mathcal F_n]=X_n')
            eq2 = Tex(r'for $m \ge n$').next_to(eq1, DOWN)
            VGroup(eq1, eq2).next_to(box, RIGHT, buff=0.5)
            self.wait(0.5)
            self.play(FadeIn(eq1, eq2), run_time=1)
            self.wait(0.5)
            self.play(FadeOut(eq1, eq2), run_time=1)

        return VGroup(eq5, eq3, eq6, box)

    def walk(self, pos, skip=False):
        print('POS', pos)
        pos = pos + RIGHT * 0.15 + DOWN * 0.05
        pos2 = RIGHT * (config.frame_x_radius - 0.25) + DOWN * (config.frame_y_radius - 0.05)
        nt = 6
        ax = Axes(x_range=[0, nt], y_range=[-4, 4],
                  axis_config={'color': BLUE, 'stroke_width': 3, 'include_ticks': False,
                               "tip_width": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               "tip_height": 0.6 * DEFAULT_ARROW_TIP_LENGTH,
                               },
                  x_axis_config={'include_ticks': True},
                  x_length=pos2[0] - pos[0],
                  y_length=pos[1] - pos2[1]
                  ).move_to((pos+pos2)/2)

        title = Tex(r'\underline{Random Walk}', font_size=40).next_to(ax.get_top(), DOWN, buff=-0.02)

        if not skip:
            self.play(FadeIn(ax, title), run_time=1)

        random.seed(4)
        items = [ax, title]

        for _ in range(3):
            y = 0
            point = ax.coords_to_point(0, y)
            dot = Dot(point, fill_color=YELLOW, z_index=2)
            plot = VGroup(dot)
            coins = []
            if not skip:
                self.play(FadeIn(dot), run_time=0.2)
            for i in range(1, nt+1):
                up = random.choice([False, True])
                y1 = y + 1 if up else y - 1
                point1 = ax.coords_to_point(i, y1)
                line = Line(point, point1, stroke_width=5, z_index=3)
                dot = Dot(point1, fill_color=YELLOW, z_index=4)
                plot.add(line, dot)
                if not skip:
                    coin = abra.get_coin('H' if up else 'T').scale(0.6) \
                        .next_to(ax.coords_to_point(i - 0.5, 0) * RIGHT + pos2 * UP, UP, buff=0)
                    coins.append(abra.animate_flip(self, coin, rate=0.1))
                if not skip:
                    self.play(FadeIn(dot), Create(line, rate_func=linear), run_time=0.27)
                point = point1
                y = y1

            self.wait(0.5)
            if not skip:
                self.play(plot[1::2].animate.set_color(ManimColor(WHITE.to_rgb() * 0.5)).set_z_index(1),
                          plot[0::2].animate.set_color(ManimColor(YELLOW.to_rgb() * 0.5)).set_z_index(2),
                          FadeOut(*coins),
                          run_time=0.5)
            else:
                plot[1::2].set_color(ManimColor(WHITE.to_rgb() * 0.5))
                plot[0::2].animate.set_color(ManimColor(YELLOW.to_rgb() * 0.5))

            items = items + [plot]
        if skip:
            self.add(*items)
        self.wait(0.5)
        return items

    def optional(self, mart_def, chart, ax, seq):
        if not self.skip:
            eq_mart = mart_def[0]
            eq1 = MathTex(r'\mathbb E[X_n]=\mathbb E[\mathbb E[X_{n+1}\vert\mathcal F_n]]')[0]\
                .next_to(mart_def, RIGHT, buff=0.5)
            eq1.next_to(eq_mart[-3], ORIGIN, submobject_to_align=eq1[5], coor_mask=UP)

            self.play(ReplacementTransform((eq_mart[:10] + eq_mart[10] + eq_mart[11:13]).copy(),
                                           eq1[8:18] + eq1[5] + eq1[2:4]),
                      run_time=2)
            self.play(FadeIn(eq1[:2], eq1[4], eq1[6:8], eq1[18]), run_time=1)
            self.wait(0.5)
            eq2 = MathTex(r'\mathbb E[X_n]=\mathbb E[X_{n+1}]')[0]
            eq2.next_to(eq1[5], ORIGIN, submobject_to_align=eq2[5])
            self.play(LaggedStart(FadeOut(eq1[8:10], eq1[14:18]),
                                  ReplacementTransform(eq1[10:14] + eq1[18], eq2[8:12] + eq2[12]),
                                  lag_ratio=0.5),
                      run_time=3)

            eq3 = MathTex(r'\mathbb E[X_0] = \mathbb E[X_1] {{= \mathbb E[X_2]}}{{= \cdots}}')\
                .next_to(eq1, DOWN).align_to(eq1, LEFT)
            self.wait(0.5)
            self.play(FadeIn(eq3[0]), run_time=1)
            self.wait(0.5)
            self.play(FadeIn(eq3[1]), run_time=1)
            self.wait(0.5)
            self.play(FadeIn(eq3[2]), run_time=1)
            self.wait(0.5)

            t = 8
            self.play(FadeOut(chart[5:]), run_time=1)
            p0=ax.coords_to_point(t, 0)
            p1=chart[2][t * 2].get_center()
            eq4 = MathTex(r'T').next_to(p0, DOWN)
            eq5 = MathTex(r'X_T').next_to(p1, UP)
            l1 = Line(p0, p1, color=GREY, stroke_width=5, stroke_opacity=1)
            self.play(FadeIn(eq4), run_time=1)
            self.play(Create(l1), run_time=1)
            self.play(FadeIn(eq5), run_time=1)
            self.wait(0.5)
            eq6 = MathTex(r'\mathbb E[X_T]=\mathbb E[X_0]').next_to(eq3, DOWN).align_to(eq1, LEFT)
            self.play(FadeIn(eq6), run_time=1)
            self.wait(0.5)
            self.play(FadeOut(eq1[:8], eq2[8:], eq3),
                      eq6.animate.next_to(mart_def[-1], RIGHT, buff=1),
                      run_time=2)
            self.wait(0.5)
        else:
            eq6 = VGroup()

        thm_size = 45
        opt1 = Tex(r'\underline{\bf Optional Sampling Theorem}', tex_environment="flushleft", font_size=thm_size)
        opt1.next_to(seq, DOWN, buff=0.2).next_to(mart_def, RIGHT, buff=0.2, coor_mask=RIGHT)
        opt2 = Tex(r'Let $X$ be a martingale and $T$ be a\\bounded stopping time.',
                   tex_environment="flushleft", font_size=thm_size).next_to(opt1, DOWN).align_to(opt1, LEFT)
        opt1.move_to(opt2, coor_mask=RIGHT)  # center heading
        opt3 = Tex(r'Then, $\displaystyle\mathbb E[X_T]=\mathbb E[X_0]$.',
                   tex_environment="flushleft", font_size=thm_size).next_to(opt2, DOWN, buff=0.2).align_to(opt2, LEFT)
        bdd = opt2[0][24:31]

        thm = VGroup(opt1, opt2, opt3)
        box_thm = SurroundingRectangle(thm, color=DARK_BLUE, corner_radius=0.1, stroke_width=5)

        mart_def.generate_target().shift(LEFT * 0.3)
        self.play(FadeIn(opt1), FadeOut(eq6), MoveToTarget(mart_def), run_time=1)
        self.play(FadeIn(opt2, opt3), run_time=1)
        self.play(FadeIn(box_thm), run_time=1)
        self.wait(0.5)
        stop1 = Tex(r'{\bf Stopping Time:} $\displaystyle\{T=n\}\in\mathcal F_n$', font_size=thm_size)\
            .next_to(box_thm, DOWN, buff=0.1).align_to(opt2, LEFT)
        self.play(FadeIn(stop1), run_time=1)
        self.wait(2)
        self.play(FadeOut(stop1), run_time=1)

        l1 = Line(bdd.get_left(), bdd.get_right(), stroke_width=6, color=RED)
        self.play(FadeIn(l1), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(FadeOut(bdd, l1),
                              opt2[0][31:44].animate.align_to(opt2, LEFT), lag_ratio=0.5),
                  run_time=2)

        opt4 = Tex(r'stopping time such that', font_size=thm_size)
        opt4.next_to(opt2[0][31], ORIGIN, submobject_to_align=opt4[0][0])
        opt4_1 = Tex(r'$\displaystyle\mathbb E[\max(\lvert X_0\rvert,\ldots,\lvert X_T\rvert)] < \infty$.',
                   font_size=thm_size).next_to(opt4, DOWN, buff=0.2).move_to(box_thm, coor_mask=RIGHT)
        self.wait(0.5)
        anim1 = AnimationGroup(ReplacementTransform(opt2[0][31:43], opt4[0][:12]),
                               FadeOut(opt2[0][43]),
                               FadeIn(opt4[0][12:20]))
        opt3.generate_target()
        opt3.target.next_to(opt4_1, DOWN, coor_mask=UP, buff=0.1)
        box2 = SurroundingRectangle(VGroup(opt1, opt2, opt3.target, opt4), color=DARK_BLUE,
                                    corner_radius=0.1, stroke_width=5)
        anim2 = AnimationGroup(Transform(box_thm, box2), MoveToTarget(opt3))
        self.play(LaggedStart(anim1, anim2, lag_ratio=0.2),
                  run_time=2)
        self.wait(1)
        self.play(FadeIn(opt4_1), run_time=1)
        self.wait(0.5)

    def construct(self):
        chart, seq, y_vals, ax = self.build_graph()
        if self.graph_only:
            return
        mart_def = self.build_def(seq, walk=True)
        self.wait(0.5)


class TowerLaw(Scene):
    def construct(self):
        MathTex.set_default(font_size=40)

        eq1 = MathTex(r'p_n=\mathbb P({\rm X\ wins}\vert\mathcal F_n)')[0]
        eq2 = MathTex(r'p_{n+1}=\mathbb P({\rm X wins}\vert\mathcal F_{n+1})')[0].next_to(eq1, DOWN)
        eq2.next_to(eq1[2], ORIGIN, submobject_to_align=eq2[4], coor_mask=RIGHT)
        self.play(FadeIn(eq1, eq2), run_time=0.5)
        eq3 = MathTex(r'\mathbb E[p_{n+1}\vert\mathcal F_n]=\mathbb E[\mathbb P({\rm X\ wins}\vert\mathcal F_{n+1})\vert\mathcal F_n]')[0].next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3.next_to(eq2[4], ORIGIN, submobject_to_align=eq3[10])
        eq4 = MathTex(r'=(\mathcal F_n)')[0]
        eq4.next_to(eq3[-9], ORIGIN, submobject_to_align=eq4[-3])
        eq5 = MathTex(r'\mathbb E[p_{n+1}\vert\mathcal F_n]=p_n')[0]
        eq5.next_to(eq3[10], ORIGIN, submobject_to_align=eq5[-3]).align_to(eq1, LEFT)
        self.play(ReplacementTransform(eq2[:4] + eq2[4] + eq2[5:], eq3[2:6] + eq3[10] + eq3[13:-4]),
                  run_time=2)
        self.play(FadeIn(eq3[:2], eq3[6:10], eq3[11:13], eq3[-4:]), run_time=1)
        self.wait(1)
        self.play(FadeOut(eq3[11], target_position=eq3[13]),
                  FadeOut(eq3[12], target_position=eq3[14]),
                  FadeOut(eq3[-1], target_position=eq4[-1]),
                  FadeOut(eq3[-7:-5]),
                  ReplacementTransform(eq3[-4:-1], eq3[-10:-7]),
                  eq3[-5].animate.move_to(eq4[-1]),
                  run_time=2)
        self.wait(0.5)
        self.play(FadeOut(eq3[13:-7], eq3[-5]),
                  ReplacementTransform(eq1[:2].copy(), eq5[-2:]),
                  run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(eq3[:11], eq5[:11]),
                  run_time=1)
        self.wait(1)


class MartingaleScaling(MartingaleDef):
    skip = False

    def mart_int(self, eq5, mart_def):
        self.wait(0.5)
        circle = abra.circle_eq(eq5)
        self.play(Create(circle), run_time=2)
        self.wait(0.5)

        eq7 = MathTex(r'\mathbb E[X_{n+1}-X_n\vert\mathcal F_n]=0')[0].next_to(mart_def, RIGHT, buff=0.5)
        eq7.next_to(eq5[-3], ORIGIN, submobject_to_align=eq7[-2], coor_mask=UP)
        self.play(ReplacementTransform((eq5[:6] + eq5[-2:] + eq5[-7:-2]).copy(),
                                       eq7[:6] + eq7[7:9] + eq7[-6:-1]),
                  FadeIn(eq7[6], target_position=eq5[-3]),
                  FadeIn(eq7[-1], target_position=eq5[-2]),
                  FadeOut(circle),
                  run_time=2)

        eq8 = MathTex(r'\mathbb E[H_n(X_{n+1}-X_n)\vert\mathcal F_n]=0')[0].next_to(eq7, DOWN).align_to(eq7, LEFT)
        eq9 = MathTex(r'=H_n\mathbb E[X_{n+1}-X_n\vert\mathcal F_n]')[0].next_to(eq8, DOWN).align_to(eq8[2], LEFT)

        self.wait(0.5)
        self.play(FadeIn(eq8[:-2]), run_time=1)
        self.play(FadeIn(eq9[0]), run_time=0.5)
        self.play(ReplacementTransform((eq8[:2] + eq8[5:12] + eq8[13:17] + eq8[2:4]).copy(),
                                       eq9[3:5] + eq9[5:12] + eq9[12:] + eq9[1:3]),
                  run_time=2)
        eq9_1 = eq7[-1].copy()
        self.wait(0.5)
        self.play(eq9_1.animate.move_to(eq9[3]), FadeOut(eq9[3:]), run_time=2)
        self.play(FadeOut(eq9[1:3]), eq9_1.animate.move_to(eq9[1], coor_mask=RIGHT), run_time=2)
        self.wait(0.5)
        self.play(ReplacementTransform(eq9[0], eq8[-2]), ReplacementTransform(eq9_1, eq8[-1]), run_time=2)

        eq10 = MathTex(r'Y_{n+1}-Y_n=H_n(X_{n+1}-X_n)')[0].next_to(eq8, DOWN).align_to(eq7, LEFT)
        #        eq10_2 = MathTex(r'=H_n(X_{n+1}-X_n)')[0].next_to(eq10_1, DOWN).align_to(eq10_1[4], LEFT)
        self.wait(0.5)
        self.play(FadeIn(eq10), run_time=1)
        self.wait(0.5)

        self.play(FadeOut(eq7, eq8),
                  eq10.animate.next_to(eq7[-2], ORIGIN, submobject_to_align=eq10[7], coor_mask=UP),
                  run_time=2)

        eq11 = MathTex(r'Y_n=Y_0+\sum_{k=0}^{n-1}H_k(X_{k+1}-X_k)')[0].next_to(eq10, DOWN).align_to(eq10, LEFT)
        self.wait(0.5)
        self.play(FadeIn(eq11), run_time=1)
        self.wait(0.5)

        return VGroup(eq10, eq11)

    def anim_int(self, k, chart, y_vals, ax):
        eq1 = MathTex(r'H_{}=-0.99'.format(k), z_index=1)[0].move_to(ax.coords_to_point(5, 3))
        box = SurroundingRectangle(eq1, stroke_opacity=0,
                                   stroke_color=DARK_BLUE, fill_opacity=0.6, fill_color=DARK_BLUE,
                                   corner_radius=0.1, z_index=0)

        plot = chart[2].copy()
        chart[2].set_z_index(2)
        for p in plot[0::2]:
            p.set_color(YELLOW_A)
        for p in plot[1::2]:
            p.set_color(GREY)

        k = 7
        scale = ValueTracker(1)
        p0, p1 = plot[2*k].get_center(), plot[2*(k+1)].get_center()
        dp = (p1 - p0) * UP

        def scale_path():
            s = scale.get_value()
            dp1 = dp * (s-1)
            new_plot = [Line(p0, p1 + dp1, color=GREY, stroke_width=5)]
            for i in range(2*(k+1), 21):
                new_plot.append(plot[i].copy().shift(dp1))
            return VGroup(*new_plot)

        def show_val():
            s = scale.get_value()
            eq = MathTex(r'{:.2f}'.format(s), z_index=1).next_to(eq1[2], RIGHT)
            return eq

        path = always_redraw(scale_path)
        val = always_redraw(show_val)
        self.add(path)
        self.play(FadeIn(eq1[:3].set_z_index(2), box, val), run_time=1)

        self.play(scale.animate.set_value(-1), run_time=2)
        self.play(scale.animate.set_value(1), run_time=2)

        self.remove(path)

        def scale_path2(scale):
            path = [plot[0]]
            p0 = plot[0].get_center()
            for i in range(10):
                dp = plot[2*(i+1)].get_center() - plot[2*i].get_center()
                dp = dp*RIGHT + dp*UP*scale[i]
                path.append(Line(p0, p0+dp, color=GREY, stroke_width=5))
                path.append(plot[2*(i+1)].copy().move_to(p0+dp))
                p0 = p0 + dp

            return VGroup(*path)

        self.wait(0.5)
        eq2 = MathTex(r'H_n=n/5').move_to(eq1).align_to(eq1, LEFT)
        box.target = SurroundingRectangle(eq2, stroke_opacity=0,
                                   stroke_color=DARK_BLUE, fill_opacity=0.6, fill_color=DARK_BLUE,
                                   corner_radius=0.1, z_index=0)

        path = scale_path2(np.linspace(0, 9/5, 10))
        self.play(LaggedStart(AnimationGroup(MoveToTarget(box), FadeOut(eq1[:3], val), FadeIn(eq2)),
                              ReplacementTransform(plot.copy(), path),
                              lag_ratio=0.5),
                  run_time=2)

        self.wait(0.5)
        self.play(FadeOut(path), run_time=0.5)
        eq3 = MathTex(r'H_n=X_n').move_to(eq1).align_to(eq1, LEFT)
        box.target = SurroundingRectangle(eq3, stroke_opacity=0,
                                   stroke_color=DARK_BLUE, fill_opacity=0.6, fill_color=DARK_BLUE,
                                   corner_radius=0.1, z_index=0)

        path = scale_path2([0.4 * x for x in y_vals[:-1]])
        self.play(LaggedStart(AnimationGroup(MoveToTarget(box), FadeOut(eq2), FadeIn(eq3)),
                              ReplacementTransform(plot.copy(), path),
                              lag_ratio=0.5),
                  run_time=2)
        self.wait(1)

        return VGroup(box, eq3, path)

    def construct(self):
        chart, seq, y_vals, ax = self.build_graph(skip=True)
        mart_def = self.build_def(seq, skip=True)

        eq_int = self.mart_int(mart_def[0], mart_def[-1])
        anim_int = self.anim_int(7, chart, y_vals, ax)
        circle = abra.circle_eq(eq_int[1])
        self.play(Create(circle), run_time=2)
        self.wait(1)
        self.play(FadeOut(circle), run_time=1)
        self.wait(1)
        self.play(FadeOut(eq_int, anim_int), run_time=0.5)
        self.wait(1)

        return

        self.optional(mart_def, chart, ax, seq)


class OptionalStopping(MartingaleDef):
    skip = False

    def optional(self, mart_def, chart, ax, seq):
        eq1 = MathTex(r'Y_n = X^T_n=\begin{cases} X_n,&{\rm if\ }n\le T,\\ X_T,&{\rm if\ }n > T.\end{cases}')[0]
        eq1.next_to(mart_def, RIGHT)
        pos = eq1[:3].get_center()
        eq1[:3].next_to(eq1[6], ORIGIN, submobject_to_align=eq1[2])
        self.play(FadeIn(eq1[:2], eq1[6:8]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(eq1[8:16]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(eq1[16:]), run_time=1)
        self.wait(0.5)
        self.play(eq1[:3].animate.move_to(pos), run_time=1)
        self.play(FadeIn(eq1[3:6]), run_time=0.5)
        self.wait(0.5)

        t = 8
        t1 = 10
        self.play(FadeOut(chart[5:]), run_time=1)
        p0 = ax.coords_to_point(t, 0)
        p_arr = [chart[2][s*2].get_center() for s in range(t, t1 + 1)]
        y = p_arr[0][1]
        for p in p_arr:
            p[1] = y
        eq4 = MathTex(r'T').next_to(p0, DOWN)
        eq5 = MathTex(r'X^T').next_to(p_arr[0], UP)
        l1 = Line(p0, p_arr[0], color=GREY, stroke_width=5, stroke_opacity=1)
        l2 = Line(p_arr[0], p_arr[-1], color=WHITE, stroke_width=5, stroke_opacity=1)
        eq5 = MathTex(r'X^T').next_to(l2, UP)

        self.play(FadeIn(eq4), run_time=1)
        self.play(Create(l1), run_time=1)
        self.play(Create(l2), FadeOut(chart[2][t*2:]), run_time=1)
        self.play(FadeIn(eq5), run_time=1)
        self.wait(0.5)

        thm_size = 45
        opt1 = Tex(r'\underline{\bf Optional Stopping Theorem}', tex_environment="flushleft", font_size=thm_size)
        opt1.next_to(seq, DOWN, buff=0.2).next_to(mart_def, RIGHT, buff=0.2, coor_mask=RIGHT)
        opt2 = Tex(r'Let $X$ be a martingale and $T$ be a\\ stopping time.',
                   tex_environment="flushleft", font_size=thm_size).next_to(opt1, DOWN).align_to(opt1, LEFT)
        opt1.move_to(opt2, coor_mask=RIGHT)  # center heading
        opt3 = Tex(r'Then, $X^T$ is a martingale.',
                   tex_environment="flushleft", font_size=thm_size).next_to(opt2, DOWN, buff=0.2).align_to(opt2, LEFT)

        box_thm = SurroundingRectangle(VGroup(opt1, opt2, opt3), color=DARK_BLUE, corner_radius=0.1, stroke_width=5)
        thm = VGroup(opt1, opt2, opt3, box_thm).next_to(mart_def, RIGHT, buff=0.2)

        mart_def.generate_target().shift(LEFT * 0.3)
        self.play(FadeIn(opt1), FadeOut(eq1), MoveToTarget(mart_def), run_time=1)
        self.play(FadeIn(opt2, opt3), run_time=1)
        self.play(FadeIn(box_thm), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(mart_def), run_time=2)
        self.wait(0.5)

        l3 = Line(LEFT * config.frame_x_radius, RIGHT * thm.get_left())
        stop1 = Tex(r'\underline{\bf Stopping Time}', font_size=thm_size)
        stop2 = Tex(r'\\$\displaystyle\{T=n\}\in\mathcal F_n$', font_size=thm_size).next_to(stop1, DOWN)
        stop3 = VGroup(stop1, stop2).next_to(thm, LEFT).move_to(l3, coor_mask=RIGHT)
        self.play(FadeIn(stop3), run_time=1)
        self.wait(2)
        self.play(FadeOut(stop3), run_time=1)
        self.wait(0.5)

        eq6 = MathTex('Y_n = X^T_n = X_{\min(T, n)}').to_edge(LEFT).align_to(thm, UP)
        self.play(FadeIn(eq6), run_time=1)
        self.wait(0.1)
        eq7 = MathTex(r'Y_{n+1}-Y_n = \begin{cases} X_{n+1}-X_n,&{\rm if\ }n < T,\\ 0,&{\rm if\ }n \ge T.\end{cases}')[0]
        eq7.next_to(eq6, DOWN).align_to(eq6, LEFT)
        thm2 = thm.copy()
        self.play(FadeIn(eq7[:9]), thm.animate.scale(0.65).align_to(thm, DR), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq7[9:23]), run_time=1)
        self.wait(0.1)
        self.play(FadeIn(eq7[23:]), run_time=1)
        self.wait(0.5)
        eq8 = MathTex(r'Y_{n+1}-Y_n =H_n(X_{n+1}-X_n)')[0].next_to(eq6, DOWN).align_to(eq6, LEFT)
        self.play(ReplacementTransform(eq7[:8] + eq7[9:16], eq8[:8] + eq8[11:18]),
                  FadeOut(eq7[8], eq7[16:]),
                  FadeIn(eq8[8:10], target_position=eq7[8]),
                  FadeIn(eq8[10], target_position=eq7[9].get_left()),
                  FadeIn(eq8[18], target_position=eq7[14:15].get_right()),
                  run_time=3)
        self.wait(0.5)
        eq9 = MathTex(r'H_n=\begin{cases}1, & {\rm if\ }n < T,\\ 0, & {\rm if\ }n\ge T.\end{cases}')[0]\
            .next_to(eq8, DOWN).align_to(eq8, LEFT)
        self.play(FadeIn(eq9), run_time=1)
        self.wait(0.5)
        thm2.scale(0.9).align_to(thm2, DR)
        self.play(ReplacementTransform(thm, thm2), run_time=1)
        self.wait(0.5)

    def construct(self):
        chart, seq, y_vals, ax = self.build_graph(skip=True)
        mart_def = self.build_def(seq, skip=True)
        self.optional(mart_def, chart, ax, seq)
        self.wait(0.5)


if __name__ == "__main__":
    with tempconfig({"quality": "high_quality", "fps": 30, "preview": True}):
        print('running...')

#        ElectionOdds().render()
