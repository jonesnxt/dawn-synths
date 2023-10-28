# okay what all do i want on this thing?

# circuit diagram with a box around cap, sponge, then filter cutoff diagram
# show equation, fill in with numbers?
# show result.

# frequency explaination ugh okay brain hurts want food hard to focus
# what is there to do today, record,

# oh god okay ugh oof ack lay down time? maybe,


# okay it never ends its always something i just wanna make some progress what am i doing today
# cut nails itll be better? yeah thats quit a bit nicer lets go

# okay its monday and i wanna feel like ive done a lot of stiff
# not outside today i think its in inside day,
# all i need to do is figure out what the animations are going to be
# write the animations
# edit the animations into the working video
# add all of the extra comments and stuff to the video
# background music play around i wanna make no music for parts but i think i'm going to not do that becaue of the mouth sounds im self concious about idk.
# ugh being in the middle of history is exhausting.
# okay the notes part is going to be text based i think so its just the
# signal decomposition into two equation solvings, honestly pretty doable

from manim import *


class SignalDecompose(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": BLUE},
            tips=False,
        )
        axes_labels = axes.get_axis_labels()
        start_graph = axes.plot(
            lambda x: 0.8 * np.sin(x) + 0.2 * np.sin(x * 10), color=WHITE
        )
        small_graph = (
            axes.plot(lambda x: 0.2 * np.sin(x * 10), color=WHITE)
            .move_to(DOWN * 2 + LEFT * 3)
            .scale(0.4)
        )

        big_graph = (
            axes.plot(lambda x: 0.8 * np.sin(x), color=WHITE)
            .move_to(UP + RIGHT * 3)
            .scale(0.4)
        )

        self.play(Create(start_graph))
        self.wait()
        self.play(start_graph.animate.scale(0.4).move_to(UP + LEFT * 3))
        self.play(TransformFromCopy(start_graph, small_graph))
        self.play(Transform(start_graph, big_graph))
        self.play(FadeOut(small_graph))
        self.remove(start_graph)
        self.play(big_graph.animate.move_to(UP + RIGHT * 10))
        self.wait()


class SolveLowPass(Scene):
    def construct(self):
        si = TexTemplate()
        si.add_to_preamble(r"\usepackage{siunitx}")

        start_eq = MathTex(r"f = \frac{1}{2\pi RC}")
        question_mark = MathTex("?", color=BLUE).move_to(DOWN * 3 + RIGHT * 6).scale(4)
        circle = Circle(color=BLUE, stroke_width=10).move_to(DOWN * 5 + RIGHT * 7)
        values_eq = MathTex(
            r"f = \frac{1}{2\pi * 50\si{\kilo\ohm} * 1\si{\micro\farad}}",
            tex_template=si,
        ).move_to(UP)
        delineated_eq = MathTex(
            r"f = \frac{1}{2\pi * 50000\si{\ohm} * 0.000001\si{\farad}}",
            tex_template=si,
        ).move_to(DOWN)

        half_solved_eq = MathTex(
            r"f = \frac{10}{\pi}",
        ).move_to(DOWN * 3)

        full_solved_eq = MathTex(
            r"f = \frac{10}{\pi} = ~3.2\si{\hertz}", tex_template=si
        ).move_to(DOWN * 3)
        self.play(Write(start_eq))
        self.wait()
        self.add(circle)
        self.play(circle.animate.shift(UP * 2 + LEFT))
        self.wait()
        self.play(Write(question_mark))
        self.wait()
        self.play(Unwrite(question_mark))
        self.play(Uncreate(circle))
        self.play(start_eq.animate.shift(UP * 3))
        self.wait()
        self.play(TransformFromCopy(start_eq, values_eq))
        self.wait()
        self.play(TransformFromCopy(values_eq, delineated_eq))
        self.wait()
        self.play(TransformFromCopy(delineated_eq, half_solved_eq))
        self.wait()
        self.play(FadeTransform(half_solved_eq, full_solved_eq))
        self.wait()


class SolveTwelveTet(Scene):
    def construct(self):
        si = TexTemplate()
        si.add_to_preamble(r"\usepackage{siunitx}")

        start_eq = MathTex(r"f = b2^{(\frac{n}{12})}").scale(2)
        with_hz = MathTex(
            r"f = 27.5\si{\hertz} * 2^{(\frac{n}{12})}", tex_template=si
        ).scale(2)

        ln = NumberLine(
            x_range=[27.5, 76.5, 27.5],
            include_tip=True,
            include_numbers=True,
            stroke_width=6,
            length=8,
        ).move_to(DOWN)

        self.play(Write(start_eq))
        self.wait()
        self.play(FadeTransform(start_eq, with_hz))
        self.wait()
        self.remove(start_eq)
        self.play(with_hz.animate.shift(UP))
        self.play(Create(ln))
        self.wait()
        for i in range(1, 17):
            self.play(Create(ln.get_tick(27.5 * 2 ** (i / 12))))
        self.wait()


# 1/2piRC

# b*2^(n/12)
