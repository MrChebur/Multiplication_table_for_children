from pathlib import Path
from PySide6.QtGui import QPixmap, QMouseEvent, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout
from PySide6.QtCore import Qt
from generate import GenerateTasks


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
        self.new_window = MultiplicationTableWindow()
        self.new_window.show()
        self.close()

    # def open_new_window(self):
    #     # Создание нового окна
    #     self.new_window = MultiplicationTableWindow()
    #     self.new_window.show()
    #     self.close()


class MultiplicationTableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(self)
        self.table.setShowGrid(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.setFont(QFont('Arial', 17))
        self.initUI()

    def initUI(self):
        min_multiplier = 2
        max_multiplier = 10
        max_rows = 1

        self.setWindowTitle(" ")
        self.setGeometry(100, 100, 1200, 600)

        self.generateTableSize(min_multiplier, max_multiplier, max_rows)
        self.fill_table(min_multiplier, max_multiplier)
        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def generateTableSize(self, min_multiplier, max_multiplier, rows_number):
        column_number = (max_multiplier - min_multiplier + 1) / rows_number
        remainder = (max_multiplier - min_multiplier + 1) % rows_number
        if remainder != 0:
            rows_number += 1
        self.table.setColumnCount(column_number)
        self.table.setRowCount(rows_number)

    def fill_table(self, min_multiplier, max_multiplier):
        column_max, row_max = self.table.columnCount(), self.table.rowCount()
        multipliers = list(range(min_multiplier, max_multiplier))
        generate = GenerateTasks()
        tasks = generate.multiplication(multipliers, shuffle=False)
        text = '\n'
        row = 0
        column = 0
        for num, task in enumerate(tasks):
            text += str(task) + str(task.solve()) + '    '
            first_value = str(task).split(' ')[0]
            try:
                next_first_value = str(tasks[num + 1]).split(' ')[0]
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

        self.setAlignment()
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def setAlignment(self):
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item is not None:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    # window = MultiplicationTableWindow()
    window.show()
    app.exec()

    # todo
    #  stopwatch - how long it takes to solve this example
    #  stopwatch - how long the entire session takes (solving time only)
    #  no text interface - only icons
