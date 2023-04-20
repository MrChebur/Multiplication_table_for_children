from pathlib import Path
from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class MainWindow(QMainWindow):

    def initUI(self):
        self.setGeometry(100, 100, 550, 400)
        self.setWindowTitle(' ')

    def __init__(self):
        super().__init__()
        self.initUI()

        self.memorizeLabel = QLabel(self)
        self.startTheTestLabel = QLabel(self)

        self.memorizeLabel.setGeometry(50, 50, 200, 200)
        self.startTheTestLabel.setGeometry(300, 50, 200, 200)

        current_py_file = Path(__file__)
        main_folder = current_py_file.parents[1]
        icons_folder = main_folder.joinpath('icons')
        memorize_icon = icons_folder.joinpath('Memorize.png')
        start_the_test_icon = icons_folder.joinpath('Start_the_test.png')
        memorizePixmap = QPixmap(str(memorize_icon))
        startTheTestPixmap = QPixmap(str(start_the_test_icon))

        self.memorizeLabel.setPixmap(memorizePixmap)
        self.startTheTestLabel.setPixmap(startTheTestPixmap)

        self.memorizeLabel.mousePressEvent = self.showMultiplicationTable
        self.startTheTestLabel.mousePressEvent = self.startTheTest

    def startTheTest(self, event: QMouseEvent):
        print('startTheTest')

    def showMultiplicationTable(self, event: QMouseEvent):
        print('showMultiplicationTable')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    # todo
    #  stopwatch - how long it takes to solve this example
    #  stopwatch - how long the entire session takes (solving time only)
    #  no text interface - only icons
