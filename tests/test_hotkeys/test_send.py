import time

from pynput import keyboard

from hotkeys import send, clip, Hotkey

time.sleep(1)
text = """This is a really long rambling sentence that may not end for a while
because we want to try testing if the send function is able to handle
very long text string without messing up along This long and dreary way,
but we still want it to send AS quickly AS it possibly can because things
that take too long are Very Annoying`!`!`!
"""
start = time.time()
# send(text, 0.01)
send(text)
send(text)

# => 2.3477
print(f'Send took {time.time() - start} secs.')

start = time.time()
clip(text)

# => 0.0038
print(f'Clip took {time.time() - start} secs.')

start = time.time()
# send('^v{up 2}')

# => 0.3221
print(f'Send paste took {time.time() - start} secs.')

# test sending with hotkey
class SpecialHotkey(Hotkey):
     def __call__(self, *args, **kwargs):
          start = time.time()
          super().__call__(*args, **kwargs)
          print(f'Send from hotkey hook took {time.time() - start} secs.')


def hotkey_tester(*args, **kwargs):
     start = time.time()
     send('^v{up 2}')
     print(f'Send inside hotkey took {time.time() - start} secs.')

# SpecialHotkey('^l', hotkey_tester)
# => 0.4367

# Hotkey.wait()
