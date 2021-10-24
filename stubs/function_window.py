from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QComboBox

from stubs.stub_window import StubWindow


class FunctionWindow(StubWindow):
    def __init__(self, parent, stub):
        super().__init__(parent, stub)
        self.add_left(QLabel('Function:'))
        self.add_left(QLabel('Parameters:'))
        self.add_left(QLabel('Return:'))
        if self.stub.has_return_type:
            self.add_left(QLabel('Return Type:'))
        if self.stub.has_privacy:
            self.add_left(QLabel('Privacy:'))
        self.add_right(QLineEdit(), 'func_edit')
        self.add_right(QLineEdit(), 'params_edit')
        self.add_right(QLineEdit(), 'retrn_edit')
        if self.stub.has_return_type:
            self.add_right(QLineEdit(), 'return_type_edit')
        if self.stub.has_privacy:
            self.privacy_select = QComboBox()
            self.privacy_select.addItems(['public', 'protected', 'private', ''])
            self.add_right(self.privacy_select)

    def submit(self):
        super().submit()
        params = [x.strip() for x in self.params_edit.text().split(',')]
        indent = ''     # todo
        privacy = self.privacy_select.text() if self.stub.has_privacy else None
        return_type = self.return_type_edit.text() if self.stub.has_return_type else None
        self.stub.create_function(self.func_edit.text(),
                                  params,
                                  self.retrn_edit.text(),
                                  indent,
                                  privacy,
                                  return_type
                                  )


