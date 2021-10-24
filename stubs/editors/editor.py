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

    def move_up(self, amount=1):
        send('{up}' * amount)

    def move_down(self, amount=1):
        send('{down}' * amount)

    def move_start_of_line(self):
        send('{home}')

    def move_end_of_line(self):
        send('{end}')

    def select_to_end_of_line(self):
        send('+{end}')

    def select_to_start_of_line(self):
        send('+{home}')

    def select_todo_line(self, up_amount=1):
        send('{up}' * up_amount + '{home}+{end}')

    def navigate_to_file(self, filename):
        raise NotImplementedError()
