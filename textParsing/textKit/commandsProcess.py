import sys

sys.path.append('textParsing/userData/')
from activeUsers import activeUsers
sys.path.append('textParsing/bugReport/')
import bugReport

bugReporter = bugReport.bugReporter()

__speechKit__ = 'exp1'
__classKit__ = '0.0.11'
__textKit__ = '0.0.3'
__gameKit__ = '0.0.4'
__faqsKit__ = '0.0.2'
__version__ = '0.0.4'
__build__ = '130518/1640'

class CommandsProcess:
    commands = ['/version', '/myRoutines', '/addRoutines', '/bug']
    bugReporter = 0

    def __init__(self, bugReporter):
        self.bugReporter = bugReporter

    def getAnswer(self, answers, quickAnswers):
        resultQuery = list()
        for answer in answers:
            curQuery = {}
            curQuery['answered'] = True
            curQuery['generatedText'] = answer
            resultQuery.append(curQuery)

        resultQuery[-1]['quickAnswers'] = quickAnswers
        return resultQuery

    def isCommand(self, text):
        command = text.split(" ")[0]
        return command in self.commands

    def process(self, userId, userText):
        command = userText.split(" ")[0]
        #print(command)
        if (userText == '/version'):
            resText = 'speechKit ' + __speechKit__ + '\n'
            resText += 'classifierKit ' + __classKit__ + '\n'
            resText += 'textKit ' + __textKit__ + '\n'
            resText += 'gameKit ' + __gameKit__ + '\n'
            resText += 'faqsKit ' + __faqsKit__ + '\n'
            resText += 'Build ' + __build__ + '\n'
            return self.getAnswer([resText], None)
        if (command == '/addRoutines'):
            return activeUsers.get(userId).routines.add(userText)
        if (command == '/myRoutines'):
            #print(activeUsers.get(userId).routines.get(userText))
            return self.getAnswer(["DEBUG"], None)
        if (command == '/bug'):
            bugReporter.saveReport(userId)
            bugReporter.clearHistory(userId)
            botAnswer, botQuickAnswers = bugReporter.apologyPharse
            return self.getAnswer(botAnswer, botQuickAnswers)
