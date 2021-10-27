import time

from hotkeys import send, clip, Hotkey

text = """This is a really long rambling sentence that may not end for a while
because we want to try testing if the send function is able to handle
very long text string without messing up along the long and dreary way,
but we still want it to send as quickly as it possibly can because things
that take too long are very annoying
"""
start = time.time()
send(text)

# => 2.3477
print(f'Send took {time.time() - start} secs.')

start = time.time()
clip(text)

# => 0.0038
print(f'Clip took {time.time() - start} secs.')

start = time.time()
send('^v{up 2}')

# => 0.3221
print(f'Send hotkey took {time.time() - start} secs.')

# test sending with hotkey
class SpecialHotkey(Hotkey):
     def __call__(self, *args, **kwargs):
          start = time.time()
          super().__call__(*args, **kwargs)
          print(f'Send from hotkey hook took {time.time() - start} secs.')


def hotkey_tester(*args, **kwargs):
     send('^v{up 2}')

SpecialHotkey('^1', hotkey_tester)
