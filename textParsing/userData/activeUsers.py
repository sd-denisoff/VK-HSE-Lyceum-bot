from user import *

class ActiveUsers:
    activeUsers = {}

    def show(self):
        print(self.activeUsers.keys())

    def add(self, userId):
        self.activeUsers[userId] = User(userId)

    def get(self, userId):
        return self.activeUsers.get(userId)

    def remove(self, userId):
        self.activeUsers[userId] = None

activeUsers = ActiveUsers()
