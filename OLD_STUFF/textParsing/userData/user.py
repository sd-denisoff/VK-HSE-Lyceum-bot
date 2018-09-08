import sys

sys.path.insert(0, '../textKit')
from routinesManager import *

__version__ = '0.0.1'

class User:
    id = None
    isInGame = False
    isChoosingGame = False
    activeModule = None
    routines = routinesManager()

    def __init__(self, userId):
        self.id = userId
        self.isInGame = False

    def activateModule(self, moduleName):
        self.activeModule = moduleName


    def exitFromModule(self):
        self.activeModule = None

    #Game
    def attachGame(self):
        self.isInGame = True
        self.isChoosingGame = False

    def choosingGame(self):
        self.isInGame = False
        self.isChoosingGame = True

    def detachGame(self):
        self.isInGame = False
        self.isChoosingGame = False

    def getRoutines(self, text):
        return routines.get(text)
