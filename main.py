from hotkeys import Hotkey

Hotkey('+{escape}', Hotkey.quit)
h = Hotkey('^d', 'Hello world!', raw=True)
x = []
# create error
Hotkey.err_handler = Hotkey.ON_ERR_CONTINUE
# Hotkey.err_handler = Hotkey.ON_ERR_QUIT
Hotkey('^1', Hotkey.toggle_pause)


Hotkey.wait()
