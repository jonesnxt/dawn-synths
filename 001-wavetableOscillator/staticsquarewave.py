import board
import analogio
import time
import math

MAX_VALUE = 65535
SAMPLES_PER_RECALIBRATION = 1000

out = analogio.AnalogOut(board.A0)

sound_frequency = 200
samples_per_second = 37000
samples_per_wave = math.trunc(samples_per_second / sound_frequency)

recalibration_index = 0
wave_index = 0
start_time = time.monotonic_ns()

while True:
    recalibration_index = (recalibration_index + 1) % SAMPLES_PER_RECALIBRATION
    wave_index = (wave_index + 1) % samples_per_wave

    out.value = 0 if wave_index < (samples_per_wave / 2) else MAX_VALUE

    if recalibration_index == 0:
        new_time = time.monotonic_ns()
        samples_per_second = math.trunc((0.8 * samples_per_second) + (0.2 * SAMPLES_PER_RECALIBRATION / ((new_time - start_time) / 1000000000)))
        samples_per_wave = math.trunc(samples_per_second / sound_frequency)
        wave_index += 4
        start_time = new_time
