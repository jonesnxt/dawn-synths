# ouput module
# real basic input right to output

import board
import analogio

left_in = analogio.AnalogIn(board.A2)
left_out = analogio.AnalogOut(board.A0)

while True:
    left_out.value = left_in.value
