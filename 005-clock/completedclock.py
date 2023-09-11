import board
import analogio
import digitalio
import time
import math
from adafruit_ht16k33 import segments

# okay we need to check for change in either knob, then output if it is changed.

i2c = board.I2C()
display = segments.Seg14x4(i2c)
display.brightness = 1

tempo_knob = analogio.AnalogIn(board.D2)
tempo_out = digitalio.DigitalInOut(board.D13)
tempo_out.direction = digitalio.Direction.OUTPUT

subtempo_one_knob = analogio.AnalogIn(board.A2)
swing_one_knob = analogio.AnalogIn(board.A3)
subtempo_one_out = digitalio.DigitalInOut(board.D9)
subtempo_one_out.direction = digitalio.Direction.OUTPUT

subtempo_two_knob = analogio.AnalogIn(board.A1)
swing_two_knob = analogio.AnalogIn(board.A4)
subtempo_two_out = digitalio.DigitalInOut(board.D10)
subtempo_two_out.direction = digitalio.Direction.OUTPUT

subtempo_three_knob = analogio.AnalogIn(board.A0)
swing_three_knob = analogio.AnalogIn(board.A5)
subtempo_three_out = digitalio.DigitalInOut(board.D11)
subtempo_three_out.direction = digitalio.Direction.OUTPUT

start_time = time.monotonic_ns()

MAX_VALUE = 65535
TEMPO_MAX = 150
TEMPO_MIN = 60
TEMPO_RANGE = TEMPO_MAX - TEMPO_MIN
STEP_SIZE = 1

SUBTEMPO_MAX = 21
SUBTEMPO_MIN = -40
SUBTEMPO_RANGE = SUBTEMPO_MAX - SUBTEMPO_MIN

SWING_MAX = 100
SWING_MIN = -100
SWING_RANGE = SWING_MAX - SWING_MIN

previous_tempo = 0
current_tempo = 120
current_subtempo_one = 1
previous_subtempo_one = 1
current_swing_one = 0
previous_swing_one = 0

current_subtempo_two = 1
previous_subtempo_two = 1
current_swing_two = 0
previous_swing_two = 0

current_subtempo_three = 1
previous_subtempo_three = 1
current_swing_three = 0
previous_swing_three = 0

# okay organize my thoughts its tough to think currently which is tough
# it takes some time to settle into it which is ultimately okay. fuzzy brain only goes for so long
# hopefully. okay we have two knobs one controls tempo which is an integer from 1/16 to 16x
# and the other one is swing which is from plus to minus one hundred

