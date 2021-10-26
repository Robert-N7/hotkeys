from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QLineEdit


class WindowLoad(QWidget):
    def __init__(self, parent, controller, text=None):
        super().__init__(parent)
        self.controller = controller
        self.edit_text = QLineEdit()
        self.edit_text.setEnabled(False)
        self.is_text_focused = False
        self.edit_text.installEventFilter(self)
        self.label = QLabel('...........')
        self.set_text(text)
        layout = QVBoxLayout()
        layout.addWidget(self.edit_text)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            self.is_text_focused = not self.is_text_focused
            self.edit_text.setEnabled(self.is_text_focused)
        return False


    def set_text(self, text):
        self.edit_text.setText(text)
        self.is_load = not text
        label = 'Load key...' if self.is_load else 'Store key...'
        self.label.setText(label)

    def keyPressEvent(self, event):
        if self.is_text_focused:
            event.accept()
            return
        self.hide()
        if event.key() != Qt.Key_Escape:
            if self.is_load:
                self.controller.load(event.key())
            else:
                self.controller.save(event.key(), self.edit_text.text())
        event.accept()
