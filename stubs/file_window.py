import time

from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox

from stubs.stub_window import StubWindow


class FileWindow(StubWindow):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('Filename:'))
        self.add_left(QLabel('Directory:'))
        self.add_left(QLabel('Class Name:'))
        self.add_left(QLabel('Base Class:'))
        self.add_left(QLabel('Interfaces:'))

        self.add_right(QLineEdit(), 'file_edit')
        self.file_edit.textEdited.connect(self.on_file_change)
        self.add_right(QLineEdit(), 'dir_edit')
        self.add_right(QLineEdit(), 'class_edit')
        self.add_right(QLineEdit(), 'base_edit')
        self.base_edit.textEdited.connect(self.on_base_change)
        self.add_right(QLineEdit(), 'interface_edit')
        if self.stub.has_privacy:
            self.add_left(QLabel('Privacy'))
            self.privacy_box = QComboBox()
            self.privacy_box.addItems(['public', 'protected', 'private'])
            self.add_right(self.privacy_box)

    def on_base_change(self):
        pass    #   todo find base file, generate stubs, add includes

    def on_file_change(self):
        text = self.stub.class_case(self.file_edit.text())
        self.class_edit.setText(text)

    def submit(self):
        super().submit()
        interfaces = [x.strip() for x in self.interface_edit.text().split(',')]
        indent = ''
        privacy = self.privacy_box.currentText() if self.stub.has_privacy else None
        class_text = self.class_edit.text()
        class_info = [class_text,
                      self.base_edit.text(),
                      interfaces,
                      indent,
                      privacy] if class_text else None

        self.stub.create_file(self.file_edit.text(), self.dir_edit.text(), class_info)

    def show(self):
        time.sleep(0.2)
        directory = self.stub.editor.get_current_directory()
        super().show()
        self.dir_edit.setText(directory)