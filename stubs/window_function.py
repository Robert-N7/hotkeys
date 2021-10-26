from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QComboBox, QCheckBox

from stubs.window_stub import WindowStub


class FunctionWindowStub(WindowStub):
    def __init__(self, parent, stub, controller):
        super().__init__(parent, stub)
        self.controller = controller
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
        if self.stub.possible_flags & self.stub.FL_ABSTRACT:
            self.abstract = QCheckBox('Abstract')
            self.add_left(self.abstract)
        if self.stub.possible_flags & self.stub.FL_STATIC:
            self.static = QCheckBox('Static')
            self.add_right(self.static)
        self.add_left(QLabel('Scope'))
        self.class_method = QCheckBox('Method')
        self.add_right(self.class_method)
        self.class_method.setChecked(True)

    @staticmethod
    def staticky(oof):
        raise NotImplementedError()

    def __get_flags(self):
        flags = 0
        if hasattr(self, 'static') and self.static.isChecked():
            flags |= self.stub.FL_STATIC
        if hasattr(self, 'abstract') and self.abstract.isChecked():
            flags |= self.stub.FL_ABSTRACT
        if self.class_method.isChecked():
            flags |= self.stub.FL_ISMETHOD
        return flags

    def submit(self):
        super().submit()
        params = [x.strip() for x in self.params_edit.text().split(',') if x]
        flags = self.__get_flags()
        params = self.stub.process_params(params, flags)
        self.controller.set_params(params)
        indent = None     # todo possibly autodetect?
        privacy = self.privacy_select.text() if self.stub.has_privacy else None
        return_type = self.return_type_edit.text() if self.stub.has_return_type else None
        self.stub.create_function(self.func_edit.text(),
                                  params,
                                  self.retrn_edit.text(),
                                  indent,
                                  privacy,
                                  return_type,
                                  flags
                                  )


