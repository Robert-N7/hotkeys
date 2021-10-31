from PyQt5.QtWidgets import QLabel, QLineEdit

from hotkeys import clip_get
from stubs.window_stub import WindowStub


class WindowFor(WindowStub):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('iterate'))
        self.items = QLineEdit()
        self.add_right(self.items)
        self.items.textChanged.connect(self.text_changed)
        self.add_left(QLabel('with'))
        self.it = QLineEdit('x')
        self.add_right(self.it)
        self.add_left(QLabel('range(?)'))
        self.max_i = QLineEdit()
        self.add_right(self.max_i)

    def show(self):
        super().show()
        items = self.stub.get_iterable_from_line(clip_get())
        self.items.setText(items)

    def text_changed(self):
        items = self.items.text()
        items = items.split(self.stub.get_separator())[-1]
        if items.endswith('s'):
            item = items.rstrip('s')
            self.it.setText(item)


    def submit(self):
        super().submit()
        max = self.max_i.text()
        self.stub.create_for(self.it.text(), self.items.text(), max)
