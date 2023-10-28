import board
import analogio
import time
import math

output_jack = analogio.AnalogOut(board.A0)
input_jack = analogio.AnalogIn(board.A1)
dry_wet_knob = analogio.AnalogIn(board.A5)

room_size_knob = analogio.AnalogIn(board.D2)
room_size_jack = analogio.AnalogIn(board.A2)
decay_time_knob = analogio.AnalogIn(board.A4)
decay_time_jack = analogio.AnalogIn(board.A3)

MAX_VALUE = 65536
SAMPLES_PER_RECALIBRATION = 200
samples_per_second = 9000

COMB_ONE_BASE = 3
COMB_TWO_BASE = 5
COMB_THREE_BASE = 7
COMB_FOUR_BASE = 11

wet_percent = dry_wet_knob.value / MAX_VALUE
room_size_multiplier = (room_size_knob.value + room_size_jack.value) >> 8
decay_multiplier = min(
    MAX_VALUE, (decay_time_knob.value + decay_time_jack.value) / MAX_VALUE
)

comb_one_offset = COMB_ONE_BASE * room_size_multiplier
comb_two_offset = COMB_TWO_BASE * room_size_multiplier
comb_three_offset = COMB_THREE_BASE * room_size_multiplier
comb_four_offset = COMB_FOUR_BASE * room_size_multiplier

LOOP_MEMORY_SIZE = 10000
loop_memory = [0] * LOOP_MEMORY_SIZE
comb_memory = [0] * LOOP_MEMORY_SIZE
loop_position = 0
calibration_position = 0

start_time = time.monotonic_ns()

# okay we just need external clock pulse idk about that tho.

while True:
    loop_position = (loop_position + 1) % LOOP_MEMORY_SIZE
    calibration_position = (calibration_position + 1) % SAMPLES_PER_RECALIBRATION

    input_value = input_jack.value

    comb_value = (
        loop_memory[loop_position - comb_one_offset % LOOP_MEMORY_SIZE]
        + loop_memory[loop_position - comb_two_offset % LOOP_MEMORY_SIZE]
        + loop_memory[loop_position - comb_three_offset % LOOP_MEMORY_SIZE]
        + loop_memory[loop_position - comb_four_offset % LOOP_MEMORY_SIZE]
    ) / 4

    allpass_one = comb_value * (1 - decay_multiplier) + (
        comb_memory[loop_position - 13 % LOOP_MEMORY_SIZE] * decay_multiplier
    )
    allpass_two = allpass_one * (1 - decay_multiplier) + (
        comb_memory[loop_position - 17 % LOOP_MEMORY_SIZE] * decay_multiplier
    )

    comb_memory[loop_position] = comb_value

    loop_memory[loop_position] = min(
        MAX_VALUE, (input_value + (comb_value * decay_multiplier))
    )
    output_jack.value = math.trunc(
        input_value * (1 - wet_percent) + (allpass_two * wet_percent)
    )

    print(comb_value)

    # recalibration time?
    if calibration_position == 0:
        new_time = time.monotonic_ns()

        # read our inputs only once per recalibration
        wet_percent = dry_wet_knob.value / MAX_VALUE
        room_size_multiplier = (room_size_knob.value + room_size_jack.value) >> 8
        decay_multiplier = min(
            MAX_VALUE,
            ((MAX_VALUE - decay_time_knob.value) + decay_time_jack.value) / MAX_VALUE,
        )

        comb_one_offset = COMB_ONE_BASE * room_size_multiplier
        comb_two_offset = COMB_TWO_BASE * room_size_multiplier
        comb_three_offset = COMB_THREE_BASE * room_size_multiplier
        comb_four_offset = COMB_FOUR_BASE * room_size_multiplier

        samples_per_second = math.trunc(
            (0.9 * samples_per_second)
            + (
                0.1
                * (SAMPLES_PER_RECALIBRATION / ((new_time - start_time) / 1000000000))
            )
        )
        print(decay_multiplier)

        start_time = time.monotonic_ns()


while True:
    print(decay_time_knob.value)
