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
    Abstract base class
    """
    def __init__(self):
        self._isUsed = False
        self._name = None

    def isUsed(self):
        """
        Mark hint as already used
        :return:
        """
        return self._isUsed

    def getName(self):
        """
        Get hint's name
        :return: hint's name
        """
        return self._name

    @abstractmethod
    def getHint(self, answers, correctAnswNum):
        """
        Abstract method
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
        self._name = "50/50"

    def getHint(self, answers, correctAnswNum):
        """
        Apply a hint
        :param answers: a list of 4 optional answers
        :param correctAnswNum: positional number of the correct answer in the list
        :return: a list of 4 optional answers, where 2 incorrect answers replaced with '', None
        """
        self._isUsed = True

        possibleAnswNums = list(range(0, 4))
        possibleAnswNums.remove(correctAnswNum)

        hintAnswNums = [correctAnswNum, choice(possibleAnswNums)]
        hintAnsws = map(lambda i: answers[i] if i in hintAnswNums else '', range(0, 4))

        return list(hintAnsws), None


class PhoneFriend(Hint):
    """
    Phone a friend hint
    """
    _fileName = "friend_phrases.txt"
    _filePath = os.path.join(PROJECT_PATH, _fileName)

    def __init__(self):
        super().__init__()
        self._name = "Phone a friend"
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
        :param answers: a list of 4 optional answers
        :param correctAnswNum: positional number of the correct answer in the list (unused)
        :return: None, hint phrase
        """
        self._isUsed = True
        hintAnsw = choice(list(filter(lambda i: i != '', answers)))
        phrase = choice(self._phrases)
        return None, phrase.format(hintAnsw)


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
        :param answers: a list of 4 optional answers
        :param correctAnswNum: positional number of the correct answer in the list
        :return: None, hint phrase
        """
        self._isUsed = True

        remainingSum = 100  # max votes sum - 100%
        votes = [0]*4

        votes[correctAnswNum] = randint(50, 100)  # generate max vote for the correct answer
        remainingSum -= votes[correctAnswNum]

        # generate votes for the other answers
        for i, a in enumerate(answers):
            if a == '' or i == correctAnswNum:  # don't generate for the empty answer or for the correct answer again
                continue
            if i == len(answers)-1 or '' in answers:  # last answer in the list or the second non empty answer
                votes[i] = remainingSum
                break
            else:
                votes[i] = randint(0, remainingSum)
                remainingSum -= votes[i]

        return None, self._generatePhrase(answers, votes)

    def _generatePhrase(self, answers, votes):
        """
        Generate hint phrase
        :param answers: a list of 4 optional answers
        :param votes: a list of audience votes
        :return: hint phrase
        """
        phrase = ""
        for i in [0, 2, 1, 3]:
            tmp = f"{i+1}: "
            if answers[i] != '':
                tmp += f"{answers[i]} - {votes[i]}%"
            phrase += f"{tmp:20}"

            if i in [2, 3]:
                phrase += '\n'

        return phrase
