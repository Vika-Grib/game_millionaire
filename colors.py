"""
Colored print and input functions
"""

bcolors = {'RED': '\033[31m', 'GREEN': '\033[32m', 'YELLOW': '\033[33m',
           'BLUE': '\033[34m', 'MAGENDA': '\033[35m', 'CYAN': '\033[36m',
           'BOLD': '\033[1m', 'UNDERLINE': '\033[4m', 'NEGATIVE': '\033[7m',
           'ENDC': '\033[0m'}


def printRed(str, end='\n'):
    print(f"{bcolors['RED']}{str}{bcolors['ENDC']}", end=end) # {bcolors - ПЕРЕМЕННАЯ, ['RED'] - КЛЮЧ, str - строка, кот выводим пользователю на экран,
    # и везде в конце добавляем bcolors['ENDC'] и end=end если нужно на новую строку или в этой же строке


def printGreen(str, end='\n'):
    print(f"{bcolors['GREEN']}{str}{bcolors['ENDC']}", end=end)


def printYellow(str, end='\n'):
    print(f"{bcolors['YELLOW']}{str}{bcolors['ENDC']}", end=end)


def printBlue(str, end='\n'):
    print(f"{bcolors['BLUE']}{str}{bcolors['ENDC']}", end=end)


def printMagenda(str, end='\n'):
    print(f"{bcolors['MAGENDA']}{str}{bcolors['ENDC']}", end=end)


def printCyan(str, end='\n'):
    print(f"{bcolors['CYAN']}{str}{bcolors['ENDC']}", end=end)


def printBold(str, end='\n'):
    print(f"{bcolors['BOLD']}{str}{bcolors['ENDC']}", end=end)


def printUnderline(str, end='\n'):
    print(f"{bcolors['UNDERLINE']}{str}{bcolors['ENDC']}", end=end)


def printNegative(str, end='\n'):
    print(f"{bcolors['NEGATIVE']}{str}{bcolors['ENDC']}", end=end)


def coloredInput(prompt):
    return input(f"{bcolors['CYAN']}{prompt}{bcolors['ENDC']}")

