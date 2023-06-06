import math
from pprint import pprint
from pathlib import Path
import logging
from collections import OrderedDict

from PySide6.QtGui import QPixmap, QMouseEvent, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QTableWidgetItem, QTableWidget, QGridLayout, \
    QVBoxLayout, QSpacerItem, QSizePolicy, QAbstractItemView, QSpinBox, QAbstractSpinBox
from PySide6.QtCore import Qt
from generate import GenerateTasks
from screeninfo import get_monitors

from task import Task


def findMainWindow() -> QMainWindow or None:
    """
    Global function to find the (open) QMainWindow in application
    :return: QMainWindow or None
    """
    #
    appication = QApplication.instance()
    for widget in appication.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None


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
        self.exam_window = None
        self.setWindowTitle(' ')

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # create layout
        self.vbox = QGridLayout(self.main_widget)
        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignCenter)
        # self.vbox.setDirection(QBoxLayout.LeftToRight)

        # create icons
        self.memorizeLabel = QLabel(self)
        self.startTheTestLabel = QLabel(self)

        # create labels
        self.min_value_label = QLabel()
        self.min_value_label.setText('2 х 2 = 4')

        self.dots_label = QLabel()
        self.dots_label.setText('.......')

        self.max_value_label = QLabel()
        self.max_value_label.setText('9 х 9 = 81')

        # create spin boxes
        self.min_value = QSpinBox()
        self.max_value = QSpinBox()
        self.min_value.setValue(2)
        self.max_value.setValue(9)
        self.min_value.setMinimum(2)
        self.min_value.setMaximum(9)
        self.max_value.setMinimum(2)
        self.max_value.setMaximum(20)
        self.min_value.valueChanged.connect(self.updateMinValueLabel)
        self.max_value.valueChanged.connect(self.updateMaxValueLabel)

        # set font size and alignment
        for widget in (self.min_value_label, self.dots_label, self.max_value_label, self.min_value, self.max_value):
            widget.setAlignment(Qt.AlignCenter)
            widget.setFont(QFont('Arial', 15))

        # add items
        self.configureIcons()
        self.vbox.addWidget(self.min_value_label, 0, 0)
        self.vbox.addWidget(self.dots_label, 1, 0)
        self.vbox.addWidget(self.max_value_label, 2, 0)

        self.vbox.addWidget(self.min_value, 0, 1)
        self.vbox.addWidget(self.max_value, 2, 1)

        self.vbox.addWidget(self.memorizeLabel, 3, 0)
        self.vbox.addWidget(self.startTheTestLabel, 3, 1)

        self.adjustSize()

    def updateMinValueLabel(self):
        min_value = self.min_value.value()
        self.min_value_label.setText(f'{min_value} х {min_value} = {min_value * min_value}')
        self.max_value.setMinimum(min_value)

    def updateMaxValueLabel(self):
        max_value = self.max_value.value()
        if max_value < 9:
            second_multiplier = 9
        else:
            second_multiplier = max_value

        self.max_value_label.setText(f'{max_value} х {second_multiplier} = {max_value * second_multiplier}')
        self.min_value.setMaximum(max_value)

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
        multipliers = list(range(self.min_value.value(), self.max_value.value()))
        generate = GenerateTasks()
        tasks = generate.multiplication(multipliers, shuffle=False)
        self.exam_window = ExamWindow(tasks)
        self.exam_window.showMaximized()
        self.hide()

        # noinspection PyUnusedLocal

    def showMultiplicationTable(self, event: QMouseEvent):
        min_multiplier = self.min_value.value()
        max_multiplier = self.max_value.value()

        self.multiplication_table_window = MultiplicationTableWindow(min_multiplier, max_multiplier)
        self.multiplication_table_window.showMaximized()
        self.hide()  # OR self.close() ?


# noinspection PyUnresolvedReferences
# noinspection PyMethodMayBeStatic
class MultiplicationTableWindow(QWidget):
    def __init__(self, min_multiplier, max_multiplier):

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
        self.initUI(min_multiplier, max_multiplier + 1)

    def closeEvent(self, event):
        """
        Overwrites `closeEvent` to display the main window after closing the table.
        :param event:
        :return:
        """
        main_window = findMainWindow()
        if main_window is not None:
            main_window.show()
        event.accept()

    def initUI(self, min_multiplier, max_multiplier):
        maximum_columns_in_the_row = 8
        max_rows = math.ceil((max_multiplier - min_multiplier) / maximum_columns_in_the_row)

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
        columns_number = (max_multiplier - min_multiplier) / rows_number
        remainder = (max_multiplier - min_multiplier) % rows_number
        if remainder != 0:
            rows_number += 1
        self.table.setColumnCount(columns_number)
        self.table.setRowCount(rows_number)

    def groupTasksByMultiplier(self, tasks: [Task], reverse_tasks=False):
        groups = {}
        SPACE = ' '
        if reverse_tasks:
            tasks.reverse()
        for num, task in enumerate(tasks):
            multiplier1 = str(task).split(SPACE)[0]
            if multiplier1 not in groups:
                groups[multiplier1] = []
            groups[multiplier1].append(task)
            print(str(task) + str(task.solve()))
        return groups

    def fill_table(self, min_multiplier, max_multiplier):
        # todo: 1 добавить возможность вывода таблицы умножения с повторениями предыдущих значений
        #  добавить переключатель кнопкой

        # todo: 2 неверно работает таблица, если указать только таблицу умножения на число Х, например, 2
        #  должна выводиться полная таблица умножения начиная с 2*2 до 2*9
        #  видимо, надо переделать генератор задач в generate.py

        NO_BREAK_SPACE = ' '
        NEW_LINE = '\n'
        column_max, row_max = self.table.columnCount(), self.table.rowCount()
        multipliers = list(range(2, max_multiplier))
        generate = GenerateTasks()
        tasks = generate.multiplication(multipliers, shuffle=False)
        groups = self.groupTasksByMultiplier(tasks)
        pprint(groups)

        row, column = 0, 0
        print(min_multiplier, max_multiplier)
        for group_number in range(min_multiplier, max_multiplier):
            tasks_list = groups[str(group_number)]
            text = ''
            for task in tasks_list:
                text += str(task) + str(task.solve()) + NO_BREAK_SPACE * 3 + NEW_LINE
            text = text.replace('*', 'x')
            item = QTableWidgetItem(text)
            self.table.setItem(row, column, item)

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


