import random
import statusVars as status

__version__ = '0.0.2'
__author__ = 'Melyohin Nikita'

#requared params
__title__ = 'cities'
__searchWords__ = ['cities', 'города', 'город', 'city']

data_path = 'textParsing/modules/gameKit/games/citiesData/cities.txt'

class Game:
    activeSessions = set() #all sessions' data here
    wordData = {} #all data about used words
    prevWord = {}  # all data about used words
    words = {}
    wordByLetter = {}

    helpText = 'Подсказка'
    ruleText = 'Отлично! Вы называете город, я говорю город на последнюю букву — и так далее. Только учтите — буквы "ь", "ы" и "й" не считаются.'
    endGame_NoWords = 'Жаль, но города закончилось. И игра. Спасибо, мне было очень интересно с Вами играть.'

    def __init__(self):

        voc = set('йцукенгшщзхъфывапролдёжэячсмитьбюqwertyuiopasdfghjklzxcvbnm ')

        for l in voc:
            self.wordByLetter[l] = []

        with open(data_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for line in lines:
            if (len(line) == 0):
                continue
            line = line.lower()
            line = line.replace('ё', 'е')
            self.wordByLetter[line[0]].append(line)

    def startSession(self, sessionId):
        # adding and prepearing new session
        self.wordData[sessionId] = set()
        self.prevWord[sessionId] = None
        self.activeSessions.add(sessionId)
        startPhrase = 'Говорите, а я подхвачу.'
        return ([startPhrase], ['Правила'])

    def help(self, sessionId):
        lastWord = self.prevWord[sessionId]
        newWord = self.generateHelpAnswer(sessionId, lastWord)
        result = ''
        print(newWord)
        if (len(newWord) >= 8):
            result = newWord[:3] + '...' + newWord[len(newWord)-3:len(newWord)]
        elif (len(newWord) >= 6):
            result = newWord[:2] + '...' + newWord[len(newWord)-2:len(newWord)]
        else:
            result = newWord[:1] + '...' + newWord[len(newWord)-1:len(newWord)]

        return (status.RESUME_GAME, [result + ' ничего не напоминает?'], [self.helpText])

    def rule(self):
        return (status.RESUME_GAME, [self.ruleText, 'А теперь продолжим.'], None)


    def generateHelpAnswer(self, sessionId, inputText):

        lastLetter = self.getLastLetter(inputText)

        words = self.wordByLetter[lastLetter]

        random.shuffle(words)

        for word in words:
            if (self.wasWord(sessionId, word) == False):
                return word

        return None

    # this method get session id and text which was inputed by user
    def nextStep(self, sessionId, inputText):
        if len(inputText) == 0:
            return (status.RESUME_GAME, ['Может не будем города придумывать?'], [self.helpText])

        if (inputText == self.helpText):
            return self.help(sessionId)

        if (inputText == 'Правила'):
            return self.rule()

        inputText = inputText.lower()
        #return answer to user

        if (self.wasWord(sessionId, inputText) == True):
            return (status.RESUME_GAME, ['Это слово уже было, я все помню)'], [self.helpText])

        if (self.hasCity(inputText) == False):
            return (status.RESUME_GAME, ['Может не будем города придумывать?'], [self.helpText])

        if (self.canUseCity(sessionId, inputText) == False):
            return (status.RESUME_GAME, ['Слово должно начинаться на ' + self.getLastLetter(self.prevWord[sessionId])], ['Подсказка'])

        self.addWord(sessionId, inputText)
        return self.generateAnswer(sessionId, inputText)

    #this method will be call when user will choose another game or end playing your game
    def closeSession(self, sessionId):
        #here you can delete data
        self.wordData[sessionId] = None
        self.prevWord[sessionId] = None
        self.activeSessions.remove(sessionId)

    def wasWord(self, sessionId, inputText):
        if (inputText in self.wordData[sessionId]):
            return True
        else:
            return False

    def addWord(self, sessionId, inputText):
        self.wordData[sessionId].add(inputText)

    def getLastLetter(self, where):
        if (where == None):
            return None
        notEnd = set('ьъый')
        lastLetter = where[-1]
        if (lastLetter in notEnd):
            lastLetter = where[-2]

        return lastLetter

    def canUseCity(self, sessionId, userCity):
        lastLetter = self.getLastLetter(self.prevWord[sessionId])
        if (lastLetter == None):
            return True
        return lastLetter == userCity[0]

    def haveAnswer(self, sessionId):
        lastLetter = self.getLastLetter(self.prevWord[sessionId])
        words = self.wordByLetter[lastLetter]

        for word in words:
            if (self.wasWord(sessionId, word) == False):
                return True
        return False


    def generateAnswer(self, sessionId, inputText):
        lastLetter = self.getLastLetter(inputText)

        words = self.wordByLetter[lastLetter]

        random.shuffle(words)

        for word in words:
            if (self.wasWord(sessionId, word) == False):
                self.wordData[sessionId].add(word)
                self.prevWord[sessionId] = word

                if (self.haveAnswer(sessionId) == False):
                    return (status.END_GAME, [self.endGame_NoWords], None)

                return (status.RESUME_GAME, ['Я выбрал - ' + word], [self.helpText])

        return (status.END_GAME, [self.endGame_NoWords], None)

    def hasCity(self, inputText):
        inputText = inputText.replace('ё', 'е')
        firstLetter = inputText[0]
        if (inputText in self.wordByLetter[firstLetter]):
            return True
        else:
            return False
