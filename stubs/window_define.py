from PyQt5.QtWidgets import QLabel, QLineEdit

from stubs.window_stub import WindowStub


class WindowDefine(WindowStub):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('Define:'))
        self.var_name = QLineEdit()
        self.add_right(self.var_name)

    def submit(self):
        super().submit()
        self.stub.create_define(self.var_name.text())