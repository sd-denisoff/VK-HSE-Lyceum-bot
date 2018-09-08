import statusVars as status

__version__ = '0.0.1'
__author__ = 'Melyohin Nikita'

__title__ = 'sample1'
__searchWords__ = ['sample1', 'пример', 'пример1', 'sample']

class Game:

    activeSessions = set()

    def startSession(self, sessionId):
        # adding and prepearing new session
        self.activeSessions.add(sessionId)
        startPhrase = 'Вы зарегистрированы. Код сессии {0}'.format(sessionId)
        return startPhrase

    def nextStep(self, sessionId, inputText):
        if (inputText == 'stop'):
            return(status.END_GAME, 'ended')

        return (status.RESUME_GAME, '😀')

    def closeSession(self, sessionId):
        self.activeSessions.remove(sessionId)
