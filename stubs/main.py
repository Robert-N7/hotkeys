import os
import sys
import time
import timeit

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit

from hotkeys import Hotkey, HK_QUIT_KEY, clip
from stubs.window_class import ClassWindowStub
from stubs.editors.pycharm import Pycharm
from stubs.window_define import WindowDefine
from stubs.window_file import FileWindowStub
from stubs.window_for import WindowFor
from stubs.window_function import FunctionWindowStub
from stubs.js_stub import JsStub
from stubs.php_stub import PhpStub
from stubs.py_stub import PyStub
from stubs.stub import Stub
from stubs.window_if import WindowIf
from stubs.window_load import WindowLoad
from stubs.window_switch import SwitchWindowStub


class StubController:
    stubs = {
        'py': PyStub,
        'js': JsStub,
        'php': PhpStub,
    }
    editors = {
        'pycharm': Pycharm,
    }

    def __init__(self, stub=None):
        self.load_config()
        self.temp_keys = {}
        self.init_windows()
        # Hotkeys
        # Editor and Language
        Hotkey('^;', self.show_main_win)
        # Method - Function
        Hotkey('^m', lambda h: self.function_window.show())
        # Class stub
        Hotkey('^+c', lambda h: self.class_window.show())
        # Create file and class
        Hotkey('^n', lambda h: self.file_window.show())
        # If statement
        Hotkey('^i', lambda h: self.if_window.show())
        # Print
        Hotkey('^p', lambda h: self.stub.create_print())
        # This, self
        Hotkey("^'", lambda h: self.stub.create_this())
        # Define var
        Hotkey("!d", lambda h: self.define_window.show())
        # For loop
        Hotkey('!f', lambda h: self.for_window.show())
        # Keep text (save into hotkey)
        Hotkey('!k', self.show_save_window)
        # Load text (load hotkey)
        Hotkey('!l', self.show_load_window)
        # Select line text
        Hotkey('z', lambda h: self.stub.editor.select_todo_line(0))
        Hotkey('!z', 'z')
        # Return
        Hotkey('!r', lambda h: self.stub.create_return())

        # Cursor manipulation
        # up
        Hotkey('!u', lambda h: self.stub.editor.up())
        Hotkey('^!u', lambda h: self.stub.editor.up(10))
        Hotkey('+!u', lambda h: self.stub.editor.select_up())
        Hotkey('^+!u', lambda h: self.stub.editor.select_up(10))

        # down
        Hotkey('!m', lambda h: self.stub.editor.down())
        Hotkey('^!m', lambda h: self.stub.editor.down(10))
        Hotkey('+!m', lambda h: self.stub.editor.select_down())
        Hotkey('^!+m', lambda h: self.stub.editor.select_down(10))

        # left
        Hotkey('!h', lambda h: self.stub.editor.left())
        Hotkey('^!h', lambda h: self.stub.editor.ctrl_left())
        Hotkey('!+h', lambda h: self.stub.editor.select_left())

        # right
        Hotkey('!;', lambda h: self.stub.editor.right())
        Hotkey('^!;', lambda h: self.stub.editor.ctrl_right())
        Hotkey('!+;', lambda h: self.stub.editor.select_right())

        # Home/End
        Hotkey('!b', lambda h: self.stub.editor.home())
        Hotkey('!e', lambda h: self.stub.editor.end())
        # Open Below/Above
        Hotkey('!o', lambda h: self.stub.editor.open_line_below())
        Hotkey('!+o', lambda h: self.stub.editor.open_line_above())

        HK_QUIT_KEY.set_callback(lambda h: self.main_window.close())

        # Number stored hotkeys
        for i in range(10):
            Hotkey(f'!{i}', lambda h: self.load(h.keys[-1]))
            Hotkey(f'^!{i}', lambda h: self.store(h.keys[-1]))

    def init_windows(self):
        stub = self.stub
        self.main_window = SwitchWindowStub(None, stub, self)
        self.function_window = FunctionWindowStub(None, stub, self)
        self.class_window = ClassWindowStub(None, stub)
        self.file_window = FileWindowStub(None, stub)
        self.define_window = WindowDefine(None, stub)
        self.for_window = WindowFor(None, stub)
        self.load_window = WindowLoad(None, self)
        self.if_window = WindowIf(None, stub)

    def show_load_window(self, h):
        self.load_window.set_text(None)
        self.load_window.show()

    def show_save_window(self, h):
        text = self.stub.editor.copy()
        if text:
            self.load_window.set_text(text)
            self.load_window.show()

    def set_params(self, params):
        ma = min(6, len(params))
        keys = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6]
        for i in range(ma):
            param = params[i]
            # remove typing
            x = param.split(' ')
            self.save(keys[i], x[len(x) - 1])

    def load_config(self):
        self.project_dir = ''
        self.stub = PyStub(Pycharm())

    def load(self, key):
        fp = self.temp_keys.get(key)
        if fp:
            fp()

    def store(self, key):
        text = self.stub.editor.copy()
        self.save(key, text)

    def save(self, key, text):
        self.temp_keys[key] = lambda: self.stub.send_to_editor(text)

    @staticmethod
    def _guess_project_path(path):
        path_names = []
        while len(path) > 1:
            dir, name = os.path.split(path)
            if name in ('IdeaProjects', 'PycharmProjects'):
                path = os.path.join(path, path_names[-1])
                break
            path_names.append(name)
            path = dir
        path_names.reverse()
        if len(path) <= 1:
            for i in range(3):
                path = os.path.join(path, path_names[i])
        return path

    def show_main_win(self, *args, **kwargs):
        project_path = None
        path = self.stub.editor.get_current_path()
        if path:
            current_file = os.path.basename(path)
            f, ext = os.path.splitext(current_file)
            if ext:
                self.main_window.language_box.setCurrentText(ext[1:])
            if not self.main_window.project_path.text():
                project_path = self._guess_project_path(path)
        self.main_window.show()
        if project_path:
            self.main_window.project_path.setText(project_path)

    def set_stub(self, language, editor, project_dir):
        editor = self.editors[editor]()
        self.stub = self.stubs[language](editor, project_dir)
        self.init_windows()


def main():
    app = QApplication([])
    c = StubController()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
