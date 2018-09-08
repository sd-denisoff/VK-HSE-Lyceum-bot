import sys

sys.path.append('textParsing/textKit/')
import findClass
import findSubject
import findDate
import genTexts
import commandsProcess

sys.path.append('textParsing/userData/')
from user import *
from activeUsers import activeUsers

sys.path.append('textParsing/modules/gameKit/')
import gameModule
sys.path.append('textParsing/modules/absenceModule/')
import absenceModule

sys.path.append('textParsing/faqsKit/')
import faqs

sys.path.append('textParsing/bugReport/')
import bugReport

findDate = findDate.findDate()
findSubject = findSubject.findSubject()
findClass = findClass.findClass()
govorilka = genTexts.genTexts()
faqs = faqs.faqs()
bugReporter = bugReport.bugReporter()
gameModule = gameModule.GameModule()
absenceModule = absenceModule.AbsenceModule()
commandProcess = commandsProcess.CommandsProcess(bugReporter)

# brain.get(user_text)
#  answered => False/True
#  class => [homework, schedule, mark, commands, game, other]
#  date => [YYYYMMDD, next_week, this_week, prev_week, None]
#  subject => [taked from 'data/subjects.csv', None]
#  generatedText => string
#  quickAnswers => array of strings

class brain:
    MAX_ALLOW_SENTENCES_LEN = 52

    def getUserModule(self, userId):
        if (activeUsers.get(userId) != None):
            return activeUsers.get(userId).activeModule
        return None

    def setUserModule(self, userId, moduleName):
        if (activeUsers.get(userId) != None):
            activeUsers.get(userId).activeModule = moduleName

    def err_max_len(self):
        return ['Я еще не научился говорить об этом']

    def getAnswer(self, answers, quickAnswers):
        resultQuery = list()
        for answer in answers:
            curQuery = {}
            curQuery['answered'] = True
            curQuery['generatedText'] = answer
            resultQuery.append(curQuery)

        resultQuery[-1]['quickAnswers'] = quickAnswers
        return resultQuery

    def generateAnswer(self, userId, userText):
        userText = str(userText)

        if (commandProcess.isCommand(userText)):
            return commandProcess.process(userId, userText)

        if (self.getUserModule(userId) == "game"):
            status, answer = gameModule.nextStep(userId, userText)
            if (status == 'END'):
                self.setUserModule(userId, None)
            return answer

        if (self.getUserModule(userId) == "lackof"):
            status, answer = absenceModule.nextStep(userId, userText)
            if (status == 'END'):
                self.setUserModule(userId, None)
            return answer

        #FAQS
        botFAQS = faqs.get(userText)
        if botFAQS != None:
            return self.getAnswer([botFAQS], None)

        if (len(userText) > self.MAX_ALLOW_SENTENCES_LEN):
            botAnswer = [self.err_max_len()]
            botQuickAnswers = None
            return self.getAnswer(botAnswer, botQuickAnswers)

        classType = findClass.get(userText)
        classType = classType[:-1]
        bugReporter.updateHistory(userId, userText, "", classType)

        if (classType == 'game'):
            activeUsers.get(userId).choosingGame()
            self.setUserModule(userId, classType)
            return self.getAnswer(["Choose game"], None)

        if (classType == 'lackof'):
            self.setUserModule(userId, classType)
            status, answer = absenceModule.nextStep(userId, userText)
            if (status == 'END'):
                self.setUserModule(userId, None)
            return answer

        if (classType == 'other'):
            botAnswer = [govorilka.get(userText)]
            botQuickAnswers = [bugReporter.botBugReportPhrase]
            bugReporter.updateHistory(userId, userText, botAnswer, classType)
            return self.getAnswer(botAnswer, botQuickAnswers)

        curQuery = {}
        curQuery['answered'] = False
        curQuery['class'] = classType
        curQuery['date'] = findDate.get(userText)
        curQuery['subject'] = findSubject.get(userText)
        return [curQuery]


    def get(self, userId, userText):
        if (activeUsers.get(userId) == None):
            activeUsers.add(userId)

        if (activeUsers.get(userId).routines.get(userText) != None):
            routinesActions = activeUsers.get(userId).routines.get(userText)
            resultAnswer = list()
            for action in routinesActions:
                curAns = self.generateAnswer(userId, action)
                for answer in curAns:
                    resultAnswer.append(answer)
            return resultAnswer


        return self.generateAnswer(userId, userText)
