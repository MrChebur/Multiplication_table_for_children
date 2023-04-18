# from task import Task
from generate import GenerateTasks


def endless():
    multipliers = select_multipliers()
    while True:
        g = GenerateTasks()
        # multipliers = list(range(2, 10))
        tsk = g.multiplication(multipliers, shuffle=True)
        for t in tsk:
            print(t, t.request_answer(), t.solve())

        # print()
        #
        # tsk = g.division(multipliers, shuffle=True)
        # for t in tsk:
        #     print(t, t.solve())

        rep = repeat()
        if rep == 'new multipliers':
            multipliers = select_multipliers()
        elif not rep:
            break

    print('Endless mode is stopped.')


def repeat():
    user_input = input('\n'
                       'Continue? \n'
                       '      y - start again, \n'
                       '      n - select new multipliers \n'
                       'any key - stop \n'
                       )
    if user_input.lower() == 'y':
        return True

    elif user_input.lower() == 'n':
        return 'new multipliers'

    return False


def ask_for_multipliers():
    user_input = input('\nInsert multipliers. Examples: \n'
                       '3,7,9 \n'
                       '* (this means: 2,3,4,5,6,7,8,9) \n'
                       'Your multipliers: '
                       )
    if user_input == '*':
        user_input = '2,3,4,5,6,7,8,9'
    multipliers = parse_multipliers(user_input)
    if not multipliers:
        print(f'Unable to convert multipliers to integer values: {user_input}')
    return multipliers


def parse_multipliers(multipliers: str, delimeter=',') -> list:
    multipliers_list = multipliers.split(delimeter)
    try:
        multipliers_list_as_int = [int(x) for x in multipliers_list]
    except ValueError:
        return []
    return multipliers_list_as_int


def select_multipliers():
    multipliers = None
    while not multipliers:
        multipliers = ask_for_multipliers()
    return multipliers


if __name__ == '__main__':
    endless()
