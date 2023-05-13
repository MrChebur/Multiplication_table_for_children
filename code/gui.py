import math
from pathlib import Path
from PySide6.QtGui import QPixmap, QMouseEvent, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout, \
    QSpacerItem, QSizePolicy, QBoxLayout, QAbstractItemView
from PySide6.QtCore import Qt
from generate import GenerateTasks
from screeninfo import get_monitors


def getMonitorResolution():
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height


def adjustFontSize(current_font_size):
    current_x, current_y = getMonitorResolution()
    default_x = 1920
    ratio = current_x / default_x
    resized_font_size = current_font_size * ratio
    return resized_font_size


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.multiplication_table_window = None
        self.setWindowTitle(' ')

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # create layout
        self.vbox = QVBoxLayout(self.main_widget)
        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignCenter)
        self.vbox.setDirection(QBoxLayout.LeftToRight)

        # create icons
        self.memorizeLabel = QLabel(self)
        self.startTheTestLabel = QLabel(self)

        # add items
        self.configureIcons()
        self.vbox.addWidget(self.memorizeLabel)
        self.vbox.addWidget(self.startTheTestLabel)

        self.adjustSize()

    def configureIcons(self):
        icon_x_size, icon_y_size = 200, 200

        self.startTheTestLabel.setFixedHeight(icon_y_size)
        self.startTheTestLabel.setFixedWidth(icon_x_size)

        self.memorizeLabel.setFixedHeight(icon_y_size)
        self.memorizeLabel.setFixedWidth(icon_x_size)

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

    #   noinspection PyUnusedLocal
    def startTheTest(self, event: QMouseEvent):
        print('startTheTest', self)

    # noinspection PyUnusedLocal
    def showMultiplicationTable(self, event: QMouseEvent):
        print('showMultiplicationTable')
        self.multiplication_table_window = MultiplicationTableWindow()
        self.multiplication_table_window.showMaximized()
        self.hide()  # OR self.close() ?


# noinspection PyUnresolvedReferences
class MultiplicationTableWindow(QWidget):
    def __init__(self):

        super().__init__()
        self.table = QTableWidget(self)
        # noinspection PyUnresolvedReferences
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.setShowGrid(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()

        # disable table selection and edit
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

        # set font parameters
        self.default_font_size = 33
        resized_font_size = adjustFontSize(self.default_font_size)
        self.table.setFont(QFont('Arial', resized_font_size))

        self.showMaximized()
        self.initUI(min_multiplier=2,
                    max_multiplier=10)

    def closeEvent(self, event):
        event.accept()

    def initUI(self, min_multiplier, max_multiplier):

        max_rows = math.ceil((max_multiplier - min_multiplier) / 8)

        self.setWindowTitle(" ")
        self.generateTableSize(min_multiplier, max_multiplier, max_rows)
        self.fill_table(min_multiplier, max_multiplier)

        # create layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # create items
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # add items
        vbox.addItem(spacer)
        vbox.addWidget(self.table)
        vbox.addStretch()

        # auto sizing
        self.setAlignment()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.adjustSize()

    def generateTableSize(self, min_multiplier, max_multiplier, rows_number):
        column_number = -1 + (max_multiplier - min_multiplier + 1) / rows_number
        remainder = (max_multiplier - min_multiplier + 1) % rows_number
        if remainder != 0:
            rows_number += 1
        self.table.setColumnCount(column_number)
        self.table.setRowCount(rows_number)

    def fill_table(self, min_multiplier, max_multiplier):
        SPACE = ' '
        column_max, row_max = self.table.columnCount(), self.table.rowCount()
        multipliers = list(range(min_multiplier, max_multiplier))
        generate = GenerateTasks()
        tasks = generate.multiplication(multipliers, shuffle=False)
        text = ''
        row = 0
        column = 0

        for num, task in enumerate(tasks):
            text += str(task) + str(task.solve()) + SPACE * 3
            first_value = str(task).split(SPACE)[0]

            try:
                next_first_value = str(tasks[num + 1]).split(SPACE)[0]
            except IndexError:
                next_first_value = None

            if first_value == next_first_value:
                text += '\n'
            else:
                item = QTableWidgetItem(text.replace('*', 'x'))
                self.table.setItem(row, column, item)
                text = '\n'
                if column < column_max - 1:
                    column += 1
                else:
                    row += 1
                    column = 0

    def setAlignment(self):
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item is not None:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()

    # todo
    #  stopwatch - how long it takes to solve this example
    #  stopwatch - how long the entire session takes (solving time only)
    #  no text interface - only icons
