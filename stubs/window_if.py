from PyQt5.QtWidgets import QLabel, QLineEdit

from .window_stub import WindowStub


class WindowIf(WindowStub):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('if'))
        self.add_right(QLineEdit(), 'if_edit')
        self.add_left(QLabel('else if'))
        self.add_right(QLineEdit(), 'else_if_edit')
        self.add_left(QLabel('else'))
        self.add_right(QLineEdit(), 'else_edit')

    def submit(self):
        super().submit()
        self.stub.create_if(self.if_edit.text(),
                            self.else_if_edit.text(),
                            self.else_edit.text())
