
import hotkeys
from hotkeys import Hotkey

# Hello World Example

# This makes hotkey stop running if there's an error
Hotkey.err_handler = Hotkey.ON_ERR_QUIT

# Always make sure you have a way to quit, here Shift + Escape will stop it
Hotkey('+{escape}', Hotkey.quit)

# Note the ease of access modifiers
# ^ = control
# + = shift
# ! = alt
# Control + h to send Hello world!
Hotkey('^h', 'Hello world!', raw=True)
Hotkey('!+h', lambda h: hotkeys.send('^+{left}'))


# This is a convenience method to prevent your script from exiting
Hotkey.wait()
