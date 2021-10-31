import sys
import time
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit

from hotkeys import send, clip, Hotkey, send_paste, HK_QUIT_KEY
from stubs.editors.pycharm import Pycharm
from stubs.stub import Stub
from stubs.window_stub import WindowStub

time.sleep(1)
start = time.time()

send('+{end}')
print(f'Finished in {time.time() - start}')

#

# class MyWin(WindowStub):
#     def __init__(self, parent, stub):
#         super().__init__(parent, stub)
#         self.add_left(QLabel('Hi!'))
#         self.add_right(QLineEdit(), 'foo')
#
#     def submit(self):
#         super().submit()
#         send('Holy Moses', 0.003)
#
#
# app = QApplication([])
# stub = Stub(Pycharm())
# win = MyWin(None, stub)
# HK_QUIT_KEY.set_callback(lambda *a, **k: win.close())
# win.show()
# sys.exit(app.exec_())
