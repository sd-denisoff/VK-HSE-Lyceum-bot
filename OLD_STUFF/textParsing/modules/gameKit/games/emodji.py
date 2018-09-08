import statusVars as status
import random

__version__ = '0.0.1'
__author__ = 'Melyohin Nikita, Uchunzhyan Michail'

__title__ = 'emodji songs'
__searchWords__ = ['песню', 'песня']

class Game:

    activeSessions = set()
    history = {}
    lastQuestion = {}

    questions = []
    answers = []
    questions_path = 'textParsing/modules/gameKit/games/emodjiData/questions.txt'
    answers_path = 'textParsing/modules/gameKit/games/emodjiData/answers.txt'

    helpText = 'Подсказка'
    nextTask = 'Сдаюсь'

    def __init__(self):

        curLine = ''

        with open(self.questions_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for id, line in enumerate(lines):
            if (len(line) == 0 or id == len(lines)-1):
                self.questions.append(curLine)
                curLine = ''

            line = line.lower()
            curLine += line + '\n'

            if (id == len(lines)-1 and len(line) >= 3):
                self.questions.append(curLine)
                curLine = ''

        with open(self.answers_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for id, line in enumerate(lines):
            if (len(line) < 3):
                continue

            line = line.lower()
            name, author = line.split(' - ')

            self.answers.append((name, author))

    def startSession(self, sessionId):
        self.activeSessions.add(sessionId)
        self.history[sessionId] = []
        return self.genNewSessionTest(sessionId)

    def help(self, sessionId, inputText):
        lastNum = self.lastQuestion[sessionId]
        name, author = self.answers[lastNum]
        return (status.RESUME_GAME, ['Автор это песни - ' + str(author)], [self.helpText, self.nextTask])

    def next(self, sessionId, inputText):
        lastNum = self.lastQuestion[sessionId]
        name, author = self.answers[lastNum]

        messages = ['Это же ' + name + ' от ' + author, 'Так дальше...']
        return self.genNewTest(sessionId, messages)

    def nextStep(self, sessionId, inputText):

        if (inputText == self.helpText):
            return self.help(sessionId, inputText)

        if (inputText == self.nextTask):
            return self.next(sessionId, inputText)

        inputText = inputText.lower()

        if (self.checkLast(sessionId, inputText)):
            return self.genNewTest(sessionId, ['Верно, вот еще!'])
        else:
            return (status.RESUME_GAME, ['Неправильный ответ', 'Можно воспользоваться подсказской'], [self.helpText, self.nextTask])

    def checkLast(self, sessionId, inputText):
        lastNum = self.lastQuestion[sessionId]
        name, author = self.answers[lastNum]
        return name == inputText

    def genNewTest(self, sessionId, startPharse):
        numbers = []
        for i in range(0, len(self.answers)):
            numbers.append(i)

        messages = []
        for pharse in startPharse:
            messages.append(pharse)

        random.shuffle(numbers)

        for num in numbers:
            if not(num in self.history[sessionId]):
                self.history[sessionId].append(num)
                self.lastQuestion[sessionId] = num
                messages.append(self.questions[num])
                return (status.RESUME_GAME, messages, [self.helpText, self.nextTask])

        return (status.END_GAME, ['game end'], None)

    def genNewSessionTest(self, sessionId):
        numbers = []
        for i in range(0, len(self.answers)):
            numbers.append(i)

        random.shuffle(numbers)

        for num in numbers:
            if not(num in self.history[sessionId]):
                self.history[sessionId].append(num)
                self.lastQuestion[sessionId] = num
                return (['Привет!', self.questions[num]], [self.helpText, self.nextTask])

    def closeSession(self, sessionId):
        self.activeSessions.remove(sessionId)
        self.history[sessionId] = None
