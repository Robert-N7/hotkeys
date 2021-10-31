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

    def copy(self):
        clip('')
        send('^c')
        return clip_wait()

    def up(self, amount=1):
        send('{up ' + str(amount) + '}')

    def select_up(self, amount=1):
        send('+{up ' + str(amount) + '}')

    def down(self, amount=1):
        send('{down ' + str(amount) + '}')

    def select_down(self, amount=1):
        send('+{down ' + str(amount) + '}')

    def left(self, amount=1):
        send('{left ' + str(amount) + '}')

    def select_left(self, amount=1):
        send('+^{left ' + str(amount) + '}')

    def right(self, amount=1):
        send('{right ' + str(amount) + '}')

    def select_right(self, amount=1):
        send('+^{right ' + str(amount) + '}')

    def home(self):
        send('{home}')

    def end(self):
        send('{end}')

    def open_line_below(self):
        send('{end}{return}')

    def open_line_above(self):
        send('{up}{end}{return}')

    def select_end(self):
        send('+{end}')

    def select_home(self):
        send('+{home}')

    def space(self):
        send('{space}')

    def ctrl_left(self, amount=1):
        send('^{left ' + str(amount) + '}')

    def ctrl_right(self, amount=1):
        send('^{right ' + str(amount) + '}')

    def select_todo_line(self, up_amount=1):
        if up_amount:
            self.up(up_amount)
        send('{end}+{home}')

    def navigate_to_file(self, filename):
        raise NotImplementedError()
