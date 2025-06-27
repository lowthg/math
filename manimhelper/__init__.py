"""
helper functions for Manim
"""
from manim import *
import numpy as np
import math


def pos(dir=ORIGIN):
    return RIGHT * config.frame_x_radius * dir[0] + UP * config.frame_y_radius * dir[1]

def align_sub(source, subobject, target, direction=ORIGIN, **kwargs) -> Mobject:
    """
    move object to align subobject with target
    """
    return source.next_to(target, direction, submobject_to_align=subobject, **kwargs)

def diff(source: Mobject, target: Mobject, coor_mask=UR):
    """
    get difference of positions from source to target
    """
    return (target.get_center() - source.get_center()) * coor_mask

def fade_replace(obj1: Mobject, obj2: Mobject, coor_mask=np.array([1, 1, 1]), **kwargs):
    """
    Fade out obj1 into obj2
    For when the objects differ so that ReplacementTransform doesn't work
    """
    return FadeOut(obj1, target_position=obj2.get_center(), **kwargs), FadeIn(obj2, target_position=obj1.get_center(), **kwargs)


def stretch_replace(source: Mobject, target: Mobject, **kwargs):
    """
    Fade out obj1 into obj2, stretching to fit
    For when the objects differ so that ReplacementTransform doesn't work
    """
    w1 = source.width
    w2 = target.width
    h1 = source.height
    h2 = target.height
    source2 = target.copy().move_to(source).stretch_to_fit_height(h1).stretch_to_fit_width(w1).set_opacity(0)
    target2 = source.copy().move_to(target).stretch_to_fit_height(h2).stretch_to_fit_width(w2).set_opacity(0)
    return ReplacementTransform(VGroup(source, source2), VGroup(target2, target), **kwargs)


def transform(*args, **kwargs):
    """
    for args a1, b1, a2, b2,...
    Transform a1 to b1, a2 to b2, etc
    """
    assert(len(args) % 2 == 0)
    return Transform(VGroup(*args[0::2]), VGroup(*args[1::2]), **kwargs)


def rtransform(*args, **kwargs):
    """
    for args a1, b1, a2, b2,...
    ReplacementTransform a1 to b1, a2 to b2, etc
    """
    assert(len(args) % 2 == 0)
    return ReplacementTransform(VGroup(*args[0::2]), VGroup(*args[1::2]), **kwargs)


def circle_eq(eq) -> ParametricFunction:
    """
    create red curve around eq
    """
    points = [
        (eq.get_corner(UL) + eq.get_top()) * 0.5 + UP * 0.3,
        eq.get_corner(UR) + UR * 0.2 + RIGHT * 0.5,
        eq.get_corner(UR) + UR * 0.05 + RIGHT * 0.5,
        eq.get_right() + RIGHT * 0.1,
        eq.get_corner(DR) + DR * 0.05 + RIGHT * 0.5,
        eq.get_corner(DR) + DR * 0.2 + RIGHT * 0.5,
        eq.get_corner(DR) + DR * 0.2 + RIGHT * 0.5,
        eq.get_bottom() + DOWN * 0.2,
        eq.get_bottom() + DOWN * 0.2,
        eq.get_corner(DL) + DL * 0.2 + LEFT * 0.5,
        eq.get_corner(DL) + DL * 0.2 + LEFT * 0.5,
        eq.get_corner(DL) + DL * 0.05 + LEFT * 0.8,
        eq.get_corner(UL) + UL * 0.2 + LEFT * 0.8,
        eq.get_corner(UL) + UL * 0.2 + LEFT * 0.5,
        (eq.get_corner(UR) + eq.get_top()) * 0.5 + UP * 0.3,
    ]
    bez = bezier(points)
    plot = ParametricFunction(bez, color=RED, stroke_width=10).set_z_index(2)
    return plot


def brace_label(x):
    return lambda text, font_size: x


class label_ctr(Text):
    def __init__(self, text, font_size):
        Text.__init__(self, text, font_size=font_size, color=RED)


class mathlabel_ctr(MathTex):
    def __init__(self, text, font_size):
        MathTex.__init__(self, text, font_size=font_size)


class mathlabel_ctr2(MathTex):
    def __init__(self, text, font_size):
        MathTex.__init__(self, text, font_size=font_size, color=RED)


def label_ctrMU(text, font_size):
    return MarkupText(text, font_size=font_size, color=RED)
