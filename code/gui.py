import random
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from __feature__ import snake_case, true_property


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = [
            "Hallo Welt",
            "你好，世界",
            "Hei maailma",
            "Hola Mundo",
            "Привет мир",
        ]

        self.button = QPushButton("Click me!")
        self.message = QLabel("Hello World")
        self.message.alignment = Qt.AlignCenter

        self.layout = QVBoxLayout(self)
        self.layout.add_widget(self.message)
        self.layout.add_widget(self.button)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        self.message.text = random.choice(self.hello)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())

# todo
#  no text interface - only icons
#  icon `test yourself icon` https://www.google.com/search?q=test+youself+icon
#  icon `memorize icon`https://www.google.com/search?q=memorize+icon
#  stopwatch - how long it takes to solve this example
#  stopwatch - how long the entire session takes (solving time only)
