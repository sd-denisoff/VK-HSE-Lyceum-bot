from config import *
from models import *
from actions import default_keyboard
from ElJurAPI.Schedule import ScheduleState
# from ElJurAPI.Homework import HomeworkState
import datetime


class EljurCapab(object):
    def __init__(self):
        self._state = None

    def change_state(self, option):
        if option == 'schedule':
            schedule_state = ScheduleState()
            self._state = schedule_state
        # elif option == 'homework':
        #     homework_state = HomeworkState()
        #     self._state = homework_state

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
        # user = User.get(User.id == id)
        # user.date = user.date[:6]
        # user.save()


def kind_processing(data, id):
    user = User.get(User.id == id)
    if data['text'] == 'Сегодня':
        user.date = datetime.date.today().strftime('%Y%m%d')
    elif data['text'] == 'Завтра':
        user.date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')
    elif data['text'] == 'На неделю' or data['text'] == 'Всё актуальное':
        user.date = ''
    user.save()
    # if data['text'] == 'Дата':
    #     now = datetime.now()
    #     user.date = ''.join(str(date(now.year, now.month, 1)).split('-'))[:6]
    #     keyboard = create_calendar(now.year, now.month)
    #     bot.send_message(msg.chat.id, 'Выберите дату', reply_markup=ReplyKeyboardRemove())
    #     bot.send_message(msg.chat.id, 'Просто нажмите на нужный день в календаре!', reply_markup=keyboard)
    #     user.save()
    # else:
    eljur_capab.get_content(id)


eljur_capab = EljurCapab()
