"""
Questions module.

Class Question for work with one separate question.
Class Questions for work with a list of Questions.
"""

import os
import os.path
from random import choice


PROJECT_PATH = os.path.dirname(__file__)
#print(PROJECT_PATH)
QUESTIONS_FOLDER = 'test_questions' # пут для смены вопросов на настоящие
SEP = f"{'-'*50}"


class Question:
    """
    A separate question. / Для конкретного одного вопроса
    """
    def __init__(self, question, answ1, answ2, answ3, answ4, correctAnsw):
        self._question = question
        self._answers = [answ1, answ2, answ3, answ4]
        self._curAnswers = self._answers  # список вариантов вопросов на текущий момент - если использовал подсказки и тд
        self._correctAnswNum = correctAnsw

    def __str__(self): # Метод __str__возвращает форматированное строковое представление вопроса
                       # и вызывается когда выполняем команду print и передаем в неё обхект типа Question
        return f"{SEP}\n{self._question}\n{SEP}\n{self.getCurAnswersStr()}{SEP}"

    def isCorrectAnswer(self, answNum):
        """
        Check if the answer is correct / проверяем правильность варианта ответа
        :param answNum: positional number of the answer
        :return: True/False
        """
        return self._correctAnswNum == answNum

    def getCorrectAnswer(self):
        """
        Get correct answer / возвращаем правильный ответ
        :return: correct answer
        """
        return self._answers[self._correctAnswNum-1]

    def useHint(self, hint):
        """
        Get a hint / для каждого вопроса можем использовать подсказку
        - этот метод реализует использование подсказки
        :param hint: hint object
        :return: hint phrase
        """
        answs, phrase = hint.getHint(self._curAnswers, self._correctAnswNum-1)
        if answs:
            self._curAnswers = answs
            phrase = self.getCurAnswersStr()
        return f"\n{SEP}\n{phrase}{SEP}"

    def getCurAnswers(self):
        """
        Get current answers (could be only 2 answers after 50/50 hint)
        Возвращает текущий вариант ответа: либо все 4, либо после подсказок
        :return: current answers
        """
        return self._curAnswers

    def getCurAnswersStr(self):
        """
        Get current answers as string
        Генерирует строчкуу для вывода вариантов ответа
        :return: string of current answers
        """
        return f"1: {self._curAnswers[0]:15} 3: {self._curAnswers[2]:15}\n" \
               f"2: {self._curAnswers[1]:15} 4: {self._curAnswers[3]:15}\n"


class Questions:
    """
    Random questions from txt files / Для списка вопросов
    """
    _folder = QUESTIONS_FOLDER
    _path = os.path.join(PROJECT_PATH, _folder)

    def __init__(self):
        self._questions = None  # список вопросов, которое изначально пустое
                                # - в итоге тут мы получаем список элементов типа вот этого класса class Question:
                                #     """
                                #     A separate question. / Для конкретного одного вопроса
                                #     """
                                #     def __init__(self, question, answ1, answ2, answ3, answ4, correctAnsw):
        self._loadQuestions()  # дальше загружаем вопросы

    def _loadQuestions(self):
        """
        Load random questions from txt files
        :return: None
        """
        files = self._findQuestionFiles() # находим вопросы
        self._questions = [None]*len(files) #список вопросов, длина кот равна количетсву  Строка кода инициализирует этот список Noneзначениями, а количество Noneзначений определяется длиной списка files.  Используя [None]*len(files), создаем список длиной, равной количеству файлов вопросов ( len(files)). Это гарантирует, что в списке будет место для каждого вопроса, который планируется загрузить.
        for file in files: #  и далее поочередно начинамем читать и загружать фуже конкретные вопросы для конкретного уровня
            self._loadLevelQuestion(file)

    def _findQuestionFiles(self):
        """
        Find txt files in the questions folder / Тут мы находим все текстовые файлы, которые находятся в обозначенной директории
        Короче говоря, этот метод ищет в папке вопросов текстовые файлы, собирает их полные пути и возвращает их в списке
        :return: a list of files paths
        """
        fileNames = os.listdir(Questions._path) # Эта строка использует os.listdirфункцию для получения списка всех имен файлов и каталогов в каталоге, указанном Questions._path. Questions._path— это полный путь к папке с вопросами, как определено ранее в классе.
        filePaths = []  # пустой список, который будет использоваться для хранения путей к текстовым файлам, найденным в папке

        for fileName in fileNames:
            filePath = os.path.join(Questions._path, fileName)
            if os.path.isfile(filePath) and os.path.splitext(filePath)[1] == '.txt': # os.path.isfile(filePath)проверяет, действительно ли текущий элемент является файлом (а не каталогом)
                                                # os.path.splitext(filePath)[1] == '.txt'проверяет, является ли расширение файла «.txt». os.path.splitextразбивает путь к файлу на кортеж, содержащий базовое имя и расширение, и [1]выбирает часть расширения.
                filePaths.append(filePath)

        return filePaths

    def _loadLevelQuestion(self, filePath):
        """
        Load random question from specified txt file
        эти строки кода считывают строку из файла, разбивают ее на компоненты
        (вопрос, варианты ответа и правильный ответ), извлекают уровень или индекс из имени файла и
        создают объект с извлеченной информацией Question. Этот процесс повторяется для каждой
        строки файла, эффективно загружая несколько вопросов из файла и сохраняя их в _questionsсписке.
        :param filePath: path to txt file with questions
        :return: None
        """
        with open(filePath, "r") as file:
            data = file.readlines()

        line = choice(data)
        q, a1, a2, a3, a4, ca = line[:-1].split("\t")   # without the last '/n'
        ind = int(os.path.basename(filePath)[:-4])      # without the last '.txt' = «3.txt», на этом шаге цифра «3» извлекается как целое число.
        self._questions[ind-1] = Question(q, a1, a2, a3, a4, int(ca)) # генерируем объект Question!

    def getQuestions(self):
        """
        Get a list of questions
        Вернуть все случайно рандомно загруженные вопросы для данной игры
        :return: a list of questions
        """
        return self._questions
