"""
Hints module.
Отдельный модуль, который реализует подсказки
Hints:
    1. 50/50
    2. phone a friend
    3. ask the audience

Abstract base class Hint.

Child class FiftyFifty.
Child class PhoneFriend.
Child class AskAudience.
"""

import os.path
from random import choice, randint
from abc import ABC, abstractmethod


PROJECT_PATH = os.path.dirname(__file__)


class Hint(ABC):
    """
    Abstract base class /
    Абстрактный класс Hint
    """
    def __init__(self):
        self._isUsed = False # каждая подсказка имеет флаг isUsed, т.е. была ли эта подсказка уже использована
        self._name = None  # каждая подсказка имеет имя. В абстрактном классе это имя нулевое

    def isUsed(self):
        """
        Mark hint as already used
        Метод, который возвращает была ли эта подсказка использована
        :return:
        """
        return self._isUsed

    def getName(self):
        """
        Get hint's name
        Возвращает имя нашей подсказки
        :return: hint's name
        """
        return self._name

    @abstractmethod
    def getHint(self, answers, correctAnswNum):
        """
        Abstract method
        Абстрактный метод, который реализует данную подсказку
        :param answers: a list of 4 optional answers
        :param correctAnswNum: positional number of the correct answer in the list
        :return: the tuple (modified answers or None, hint phrase or None)
        """
        pass


class FiftyFifty(Hint):
    """
    50/50 hint
    """
    def __init__(self):
        super().__init__()
        self._name = "50/50"  # устанавливаем имя

    def getHint(self, answers, correctAnswNum):
        """
        Apply a hint
        РЕАЛИЗАЦИЯ ДАННОГО МЕТОДА

        :param answers: a list of 4 optional answers
        :param correctAnswNum: positional number of the correct answer in the list
        :return: a list of 4 optional answers, where 2 incorrect answers replaced with '', None
        """
        self._isUsed = True

        possibleAnswNums = list(range(0, 4))
        possibleAnswNums.remove(correctAnswNum)

        hintAnswNums = [correctAnswNum, choice(possibleAnswNums)]
        hintAnsws = map(lambda i: answers[i] if i in hintAnswNums else '', range(0, 4))

        return list(hintAnsws), None  # возвращаем кортеж из ответов и пустой строки т.к.
                                      # все ответы должны выглядеть одинаково - и мы должны возвращать
                                      # все элементы кортежа, даже если некоторые из них не нужны


class PhoneFriend(Hint):
    """
    Phone a friend hint
    """
    _fileName = "friend_phrases.txt"  # файл с вариантами ответа друга
    _filePath = os.path.join(PROJECT_PATH, _fileName)

    def __init__(self):
        super().__init__()
        self._name = "Phone a friend"  # снова определяем имя нашей подсказки
        self._loadPhrases()

    def _loadPhrases(self):
        """
        Load friend's phrases from the file
        :return: None
        """
        with open(PhoneFriend._filePath, 'r') as f:
            self._phrases = f.readlines()

    def getHint(self, answers, correctAnswNum):
        """
        Apply a hint
        Метод реализующий подсказку
        :param answers: a list of 4 optional answers
        :param correctAnswNum: positional number of the correct answer in the list (unused)
        :return: None, hint phrase
        """
        self._isUsed = True
        hintAnsw = choice(list(filter(lambda i: i != '', answers)))
        phrase = choice(self._phrases)
        return None, phrase.format(hintAnsw)
        # варианты ответа возвращаем те же самые т.е. None, но ещё фразу нашего друга


class AskAudience(Hint):
    """
    Ask the audience hint
    """
    def __init__(self):
        super().__init__()
        self._name = "Ask The Audience"

    def getHint(self, answers, correctAnswNum):
        """
        Apply a hint
        Метод, который вычисляет статистику распределения по ответам
        эта подсказка всегда дает наибольший процент правильному варианту ответа

        :param answers: a list of 4 optional answers
        :param correctAnswNum: positional number of the correct answer in the list
        :return: None, hint phrase
        """
        self._isUsed = True

        remainingSum = 100  # max votes sum - 100%
        votes = [0]*4 #инициализирует список votesс четырьмя элементами, всем из которых изначально присвоено значение 0. В votesсписке будет храниться распределение голосов среди вариантов ответа.


        votes[correctAnswNum] = randint(50, 100)  # generate max vote for the correct answer
        remainingSum -= votes[correctAnswNum]

        # generate votes for the other answers
        for i, a in enumerate(answers): # i представляет индекс выбора ответа и a представляет содержание ответа
            if a == '' or i == correctAnswNum:  # don't generate for the empty answer or for the correct answer again
                continue
            if i == len(answers)-1 or '' in answers:  # last answer in the list or the second non empty answer: также проверяет, является ли это последним ответом в списке или в списке есть пустые ответы. Если это так, он присваивает оставшиеся голоса ( remainingSum) этому варианту ответа, чтобы обеспечить учет всех голосов
                votes[i] = remainingSum
                break
            else:
                votes[i] = randint(0, remainingSum)
                remainingSum -= votes[i]

        return None, self._generatePhrase(answers, votes)
        # None - все вариатны ответов как и были, и второй элемент кортежа - сгенерированная фраза

    def _generatePhrase(self, answers, votes):
        """
        Generate hint phrase
        В ДАННОМ СЛУЧАЕ СГЕНЕРИРОВАННАЯ ФРАЗА ЭТО НАШИ ВАРИАНТЫ ОТВЕТОВ И ДОБАВЛЕННЫЙ К НИМ %
        :param answers: a list of 4 optional answers
        :param votes: a list of audience votes
        :return: hint phrase
        """
        phrase = "" #  инициализирует пустую строкуphrase , которая будет использоваться для построения фразы-подсказки
        for i in [0, 2, 1, 3]:
            tmp = f"{i+1}: "  # Для каждого индекса выбора ответаi создается временная строка tmp, представляющая номер варианта ответа (увеличенный на 1, чтобы соответствовать человеческой нумерации, поскольку Python использует индексацию, начинающуюся с 0), за которой следует двоеточие и пробел
            if answers[i] != '':   # проверяет, не является ли содержимое выбора ответа по индексу iпустой строкой. Если вариант ответа не пуст, он добавляет его к фразе-подсказке.
                tmp += f"{answers[i]} - {votes[i]}%"
            phrase += f"{tmp:20}"

            if i in [2, 3]:
                phrase += '\n'  # если i2 или 3, добавляется символ новой строки.\n

        return phrase
