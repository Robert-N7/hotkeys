from PyQt5.QtWidgets import QLabel, QLineEdit

from stubs.window_stub import WindowStub


class WindowFor(WindowStub):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('for'))
        self.it = QLineEdit()
        self.add_right(self.it)
        self.add_left(QLabel('in'))
        self.items = QLineEdit()
        self.add_right(self.items)
        self.add_left(QLabel('range(?)'))
        self.max_i = QLineEdit()
        self.add_right(self.max_i)

    def submit(self):
        super().submit()
        max = 0
        try:
            t = self.max_i.text()
            if t:
                max = int(t)
        except ValueError:
            print('Invalid i ' + t)
        self.stub.create_for(self.it.text(), self.items.text(), max)