while True:
    current_tempo = math.trunc(
        ((TEMPO_MIN + ((tempo_knob.value / MAX_VALUE) * TEMPO_RANGE)) * 0.1)
        + (current_tempo * 0.9)
    )

    # if we change tempo, don't worry and just start over
    if current_tempo != previous_tempo:
        start_time = time.monotonic_ns()
        display.print((" " if current_tempo > 100 else "  ") + str(current_tempo))
        print("changed tempo")
        previous_tempo = current_tempo

    nanoseconds_per_beat = 60000000000 / current_tempo
    current_time_elapsed = time.monotonic_ns() - start_time
    should_tempo_be_high = current_time_elapsed % nanoseconds_per_beat > (
        nanoseconds_per_beat / 2
    )

    current_subtempo_one = math.trunc(
        (
            (SUBTEMPO_MIN + ((subtempo_one_knob.value / MAX_VALUE) * SUBTEMPO_RANGE))
            * 0.2
        )
        + (current_subtempo_one * 0.8)
    )

    # quick hack to fix a divide by zero issue
    if current_subtempo_one == 0:
        current_subtempo_one = 1

    if current_subtempo_one != previous_subtempo_one:
        previous_subtempo_one = current_subtempo_one
        display.print(
            " " + str(current_subtempo_one).replace("-", "1/")
            if str(current_subtempo_one)[0] == "-"
            else "   " + str(current_subtempo_one) + "X"
        )

    current_swing_one = math.trunc(
        ((SWING_MIN + ((swing_one_knob.value / MAX_VALUE) * SWING_RANGE)) * 0.05)
        + (current_swing_one * 0.95)
    )

    if current_swing_one != previous_swing_one:
        previous_swing_one = current_swing_one
        display.print(
            "  +" + str(current_swing_one)
            if current_swing_one > 0
            else "   " + str(current_swing_one)
        )

    nanoseconds_per_subtempo_one_flat_beat = (
        -1 * nanoseconds_per_beat * current_subtempo_one
        if current_subtempo_one < 0
        else nanoseconds_per_beat / abs(current_subtempo_one)
    )

    nanoseconds_per_subtempo_one_skew_beat = nanoseconds_per_subtempo_one_flat_beat * (
        (2 * (current_swing_one + SWING_MAX)) / SWING_RANGE
    )

    subtempo_one_current_beat_position = current_time_elapsed % (
        nanoseconds_per_subtempo_one_flat_beat * 2
    )

    should_subtempo_one_be_high = (
        subtempo_one_current_beat_position < nanoseconds_per_subtempo_one_skew_beat
        and subtempo_one_current_beat_position
        > nanoseconds_per_subtempo_one_skew_beat / 2
    ) or (
        subtempo_one_current_beat_position > nanoseconds_per_subtempo_one_skew_beat
        and subtempo_one_current_beat_position
        > (
            (nanoseconds_per_subtempo_one_flat_beat * 2)
            - (
                (
                    (nanoseconds_per_subtempo_one_flat_beat * 2)
                    - nanoseconds_per_subtempo_one_skew_beat
                )
                / 2
            )
        )
    )

    # and now two
    current_subtempo_two = math.trunc(
        (
            (SUBTEMPO_MIN + ((subtempo_two_knob.value / MAX_VALUE) * SUBTEMPO_RANGE))
            * 0.2
        )
        + (current_subtempo_two * 0.8)
    )

    # quick hack to fix a divide by zero issue
    if current_subtempo_two == 0:
        current_subtempo_two = 1

    if current_subtempo_two != previous_subtempo_two:
        previous_subtempo_two = current_subtempo_two
        display.print(
            " " + str(current_subtempo_two).replace("-", "1/")
            if str(current_subtempo_two)[0] == "-"
            else "   " + str(current_subtempo_two) + "X"
        )

    current_swing_two = math.trunc(
        ((SWING_MIN + ((swing_two_knob.value / MAX_VALUE) * SWING_RANGE)) * 0.05)
        + (current_swing_two * 0.95)
    )

    if current_swing_two != previous_swing_two:
        previous_swing_two = current_swing_two
        display.print(
            "  +" + str(current_swing_two)
            if current_swing_two > 0
            else "   " + str(current_swing_two)
        )

    nanoseconds_per_subtempo_two_flat_beat = (
        -1 * nanoseconds_per_beat * current_subtempo_two
        if current_subtempo_two < 0
        else nanoseconds_per_beat / abs(current_subtempo_two)
    )

    nanoseconds_per_subtempo_two_skew_beat = nanoseconds_per_subtempo_two_flat_beat * (
        (2 * (current_swing_two + SWING_MAX)) / SWING_RANGE
    )

    subtempo_two_current_beat_position = current_time_elapsed % (
        nanoseconds_per_subtempo_two_flat_beat * 2
    )

    should_subtempo_two_be_high = (
        subtempo_two_current_beat_position < nanoseconds_per_subtempo_two_skew_beat
        and subtempo_two_current_beat_position
        > nanoseconds_per_subtempo_two_skew_beat / 2
    ) or (
        subtempo_two_current_beat_position > nanoseconds_per_subtempo_two_skew_beat
        and subtempo_two_current_beat_position
        > (
            (nanoseconds_per_subtempo_two_flat_beat * 2)
            - (
                (
                    (nanoseconds_per_subtempo_two_flat_beat * 2)
                    - nanoseconds_per_subtempo_two_skew_beat
                )
                / 2
            )
        )
    )

    # and now three
    current_subtempo_three = math.trunc(
        (
            (SUBTEMPO_MIN + ((subtempo_three_knob.value / MAX_VALUE) * SUBTEMPO_RANGE))
            * 0.2
        )
        + (current_subtempo_three * 0.8)
    )

    # quick hack to fix a divide by zero issue
    if current_subtempo_three == 0:
        current_subtempo_three = 1

    if current_subtempo_three != previous_subtempo_three:
        previous_subtempo_three = current_subtempo_three
        display.print(
            " " + str(current_subtempo_three).replace("-", "1/")
            if str(current_subtempo_three)[0] == "-"
            else "   " + str(current_subtempo_three) + "X"
        )

    current_swing_three = math.trunc(
        ((SWING_MIN + ((swing_three_knob.value / MAX_VALUE) * SWING_RANGE)) * 0.05)
        + (current_swing_three * 0.95)
    )

    if current_swing_three != previous_swing_three:
        previous_swing_three = current_swing_three
        display.print(
            "  +" + str(current_swing_three)
            if current_swing_three > 0
            else "   " + str(current_swing_three)
        )

    nanoseconds_per_subtempo_three_flat_beat = (
        -1 * nanoseconds_per_beat * current_subtempo_three
        if current_subtempo_three < 0
        else nanoseconds_per_beat / abs(current_subtempo_three)
    )

    nanoseconds_per_subtempo_three_skew_beat = (
        nanoseconds_per_subtempo_three_flat_beat
        * ((2 * (current_swing_three + SWING_MAX)) / SWING_RANGE)
    )

    subtempo_three_current_beat_position = current_time_elapsed % (
        nanoseconds_per_subtempo_three_flat_beat * 2
    )

    should_subtempo_three_be_high = (
        subtempo_three_current_beat_position < nanoseconds_per_subtempo_three_skew_beat
        and subtempo_three_current_beat_position
        > nanoseconds_per_subtempo_three_skew_beat / 2
    ) or (
        subtempo_three_current_beat_position > nanoseconds_per_subtempo_three_skew_beat
        and subtempo_three_current_beat_position
        > (
            (nanoseconds_per_subtempo_three_flat_beat * 2)
            - (
                (
                    (nanoseconds_per_subtempo_three_flat_beat * 2)
                    - nanoseconds_per_subtempo_three_skew_beat
                )
                / 2
            )
        )
    )

    tempo_out.value = should_tempo_be_high
    subtempo_one_out.value = should_subtempo_one_be_high
    subtempo_two_out.value = should_subtempo_two_be_high
    subtempo_three_out.value = should_subtempo_three_be_high
