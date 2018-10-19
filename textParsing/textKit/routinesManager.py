class routinesManager:
    routines = dict()

    def getAnswer(self, answers, quickAnswers):
        resultQuery = list()
        for answer in answers:
            curQuery = {}
            curQuery['answered'] = True
            curQuery['generatedText'] = answer
            resultQuery.append(curQuery)

        resultQuery[-1]['quickAnswers'] = quickAnswers
        return resultQuery

    def smartSplit(self, s):
        firstSpace = s.find(" ")
        return (s[:firstSpace-1], s[firstSpace+1:])

    def fixStr(self, s):
        lastElementOnIndex = -1
        index = 0
        for char in s:
            if char != " ":
                lastElementOnIndex = index
            index+=1

        return self.delSign(s[:lastElementOnIndex+1])

    def delSign(self, s):
        delitable_sign = set('[]{}();:",.?!')
        for i in delitable_sign:
            s = s.replace(i, '')
        return s

    def all(self):
        print(self.routines.keys())

    def add(self, userText):
        userText = userText.lower()
        commands, body = self.smartSplit(userText)
        body = body.split(':')
        if (len(body) != 2):
            return self.getAnswer(["Неверный формат. Пример: /addRoutines название:команда1,команда2,(...)"], None)
        self.routines[self.fixStr(body[0])] = body[1].split(',')
        return self.getAnswer(["Добавлено"], None)

    def get(self, userText):
        userText = self.fixStr(userText.lower())
        return self.routines.get(userText)
