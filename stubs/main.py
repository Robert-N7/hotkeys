import os
import sys

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
        Hotkey('^;', self.show_main_win)
        Hotkey('^m', lambda *args, **kwargs: self.function_window.show())
        Hotkey('^k', lambda *args, **kwargs: self.class_window.show())
        Hotkey('^i', lambda *args, **kwargs: self.file_window.show())
        Hotkey('^p', lambda *args, **kwargs: self.stub.create_print())
        Hotkey("^'", lambda *args, **kwargs: self.stub.create_this())
        Hotkey("!d", lambda *args, **kwargs: self.define_window.show())
        Hotkey('!a', lambda *args, **kwargs: self.for_window.show())
        Hotkey('!k', self.show_save_window)
        Hotkey('!l', self.show_load_window)
        HK_QUIT_KEY.set_callback(lambda *args, **k: self.main_window.close())

    def init_windows(self):
        stub = self.stub
        self.main_window = SwitchWindowStub(None, stub, self)
        self.function_window = FunctionWindowStub(None, stub, self)
        self.class_window = ClassWindowStub(None, stub)
        self.file_window = FileWindowStub(None, stub)
        self.define_window = WindowDefine(None, stub)
        self.for_window = WindowFor(None, stub)
        self.load_window = WindowLoad(None, self)

    def show_load_window(self, *args, **kwargs):
        self.load_window.set_text(None)
        self.load_window.show()

    def show_save_window(self, *args, **kwargs):
        text = self.stub.editor.copy()
        if text:
            self.load_window.set_text(text)
            self.load_window.show()

    def set_params(self, params):
        ma = min(6, len(params))
        keys = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6]
        for i in range(ma):
            self.save(keys[i], params[i], False)

    def load_config(self):
        self.project_dir = ''
        self.stub = PyStub(Pycharm())

    def load(self, key):
        fp = self.temp_keys.get(key)
        if fp:
            fp()

    def save(self, key, text, save_last=True):
        self.temp_keys[key] = lambda: self.stub.send_to_editor(text)
        if save_last:
            self.temp_keys[Qt.Key_L] = lambda: self.stub.send_to_editor(text)

    @staticmethod
    def _guess_project_path(path):
        name = ''
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
