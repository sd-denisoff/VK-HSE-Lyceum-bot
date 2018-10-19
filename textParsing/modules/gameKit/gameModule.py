import statusVars as status
import launcher

import sys

sys.path.insert(0, '../../userData')
from activeUsers import activeUsers

gameLauncher = launcher.Launcher()

class GameModule:

    def getAnswer(self, answers, quickAnswers):
        resultQuery = list()
        for answer in answers:
            curQuery = {}
            curQuery['answered'] = True
            curQuery['generatedText'] = answer
            resultQuery.append(curQuery)

        resultQuery[-1]['quickAnswers'] = quickAnswers
        return resultQuery

    def isUserInGame(self, userId):
        if (activeUsers.get(userId) != None):
            return activeUsers.get(userId).isInGame
        return False

    def isUserChooseGame(self, userId):
        if (activeUsers.get(userId) != None):
            return activeUsers.get(userId).isChoosingGame
        return False

    def nextStep(self, userId, userText):
        if (self.isUserInGame(userId)):
            gameStatus, gameAnswer, gameQuickAnswers = gameLauncher.nextStep(userId, userText)
            returnedStatus = "COUNTINUE"
            if gameStatus == status.END_GAME:
                returnedStatus = "END"
            return (returnedStatus, self.getAnswer(gameAnswer, gameQuickAnswers))

        if (self.isUserChooseGame(userId)):
            gameStatus, gameAnswer, gameQuickAnswers = gameLauncher.startGameByName(userId, userText)
            returnedStatus = "COUNTINUE"
            if gameStatus == status.END_GAME:
                returnedStatus = "END"
            return (returnedStatus, self.getAnswer(gameAnswer, gameQuickAnswers))
