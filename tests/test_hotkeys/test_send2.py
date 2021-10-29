import time
from hotkeys import send
time.sleep(1)
start = time.time()

from pynput import keyboard

START = None

def on_press(key):
    global START
    START = time.time()
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    elif key == keyboard.Key.ctrl:
        print(f'Released after {time.time() - START}')

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
