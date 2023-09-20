import itertools
import random
from task import Task


# noinspection PyMethodMayBeStatic

class GenerateTasks:

    @staticmethod
    def _generate_uniq_permutations(list1: list, list2: list) -> list:
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

    def sum(self, summands: list[int], limit=None, shuffle=True) -> list[Task]:
        """
        Generate list of difference `Task`s
        :param summands: List of summands to be used in generation.
        :param shuffle: True - will shuffle list randomly, False - the list will be ordered
        :param limit: A value that limits the maximum value of the sum of two summands. Sums exceeding this value will
        not be included in the generated sample. If None no values skipped.
        :return: List of Tasks
        """
        tasks = []
        permutations = self._generate_uniq_permutations(summands, summands)
        for permutation in permutations:
            permutation_as_string = [str(_) for _ in permutation]
            task = Task(' + '.join(permutation_as_string))

            if limit is None:
                tasks.append(task)
            elif task.solve() <= limit:
                tasks.append(task)

        if shuffle:
            random.shuffle(tasks)
        return tasks

    # todo: это полностью неправильный способ генерации!!! Нет многих значений, см. результаты.
    def difference(self, values: list[int], limit=None, shuffle=True) -> list[Task]:
        """
        Generate list of difference `Task`s
        :param values: List of minuend and subtrahend values to be used in generation (reversed generation)
        :param shuffle: True - will shuffle list randomly, False - the list will be ordered
        :param limit: A value that limits the maximum value of the minuend. Minuend exceeding this value will not
        be included in the generated sample. If None no values skipped.
        :return: List of Tasks
        """
        tasks = []
        permutations = self._generate_uniq_permutations(values, values)
        for permutation in permutations:
            random.shuffle(permutation)  # randomizes divisor and result
            minuend = str(permutation[0] + permutation[1])
            subtrahend = str(permutation[0])
            task = Task(f'{minuend} - {subtrahend}')

            if limit is None:
                tasks.append(task)
            elif int(minuend) <= limit:
                tasks.append(task)

        if shuffle:
            random.shuffle(tasks)
        return tasks

    def multiplication(self, multipliers: list[int], shuffle=True) -> list[Task]:
        """
        Generate list of multiplication `Task`s
        :param multipliers: List of multipliers to be used in generation
        :param shuffle: True - will shuffle list randomly, False - the list will be ordered
        :return: List of Tasks
        """
        tasks = []

        if max(multipliers) > 9:
            last_constant_multiplier = max(multipliers)
        else:
            last_constant_multiplier = 9
        constant_multipliers = list(range(2, last_constant_multiplier + 1))

        permutations = self._generate_uniq_permutations(constant_multipliers, multipliers)
        for permutation in permutations:
            permutation_as_string = [str(_) for _ in permutation]
            task = Task(' * '.join(permutation_as_string))
            tasks.append(task)
        if shuffle:
            random.shuffle(tasks)
        return tasks

    # todo: это полностью неправильный способ генерации!!! Нет многих значений, см. результаты.
    def division(self, multipliers: list[int], shuffle=True) -> list[Task]:
        """
        Generate list of division `Task`s
        :param multipliers: List of multipliers to be used in generation (reversed generation)
        :param shuffle: True - will shuffle list randomly, False - the list will be ordered
        :return: List of Tasks
        """
        tasks = []
        permutations = self._generate_uniq_permutations(multipliers, multipliers)
        for permutation in permutations:
            random.shuffle(permutation)  # randomizes divisor and result
            dividend = str(permutation[0] * permutation[1])
            divisor = str(permutation[0])
            task = Task(f'{dividend} / {divisor}')
            tasks.append(task)
        if shuffle:
            random.shuffle(tasks)
        return tasks

    def russian_syllables(self, shuffle=True, skip_censored=True):
        """
        Source:
        https://traditio.wiki/Список_слогов
        https://traditio.wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D0%BB%D0%BE%D0%B3%D0%BE%D0%B2

        :param shuffle: True - will shuffle list randomly, False - the list will be ordered
        :param skip_censored: True - will skip some syllables like 'хуй', False - will return all syllables
        :return: List of russian syllables.
        """

        censored_list = ['ебь', 'ёб', 'еб', 'ёп', 'ёпть', 'хуй', ]
        syllables = ['аб', 'абь', 'ав', 'авь', 'аг', 'агь', 'ад', 'адь', 'аж', 'ажь', 'аз', 'азь', 'аи', 'ай', 'ак',
                     'акь', 'ал', 'аль', 'ам', 'амь', 'ан', 'ань', 'ап', 'апь', 'ар', 'арь', 'ас', 'ась', 'ат', 'ать',
                     'ау', 'аф', 'афь', 'ах', 'ахь', 'ац', 'аць', 'ач', 'ачь', 'аш', 'ашь', 'ащ', 'ащь', 'аю', 'ая',
                     'ба', 'баб', 'баг', 'бар', 'бат', 'бе', 'бё', 'бер', 'берж', 'би', 'бир', 'бо', 'бор', 'борь',
                     'бра', 'бре', 'брит', 'брь', 'бу', 'бъ', 'бы', 'бык', 'бырь', 'бь', 'бэ', 'бю', 'бюст', 'бя', 'ва',
                     'ват', 'вать', 'ве', 'вё', 'век', 'вель', 'вен', 'ви', 'виль', 'во', 'воль', 'все', 'ву', 'въ',
                     'вы', 'выд', 'вый', 'вь', 'вэ', 'вю', 'вя', 'га', 'гад', 'гар', 'гард', 'гат', 'ге', 'гё', 'ги',
                     'гим', 'гин', 'го', 'год', 'горд', 'гу', 'гум', 'гус', 'гусь', 'гъ', 'гы', 'гь', 'гэ', 'гю', 'гюс',
                     'гя', 'да', 'дам', 'дар', 'де', 'дё', 'ди', 'до', 'доз', 'ду', 'дъ', 'ды', 'дыб', 'дым', 'дыр',
                     'дь', 'дэ', 'дю', 'дя', 'еа', 'еб', 'ёб', 'ебь', 'ев', 'ёв', 'евь', 'ег', 'ёг', 'егь', 'ед', 'ёд',
                     'едь', 'ее', 'её', 'еж', 'ёж', 'ежь', 'ез', 'ёз', 'езь', 'еи', 'ей', 'ёй', 'ек', 'ёк', 'екь', 'ел',
                     'ёл', 'ель', 'ем', 'ём', 'емь', 'ен', 'ён', 'ень', 'ео', 'еп', 'ёп', 'ёпть', 'епь', 'ер', 'ёр',
                     'ерь', 'ес', 'ёс', 'есь', 'ет', 'ёт', 'еть', 'еу', 'еф', 'ёф', 'ефь', 'ех', 'ёх', 'ехь', 'ец',
                     'ёц', 'ець', 'еч', 'ёч', 'ечь', 'еш', 'ёш', 'ешь', 'ещ', 'ёщ', 'ещь', 'ею', 'ея', 'жа', 'же', 'жё',
                     'жест', 'жи', 'жо', 'жу', 'жъ', 'жы', 'жь', 'жэ', 'жю', 'жя', 'за', 'зе', 'зё', 'зи', 'зо', 'зу',
                     'зъ', 'зы', 'зь', 'зэ', 'зю', 'зя', 'иб', 'ив', 'иг', 'ид', 'иж', 'из', 'ии', 'ий', 'ик', 'ил',
                     'им', 'ин', 'ип', 'ир', 'ис', 'ит', 'ить', 'иф', 'их', 'иц', 'ич', 'иш', 'ищ', 'ия', 'йод', 'ка',
                     'кар', 'ке', 'кё', 'ки', 'ко', 'ком', 'коч', 'ку', 'къ', 'кы', 'кь', 'кэ', 'кю', 'кя', 'ла', 'ле',
                     'лё', 'лен', 'ли', 'ло', 'лов', 'лон', 'лу', 'лъ', 'лы', 'ль', 'лэ', 'лю', 'люк', 'ля', 'ляж',
                     'ляжь', 'ма', 'мат', 'ме', 'мё', 'мед', 'мёд', 'ми', 'мн', 'мо', 'мод', 'мож', 'мон', 'монт',
                     'мор', 'му', 'муж', 'мъ', 'мы', 'мыт', 'мь', 'мэ', 'мю', 'мя', 'мят', 'на', 'нг', 'не', 'нё', 'ни',
                     'но', 'нов', 'ной', 'ну', 'нъ', 'ны', 'ный', 'нь', 'нэ', 'ню', 'ня', 'об', 'ов', 'ог', 'од', 'ое',
                     'ож', 'оз', 'ой', 'ок', 'ол', 'ом', 'он', 'оо', 'оп', 'ор', 'ос', 'от', 'оу', 'оф', 'ох', 'оц',
                     'оч', 'ош', 'ощ', 'па', 'пас', 'пе', 'пё', 'пёр', 'пёс', 'печь', 'пи', 'по', 'пол', 'порт', 'пру',
                     'прус', 'прусь', 'прян', 'пси', 'пу', 'пъ', 'пы', 'пь', 'пьян', 'пэ', 'пю', 'пя', 'ра', 'раб',
                     'раж', 'раз', 'рап', 'рас', 'рат', 'ре', 'рё', 'реп', 'ри', 'ро', 'роч', 'ру', 'руль', 'рус',
                     'русь', 'ръ', 'ры', 'рь', 'рэ', 'рэп', 'рю', 'ря', 'са', 'свеж', 'се', 'сё', 'сен', 'си', 'ска',
                     'сказ', 'ский', 'ской', 'ску', 'скуй', 'сло', 'сме', 'сне', 'снег', 'со', 'сол', 'солн', 'степ',
                     'степь', 'стэп', 'су', 'суп', 'съ', 'сы', 'сын', 'сь', 'сэ', 'сю', 'ся', 'та', 'тать', 'таю', 'те',
                     'тё', 'тес', 'ти', 'то', 'тор', 'ту', 'тъ', 'ты', 'ть', 'тэ', 'тю', 'тя', 'уб', 'ув', 'уг', 'уд',
                     'уж', 'уз', 'уй', 'ук', 'ул', 'ум', 'ун', 'уп', 'ур', 'ус', 'ут', 'уу', 'уф', 'ух', 'уц', 'уч',
                     'уш', 'ущ', 'ф', 'фа', 'фе', 'фё', 'фи', 'фит', 'фо', 'фу', 'фъ', 'фы', 'фь', 'фэ', 'фю', 'фя',
                     'ха', 'хе', 'хё', 'хи', 'хит', 'хо', 'ху', 'хуй', 'хъ', 'хы', 'хь', 'хэ', 'хю', 'хя', 'ца', 'цап',
                     'це', 'цё', 'ци', 'цип', 'цо', 'цу', 'цъ', 'цы', 'ць', 'цэ', 'цю', 'ця', 'ча', 'че', 'чё', 'чел',
                     'чи', 'чист', 'чка', 'чо', 'чу', 'чъ', 'чы', 'чь', 'чэ', 'чю', 'чя', 'ша', 'ше', 'шё', 'ши', 'шо',
                     'шу', 'шъ', 'шы', 'шь', 'шэ', 'шю', 'шя', 'ща', 'ще', 'щё', 'щёт', 'щи', 'що', 'щу', 'щъ', 'щы',
                     'щь', 'щэ', 'щю', 'щя', 'ъ', 'ыб', 'ыв', 'ыг', 'ыд', 'ыж', 'ыз', 'ый', 'ык', 'ыл', 'ым', 'ын',
                     'ып', 'ыр', 'ыс', 'ыт', 'ыф', 'ых', 'ыц', 'ыч', 'ыш', 'ыщ', 'ь', 'эб', 'эв', 'эвр', 'эг', 'эд',
                     'эж', 'эз', 'эи', 'эй', 'эк', 'эл', 'эм', 'эн', 'эп', 'эр', 'эс', 'эт', 'эф', 'эх', 'эц', 'эч',
                     'эш', 'эщ', 'юб', 'юв', 'юг', 'юд', 'юж', 'юз', 'юй', 'юк', 'юл', 'юм', 'юн', 'юп', 'юр', 'юс',
                     'ют', 'юф', 'юх', 'юц', 'юч', 'юш', 'ющ', 'юя', 'яб', 'яв', 'яг', 'яд', 'яж', 'яз', 'яй', 'як',
                     'ял', 'ям', 'ян', 'яп', 'яр', 'яс', 'ят', 'яу', 'яф', 'ях', 'яц', 'яч', 'яш', 'ящ', 'яю', 'яя',
                     ]

        syllables = list(set(syllables))  # removal of duplicates (if any)
        syllables.sort()

        if skip_censored:
            for syllable in censored_list:
                syllables.remove(syllable)

        if shuffle:
            random.shuffle(syllables)

        return syllables


if __name__ == '__main__':
    g = GenerateTasks()

    # s = g.russian_syllables(shuffle=False)
    # print(s)
    # print(len(s))
    #
    # s = g.russian_syllables(shuffle=False, skip_censored=False)
    # print(s)
    # print(len(s))

    multipliers_ = list(range(2, 10))
    # # print(multipliers_)    #
    # tsks = g.multiplication(multipliers_, shuffle=False)
    # for t in tsks:
    #     print(t, t.solve())
    #

    print()
    tsks = g.division(multipliers_, shuffle=False)
    for t in tsks:
        print(t, t.solve())

    print()
    tsks = g.difference(multipliers_, shuffle=False, limit=10)
    tsks.sort()
    for t in tsks:
        print(t, t.solve())

    # summands_ = list(range(0, 10))
    # print(summands_)
    # tsks = g.sum(summands_, shuffle=False, limit=10)
    # print(len(tsks))
    # for t in tsks:
    #     print(t, t.solve())
