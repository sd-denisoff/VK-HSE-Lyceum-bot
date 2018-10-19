import secrets
import sys
import gameData
import statusVars as status
import data.phrases as ph

sys.path.insert(0, '../userData')
from activeUsers import activeUsers

__version__ = '0.0.4'

class Launcher:
    gameByName = list()
    userSessionId = dict()
    gamesName = dict()

    def __init__(self):
        self.gameByName = gameData.GamesData.gamesClass
        self.gamesName = gameData.GamesData.searchKeyWords

    #def showGameList(self):

    def startGameByName(self, userId, gameName):
        gameName = gameName.lower()

        if (gameName in ph.askEndGamePhrases):
            self.endGame(userId)
            return (status.END_GAME, [ph.messEndGame], None)

        gameId = None

        for word in gameName.split():
            if (self.gamesName.get(word) != None):
                gameId = self.gamesName[word]

        if (gameId == None):
            activeUsers.get(userId).choosingGame()
            return (status.RESUME_GAME, [ph.messNoSuchTitleGame, ph.messTryAgain], [ph.buttonBreak])

        #activeUsers.get(userId).attachGame()
        return self.startGame(userId, gameId)

    def startGame(self, userId, gameName):
        generatedSessionKey = secrets.token_hex(16)
        self.userSessionId[userId] = (gameName, generatedSessionKey)
        try:
            gameAnswer, gameHelpMes = self.gameByName[gameName].startSession(generatedSessionKey)
            activeUsers.get(userId).attachGame()
            return (status.RESUME_GAME, gameAnswer, gameHelpMes)
        except:
            self.userSessionId[userId] = None
            activeUsers.get(userId).continueGame()
            return (status.RESUME_GAME, [ph.messNoSuchGame, ph.messTryAgain], [ph.buttonBreak])

    def nextStep(self, userId, tranferData):
        if (tranferData.lower() in ph.askEndGamePhrases):
            self.endGame(userId)
            return (status.END_GAME, [ph.messEndGame], None)

        userGameData = self.userSessionId.get(userId)
        if (userGameData == None):
            activeUsers.get(userId).detachGame()
            return (["Incorrect Session Key! Try to reboot game!"], None)

        gameName, sessionId = userGameData
        gameStatus, gameAnswer, gameHelpMes = self.gameByName[gameName].nextStep(sessionId, tranferData)

        if (gameStatus == status.END_GAME):
            self.endGame(userId)

        return (gameStatus, gameAnswer, gameHelpMes)

    def endGame(self, userId):

        activeUsers.get(userId).detachGame()

        userGameData = self.userSessionId.get(userId)
        if (userGameData == None):
            return
        gameName, sessionId = userGameData
        gameAnswer = self.gameByName[gameName].closeSession(sessionId)
        self.userSessionId[userId] = None
