import sys
import time

from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit

from hotkeys import send, clip, Hotkey, send_paste, HK_QUIT_KEY
from stubs.editors.pycharm import Pycharm
from stubs.stub import Stub
from stubs.window_stub import WindowStub

time.sleep(1)
text = """array_push($arr, $item)
"""
start = time.time()
# send(text, raw=True)

# => 2.3477
print(f'Send took {time.time() - start} secs.')

start = time.time()
# clip(text)
# => 0.0038
print(f'Clip took {time.time() - start} secs.')

start = time.time()
# send_paste(text)

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


# SpecialHotkey('^!l', text, raw=True)
# => 0.094
# SpecialHotkey('2', 'Holy Moses')
# SpecialHotkey('1', 'Foo_Bar')

class MyWin(WindowStub):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('Hi!'))
        self.add_right(QLineEdit(), 'foo')

    def submit(self):
        super().submit()
        send('Holy Moses')


app = QApplication([])
stub = Stub(Pycharm())
win = MyWin(None, stub)
HK_QUIT_KEY.set_callback(lambda *a, **k: win.close())
win.show()
sys.exit(app.exec_())
# 
