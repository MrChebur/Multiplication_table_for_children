import string
import time


class Task:
    """Class contains a task that the child will solve."""
    user_answer = None
    start_time = None
    time_elapsed = None
    dot2comma = True

    __supported_operators = '+-*/() '
    __allowed_characters = string.digits + __supported_operators + '.,'  # is used to limit the execution of `eval()`

    def __init__(self, task: str, dot2comma=True):
        """
        :param task: The string with the task. Example: '1 + 1'
        :param dot2comma: Replace dot with comma in `print()` function
        """
        self.dot2comma = dot2comma
        self.task_string = task
        self._checkParameters()

    def isCorrect(self):
        if self.user_answer == self.solve():
            return True
        return False

    def _checkParameters(self):
        """Check parameters to make sure they don't harm us with `eval()` function.
        :return:
        """
        unallowed_characters = [task_sub_str for task_sub_str in self.task_string if
                                task_sub_str not in self.__allowed_characters]
        assert unallowed_characters == [], f'The task contain unallowed characters: {unallowed_characters}'

    def solve(self):
        """Solve the task and return result"""
        self._checkParameters()  # check again
        result = eval(self.task_string)  # Ye, eval() is bad, but input parameters are checked before execution!
        if float(result) == int(result):
            return int(result)
        return result

    def startTimer(self):
        self.start_time = time.time()

    def stopTimer(self):
        self.time_elapsed = round(time.time() - self.start_time, 2)

    def __str__(self):
        """print() overload"""
        new_str = self.task_string + ' = '
        if self.dot2comma:
            new_str.replace('.', ',')
        return new_str

    def request_answer(self, validate=True):
        print(t, end='')
        t.startTimer()
        # TODO pip install restricted_input https://pypi.org/project/restricted-input/ restrict user input in real time
        self.user_answer = float(input())
        t.stopTimer()
        if validate:
            if self.isCorrect():
                print('Correct!')
            else:
                print('Error!')


if __name__ == '__main__':
    t = Task('1 + 1')  # 2
    t.request_answer()

    t = Task('2 * 2')  # 4
    t.request_answer()

    t = Task('8 / 2')  # 4
    t.request_answer()

    t = Task('1 + 2 * 3')  # 7
    t.request_answer()

    t = Task('3.6 / 6')  # 0.6
    t.request_answer()

    t = Task('(2 + 4) + ( 2 + 2 ) * 5')  # 26
    t.request_answer()

    t = Task('(2 + 4 + 2 + 2 ) * 5')  # 50
    t.request_answer()
