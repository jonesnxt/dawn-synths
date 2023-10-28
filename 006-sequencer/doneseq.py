import board
import analogio
import digitalio
import math
from adafruit_ht16k33 import segments

note_select_knob = analogio.AnalogIn(board.A4)
step_advance_button = digitalio.DigitalInOut(board.D12)
step_advance_button.direction = digitalio.Direction.INPUT
step_advance_button.pull = digitalio.Pull.UP
step_advance_jack = analogio.AnalogIn(board.A3)

left_output_jack = analogio.AnalogOut(board.A0)
right_output_jack = analogio.AnalogOut(board.A1)

channel_select_switch = digitalio.DigitalInOut(board.D11)
channel_select_switch.direction = digitalio.Direction.INPUT
channel_select_switch.pull = digitalio.Pull.UP
step_count_select_knob = analogio.AnalogIn(board.A5)
step_count_select_jack = analogio.AnalogIn(board.D2)

i2c = board.I2C()
display = segments.Seg14x4(i2c)
display.brightness = 1

MAX_VALUE = 65536
GATE_THRESHOLD = 20000
NOTE_NAMES = ["A", "A.", "B", "C", "C.", "D", "D.", "E.", "F", "F.", "G", "G."]
TOTAL_NOTES = 88
TICKS_PER_NOTE = MAX_VALUE / TOTAL_NOTES
A0_FREQUENCY = 27.5

MAX_STEPS = 16
TICKS_PER_STEP_SELECT = MAX_VALUE / (MAX_STEPS + 1)
current_number_of_steps = MAX_STEPS
current_step = 0
steps_change_counter = 0

note_select_knob_running_value = MAX_VALUE - note_select_knob.value
step_count_select_knob_running_value = step_count_select_knob.value
step_advance_jack_running_value = step_advance_jack.value
previous_step_advance_button_state = step_advance_button.value
previous_number_of_steps = current_number_of_steps

channel_one_step_memory = [48] * 16
channel_two_step_memory = [48] * 16
is_channel_one_active = True
was_channel_one_active = True

KNOB_RESET_DISTANCE = 5000
note_select_knob_starting_position = 0
is_note_select_knob_active = False
is_step_advance_jack_high = False

while True:
    # if we change channels, reset our knob start position so we don't immediately overwrite anything
    is_channel_one_active = channel_select_switch.value
    if is_channel_one_active != was_channel_one_active:
        note_select_knob_starting_position = note_select_knob_running_value
        is_note_select_knob_active = False

        if is_channel_one_active:
            knob_note_number = channel_one_step_memory[current_step]
        else:
            knob_note_number = channel_two_step_memory[current_step]

        selected_note_name = NOTE_NAMES[knob_note_number % 12]
        selected_note_octave = math.trunc(knob_note_number / 12)

    was_channel_one_active = is_channel_one_active

    step_count_select_knob_running_value = (
        0.9 * step_count_select_knob_running_value
    ) + (0.1 * step_count_select_knob.value)

    current_number_of_steps = min(
        math.trunc(step_count_select_knob_running_value / TICKS_PER_STEP_SELECT)
        + math.trunc(step_count_select_jack.value / TICKS_PER_STEP_SELECT),
        16,
    )

    if current_number_of_steps == 0:
        current_number_of_steps = 1

    print(math.trunc(step_count_select_jack.value / TICKS_PER_STEP_SELECT))

    # note select knob stuff
    note_select_knob_running_value = (0.9 * note_select_knob_running_value) + (
        0.1 * (MAX_VALUE - note_select_knob.value)
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
        # store in memory early so we can sample the output value in real time
        if is_channel_one_active:
            channel_one_step_memory[current_step] = knob_note_number
        else:
            channel_two_step_memory[current_step] = knob_note_number

    # step advance stuff (note i might need debounce here)
    current_step_advance_button_value = step_advance_button.value
    current_step_advance_jack_value = step_advance_jack.value
    if (
        previous_step_advance_button_state == False
        and current_step_advance_button_value == True
    ) or (
        current_step_advance_jack_value > GATE_THRESHOLD
        and is_step_advance_jack_high == False
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
            + (
                "."
                if math.trunc(
                    step_count_select_knob_running_value / TICKS_PER_STEP_SELECT
                )
                == 0
                else ""
            )
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

    left_output_jack.value = math.trunc(
        channel_one_step_memory[current_step] * TICKS_PER_NOTE
    )
    right_output_jack.value = math.trunc(
        channel_two_step_memory[current_step] * TICKS_PER_NOTE
    )

    previous_number_of_steps = current_number_of_steps
    previous_step_advance_button_state = current_step_advance_button_value
    is_step_advance_jack_high = current_step_advance_jack_value > GATE_THRESHOLD
