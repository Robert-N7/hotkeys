import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit

from hotkeys import Hotkey, HK_QUIT_KEY
from stubs.class_window import ClassWindow
from stubs.editors.pycharm import Pycharm
from stubs.file_window import FileWindow
from stubs.function_window import FunctionWindow
from stubs.js_stub import JsStub
from stubs.php_stub import PhpStub
from stubs.py_stub import PyStub
from stubs.stub import Stub
from stubs.stub_switch_window import StubSwitchWindow


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
        self.main_window = StubSwitchWindow(None, self.stub, self)
        self.function_window = FunctionWindow(None, self.stub)
        self.class_window = ClassWindow(None, self.stub)
        self.file_window = FileWindow(None, self.stub)

        # Hotkeys
        Hotkey('^;', self.show_main_win)
        Hotkey('^m', lambda *args, **kwargs: self.function_window.show())
        Hotkey('^k', lambda *args, **kwargs: self.class_window.show())
        Hotkey('^i', lambda *args, **kwargs: self.file_window.show())
        Hotkey('^p', lambda *args, **kwargs: self.stub.create_print())
        Hotkey("^'", lambda *args, **kwargs: self.stub.create_this())
        HK_QUIT_KEY.set_callback(lambda *args, **k: self.main_window.close())

    def load_config(self):
        self.project_dir = ''
        self.stub = PyStub(Pycharm())

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
        self.function_window = FunctionWindow(None, self.stub)
        self.class_window = ClassWindow(None, self.stub)
        self.file_window = FileWindow(None, self.stub)


def main():
    app = QApplication([])
    c = StubController()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
