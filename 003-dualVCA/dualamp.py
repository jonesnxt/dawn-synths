import analogio
import board
import math

MAX_VALUE = 2**16

left_out = analogio.AnalogOut(board.A0)
right_out = analogio.AnalogOut(board.A1)

left_in = analogio.AnalogIn(board.A4)
right_in = analogio.AnalogIn(board.A5)

left_amplitude = analogio.AnalogIn(board.A2)
right_amplitude = analogio.AnalogIn(board.A3)

global_amplitude = analogio.AnalogIn(board.D2)

while True:
    global_adjustment = global_amplitude.value / MAX_VALUE

    left = math.trunc(
        left_in.value * (left_amplitude.value / MAX_VALUE) * global_adjustment
    )
    right = math.trunc(
        right_in.value * (right_amplitude.value / MAX_VALUE) * global_adjustment
    )

    left_out.value = left
    right_out.value = right
