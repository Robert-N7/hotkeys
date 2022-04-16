# This example shows how you can remap your key modifiers on Ubuntu
# This can be useful to create hotkeys specific to your keyboard,
# or to modify your keyboard to map to specific modifier masks

import hotkeys
from hotkeys import Hotkey, linux_key_bind
from Xlib import X


# This command sets your key map that will automatically be loaded on startup
# by adding a command to your .bashrc file. You only need to run this once.
# In this example, Control_R is separated (control events will no longer be triggered)
# and placed in the mod3 slot. ALT_R is separated and placed over Num_Lock (alt events no longer triggered)
# linux_key_bind.set_key_map({
#     'Control': 'Control_L',
#     'mod1': 'Alt_L',
#     'mod2': 'Alt_R',
#     'mod3': 'Control_R',
#     'mod4': 'Super_L',
#     'mod5': 'Super_R',
# })

# This tells hotkey about your key remap.
# You'll need to run this every time you want to customize your hotkeys
ignore_modifiers = [
    X.LockMask,     # These modifiers are ignored (hotkey still triggers even if capslock is engaged)
]
hotkeys.set_key_map({
    'CtrlLeft': X.ControlMask,
    'AltLeft': X.Mod1Mask,
    'AltRight': X.Mod2Mask,
    'CtrlRight': X.Mod3Mask,
}, ignore_modifiers)

# If there is an error when running a hotkey, stop
Hotkey.err_handler = Hotkey.ON_ERR_QUIT

# Now we can use AltLeft, CtrlLeft, AltRight, CtrlRight, or any other modifier you choose
# AltLeft+m sends Hi
Hotkey('{AltLeft}m', 'Hi')
# Shift+Escape to quit
Hotkey('+{escape}', Hotkey.quit)
Hotkey('^1', Hotkey.toggle_pause)


Hotkey('{AltRight}m', 'Hi!', raw=True)
Hotkey('{CtrlRight}m', 'Hello world!', raw=True)
Hotkey('{CtrlLeft}m', 'Hello world2!', raw=True)

# Note that since Right Alt is no longer mapped to the alt modifier, it will no longer trigger
# regular alt hotkeys. Only Left Alt will trigger this one
Hotkey('!y', 'Hello world Alt', raw=True)


Hotkey.wait()
