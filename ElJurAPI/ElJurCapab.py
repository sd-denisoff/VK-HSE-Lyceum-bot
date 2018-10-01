from config import *
from models import *
from ElJurAPI.Schedule import ScheduleState
from ElJurAPI.Homework import HomeworkState
from ElJurAPI.Marks import MarksState
from ElJurAPI.UserInfo import UserInfoState
from actions import default_keyboard
from calendar_keyboard import create_calendar
import datetime


class EljurCapab(object):
    def __init__(self):
        self._state = None

    def change_state(self, option):
        if option == 'schedule':
            schedule_state = ScheduleState()
            self._state = schedule_state
        elif option == 'homework':
            homework_state = HomeworkState()
            self._state = homework_state
        elif option == 'marks':
            marks_state = MarksState()
            self._state = marks_state
        elif option == 'user_info':
            user_info_state = UserInfoState()
            self._state = user_info_state

    def kind_of_content(self, id):
        user = User.get(User.id == id)
        if user.token is not None:
            func = getattr(self._state, 'kind_of')
            func(id)
        else:
            vk.messages.send(user_id=id, message='Функция недоступна. Пройдите авторизацию в ЭлЖур', keyboard=default_keyboard)

    def get_content(self, id):
        func = getattr(self._state, 'get')
        content = func(id)
        eljur_capab.send_content(id, content)

    def send_content(self, id, content):
        if content is not None:
            func = getattr(self._state, 'send')
            func(id, content)


def kind_processing(data, id):
    user = User.get(User.id == id)
    if data['text'] == 'Сегодня':
        user.date = datetime.date.today().strftime('%Y%m%d')
    elif data['text'] == 'Завтра':
        user.date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')
    elif data['text'] == 'На неделю' or data['text'] == 'Всё актуальное':
        user.date = ''
    user.save()

    if data['text'] == 'Дата':
        vk.messages.send(user_id=id, message='Календарь 👇', keyboard=create_calendar())
    else:
        eljur_capab.get_content(id)


eljur_capab = EljurCapab()
