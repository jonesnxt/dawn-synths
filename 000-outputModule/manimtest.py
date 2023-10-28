from manim import *
import math


class SquareToCircle(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 100], y_range=[0, 2], axis_config={"include_tip": False})

        axes_labels = ax.get_axis_labels()
        curve_1 = ax.plot(
            lambda x: math.sqrt(2 + (2 * math.cos(x / 2))),
            x_range=[0, 100],
            color=BLUE_C,
        )
        curve_2 = ax.plot(
            lambda x: math.sqrt(2 + (2 * math.cos(x / 3))),
            x_range=[0, 100],
            color=BLUE_A,
        )

        self.play(Create(ax), Write(axes_labels))
        self.wait()
        self.play(Create(curve_1))
        self.wait()
        self.play(Create(curve_2))
        self.wait()
