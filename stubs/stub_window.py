import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QAction, QLineEdit

from hotkeys import send


class StubWindow(QWidget):
    def __init__(self, parent, stub):
        super().__init__(parent)
        self.stub = stub
        main_layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.clear_widgets = []
        hlayout.addLayout(self.left_layout)
        self.right_layout = QVBoxLayout()
        hlayout.addLayout(self.right_layout)
        main_layout.addLayout(hlayout)
        hlayout = QHBoxLayout()
        self.cancel_action = QAction('Cancel', self)
        self.cancel_action.triggered.connect(self.cancel)
        self.cancel_action.setShortcut('Escape')
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.addAction(self.cancel_action)
        self.cancel_button.clicked.connect(self.cancel)
        self.submit_action = QAction('Go!', self)
        self.submit_action.triggered.connect(self.submit)
        self.submit_action.setShortcut('Return')
        self.submit_button = QPushButton('Go!')
        self.submit_button.addAction(self.submit_action)
        self.submit_button.clicked.connect(self.submit)
        hlayout.addWidget(self.cancel_button)
        hlayout.addWidget(self.submit_button)
        main_layout.addLayout(hlayout)
        self.setLayout(main_layout)
        self.first_widget = None

    def add_left(self, widget, var_name=None):
        if var_name:
            setattr(self, var_name, widget)
        self.left_layout.addWidget(widget)

    def add_right(self, widget, var_name=None):
        if var_name:
            setattr(self, var_name, widget)
        self.right_layout.addWidget(widget)
        if not self.first_widget:
            self.first_widget = widget
        if type(widget) is QLineEdit:
            self.clear_widgets.append(widget)

    def cancel(self):
        self.hide()

    def submit(self):
        self.hide()
        time.sleep(0.1)

    def show(self):
        super().show()
        for x in self.clear_widgets:
            x.clear()
        self.first_widget.setFocus()
