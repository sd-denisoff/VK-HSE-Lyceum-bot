from config import *
from models import *
from actions import default_keyboard
from ElJurAPI.ElJurRequest import ElJurRequest
from ElJurAPI.AbstractState import AbstractState


class MarksState(AbstractState):
    def get(self, id):
        user = User.get(User.id == id)
        r = ElJurRequest('/getmarks?auth_token=' + user.token)
        if not r.is_valid:
            vk.messages.send(user_id=id, message=r.query, keyboard=default_keyboard)
            return None
        if not r.query:
            vk.messages.send(user_id=id, message='Оценок на этой неделе ещё нет 😔', keyboard=default_keyboard)
            return None
        marks = r.query.get('students', {})
        marks = marks[user.eljur_id].get('lessons', {})
        return marks

    def send(self, id, marks):
        response = 'Оценки на текущей неделе\n\n'
        for subj in marks:
            response += subj['name'] + ' - '
            list_of_marks = subj['marks']
            for mark in list_of_marks:
                response += mark['value'].upper() + ' '
            response += '\n'
        vk.messages.send(user_id=id, message=response, keyboard=default_keyboard)
