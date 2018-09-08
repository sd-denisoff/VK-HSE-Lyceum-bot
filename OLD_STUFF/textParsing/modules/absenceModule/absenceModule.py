import statusVars as status
import launcher

import sys

sys.path.insert(0, '../../userData')
from activeUsers import activeUsers

gameLauncher = launcher.Launcher()

class AbsenceModule:
    memory = dict()
    def getAnswer(self, answers, quickAnswers):
        resultQuery = list()
        for answer in answers:
            curQuery = {}
            curQuery['answered'] = True
            curQuery['generatedText'] = answer
            resultQuery.append(curQuery)

        resultQuery[-1]['quickAnswers'] = quickAnswers
        return resultQuery

    def nextStep(self, userId, userText):
        if (self.memory.get(userId) == None):
            self.memory[userId] = 1
            return ("COUNTINUE", self.getAnswer(["Вы уверены?"], ["Да", "Нет"]))

        if (self.memory.get(userId) == 1):
            self.memory[userId] = None
            if (userText == "Да"):
                return ("END", self.getAnswer(["Soon"], None))
            else:
                return ("END", self.getAnswer(["Отменено"], None))
