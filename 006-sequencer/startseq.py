import board
import analogio
import digitalio
import math
from adafruit_ht16k33 import segments

note_select_knob = analogio.AnalogIn(board.D2)
step_select_button = digitalio.DigitalInOut(board.D13)
step_select_button.direction = digitalio.Direction.INPUT
channel_select_switch = digitalio.DigitalInOut(board.D12)
channel_select_switch.direction = digitalio.Direction.INPUT
channel_select_switch.pull = digitalio.Pull.UP
step_count_select_knob = analogio.AnalogIn(board.A2)

# okay we have the basics,
# stuff left to do
# second channel
# step number select
# output ports
# clock pulse jack, same as button i guess.

i2c = board.I2C()
display = segments.Seg14x4(i2c)
display.brightness = 1

MAX_VALUE = 65536
NOTE_NAMES = ["A", "A.", "B", "C", "C.", "D", "D.", "E.", "F", "F.", "G", "G."]
TOTAL_NOTES = 88
TICKS_PER_NOTE = MAX_VALUE / TOTAL_NOTES
A0_FREQUENCY = 27.5

MAX_STEPS = 16
TICKS_PER_STEP_SELECT = MAX_VALUE / (MAX_STEPS + 1)
current_number_of_steps = MAX_STEPS
current_step = 0
steps_change_counter = 0

note_select_knob_running_value = note_select_knob.value
step_count_select_knob_running_value = step_count_select_knob.value
previous_step_select_button_state = step_select_button.value
previous_number_of_steps = current_number_of_steps

channel_one_step_memory = [48] * 16
channel_two_step_memory = [48] * 16
is_channel_one_active = True

KNOB_RESET_DISTANCE = 5000
note_select_knob_starting_position = 0
is_note_select_knob_active = False

while True:
    is_channel_one_active = channel_select_switch.value

    step_count_select_knob_running_value = (
        0.9 * step_count_select_knob_running_value
    ) + (0.1 * step_count_select_knob.value)

    current_number_of_steps = math.trunc(
        step_count_select_knob_running_value / TICKS_PER_STEP_SELECT
    )
    print(current_number_of_steps)

    # note select knob stuff
    note_select_knob_running_value = (0.9 * note_select_knob_running_value) + (
        0.1 * note_select_knob.value
    )

    if (
        is_note_select_knob_active == False
        and abs(note_select_knob_starting_position - note_select_knob_running_value)
        > KNOB_RESET_DISTANCE
    ):
        is_note_select_knob_active = True

    if is_note_select_knob_active:
        knob_note_number = math.trunc(note_select_knob_running_value / TICKS_PER_NOTE)
        selected_note_name = NOTE_NAMES[knob_note_number % 12]
        selected_note_octave = math.trunc(knob_note_number / 12)

    # current step select button stuff
    current_step_select_button_value = step_select_button.value
    if (
        previous_step_select_button_state == False
        and current_step_select_button_value == True
    ):
        if is_channel_one_active:
            channel_one_step_memory[current_step] = knob_note_number
        else:
            channel_two_step_memory[current_step] = knob_note_number
        current_step = (current_step + 1) % current_number_of_steps
        note_select_knob_starting_position = note_select_knob_running_value
        is_note_select_knob_active = False

        if is_channel_one_active:
            knob_note_number = channel_one_step_memory[current_step]
        else:
            knob_note_number = channel_two_step_memory[current_step]

        selected_note_name = NOTE_NAMES[knob_note_number % 12]
        selected_note_octave = math.trunc(knob_note_number / 12)

    # show the step change for a few frames
    if current_number_of_steps != previous_number_of_steps:
        steps_change_counter = 100
    if steps_change_counter > 0:
        steps_change_counter -= 1
        display.print(
            "("
            + str(current_number_of_steps)
            + (")" if current_number_of_steps > 9 else ") ")
        )
    else:
        display.print(
            (hex(current_step)[2]).upper()
            + (".)" if is_channel_one_active else ")")
            + selected_note_name
            + str(selected_note_octave)
        )

    print(channel_select_switch.value)

    previous_number_of_steps = current_number_of_steps
    previous_step_select_button_state = current_step_select_button_value
