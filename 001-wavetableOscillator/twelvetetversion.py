import board
import analogio
import time
import math

MAX_VALUE = 65535
SAMPLES_PER_RECALIBRATION = 200
A0_FREQUENCY = 27.5
C8_FREQUENCY = 4186
TOTAL_NOTES = 88
TICKS_PER_NOTE = MAX_VALUE / TOTAL_NOTES
FREQUENCY_RANGE = C8_FREQUENCY - A0_FREQUENCY

out = analogio.AnalogOut(board.A0)
waveshape_knob = analogio.AnalogIn(board.A2)
waveshape_jack = analogio.AnalogIn(board.A3)
frequency_knob = analogio.AnalogIn(board.A4)
frequency_jack = analogio.AnalogIn(board.A5)

frequency_knob_running_value = MAX_VALUE - frequency_knob.value

sound_frequency = 440
samples_per_second = 37000
samples_per_wave = math.trunc(samples_per_second / sound_frequency)

recalibration_index = 0
wave_index = 0
wave_delta = MAX_VALUE
wave_value = 0
start_time = time.monotonic_ns()

while True:
    recalibration_index = (recalibration_index + 1) % SAMPLES_PER_RECALIBRATION
    wave_index = (wave_index + 1) % samples_per_wave

    wave_value = min(
        max(
            wave_value
            + (wave_delta if (wave_index < (samples_per_wave / 2)) else -wave_delta),
            0,
        ),
        MAX_VALUE,
    )
    out.value = wave_value

    if recalibration_index == 0:
        new_time = time.monotonic_ns()
        samples_per_second = math.trunc(
            (0.8 * samples_per_second)
            + (0.2 * SAMPLES_PER_RECALIBRATION / ((new_time - start_time) / 1000000000))
        )

        frequency_jack_value = frequency_jack.value
        # treat any frequency jack value as an override
        if frequency_jack_value > 500:
            # 12 tet time
            sound_frequency = A0_FREQUENCY * math.pow(
                2, math.trunc(frequency_jack_value / TICKS_PER_NOTE) / 12
            )
        else:
            frequency_knob_running_value = (0.8 * frequency_knob_running_value) + (
                0.2 * (MAX_VALUE - frequency_knob.value)
            )
            sound_frequency = A0_FREQUENCY * math.pow(
                2, math.trunc(frequency_knob_running_value / TICKS_PER_NOTE) / 12
            )

        print(sound_frequency)
        samples_per_wave = samples_per_second / sound_frequency
        minimum_wave_delta = MAX_VALUE / (samples_per_wave / 2)
        wave_delta = math.trunc(
            minimum_wave_delta
            + (
                (MAX_VALUE - minimum_wave_delta)
                * (((waveshape_knob.value + waveshape_jack.value) / MAX_VALUE) ** 2)
            )
        )

        wave_index += samples_per_second * (
            (time.monotonic_ns() - new_time) / 1000000000
        )
        start_time = new_time