# noinspection PyUnresolvedReferences
# noinspection PyMethodMayBeStatic
class ExamWindow(QWidget):

    def __init__(self, tasks: [Task]):
        super().__init__()
        self.setWindowTitle(' ')
        self.main_widget = QWidget()

        self.tasks = tasks
        self.current_task_number = None
        self.current_task = None

        # create layout
        self.vbox = QGridLayout(self.main_widget)
        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignCenter)

        # create widgets
        self.task_label = QLabel()
        self.task_label.setText("? × ? = ")
        self.answer = QSpinBox()
        self.answer.setButtonSymbols(QAbstractSpinBox.NoButtons)  # hide spinbox arrows
        self.answer.setMaximum(1000)

        self.nextTaskLabel = QLabel()
        self.stopLabel = QLabel()

        # add items
        self.adjustSize()
        self.configureIcons()

        self.vbox.addWidget(self.stopLabel, 1, 4)

        self.vbox.addWidget(self.task_label, 1, 1)
        self.vbox.addWidget(self.answer, 1, 2)
        self.vbox.addWidget(self.nextTaskLabel, 1, 3)

        for widget in (self.task_label, self.answer, self.nextTaskLabel, self.stopLabel):
            widget.setAlignment(Qt.AlignCenter)
            widget.setFont(QFont('Arial', 80))

    def configureIcons(self):
        self.nextTaskLabel.setText('⏩')
        self.stopLabel.setText('⏹')

        self.nextTaskLabel.mousePressEvent = self.nextTaskPressed
        self.stopLabel.mousePressEvent = self.stopPressed

    def updateTaskLabel(self):
        self.current_task.dot2comma = True
        task_string = str(self.current_task).replace('*', '×')
        self.task_label.setText(task_string)

    def nextTask(self):
        if self.current_task_number is None:
            self.current_task_number = 0
            self.current_task = self.tasks[self.current_task_number]
        else:
            max_number = len(self.tasks)
            if self.current_task_number < max_number:
                self.current_task_number += 1
                self.current_task = self.tasks[self.current_task_number]
            else:
                raise IndexError

    def nextTaskPressed(self, event: QMouseEvent):
        if self.current_task is None:  # If the exam has just begun
            self.nextTask()
            self.updateTaskLabel()
            self.current_task.startTimer()
            self.answer.cleanText()
            # TODO Clear spinbox value
            # TODO Move keyboard cursor to spinbox
        else:
            self.current_task.stopTimer()
            self.current_task.user_answer = self.answer.value()
            logging.info(' '.join(str(x) for x in [self.current_task,
                                                   self.current_task.solve(),
                                                   self.current_task.user_answer,
                                                   self.current_task.isCorrect(),
                                                   self.current_task.time_elapsed,
                                                   ]
                                  ))

            self.nextTask()
            self.updateTaskLabel()
            self.current_task.startTimer()
            self.answer.cleanText()
            # TODO Clear spinbox value
            # TODO Move keyboard cursor to spinbox

    def cycleSymbols(self, qlabel: QLabel, symbols: str):
        """
        :param qlabel: QLabel
        :param symbols: Characters that will be cycled.
        :return:
        """
        uniq_symbols = ''.join(list(OrderedDict.fromkeys([x for x in symbols])))
        current_symbol = qlabel.text()
        if current_symbol not in uniq_symbols:
            current_symbol = uniq_symbols[0]
        current_position = uniq_symbols.find(current_symbol)
        next_symbol_index = current_position + 1
        if next_symbol_index >= len(uniq_symbols):
            next_symbol_index = 0
        qlabel.setText(uniq_symbols[next_symbol_index])

    def stopPressed(self, event: QMouseEvent):
        self.cycleSymbols(self.stopLabel, symbols='⏹⏸')  # '⏹⏸▷' '⏹■▣◀◁▶▷◽◾↪↩↵√Ꚙ∞±×⏸⏩'

    # def iterateOverTasks(self):
    #     for task in self.tasks:
    #         self.updateTaskLabel()

    def closeEvent(self, event):
        """
        Overwrites `closeEvent` to display the main window after closing the table.
        :param event:
        :return:
        """
        main_window = findMainWindow()
        if main_window is not None:
            main_window.show()
        event.accept()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    # todo
    #  stopwatch - how long it takes to solve this example
    #  stopwatch - how long the entire session takes (solving time only)
    #  no text interface - only icons

    # ■▣◀◁▶▷◼◽◾↪↩↵√Ꚙ∞±×⏸⏩
