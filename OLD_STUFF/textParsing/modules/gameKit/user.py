from launcher import *
import statusVars as status

launcher = Launcher()

__version__ = '0.0.3.1'

class User:
    id = None
    isInGame = False
    choosingGame = False

    def __init__(self, userId):
        self.id = userId
        self.isInGame = False

    def startPhrase(self):
        self.choosingGame = True
        return (['Теперь выберите игру'], None)

    def startGameByName(self, gameId):

        resultStatus, resultMessage, resultHelpMes = launcher.startGameByName(self.id, gameId)

        if (resultStatus == status.END_GAME):
            self.isInGame = False
            self.choosingGame = False

        if (resultStatus == status.NO_GAME):
            self.isInGame = False

        if (resultStatus == status.START_GAME):
            self.isInGame = True
            self.choosingGame = False

        return resultMessage, resultHelpMes

    def startGame(self, gameId):
        self.choosingGame = False
        resultStatus, resultMessage, resultHelpMes = launcher.startGame(self.id, gameId)

        if (resultStatus == status.END_GAME):
            self.isInGame = False
            self.choosingGame = False

        if (resultStatus == status.NO_GAME):
            self.isInGame = False

        if (resultStatus == status.START_GAME):
            self.isInGame = True
            self.choosingGame = False

        return resultMessage, resultHelpMes

    def nextStep(self, inputData):
        resultStatus, resultMessage, resultHelpMes = launcher.continueGame(self.id, inputData)

        if (resultStatus == status.END_GAME):
            self.isInGame = False
            self.choosingGame = False

        return resultMessage, resultHelpMes

    def endGame(self):
        self.isInGame = False
        self.choosingGame = False
        launcher.endGame(self.id)
