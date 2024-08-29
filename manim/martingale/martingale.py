from manim import *
import numpy as np
import math
import random
import csv
import datetime


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

            txt_year = Tex('2024', font_size=30).move_to(ax.coords_to_point((datetime.date(2024, 1, 1) - dates[0]).days, -0.15))

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
                    lines = [Line(oldpoints[j], points[j], stroke_color=colours[j], stroke_width=5, z_index=0) for j in jnames]
                    creates = [Create(lines[j], rate_func=linear) for j in jnames]
                    self.play(*creates, run_time=2.1/30)

                oldpoints = points


if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "fps": 15, "preview": True}):
        ElectionOdds().render()
