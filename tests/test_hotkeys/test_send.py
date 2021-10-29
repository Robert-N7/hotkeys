import time


from hotkeys import send, clip, Hotkey, send_paste

time.sleep(1)
text = """This is a really
"""
start = time.time()
send(text, raw=True)

# => 2.3477
print(f'Send took {time.time() - start} secs.')

start = time.time()
# clip(text)
# => 0.0038
print(f'Clip took {time.time() - start} secs.')

start = time.time()
send_paste(text)

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

# SpecialHotkey('^!l', hotkey_tester)
# => 0.4367

# Hotkey.wait()
