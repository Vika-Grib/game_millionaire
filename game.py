"""
Game class
"""

import os
import hints
from questions import Questions
from colors import *


class Game:
    """
    Game class
    """
    _levels = [100, 200, 300, 500, 1000,
               2000, 4000, 8000, 16000, 32000,
               64000, 125000, 250000, 500000, 1000000]  # список сумм, кот игрок получает при ответе на очередной вопрос
    _levelsNum = len(_levels)  # количество уровней - можем добавлять уровни в _levels и они будут учитываться в будущем
    _guaranteedSums = [_levels[4], _levels[9], _levels[14]]

    def __init__(self, userName):
        self._questions = Questions().getQuestions()  # сразу мы получаем список вопросов для игры - обращаемся к классу Questions и методу getQuestions, кот возвращает нам рандомный список вопросов
        self._userName = userName   #храним имя пользователя
        self._curLevel = -1     # until first question - текущий уровень на котором мы сейчас находимся. т.е. как только мы создаем этот класс - мы еще не перешли к 1-му уровню, поэтому изначально он у нас -1
        self._curPrize = 0      # the last guaranteed sum or the last won sum (if get prize chosen)
        self._hints = [hints.FiftyFifty(), hints.PhoneFriend(), hints.AskAudience()]  # имеющиеся подсказки -- сразу создаем объекты соответствующих классов

    # у всех уровень доступа _protected
    def _getCurQuestion(self):
        """
        Get current question's object -  вопрос текущего уровня
        :return: current question's object
        """
        return self._questions[self._curLevel]

    def _toNextLevel(self):
        """
        Go to the next level
        :return: None
        """
        if self._curLevel < Game._levelsNum - 1:
            self._curLevel += 1
            self._toLevel()
        else:
            self._finish()

    def _toCurLevel(self, showQuestion=True):
        """
        Go back to the current level - если нужно перейти именно к текущему уровню.
        Нужно когда - захотели взять подсказку, взяли - перешли на другой экран с подсказками и после того как мы ее
        использовали - мы хотим вернуться к текущемуу уровню или же мы не импользовали подсказку и нажали клавишу back
        и мы снова хотим вернуться к текущему уровню посмотеть на табл сс суммами, снова посмотреть на вопрос, варинаты
        ответов и тд
        :param showQuestion: show question if True
        :return: None
        """
        self._toLevel(isNextQuestion=False, showQuestion=showQuestion)

    def _toLevel(self, isNextQuestion=True, showQuestion=True): # отпраляем 2 опциональных параметра
        """
        Print question and wait for user's choice - более общая функция,, к которой обращаются предыдущие 2 функкции
        :param isNextQuestion: next question (True) - если переходим на след уровень or current question (False) - если остаемся на текущем
        :param showQuestion: show question (True) or don't show question (False) - хотим ли распечатать снова вопрос
        :return: None
        """
        if isNextQuestion:    # print levels tree
            Game.clearScr()
            self._printLevels()
            # Game.waitForEnter()

        if showQuestion:
            self._printQuestion(isNextQuestion)

        choice = self._getUserChoice()
        self._execUserChoice(choice)

    def _printLevels(self):
        """
        Print levels' tree with the current position and next level's arrow - печатает всё дерево с вопросами и стоимостью за ответы
        :return: None
        """
        for i, l in enumerate(Game._levels):
            if i == self._curLevel:
                print("--> ", end='')
            else:
                print("    ", end='')

            if i == self._curLevel - 1:
                printNegative(f"${l}")
            elif l in Game._guaranteedSums:
                printBold(f"${l}")
            else:
                print(f"${l}")

    def _printQuestion(self, isNextQuestion):
        """
        Print question
        :param isNextQuestion: the next question (True) or the current question (False)
        :return: None
        """
        if isNextQuestion:
            if self._curLevel == 0:
                num = "first"
            elif self._curLevel == Game._levelsNum - 1:
                num = "last"
            else:
                num = "next"

            nextSum = Game._levels[self._curLevel]
            printBold(f"\n{self._userName}, your {num} question for ${nextSum} is:")

        print(self._getCurQuestion())

    def _getUserChoice(self, chooseHint=False):
        """
        Get user's choice -  после каждого вопроса получить выбор пользователя - хочет ли подсказку,ответить на вопрос
        или завершить игру
        :param chooseHint: choose hint (True) or choose answers' option (False)
        :return:
        """
        correctChoices = self._printHintChoices() if chooseHint else self._printAnswerChoices()
        choice = coloredInput(f"\n{self._userName}, enter your choice: ")

        if choice in correctChoices:
            return choice

        printRed("Incorrect input! Please, try again...\n")
        return self._getUserChoice(chooseHint)      # recursion while incorrect input

    def _printAnswerChoices(self):
        """
        Print input options after a question is asked - позволяет распечатать варианты ответа для текущего вопроса
        этот метод подготавливает и печатает доступные для пользователя параметры ввода на основе текущего вопроса
        и наличия подсказок. Варианты включают ответ на вопрос, использование подсказки и выход из игры
        :return: correct input options
        """
        correctInput = []

        answs = self._getCurQuestion().getCurAnswers()  # Эта строка извлекает текущие варианты ответа (варианты) для текущего вопроса с использованием метода _getCurQuestion.
        # Затем он вызывает getCurAnswersметод текущего вопроса, чтобы получить список текущих вариантов ответа: выбрать подсказку или завершить игру

        for i, a in enumerate(answs):  # Функция enumerate() возвращает объект, который генерирует кортежи, состоящие из двух элементов - индекса элемента и самого элемента.
            if a != '':
                correctInput.append(str(i+1))

        printNegative(f"({'/'.join(correctInput)} - for answer, ", end='')  # Он печатает варианты ответа, объединяя элементы списка correctInputкосой чертой ( /), а затем добавляет «- для ответа», чтобы указать, что эти варианты предназначены для ответа на вопроc


        if len(self._getNotUsedHints()) > 0:
            correctInput.extend(['h', 'H'])
            printNegative("H - for hint, ", end='')

        correctInput.extend(['q', 'Q'])
        printNegative(f"Q - for get prize and quit)")

        return correctInput

    def _printHintChoices(self):
        """
        Print input options after 'get hint' is chosen
        Если игрок выбирает подсказку, то ему нужно распечатать какие подсказки у него остались
        :return: correct input options
        """
        notUsedHints = self._getNotUsedHints()
        printBlue(f"\n{self._userName}, you have {len(notUsedHints)} hint(s): ")

        for i, hint in enumerate(notUsedHints):
            printBold(f"{i + 1}: {hint.getName():20}", end='')  # без переноса - в одной строке
        printBold(f"b: Back")

        correctInput = [str(i) for i in range (1, len(notUsedHints)+1)]
        correctInput.extend(['b', 'B'])

        return correctInput

    def _getNotUsedHints(self):
        """
        Get not used hints
        :return: a list of not used hints
        """
        return list(filter(lambda i: not i.isUsed(), self._hints))

    def _execUserChoice(self, choice):
        """
        Execute user's choice
        :param choice: user's choice
        :return: None
        """
        if choice in ['1', '2', '3', '4']:
            self._checkAnswer(int(choice))

        elif choice in ['h', 'H']:
            self._useHint()

        elif choice in ['q', 'Q']:
            if self._curLevel > 0:
                self._curPrize = Game._levels[self._curLevel-1]
            self._finish()

    def _checkAnswer(self, answNum):
        """
        Check if user's answer is correct
        :param answNum: user's choice (positional answer's num)
        :return: None
        """
        if self._getCurQuestion().isCorrectAnswer(answNum):
            printMagenda("\nGreat job, you are absolutely right!\n")
            Game.waitForEnter()

            prize = Game._levels[self._curLevel]
            if prize in Game._guaranteedSums:
                self._curPrize = prize

            self._toNextLevel()
        else:
            printRed("\nOh, no! Unfortunately, you're wrong :-(")
            printBold(f"The correct answer was '{self._getCurQuestion().getCorrectAnswer()}'.\n")
            self._finish()

    def _useHint(self):
        """
        Use a hint
        :return: None
        """
        choice = self._getUserChoice(chooseHint=True)
        if choice in ['b', 'B']:
            self._toCurLevel()
        else:
            notUsedHints = self._getNotUsedHints()
            hint = self._getCurQuestion().useHint(notUsedHints[int(choice) - 1])
            printYellow(hint)
            self._toCurLevel(showQuestion=False)

    def _finish(self):
        """
        Show prize sum and finish the game
        :return: None
        """
        print(f'\n{"="*50}')
        if self._curPrize == Game._guaranteedSums[-1]:
            printBlue(f"{self._userName}, you win $ 1.000.000. CONGRATULATIONS!!!")
        elif self._curPrize != 0:
            printBlue(f"{self._userName}, your prize is ${self._curPrize}. Congratulations!")
        else:
            printBlue(f"{self._userName}, unfortunately you prize is $0.")


    # 3 внешних public метода
    @staticmethod
    def waitForEnter():
        """
        Waiting for Enter
        :return: None
        """
        coloredInput("\nPress 'Enter' to continue...")   # используем наш модуль colors -т.к. часто требуется задавать
                                                         # вопрос и просить нажать enter для продолжения
                                                         # - поэтому в виде отдельного метода

    @staticmethod
    def clearScr(): # каждый раз после того как мы ответили на очередной вопрос - я очищаю экран и перехожу к след вопросу,
        # чтобы вывод не засорял экран и визуально было красиво
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def start(self):  # позволяет непосредственно запустить игру
        """
        Start the game
        :return: None
        """
        printBlue(f"\n{self._userName}, welcome to the game! Let's start :-)\n")
        self._toNextLevel()
