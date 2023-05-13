import itertools
import random
from task import Task


class GenerateTasks:

    @staticmethod
    def generate_uniq_permutations(list1: list, list2: list) -> list:
        """
        Generates all possible permutations of the values in the two lists without repeats.

        :param list1: First list of values
        :param list2: Second list of values
        :return: List of permutations of the values without repeats
        """
        permutations_list = []
        for first_multiplier in list1:
            for second_multiplier in list2:
                multipliers = [first_multiplier, second_multiplier]
                multipliers.sort()
                permutations_list.append(multipliers)

        permutations_list.sort()
        permutations_list_without_repeats = list(k for k, _ in itertools.groupby(permutations_list))
        return permutations_list_without_repeats

    def multiplication(self, multipliers: list[int], shuffle=True) -> list[Task]:
        """
        Generate list of multiplication `Task`s
        :param multipliers: List of multipliers to be used in generation
        :param shuffle: True - will shuffle list randomly, False - the list will be ordered
        :return: List of Tasks
        """
        tasks = []
        permutations = self.generate_uniq_permutations(multipliers, multipliers)
        for permutation in permutations:
            permutation_as_string = [str(_) for _ in permutation]
            task = Task(' * '.join(permutation_as_string))
            tasks.append(task)
        if shuffle:
            random.shuffle(tasks)
        return tasks

    def division(self, multipliers: list[int], shuffle=True) -> list[Task]:
        """
        Generate list of division `Task`s
        :param multipliers: List of multipliers to be used in generation (reversed generation)
        :param shuffle: True - will shuffle list randomly, False - the list will be ordered
        :return: List of Tasks
        """
        tasks = []
        permutations = self.generate_uniq_permutations(multipliers, multipliers)
        for permutation in permutations:
            random.shuffle(permutation)  # randomizes divisor and result
            dividend = str(permutation[0] * permutation[1])
            divisor = str(permutation[0])
            task = Task(f'{dividend} / {divisor}')
            tasks.append(task)
        if shuffle:
            random.shuffle(tasks)
        return tasks


if __name__ == '__main__':
    g = GenerateTasks()

    multipliers_ = list(range(2, 10))

    tsk = g.multiplication(multipliers_, shuffle=False)
    for t in tsk:
        print(t, t.solve())

    print()

    tsk = g.division(multipliers_, shuffle=False)
    for t in tsk:
        print(t, t.solve())
