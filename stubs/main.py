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
        'python': PyStub,
        'javascript': JsStub,
        'php': PhpStub,
    }
    editors = {
        'pycharm': Pycharm,
    }

    def __init__(self, stub=None):
        self.load_config()
        self.main_window = StubSwitchWindow(None, self.stub, self)
        Hotkey('^;', lambda *args, **kwargs: self.main_window.show())
        self.function_window = FunctionWindow(None, self.stub)
        Hotkey('^m', lambda *args, **kwargs: self.function_window.show())
        self.class_window = ClassWindow(None, self.stub)
        Hotkey('^k', lambda *args, **kwargs: self.class_window.show())
        self.file_window = FileWindow(None, self.stub)
        Hotkey('^i', lambda *args, **kwargs: self.file_window.show())
        HK_QUIT_KEY.set_callback(lambda *args, **k: self.main_window.close())

    def load_config(self):
        self.project_dir = ''
        self.stub = PyStub(Pycharm())
        self.stub.editor.get_current_directory()


    def set_stub(self, language, editor):
        editor = self.editors[editor]()
        self.stub = self.stubs[language](editor)
        self.function_window = FunctionWindow(None, self.stub)
        self.class_window = ClassWindow(None, self.stub)
        self.file_window = FileWindow(None, self.stub)


def main():
    app = QApplication([])
    c = StubController()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
