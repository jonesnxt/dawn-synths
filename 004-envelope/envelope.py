import board
import analogio
import digitalio
import math

out = analogio.AnalogOut(board.A0)

gate_jack = analogio.AnalogIn(board.A1)
gate_button = digitalio.DigitalInOut(board.D11)
gate_button.direction = digitalio.Direction.INPUT
gate_button.pull = digitalio.Pull.DOWN
gate_light = digitalio.DigitalInOut(board.D10)
gate_light.direction = digitalio.Direction.OUTPUT
gate_mode_switch = digitalio.DigitalInOut(board.D12)
gate_mode_switch.direction = digitalio.Direction.INPUT
gate_mode_switch.pull = digitalio.Pull.DOWN


attack_knob = analogio.AnalogIn(board.A2)
attack_jack = analogio.AnalogIn(board.A3)

release_knob = analogio.AnalogIn(board.A5)
release_jack = analogio.AnalogIn(board.A4)

GATE_THRESHOLD = 32000
MAX_VALUE = 65535

out_value = 0
gate_delta = 0
trigger_mode_is_gate_activated = False
trigger_mode_has_button_been_released = True

while True:
    is_gate = gate_jack.value > GATE_THRESHOLD or not gate_button.value
    attack_delta = (
        1 / (1 - min(((attack_knob.value + attack_jack.value) / MAX_VALUE), 0.999)) * 10
    )
    release_delta = (
        -1
        / (1 - min(((release_knob.value + release_jack.value) / MAX_VALUE), 0.999))
        * 10
    )

    if gate_mode_switch.value:
        # gate mode
        gate_delta = attack_delta if is_gate else release_delta
        gate_light.value = is_gate
    else:
        # trigger mode
        if (
            not trigger_mode_is_gate_activated
            and is_gate
            and trigger_mode_has_button_been_released
        ):
            trigger_mode_is_gate_activated = True
            trigger_mode_has_button_been_released = False
        if not is_gate and not trigger_mode_has_button_been_released:
            trigger_mode_has_button_been_released = True
        if trigger_mode_is_gate_activated and out_value == MAX_VALUE:
            trigger_mode_is_gate_activated = False

        gate_delta = attack_delta if trigger_mode_is_gate_activated else release_delta
        gate_light.value = trigger_mode_is_gate_activated

    out_value = min(max(out_value + gate_delta, 0), 65535)
    out.value = math.trunc(out_value)
    print(attack_delta)
