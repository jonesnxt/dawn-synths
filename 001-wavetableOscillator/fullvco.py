import board
import analogio
import time
import math

MAX_VALUE = 65535
SAMPLES_PER_RECALIBRATION = 1000
MIN_FREQUENCY = 20
FREQUENCY_RANGE = 2000

out = analogio.AnalogOut(board.A0)
waveshape_knob = analogio.AnalogIn(board.A2)
frequency_knob = analogio.AnalogIn(board.A3)

sound_frequency = 200
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

    wave_value = min(max(wave_value + (wave_delta if (wave_index < (samples_per_wave / 2)) else -wave_delta), 0), MAX_VALUE)
    out.value = wave_value

    if recalibration_index == 0:
        new_time = time.monotonic_ns()
        samples_per_second = math.trunc((0.8 * samples_per_second) + (0.2 * SAMPLES_PER_RECALIBRATION / ((new_time - start_time) / 1000000000)))
        sound_frequency = math.trunc(MIN_FREQUENCY + (FREQUENCY_RANGE * (frequency_knob.value / MAX_VALUE)))
        samples_per_wave = math.trunc(samples_per_second / sound_frequency)
        minimum_wave_delta = MAX_VALUE / (samples_per_wave / 2)
        wave_delta = math.trunc(minimum_wave_delta + ((MAX_VALUE - minimum_wave_delta) * ((waveshape_knob.value / MAX_VALUE)**2)))

        wave_index += 4
        print(samples_per_second)
        start_time = new_time





