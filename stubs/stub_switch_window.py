from PyQt5.QtWidgets import QLabel, QComboBox

from stubs.editors.pycharm import Pycharm
from stubs.py_stub import PyStub
from stubs.stub_window import StubWindow


class StubSwitchWindow(StubWindow):

    def __init__(self, parent, stub, controller):
        super().__init__(parent, stub)
        self.controller = controller
        self.add_left(QLabel('Language:'))
        self.language_box = QComboBox()
        self.language_box.addItems(controller.stubs.keys())
        self.add_right(self.language_box)
        self.add_left(QLabel('Editor:'))
        self.editor_box = QComboBox()
        self.editor_box.addItems(controller.editors.keys())
        self.add_right(self.editor_box)

    def submit(self):
        super().submit()
        self.controller.set_stub(self.language_box.currentText(), self.editor_box.currentText())