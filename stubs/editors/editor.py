import os
import time

from hotkeys import send, clip, clip_wait


class Editor:
    def get_current_directory(self):
        d = self.get_current_path()
        if d:
            d = os.path.dirname(d)
        return d

    def get_current_path(self):
        raise NotImplementedError()

    def paste(self):
        send('^v')
        time.sleep(0.1)

    def copy(self):
        clip('')
        send('^c')
        return clip_wait()

    def up(self, amount=1):
        send('{up ' + str(amount) + '}')

    def down(self, amount=1):
        send('{down ' + str(amount) + '}')

    def left(self, amount=1):
        send('{left ' + str(amount) + '}')

    def right(self, amount=1):
        send('{right ' + str(amount) + '}')

    def home(self):
        send('{home}')

    def end(self):
        send('{end}')

    def select_end(self):
        send('+{end}')

    def select_home(self):
        send('+{home}')

    def space(self):
        send('{space}')

    def ctrl_left(self, amount):
        send('^{left ' + str(amount) + '}')

    def ctrl_right(self, amount):
        send('^{right ' + str(amount) + '}')

    def select_todo_line(self, up_amount=1):
        self.up(up_amount)
        send('{home}+{end}')

    def navigate_to_file(self, filename):
        raise NotImplementedError()
