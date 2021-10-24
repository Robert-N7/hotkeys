from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox

from stubs.stub_window import StubWindow


class ClassWindow(StubWindow):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('Class Name:'))
        self.add_left(QLabel('Base Class:'))
        self.add_left(QLabel('Interfaces:'))

        self.add_right(QLineEdit(), 'class_edit')
        self.add_right(QLineEdit(), 'base_edit')
        self.add_right(QLineEdit(), 'interface_edit')
        if self.stub.has_privacy:
            self.add_left(QLabel('Privacy'))
            self.privacy_box = QComboBox()
            self.privacy_box.addItems(['public', 'protected', 'private'])
            self.add_right(self.privacy_box)

    def submit(self):
        super().submit()
        interfaces = [x.strip() for x in self.interface_edit.text().split(',')]
        indent = ''
        privacy = self.privacy_box.currentText() if self.stub.has_privacy else None
        self.stub.create_class(self.class_edit.text(),
                               self.base_edit.text(),
                               interfaces,
                               indent,
                               privacy
                               )