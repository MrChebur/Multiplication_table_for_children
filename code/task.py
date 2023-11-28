import string
import time


class Task:
    """Class contains a task that the child will solve."""
    user_answer = None
    start_time = None
    time_elapsed = None
    response_speed = None
    dot2comma = True
    asterisk2multiplication_sign = True

    # is used to limit the execution of `eval()`
    __supported_operators = '+-*/() '  # the space was added intentionally
    __allowed_characters = string.digits + __supported_operators + '.,'

    def __init__(self, task: str, dot2comma=True, asterisk2multiplication_sign=True, slash2devision_sign=True):
        """
        :param task: The string with the task. Example: '1 + 1'
        :param dot2comma: Replace dot with comma in `print()` function
        """
        self.dot2comma = dot2comma
        self.asterisk2multiplication_sign = asterisk2multiplication_sign
        self.slash2devision_sign = slash2devision_sign
        self.task_string = task
        self._checkParameters()

    def isCorrect(self):
        if self.user_answer == self.solve():
            return True
        return False

    def measureAnsweringSpeed(self):
        medium_value = 10
        fast_value = 5

        if self.time_elapsed is None:
            raise AttributeError('The answer has not yet been given. '
                                 'It is not possible to measure the speed of the response.')
        elif 0 <= self.time_elapsed <= fast_value:
            self.response_speed = 'fast'
            return 'fast'
        elif fast_value < self.time_elapsed <= medium_value:
            self.response_speed = 'medium'
            return 'medium'
        elif self.time_elapsed > medium_value:
            self.response_speed = 'slow'
            return 'slow'
        else:
            raise ValueError(f'Strange `self.time_elapsed` value={self.time_elapsed}')

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
            new_str = new_str.replace('.', ',')
        if self.asterisk2multiplication_sign:
            new_str = new_str.replace('*', '×')
        if self.slash2devision_sign:
            new_str = new_str.replace('/', '÷')
        return new_str

    def __lt__(self, other):
        """overload to implement .sort() in [Task]"""
        # noinspection PyProtectedMember
        return self._get_numbers() < other._get_numbers()

    def _get_numbers(self):
        SPLITTER = '%SPLITTER%'
        new_task_string = self.task_string
        for operator in self.__supported_operators:
            if operator == ' ':
                continue
            new_task_string = new_task_string.replace(operator, SPLITTER)

        task_numbers = new_task_string.split(SPLITTER)
        task_numbers = [float(number) for number in task_numbers]

        # print(self.task_string)
        # print(task_numbers)

        return task_numbers

    def request_answer(self, validate=True):
        """
        Only for command line verison!

        :param validate:
        :return:
        """
        print(self, end='')
        self.startTimer()
        self.user_answer = float(input())
        self.stopTimer()
        if validate:
            if self.isCorrect():
                print('Correct!')
            else:
                print('Error!')


if __name__ == '__main__':
    # t = Task('1 + 1')  # 2
    # t.request_answer()
    #
    # t = Task('2 * 2')  # 4
    # t.request_answer()
    #
    # t = Task('8 / 2')  # 4
    # t.request_answer()
    #
    # t = Task('1 + 2 * 3')  # 7
    # t.request_answer()
    #
    # t = Task('3.6 / 6')  # 0.6
    # t.request_answer()
    #
    # t = Task('(2 + 4) + ( 2 + 2 ) * 5')  # 26
    # t.request_answer()
    #
    # t = Task('(2 + 4 + 2 + 2 ) * 5')  # 50
    # t.request_answer()

    # tasks = [
    #     '2 * 5',
    #     '5 * 4',
    #     '1 * 3',
    # ]

    # tasks = [
    #     Task('2.1 * 5'),
    #     Task('5 * 4'),
    #     Task('1 / 3'),
    #     Task('10 + 1'),
    #     Task('1 + 1'),
    #     Task('1 + 5'),
    #     Task('20 + 5'),
    #     Task('30 + 10'),
    # ]

    # for t in tasks:
    #     t._get_numbers()

    import random
    from generate import GenerateTasks

    tasks = GenerateTasks().multiplication(list(range(0, 12)), shuffle=False)

    print(f'\ntasks sorted')
    for t in tasks:
        print(t)

    random.shuffle(tasks)

    print(f'\ntasks shuffled')
    for t in tasks:
        print(t)

    sorted_tasks = tasks.copy()
    sorted_tasks = sorted(sorted_tasks)

    print(f'\ntasks.copy() sorted')
    for t in sorted_tasks:
        print(str(t))
