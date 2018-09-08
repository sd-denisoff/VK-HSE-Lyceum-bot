from config import *
from models import *
from telebot.types import ReplyKeyboardRemove
from ElJurAPI.Schedule import ScheduleState
from ElJurAPI.Homework import HomeworkState
from InlineCalendar import create_calendar
from datetime import datetime, date


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

    def kind_of_content(self, chat_id):
        user = User.get(User.id == chat_id)
        if user.token is not None:
            func = getattr(self._state, 'kind_of')
            func(chat_id)
        else:
            bot.send_message(chat_id, 'Функция недоступна. Пройдите авторизацию в ЭлЖур (/auth)')
        user.act = 'kind_processing'
        user.save()

    def get_content(self, chat_id):
        func = getattr(self._state, 'get')
        content = func(chat_id)
        eljur_capab.send_content(chat_id, content)

    def send_content(self, chat_id, content):
        if content is not None:
            func = getattr(self._state, 'send')
            func(chat_id, content)
        user = User.get(User.id == chat_id)
        user.date = user.date[:6]
        user.act = None
        user.save()


def kind_processing(msg):
    user = User.get(User.id == msg.chat.id)
    if msg.text == 'На сегодня':
        user.date = datetime.now().strftime('%Y%m%d')
        user.save()
    elif msg.text == 'На завтра':
        user.date = str(int(datetime.now().strftime('%Y%m%d')) + 1)
        user.save()
    elif msg.text == 'На неделю' or msg.text == 'Всё актуальное':
        user.date = ''
        user.save()
    if msg.text == 'На конкретную дату':
        now = datetime.now()
        user.date = ''.join(str(date(now.year, now.month, 1)).split('-'))[:6]
        keyboard = create_calendar(now.year, now.month)
        bot.send_message(msg.chat.id, 'Выберите дату', reply_markup=ReplyKeyboardRemove())
        bot.send_message(msg.chat.id, 'Просто нажмите на нужный день в календаре!', reply_markup=keyboard)
        user.save()
    else:
        eljur_capab.get_content(msg.chat.id)


eljur_capab = EljurCapab()
