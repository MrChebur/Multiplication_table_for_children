from pathlib import Path
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
    current_py_file = Path(__file__)
    main_folder = current_py_file.parents[1]
    icons_folder = main_folder.joinpath('icons')
    memorize_icon = icons_folder.joinpath('Memorize.png')
    start_the_test_icon = icons_folder.joinpath('Start_the_test.png')

    print(icons_folder)
    print(memorize_icon)
    print(start_the_test_icon)

    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())

    # todo
    #  stopwatch - how long it takes to solve this example
    #  stopwatch - how long the entire session takes (solving time only)
    #  no text interface - only icons
