import board
import analogio
import math
import time

MAX_VALUE = 65536
SAMPLES_PER_RECALIBRATION = 200

MINIMUM_LOOP_MS = 50
MAXIMUM_LOOP_MS = 8000
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
loop_memory = bytearray(100000)
loop_position = 0
calibration_position = 0

start_time = time.monotonic_ns()

wet_multiplier = dry_wet_knob.value >> 8
feedback_multiplier = min(MAX_VALUE, feedback_knob.value + feedback_jack.value) >> 8

# okay we just need external clock pulse idk about that tho.

while True:
    loop_position = (loop_position + 1) % samples_per_loop
    calibration_position = (calibration_position + 1) % SAMPLES_PER_RECALIBRATION

    input_value = input_jack.value

    output_jack.value = ((input_value >> 8) * (256 - wet_multiplier)) + (
        loop_memory[loop_position] * wet_multiplier
    )

    loop_memory[loop_position] = min(
        (input_value + ((loop_memory[loop_position]) * feedback_multiplier)) >> 8, 255
    )

    # recalibration time?
    if calibration_position == 0:
        new_time = time.monotonic_ns()

        # read our inputs only once per recalibration
        wet_multiplier = dry_wet_knob.value >> 8
        feedback_multiplier = (
            min(MAX_VALUE, feedback_knob.value + feedback_jack.value) >> 8
        )

        samples_per_second = math.trunc(
            (0.9 * samples_per_second)
            + (
                0.1
                * (SAMPLES_PER_RECALIBRATION / ((new_time - start_time) / 1000000000))
            )
        )

        loop_ms = MINIMUM_LOOP_MS + (pow(time_knob.value / MAX_VALUE, 2) * LOOP_RANGE)
        samples_per_loop = math.trunc(samples_per_second * (loop_ms / 1000))
        if samples_per_loop > 100000:
            samples_per_loop = 100000
        print(samples_per_second)

        start_time = time.monotonic_ns()
