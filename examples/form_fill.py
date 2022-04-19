import random

from hotkeys import Hotkey, send

# Example to fill a form automatically with random numbers

# Shift + Escape to stop
Hotkey('+{escape}', Hotkey.quit)


def fill_fields(h):
    field_len = int(h.keys[-1])
    s = ''
    for i in range(field_len):
        s += str(random.randint(1, 50))
        s += '{tab}'
    send(s)

# Create Numbered hotkeys, Control + 5 will fill out 5 fields
for i in range(1, 10):
    Hotkey(f'^{i}', fill_fields)

def create_multiplication_table(h):
    digit = int(h.keys[-1])
    for i in range(1, digit + 1):
        send(f'{i}x{digit}={i*digit}' + '{return}')

# alt + 1 - 9 will create a multiplication table up to that number
for i in range(1, 10):
    Hotkey(f'!{i}', create_multiplication_table)

Hotkey.wait()

