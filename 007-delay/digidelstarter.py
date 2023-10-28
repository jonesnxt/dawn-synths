# eee


# okay what needs to get done here
# gotta go at one, start getting ready soon,
# initialize, main loop as fast as possible.
# same offset sync method as the other thing i think. eh maybe.
# ooh, if its a variable frame rate all of this is really confusing.

# okay i just feel unconfortable, its not fun.

# initialize
import board
import analogio
import math
import time

MAX_VALUE = 65536
SAMPLES_PER_RECALIBRATION = 200

MINIMUM_LOOP_MS = 50
MAXIMUM_LOOP_MS = 3000
LOOP_RANGE = MAXIMUM_LOOP_MS - MINIMUM_LOOP_MS

input_jack = analogio.AnalogIn(board.D2)
output_jack = analogio.AnalogOut(board.A1)

clock_input_jack = analogio.AnalogIn(board.A0)
time_knob = analogio.AnalogIn(board.A2)
feedback_jack = analogio.AnalogIn(board.A5)
feedback_knob = analogio.AnalogIn(board.A3)

dry_wet_knob = analogio.AnalogIn(board.A4)

samples_per_second = 9000
samples_per_loop = 30000
loop_memory = [0] * samples_per_loop
loop_position = 0

start_time = time.monotonic_ns()

wet_percent = dry_wet_knob.value / MAX_VALUE
feedback_percent = min(MAX_VALUE, feedback_knob.value + feedback_jack.value) / MAX_VALUE

# okay we just need external clock pulse idk about that tho.

while True:
    loop_position = (loop_position + 1) % samples_per_loop

    input_value = input_jack.value

    output_jack.value = math.trunc(
        (input_value * (1 - wet_percent)) + (loop_memory[loop_position] * wet_percent)
    )

    loop_memory[loop_position] = min(
        input_value + (loop_memory[loop_position] * feedback_percent),
        MAX_VALUE,
    )

    # recalibration time?
    if loop_position % SAMPLES_PER_RECALIBRATION == 0:
        new_time = time.monotonic_ns()

        # read our inputs only once per recalibration
        wet_percent = dry_wet_knob.value / MAX_VALUE
        feedback_percent = (
            min(MAX_VALUE, feedback_knob.value + feedback_jack.value) / MAX_VALUE
        )

        samples_per_second = math.trunc(
            (0.9 * samples_per_second)
            + (0.1 * SAMPLES_PER_RECALIBRATION / ((new_time - start_time) / 1000000000))
        )

        loop_ms = MINIMUM_LOOP_MS + (pow(time_knob.value / MAX_VALUE, 2) * LOOP_RANGE)
        samples_per_loop = math.trunc(samples_per_second * (loop_ms / 1000))
        if samples_per_loop > 30000:
            samples_per_loop = 30000
        print(samples_per_second)

        start_time = time.monotonic_ns()
