from hotkeys import Hotkey

h = Hotkey('!d', 'Hello world!', raw=True)
x = []
# create error
Hotkey.err_handler = Hotkey.ON_ERR_CONTINUE
# Hotkey.err_handler = Hotkey.ON_ERR_QUIT
Hotkey('^1', lambda h: x[0])

Hotkey.wait()
