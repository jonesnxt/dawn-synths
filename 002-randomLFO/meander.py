import board
import analogio
import time
import math

knob = analogio.AnalogIn(board.A3)
jack = analogio.AnalogIn(board.A1)
out = analogio.AnalogOut(board.A0)

random_number = 2**15;
previous_random = random_number;

acceleration = 2**15;
previous_acceleration = acceleration;

velocity = 2**15;
previous_velocity = velocity;

position = 2**15;
previous_position = position;

scaled_position = 2**15;
previous_scaled_position = 2**15;

while True:
    random_number = ((previous_random + 2013) * 10061) % 65521;

    acceleration = (random_number >> 4) + ((previous_acceleration >> 4) * 15);
    velocity = (acceleration >> 4) + ((previous_velocity >> 4) * 15);
    position = (velocity >> 4) + ((previous_position >> 4) * 15);

    scaled_position = max(min((((position - 2**15) * 6)) + 2**15, 65535), 0);

    steps = (math.trunc(math.pow((knob.value + jack.value) >> 8, 2)) >> 8) + 1;
    step_amount = ((scaled_position - previous_scaled_position) / steps);
    for k in range(0, steps):
        interpolated_value = previous_scaled_position + math.trunc(step_amount * k);
        out.value = interpolated_value;

    previous_random = random_number;
    previous_acceleration = acceleration;
    previous_velocity = velocity;
    previous_position = position;
    previous_scaled_position = scaled_position;


