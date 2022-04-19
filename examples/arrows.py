import hotkeys
from hotkeys import Hotkey

# Custom arrow keys example

# This makes hotkey stop running if there's an error
Hotkey.err_handler = Hotkey.ON_ERR_QUIT

# Always make sure you have a way to quit, here Shift + Escape will stop it
Hotkey('+{escape}', Hotkey.quit)

# remap wsad to arrow keys
arrows = [
    Hotkey('w', '{up}', raw=False),
    Hotkey('s', '{down}', raw=False),
    Hotkey('a', '{left}', raw=False),
    Hotkey('d', '{right}', raw=False),
]


# Enable/Disable arrow hotkeys
def toggle_keys(h):
    for x in arrows:
        x.unregister() if h.enabled else x.register()
    h.enabled = not h.enabled

# Control + 1 to toggle arrow hotkeys
h = Hotkey('^1', toggle_keys)
h.enabled = True

# This is a convenience method to prevent your script from exiting
Hotkey.wait()
