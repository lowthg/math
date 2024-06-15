from manim import *


class Quartic(Scene):
    def divx2(self, a, b, c, d, e, pos=UP * config.frame_y_radius + DOWN):
        coeff = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e}
        eq1 = MathTex(r'{a}x^4+{b}x^3+{c}x^2+{d}x+{e}=0'.format(**coeff))[0].next_to(pos, DOWN)
        eq2 = MathTex(r'\frac{{1}}{{x^2}}({a}x^4+{b}x^3+{c}x^2+{d}x+{e})=0'.format(**coeff))[0]
        eq2.shift(eq1[-2].get_center()-eq2[-2].get_center())
        eq3_1 = MathTex(r'\frac{{1}}{{x^2}}(\frac{{{a}x^4}}{{x^2}}+\frac{{{b}x^3}}{{x^2}}+\frac{{{c}x^2}}{{x^2}}'
                        r'+\frac{{{d}x}}{{x^2}}+\frac{{{e}}}{{x^2}})=0'.format(**coeff))[0]
        eq3_1.shift(eq1[-2].get_center()-eq3_1[-2].get_center())
        eq3 = eq3_1[5:]
        eq4 = MathTex(r'{a}x^2 + {b}x^1 + {c}x^1 + \frac{{{d}}}{{x^1}} + \frac{{{e}}}{{x^2}} =0'.format(**coeff))[0]
        eq4.shift(eq1[-2].get_center()-eq4[-2].get_center())
        eq4[6].set_opacity(0)
        eq4[9:11].set_opacity(0)

        eq5 = MathTex(r'\left({a}x^2+\frac{{{e}}}{{x^2}}\right) {{{{+}}}} \left({{b}}x+\frac{{{d}}}{{x}}\right)'
                      r' {{{{+}}}} {c} {{{{=}}}} 0'.format(**coeff))
        eq5.shift(eq1[-2].get_center()-eq5[-2][0].get_center())

        self.play(FadeIn(eq1), run_time=1)
        self.play(ReplacementTransform(eq1[:-2], eq2[5:-3]), run_time=1)
        self.play(FadeIn(eq2[:5], eq2[-3:]), run_time=1)
        self.play(FadeOut(eq2[:2], eq2[-3]),
                  FadeOut(eq2[4], target_position=eq3_1[4]),
                  ReplacementTransform(eq2[5:8] + eq2[8:12] + eq2[12:16] + eq2[16:19] + eq2[19:21],
                                       eq3[:3] + eq3[6:10] + eq3[13:17] + eq3[20:23] + eq3[26:28]),
                  ReplacementTransform(eq2[2:4] + eq2[2:4].copy() + eq2[2:4].copy()+ eq2[2:4].copy() + eq2[2:4].copy(),
                                       eq3[4:6] + eq3[11:13] + eq3[18:20] + eq3[24:26] + eq3[29:31]),
                  FadeIn(eq3[3], eq3[10], eq3[17], eq3[23], eq3[28]),
                  run_time=2)

        eq4[12:16].move_to(eq3[21:26])
        anims = [ReplacementTransform(eq3[22:23], eq4[14:15]),
                 ReplacementTransform(eq3[24], eq4[14]),
                 FadeOut(eq3[25], target_position=eq4[15])]
        for i, j in [(0, 0), (7, 4), (14, 8)]:
            eq4[j:j+3].move_to(eq3[i:i+6], coor_mask=RIGHT)
            anims += [ReplacementTransform(eq3[i:i+2], eq4[j:j+2]),
                      ReplacementTransform(eq3[i+4], eq4[j+1]),
                      FadeOut(eq3[i+2], target_position=eq4[j+2]),
                      FadeOut(eq3[i+5], target_position=eq4[j+2]),
                      FadeIn(eq4[j+2], target_position=eq3[i+2]),
                      FadeOut(eq3[i+3])]

        self.play(anims, run_time=2)

        eq4b = eq4[:3] + eq3[6] + eq4[4] + eq4[5] + eq3[13] + eq4[8] + eq3[20] + eq3[21] + eq3[23] + eq4[14] + eq3[26]\
               + eq3[27] + eq3[28] + eq3[29] + eq3[30]

        self.play(ReplacementTransform(eq4b[:3] + eq4b[3] + eq4b[4:6] + eq4b[6] + eq4b[7] + eq4b[8:12] + eq4b[12:17],
                                       eq5[0][1:4] + eq5[1][0] + eq5[2][1:3] + eq5[3][0] + eq5[4][0] + eq5[2][3:7] + eq5[0][4:9]),
                  run_time=2)
        self.play(FadeIn(eq5[0][0], eq5[0][-1], eq5[2][0], eq5[2][-1]), ReplacementTransform(eq1[-2:-1] + eq1[-1], eq5[-2][:] + eq5[-1][0]), run_time=1)
        return eq5

    def symmetric(self):
        eq1 = self.divx2('a', 'b', 'c', 'b', 'a')
        eq2 = MathTex(r'a\left(x^2+\frac{1}{x^2}\right) {{+}} b\left(x+\frac{1}{x}\right) {{+}} c {{=}} 0')
        eq2.shift(eq1[-1].get_center()-eq2[-1].get_center())

        anims = [[ReplacementTransform(eq1[i][1:2] + eq1[i][0] + eq1[i][2:4+j] + eq1[i][5+j:],
                                      eq2[i][0:1] + eq2[i][1] + eq2[i][2:4+j] + eq2[i][5+j:]),
                 ReplacementTransform(eq1[i][4+j], eq2[i][0]),
                 FadeIn(eq2[i][4+j], target_position=eq1[i][4+j])] for i, j in [(0, 1), (2, 0)]]

        self.play(ReplacementTransform(eq1[3:] + eq1[1], eq2[3:] + eq2[1]), *anims, run_time=2)

        eq3 = MathTex(r'a\left(\left(x^2+\frac{1}{x^2}\right)^2-2\right) {{+}} ')
        eq3.shift(eq2[1].get_center()-eq3[1].get_center())
        self.play(ReplacementTransform(eq2[0][:2] + eq2[0][2:9] + eq2[0][-1],
                                       eq3[0][:2] + eq3[0][3:10] + eq3[0][-1]),
                  FadeIn(eq3[0][2], target_position=eq2[0][1]),
                  FadeIn(eq3[0][10], target_position=eq2[0][-1]),
                  run_time=2)
        self.play(ReplacementTransform(eq3[0][4], eq3[0][11]),
                  ReplacementTransform(eq3[0][9], eq3[0][11]),
                  FadeIn(eq3[0][12:14]),
                  run_time=2)

        fq1 = MathTex(r'-y=x+\frac1x=0').next_to(eq2, DOWN)[0]
        fq2 = MathTex(r'0=x-y+\frac1x=0').next_to(eq2, DOWN)[0]
        fq2.shift((eq2[-2][0].get_center()-fq2[-2].get_center())*RIGHT)
        fq1.shift((eq2[-2][0].get_center()-fq1[-2].get_center())*RIGHT)
        self.play(FadeIn(fq1[1:-2]), run_time=2)

        eq3_1 = MathTex(r'ay^{2} {{=}} y {{1 - 2a}}')
        eq3_1.shift(eq2[-2].get_center()-eq3_1[1].get_center())
        eq3_1[2].move_to(eq2[2][3], coor_mask=RIGHT)
        eq3_1[0].shift((eq3[0][5].get_center()-eq3_1[0][1].get_center())*RIGHT)
        eq3_1[3].shift((eq3[0][-2].get_right()-eq3_1[3][-1].get_right())*RIGHT)
        self.play(FadeIn(eq3_1[0][1], eq3_1[2]), FadeOut(eq3[0][3], eq3[0][5:9], eq2[2][2:7]), run_time=2)
        self.play(FadeOut(eq3[0][2], eq3[0][10], eq2[2][1], eq2[2][-1]),
                  Transform(eq3[0][-4], eq3_1[0][2]),
                  run_time=2)
        self.play(Transform(eq3[0][0], eq3_1[0][0]),
                  ReplacementTransform(eq3[0][-3:-1] + eq3[0][0].copy(), eq3_1[3][-3:-1] + eq3_1[3][-1]),
                  FadeOut(eq3[0][1], eq3[0][-1]),
                  run_time=2)

        eq4 = MathTex('ay^2+by+c-2a=0')[0]
        eq4.shift(eq2[-2][0].get_center()-eq4[-2].get_center())
        self.play(ReplacementTransform(eq3_1[3][1:] + eq2[-3][0:1] + eq2[-4][0] + eq3_1[2][0] + eq2[2][0] + eq2[1][0] + eq3[0][-4] + eq3_1[0][1] + eq3[0][0],
                                       eq4[8:11] + eq4[7:8] + eq4[6] + eq4[5] + eq4[4] + eq4[3] + eq4[2] + eq4[1] + eq4[0]),
                  run_time=2)

        self.play(ReplacementTransform(fq1[4:8] + fq1[3] + fq1[1],
                                       fq2[5:9] + fq2[2] + fq2[4]),
                  FadeIn(fq2[3], target_position=fq1[0]),
                  FadeIn(fq2[-2:]),
                  FadeOut(fq1[2], target_position=fq2[3]),
                  run_time=2)
        fq3 = MathTex(r'x^2-yx+1=0')[0]
        fq3.shift(fq2[-2].get_center()-fq3[-2].get_center())
        self.play(ReplacementTransform(fq2[-2:] + fq2[2] + fq2[3:5] + fq2[5:7],
                                       fq3[-2:] + fq3[0] + fq3[2:4] + fq3[5:7]),
                  FadeOut(fq2[-4]),
                  ReplacementTransform(fq2[-3], fq3[0]),
                  ReplacementTransform(fq2[-3].copy(), fq3[4]),
                  FadeIn(fq3[1]),
                  run_time=2)

    def special(self):
        eq1 = self.divx2('a', 'b', 'c', 'd', 'e').set_z_index(1)
        eq10 = MathTex(r'ay^2+by+bc-2ad=0')[0]
        eq10.shift(eq1[5][0].get_center()-eq10[-2].get_center())

        eq2 = MathTex(r'y=bx+\frac{d}{x}').next_to(eq1, DOWN)[0]
        eq1_1=MathTex(r'y')[0].move_to(eq1[2][3])
        self.play(ReplacementTransform(eq1[2][1:-1], eq2[2:]), run_time=2)
        self.play(FadeIn(eq2[:2], eq1_1), FadeOut(eq1[2][0], eq1[2][-1]), run_time=2)
        eq3 = MathTex(r'y^2=b^2x^2+\frac{d^2}{x^2}+2bd').next_to(eq2, DOWN).set_z_index(1)[0]
        eq3.shift((eq2[1].get_center()-eq3[2].get_center())*RIGHT)
        self.play(FadeIn(eq3), run_time=2)
        color='#3f9c28'

        eq4 = MathTex(r'\frac{ay^2}{b^2}=b^2x^2+\frac{ad^2}{b^2x^2}+\frac{2bd}{b^2}').next_to(eq2, DOWN).set_z_index(1)[0]
        eq4.shift(eq3[2].get_center()-eq4[6].get_center())

        rect1 = SurroundingRectangle(eq1[0][1:-1], stroke_opacity=0, fill_opacity=1, color=color, corner_radius=0.1)
        rect2 = SurroundingRectangle(eq3[3:13], stroke_opacity=0, fill_opacity=1, color=color, corner_radius=0.1)
        rect3 = SurroundingRectangle(eq4[7:20], stroke_opacity=0, fill_opacity=1, color=color, corner_radius=0.1)
        self.play(FadeIn(rect1, rect2), FadeOut(eq1[0][0], eq1[0][-1]), run_time=2)
        self.play(ReplacementTransform(eq3[3:5] + eq3[:2] + eq3[11:17] + eq3[8:11] + eq3[2] + eq3[5:8],
                                       eq4[4:6] + eq4[1:3] + eq4[18:24] + eq4[13:16] + eq4[6] + eq4[9:12]),
                  ReplacementTransform(eq3[3:5].copy(), eq4[16:18]),
                  ReplacementTransform(eq3[3:5].copy(), eq4[-2:]),
                  ReplacementTransform(rect2, rect3),
                  FadeIn(eq4[3], eq4[-3]),
                  run_time=2)

        eq5 = MathTex(r'ax^2+\frac{2abd}{b^2}')[0].set_z_index(1)
        eq5[:3].shift(eq4[9].get_center()-eq5[1].get_center())
        eq5[3:].shift(eq4[-7].get_center()-eq5[3].get_center())
        self.play(FadeIn(eq4[0], eq4[12], eq5[0], eq5[-6]),
                  ReplacementTransform(eq4[-5:] + eq4[-6], eq5[-5:] + eq5[-7]),
                  run_time=2)

        eq6 = MathTex(r'{{ {\rm Assumption:\ } }} e = \frac{ad^2}{b^2}').next_to(eq4, DOWN).align_to(eq10, LEFT)
        eq6[0].set_color(RED)
        self.play(FadeIn(eq6[0]), run_time=1)
        self.play(LaggedStart(ReplacementTransform(eq1[0][5].copy(), eq6[1][0]), FadeIn(eq6[1][1]), lag_ratio=0.5), run_time=2)
        self.play(ReplacementTransform(eq4[12:18].copy(), eq6[1][2:]), run_time=2)

        eq7 = MathTex(r'\frac{e}{b^2x^2}')[0]
        eq7.shift(eq4[15].get_center()-eq7[1].get_center())
        self.play(FadeOut(eq4[12:15], eq4[16:18]), ReplacementTransform(eq6[1][0].copy(), eq7[0]), run_time=2)

        l1 = Line(LEFT*0.2, RIGHT*0.2, color=BLUE, stroke_width=10).move_to(eq5[-5]).rotate(0.8)
        l2 = Line(LEFT*0.15, RIGHT*0.15, color=BLUE, stroke_width=8).move_to(eq5[-1]).rotate(0.8)

        self.play(FadeIn(l1, l2), run_time=1)
        self.play(FadeOut(l1, l2, eq5[-5], eq5[-1]), run_time=2)

        eq8 = MathTex(r'\frac{a}{b}y^2-\frac{2ad}{b}+')[0].set_z_index(1)
        eq8.shift(eq1[1][0].get_center()-eq8[-1].get_center())
        rect4 = SurroundingRectangle(eq8[:-1], stroke_opacity=0, fill_opacity=1, color=color, corner_radius=0.1)
        self.play(FadeOut(eq1[0][1:-1]),
                  ReplacementTransform(rect1, rect4),
                  ReplacementTransform((eq4[1:3] + eq4[0] + eq4[3:5] + eq5[-4:-1] + eq5[-7:-5]).copy(),
                                       eq8[3:5] + eq8[0] + eq8[1:3] + eq8[-4:-1] + eq8[-6:-4]),
                  FadeIn(eq8[-7], target_position=eq4[-7]),
                  run_time=3)
        self.play(FadeOut(rect4, rect3), run_time=1)

        eq9 = MathTex(r'ay^2-2ad+by+bc=0')[0]
        eq9[0].shift(eq8[3].get_center()-eq9[1].get_center())
        eq9[8].shift(eq1_1[0].get_center()-eq9[9].get_center())
        eq9[-5:-3].shift(eq1[4][0].get_center()-eq9[-3].get_center())
        eq9[4:7].shift(eq8[5].get_center()-eq9[3].get_center())
        self.play(ReplacementTransform(eq8[0], eq9[0]),
                  ReplacementTransform(eq8[2], eq9[8]),
                  ReplacementTransform(eq8[6:9], eq9[4:7]),
                  ReplacementTransform(eq8[-2], eq9[-4]),
                  ReplacementTransform(eq1[3][0], eq9[-5]),
                  FadeOut(eq8[1], eq8[-3]),
                  run_time=2)

        self.play(ReplacementTransform(eq1[4][0], eq10[8]),
                  ReplacementTransform(eq9[-5], eq10[6]),
                  ReplacementTransform(eq1_1[0], eq10[5]),
                  ReplacementTransform(eq9[4:7], eq10[10:13]),
                  ReplacementTransform(eq9[-4], eq10[7]),
                  ReplacementTransform(eq8[5], eq10[9]),
                  ReplacementTransform(eq9[8], eq10[4]),
                  ReplacementTransform(eq1[1][0], eq10[3]),
                  ReplacementTransform(eq8[3:5], eq10[1:3]),
                  ReplacementTransform(eq9[0], eq10[0]),
                  run_time=2)

        self.play(FadeOut(eq4[:7], eq5[0], eq4[9:12], eq4[15], eq4[18:21], eq7[0], eq5[-7:-5], eq5[-4:-1]), run_time=1)

        eq11 = MathTex(r'=bx-y+\frac{d}{x}=0')[0]
        eq11.shift(eq2[-1].get_center()-eq11[-3].get_center())
        self.play(ReplacementTransform(eq2[2:4]+eq2[4:] + eq2[0],
                                       eq11[1:3] + eq11[5:-2] + eq11[4]),
                  FadeIn(eq11[3], target_position=eq11.get_left()),
                  FadeOut(eq2[1], target_position=eq11[0]),
                  FadeIn(eq11[-2:]),
                  run_time=2)

        eq12 = MathTex(r'bx^2-yx+d=0')[0]
        eq12.shift(eq11[-2].get_center()-eq12[-2].get_center())
        self.play(ReplacementTransform(eq11[1:3] + eq11[3:5] + eq11[5:7] + eq11[-2:] + eq11[8],
                                       eq12[:2] + eq12[3:5] + eq12[6:8] + eq12[-2:] + eq12[5]),
                  ReplacementTransform(eq11[-3].copy(), eq12[1]),
                  FadeIn(eq12[2]),
                  FadeOut(eq11[-4]),
                  run_time=2)

        eq13 = MathTex(r'ad^2=b^2e')[0]
        eq13.shift(eq6[1][1].get_center()-eq13[3].get_center()).align_to(eq6[1], LEFT)
        self.play(eq6[1][0].animate.move_to(eq13[4], coor_mask=RIGHT),
                  eq6[1][1].animate.move_to(eq13[3], coor_mask=RIGHT),
                  eq6[1][2:].animate.move_to(eq13[:3], coor_mask=RIGHT),
                  run_time=2)
        self.play(ReplacementTransform(eq6[1][2:5] + eq6[1][6:] + eq6[1][1] + eq6[1][0],
                                       eq13[:3] + eq13[4:6] + eq13[3] + eq13[6]),
                  FadeOut(eq6[1][5]),
                  run_time=2)

    def change_var1(self):
        eq1 = MathTex('ax^4 + bx^3 + cx^2+dx+e=0').to_edge(UP)[0]
        eq2 = MathTex(r'a(y+k)^4+b(y+k)^3+c(y+k)^2+d(y+k)+e=0').to_edge(UP)[0]
        self.play(FadeIn(eq1), run_time=2)
        self.play(ReplacementTransform(eq1[2:5] + eq1[6:9] + eq1[10:13] + eq1[14:] + eq1[0],
                                       eq2[6:9] + eq2[14:17] + eq2[22:25] + eq2[30:] + eq2[0]),
                  FadeIn(eq2[1:6], target_position=eq1[1]),
                  FadeIn(eq2[9:14], target_position=eq1[5]),
                  FadeIn(eq2[17:22], target_position=eq1[9]),
                  FadeIn(eq2[25:30], target_position=eq1[13]),
                  FadeOut(eq1[1], target_position=eq2[1:6]),
                  FadeOut(eq1[5], target_position=eq2[9:14]),
                  FadeOut(eq1[9], target_position=eq2[17:22]),
                  FadeOut(eq1[13], target_position=eq2[25:30]),
                  run_time=2)
        eq3 = MathTex(r'{{a(y^4+4ky^3+6k^2y^2+4k^3y+k^4)}}+{{b(y^3+3ky^2+3k^2y+k^3)}}'
                      r'+{{c(y^2+2ky+k^2)}}+{{d(y+k)}}+{{e}}=0').move_to(eq1, LEFT)

        eq3[1:].next_to(eq3[0], DOWN)
        eq3[3:].next_to(eq3[:3], DOWN)
        eq3[5:].next_to(eq3[:5], DOWN)
        eq3[7:].next_to(eq3[:7], DOWN)
        eq3[2][14:].shift((eq3[0][-3].get_right()-eq3[2][15].get_right())*RIGHT)
        eq3[2][9:14].align_to(eq3[0][-5], RIGHT)
        eq3[2][4:9].align_to(eq3[0][-10], RIGHT)
        (eq3[2][:4] + eq3[1]).align_to(eq3[0][8], RIGHT)
        eq3[4][8:].shift((eq3[2][-3].get_right()-eq3[4][9].get_right())*RIGHT)
        eq3[4][4:8].align_to(eq3[2][-5], RIGHT)
        (eq3[4][:4] + eq3[3]).align_to(eq3[2][8], RIGHT)
        eq3[6][3:].shift((eq3[4][-3].get_right()-eq3[6][4].get_right())*RIGHT)
        (eq3[6][:3] + eq3[5]).align_to(eq3[4][7], RIGHT)
        eq3[7:].shift((eq3[6][-2].get_right()-eq3[8][0].get_right())*RIGHT)


        eq2_1, eq2_2 = eq2[:7], eq2[7:]
        eq2_1.generate_target()
        eq2_1.target[5:7].shift((eq3[0][-1].get_center()-eq2[5].get_center())*RIGHT)
        eq2_1.target[:2].shift((eq3[0][1].get_center()-eq2[1].get_center())*RIGHT)
        eq2_1.target[2:5].shift((eq3[0][2:-1].get_center()-eq2[2:5].get_center()))

        self.play(LaggedStart(eq2_2.animate.shift(eq3[1][0].get_center()-eq2_2[0].get_center()),
                              MoveToTarget(eq2_1),
                              lag_ratio=0.2),
                  run_time=2)

        self.play(FadeOut(eq2[2:5], eq2[6]), FadeIn(eq3[0][2:-1]),
                  ReplacementTransform(eq2[:2] + eq2[5], eq3[0][:2] + eq3[0][-1]), run_time=2)


        eq2_1, eq2_2 = eq2[7:15], eq2[15:]
        eq2_1.generate_target()
        eq2_1.target[:3].shift((eq3[2][1].get_center()-eq2[9].get_center())*RIGHT)
        eq2_1.target[6:].shift((eq3[2][-1].get_center()-eq2[13].get_center())*RIGHT)
        eq2_1.target[3:6].shift((eq3[2][2:-1].get_center()-eq2[10:13].get_center())*RIGHT)

        self.play(LaggedStart(eq2_2.animate.shift(eq3[3][0].get_center()-eq2_2[0].get_center()),
                              MoveToTarget(eq2_1),
                              lag_ratio=0.2),
                  run_time=2)

        self.play(FadeOut(eq2[10:13], eq2[14]), FadeIn(eq3[2][2:-1]),
                  ReplacementTransform(eq2[8:10] + eq2[7] + eq2[13], eq3[2][:2] + eq3[1][0] + eq3[2][-1]),
                  run_time=2)


        eq2_1 = eq2[15:23]
        eq2_1.generate_target()
        eq2_1.target[:3].shift((eq3[4][1].get_center()-eq2[17].get_center())*RIGHT)
        eq2_1.target[3:6].shift((eq3[4][2:-1].get_center()-eq2[18:21].get_center())*RIGHT)
        eq2_1.target[6:].shift((eq3[4][-1].get_center()-eq2[21].get_center())*RIGHT)

        self.play(LaggedStart(eq2[23:].animate.shift(eq3[5][0].get_center()-eq2[23].get_center()),
                              MoveToTarget(eq2_1),
                              lag_ratio=0.2),
                  run_time=2)

        self.play(FadeOut(eq2[18:21], eq2[22]), FadeIn(eq3[4][2:-1]),
                  ReplacementTransform(eq2[16:18] + eq2[15] + eq2[21], eq3[4][:2] + eq3[3][0] + eq3[4][-1]),
                  run_time=2)

        self.play(ReplacementTransform(eq2[24:30] + eq2[23] + eq2[30] + eq2[31] + eq2[32:],
                                       eq3[6][:] + eq3[5][0] + eq3[7][0] + eq3[8][0] + eq3[9][:]),
                  run_time=2)

        eq4 = MathTex(r'ay^4+\tilde by^3 + \tilde cy^2 + \tilde dy + \tilde e=0').next_to(eq3, DOWN).align_to(eq3, RIGHT)[0]
        eq4[:3].align_to(eq3[0][3], RIGHT)
        eq4[3:8].align_to(eq3[2][3], RIGHT)
        eq4[8:13].align_to(eq3[4][3], RIGHT)
        eq4[13:17].align_to(eq3[6][2], RIGHT)
        eq4[17:20].align_to(eq3[8][0], RIGHT)
        eq5 = MathTex(r'\tilde b = 4ak+b').next_to(eq4, DOWN).align_to(eq4, LEFT)[0]
        eq6 = MathTex(r'\tilde c = 6ak^2+3bk+c').next_to(eq5, DOWN).align_to(eq5, LEFT)[0]
        eq7 = MathTex(r'\tilde d = 4ak^3+3bk^2+2ck+d').next_to(eq6, DOWN).align_to(eq5, LEFT)[0]
        eq8 = MathTex(r'\tilde e = ak^4 + bk^3 + ck^2 + dk+e').next_to(eq7, DOWN).align_to(eq5, LEFT)[0]

        self.play(FadeIn(eq4[1:3]), run_time=1)
        self.play(ReplacementTransform(eq3[0][0].copy(), eq4[0]), run_time=2)

        self.play(FadeIn(eq4[3:8], eq5[:3]), run_time=1)
        self.play(ReplacementTransform(eq3[0][:1] + eq3[0][5] + eq3[0][6],
                                       eq5[4:5] + eq5[3] + eq5[5]),
                  run_time=2)
        self.play(ReplacementTransform(eq3[2][0], eq5[7]), FadeIn(eq5[6]),
                  run_time=2)

        self.play(FadeIn(eq4), run_time=1)

        self.play(FadeIn(eq5, eq6, eq7, eq8))


    def change_var(self):
        eq1 = MathTex('ax^4 + bx^3 + cx^2+dx+e=0').to_edge(UL)[0]
        eq2 = MathTex('x=y+k').next_to(eq1, DOWN).align_to(eq1, LEFT)
        eq3 = MathTex('f(x)=ax^4 + bx^3 + cx^2+dx+e').next_to(eq2, DOWN).align_to(eq2, LEFT)
        eq4 = MathTex(r'f(y+k) {{=}} f(k) {{+}} f^\prime(k)y+\frac12f^{(2)}(k)y^2+\frac16f^{(3)}(k)y^3+\frac1{24}f^{(4)}(k)y^4').next_to(eq3, DOWN).align_to(eq3, LEFT)
        eq5 = MathTex(r'\tilde a = \frac1{24}f^{(4)}(k)').next_to(eq4, DOWN).align_to(eq4, LEFT)
        eq6 = MathTex(r'\tilde b = \frac1{6}f^{(3)}(k)').next_to(eq5, DOWN).align_to(eq4, LEFT)


        self.add(eq1, eq2, eq3, eq4)
        eq9 = MathTex(r'\tilde e = f(k)').next_to(eq4, DOWN).align_to(eq4, LEFT)[0]
        self.play(FadeIn(eq9), run_time=1)
        eq9_1 = eq9[:2].copy()
        self.play(eq9_1.animate.shift(eq4[1][0].get_center()-eq9[2].get_center()).move_to(eq4[2][:4], coor_mask=RIGHT),
                  FadeOut(eq4[2][:4]),
                  run_time=2)
        eq9_2 = MathTex(r'= ak^4+bk^3+ck^2+dk+e')[0]
        eq9_2.shift(eq9[2].get_center()-eq9_2[0].get_center())
        self.play(FadeOut(eq9[3:]), FadeIn(eq9_2[1:]), run_time=2)
        eq8 = MathTex(r'\tilde d = f^\prime(k)').next_to(eq9, DOWN).align_to(eq4, LEFT)[0]
        self.play(FadeIn(eq8), run_time=1)
        eq8_1 = eq8[:2].copy()
        self.play(eq8_1.animate.shift(eq4[1][0].get_center()-eq8[2].get_center()).align_to(eq4[4][:5], RIGHT),
                  FadeOut(eq4[4][:5]),
                  run_time=2)
        eq8_2 = MathTex(r'=4ak^3+3bk^2+2ck+d')[0]
        eq8_2.shift(eq8[2].get_center()-eq8_2[0].get_center())
        eq8_3 = MathTex(r'=()^\prime')[0]
        eq8_3.shift(eq8[2].get_center()-eq8_3[0].get_center())
        eq8_3[2:].shift(RIGHT * eq9_2[1:].width)
        eq8_4 = eq9_2[1:].copy()
        self.play(FadeOut(eq8[3:]),
                  FadeIn(eq8_3[1:]),
                  eq8_4.animate.shift(eq8_3[1].get_right()-eq9_2[1].get_left()),
                  run_time=2)
        self.play(FadeOut(eq8_3[1:]),
                  ReplacementTransform(eq8_4[:2] + eq8_4[2] + eq8_4[3] + eq8_4[4:6] + eq8_4[6] + eq8_4[7],
                                       eq8_2[2:4] + eq8_2[1] + eq8_2[5] + eq8_2[7:9] + eq8_2[6] + eq8_2[10]),
                  ReplacementTransform(eq8_4[8:10] + eq8_4[10] + eq8_4[11:13],
                                       eq8_2[12:14] + eq8_2[11] + eq8_2[14:]),
                  FadeIn(eq8_2[4], target_position=eq8_4[2]),
                  FadeIn(eq8_2[9], target_position=eq8_4[6]),
                  FadeOut(eq8_4[13:]),
                  run_time=2)

        eq7 = MathTex(r'\tilde c = \frac1{2}f^{(2)}(k)').next_to(eq8, DOWN).align_to(eq4, LEFT)
        self.play(FadeIn(eq7), run_time=1)

        self.wait(1)

    def construct(self):
        MathTex.set_default(font_size=40)
        self.change_var1()
