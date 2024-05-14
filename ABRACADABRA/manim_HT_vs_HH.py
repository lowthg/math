# cell 1

from manim import *

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