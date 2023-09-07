"""
Questions module.

Class Question for work with one separate question.
Class Questions for work with a list of Questions.
"""

import os
import os.path
from random import choice


PROJECT_PATH = os.path.dirname(__file__)
QUESTIONS_FOLDER = 'test_questions'
SEP = f"{'-'*50}"


class Question:
    """
    A separate question.
    """
    def __init__(self, question, answ1, answ2, answ3, answ4, correctAnsw):
        self._question = question
        self._answers = [answ1, answ2, answ3, answ4]
        self._curAnswers = self._answers
        self._correctAnswNum = correctAnsw

    def __str__(self):
        return f"{SEP}\n{self._question}\n{SEP}\n{self.getCurAnswersStr()}{SEP}"

    def isCorrectAnswer(self, answNum):
        """
        Check if the answer is correct
        :param answNum: positional number of the answer
        :return: True/False
        """
        return self._correctAnswNum == answNum

    def getCorrectAnswer(self):
        """
        Get correct answer
        :return: correct answer
        """
        return self._answers[self._correctAnswNum-1]

    def useHint(self, hint):
        """
        Get a hint
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
        :return: current answers
        """
        return self._curAnswers

    def getCurAnswersStr(self):
        """
        Get current answers as string
        :return: string of current answers
        """
        return f"1: {self._curAnswers[0]:15} 3: {self._curAnswers[2]:15}\n" \
               f"2: {self._curAnswers[1]:15} 4: {self._curAnswers[3]:15}\n"


class Questions:
    """
    Random questions from txt files
    """
    _folder = QUESTIONS_FOLDER
    _path = os.path.join(PROJECT_PATH, _folder)

    def __init__(self):
        self._questions = None
        self._loadQuestions()

    def _loadQuestions(self):
        """
        Load random questions from txt files
        :return: None
        """
        files = self._findQuestionFiles()
        self._questions = [None]*len(files)
        for file in files:
            self._loadLevelQuestion(file)

    def _findQuestionFiles(self):
        """
        Find txt files in the questions folder
        :return: a list of files paths
        """
        fileNames = os.listdir(Questions._path)
        filePaths = []

        for fileName in fileNames:
            filePath = os.path.join(Questions._path, fileName)
            if os.path.isfile(filePath) and os.path.splitext(filePath)[1] == '.txt':
                filePaths.append(filePath)

        return filePaths

    def _loadLevelQuestion(self, filePath):
        """
        Load random question from specified txt file
        :param filePath: path to txt file with questions
        :return: None
        """
        with open(filePath, "r") as file:
            data = file.readlines()

        line = choice(data)
        q, a1, a2, a3, a4, ca = line[:-1].split("\t")   # without the last '/n'
        ind = int(os.path.basename(filePath)[:-4])      # without the last '.txt'
        self._questions[ind-1] = Question(q, a1, a2, a3, a4, int(ca))

    def getQuestions(self):
        """
        Get a list of questions
        :return: a list of questions
        """
        return self._questions
