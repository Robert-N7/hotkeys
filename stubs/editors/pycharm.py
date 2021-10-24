import os
import time

from hotkeys import clip, send, clip_wait
from stubs.editors.editor import Editor


class Pycharm(Editor):
    def navigate_to_file(self, filename):
        time.sleep(0.3)
        send('+^N')
        clip(filename)
        self.paste()
        send('{Enter}')

    def get_current_path(self):
        clip('')
        send('^+c')
        return clip_wait()
