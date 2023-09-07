import os.path
from game import Game

"""автоматически генерирует тестовые файлы с вопросами"""
LEVELS = Game._levels

PROJECT_PATH = os.path.dirname(__file__)
QUESTIONS_PATH = os.path.join(PROJECT_PATH, "test_questions")


def generateQuestion(level, num):
    correct_answ = num%4 if num%4 != 0 else 4
    #print(f"{level} - question {num}?\tansw1\tansw2\tansw3\tansw4\t{correct_answ}\n")
    return f"{level} - question {num}?\tansw1\tansw2\tansw3\tansw4\t{correct_answ}\n"


def generateQuestionFiles():
    for i in range(1, len(LEVELS)+1):
        filePath = os.path.join(QUESTIONS_PATH, f"{i}.txt")
        #print(f"{i}.txt")
        with open(filePath, 'w') as file:
            q = []
            for num in range(1, 11):
                q.append(generateQuestion(i, num))
            file.writelines(q)


if __name__ == "__main__":
    generateQuestionFiles()