class bugReporter:
    botBugReportPhrase = '/bug'
    apologyPharse = (['Не знаю, что на меня нашло. Я исправлюсь...'], None)
    conversationHistory = {}
    reportFile = 0
    reportFilePath = 'textParsing/bugReport/reports.txt'

    def __init__(self):
        pass

    def clearHistory(self, userId):
        self.conversationHistory[userId] = None

    def updateHistory(self, userId, userRequest, botAnswer, classType):
        self.conversationHistory[userId] = (userRequest, botAnswer, classType)

    def saveReport(self, userId):
        historyData = self.conversationHistory.get(userId)
        if (historyData != None):
            userText, botAnswer, classType = historyData
            with open(self.reportFilePath, 'a') as reportFile:
                reportFile.write(str(userText) + ';' + str(botAnswer) + ';' + str(classType) + '\n')


    def getConvHistory(self, userId):
        return self.conversationHistory.get(userId)

    def isBugReport(self, text):
        return text == self.botBugReportPhrase
