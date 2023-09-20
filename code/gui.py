import math
from pprint import pprint
from pathlib import Path
import logging
from datetime import datetime
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
        tasks = generate.multiplication(multipliers, shuffle=True)
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


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
            # print(str(task) + str(task.solve()))
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


# noinspection PyUnresolvedReferences
# noinspection PyMethodMayBeStatic
class ExamWindow(QWidget):

    def __init__(self, tasks: [Task]):
        super().__init__()
        self.results_window = None
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
        self.task_label.setText('? × ? = ')
        self.answer = QSpinBox()
        self.answer.setDisabled(True)
        self.answer.setSpecialValueText(' ')
        self.answer.setButtonSymbols(QAbstractSpinBox.NoButtons)  # hide spinbox arrows
        self.answer.setMaximum(1000)

        self.nextTaskLabel = QLabel()
        self.stopLabel = QLabel()
        self.tasks_left_label = QLabel()
        self.tasks_left_label.setText(f'0/{len(self.tasks)}')

        # add items
        self.adjustSize()
        self.configureIcons()

        # self.vbox.addWidget(self.stopLabel, 1, 4)
        self.vbox.addWidget(self.task_label, 1, 1)
        self.vbox.addWidget(self.answer, 1, 2)
        self.vbox.addWidget(self.nextTaskLabel, 1, 3)
        self.vbox.addWidget(self.tasks_left_label, 1, 5)

        for widget in (self.task_label, self.answer, self.nextTaskLabel, self.stopLabel, self.tasks_left_label):
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
            max_number = len(self.tasks) - 1
            if self.current_task_number < max_number:
                self.current_task_number += 1
                self.current_task = self.tasks[self.current_task_number]

    def nextTaskPressed(self, event: QMouseEvent):
        if self.current_task is None:  # If the exam has just begun
            self.answer.setEnabled(True)
            self.answer.setFocus()
        else:

            # do nothing if no new value is entered
            if self.answer.value() == self.answer.minimum():
                if self.current_task.solve() == self.answer.minimum():
                    pass
                else:
                    return

            self.current_task.stopTimer()
            self.current_task.user_answer = self.answer.value()
            logging.info(' '.join(str(x) for x in [self.current_task,
                                                   self.current_task.solve(),
                                                   self.current_task.user_answer,
                                                   self.current_task.isCorrect(),
                                                   self.current_task.time_elapsed,
                                                   ]))

            # If it was the last task - show results
            if self.current_task_number + 1 == len(self.tasks):
                sorted_tasks = self.tasks.copy()
                sorted_tasks.sort()
                self.results_window = ResultsWindow(sorted_tasks, self)
                self.results_window.show()
                self.hide()

        self.nextTask()
        self.updateTaskLabel()
        self.tasks_left_label.setText(f'{self.current_task_number + 1}/{len(self.tasks)}')
        self.answer.setValue(0)
        self.answer.selectAll()
        self.answer.setFocus()
        self.current_task.startTimer()

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.nextTaskPressed(event)
        if event.key() == Qt.Key_Escape:
            self.close()

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


class ResultsWindow(QWidget):

    def __init__(self, tasks: [Task], exam_window_class: QWidget):
        super().__init__()
        self.setWindowTitle(' ')
        self.main_widget = QWidget()

        self.tasks = tasks
        self.exam_window_class = exam_window_class
        self.time_ranges = {'fast': [0, 5, 'green'],
                            'medium': [5, 10, 'orange'],
                            'slow': [10, float('inf'), 'red'],
                            }

        # create layout
        self.vbox = QGridLayout(self.main_widget)
        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignCenter)

        # create widgets
        self.results_label = QLabel()

        results = self.generateResultsString()
        self.results_label.setText(results)
        self.vbox.addWidget(self.results_label, 1, 1)
        self.results_label.setAlignment(Qt.AlignLeft)
        self.results_label.setFont(QFont('Arial', 12))

    def generateResultsString(self):
        HTML_NEWLINE = '<br>'
        lines = []

        for task in self.tasks:

            # colorizing results
            if task.isCorrect():
                results_color = 'green'
            else:
                results_color = 'red'

            # colorizing elapsed time
            time_color = None
            for key in self.time_ranges.keys():
                if self.time_ranges[key][0] <= task.time_elapsed <= self.time_ranges[key][1]:
                    time_color = self.time_ranges[key][2]
                    break
            assert time_color is not None

            task_line = f'{str(task)}{task.solve()}'
            user_anser_line = f"({str(task.user_answer)})"
            colored_line = f"{task_line} <span style='color: {results_color};'>{user_anser_line}</span>"
            colored_time = f"<span style='color: {time_color};'>⌛ {task.time_elapsed}</span>"

            lines.append(colored_line + colored_time)

        results = HTML_NEWLINE.join(lines)
        return results

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        """
        Overwrites `closeEvent` to display the main window after closing the table.
        :param event:
        :return:
        """
        main_window = findMainWindow()
        if main_window is not None:
            main_window.show()
        self.exam_window_class.close()
        event.accept()


if __name__ == '__main__':
    current_time = datetime.now()
    time_stamp = datetime.now().strftime('%Y.%m.%d_%H-%M-%S')
    logging.basicConfig(level=logging.DEBUG, filename=f"py_log_{time_stamp}.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    # todo:
    #  stopwatch - how long it takes to solve this example
    #  stopwatch - how long the entire session takes (solving time only)
    #  no text interface - only icons

    # ■▣◀◁▶▷◼◽◾↪↩↵√Ꚙ∞±×⏸⏩

# todo: use this symbol ✍ (writing hand) instead of Start_the_test.png?
# todo: add scrollbar in the results windows
# todo: tasks in the results window should be separated into 4 columns: wrong, slow, medium, fast
