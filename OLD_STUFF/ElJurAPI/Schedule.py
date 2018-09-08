from config import *
from models import *
from ElJurAPI.ElJurRequest import ElJurRequest
from ElJurAPI.AbstractState import AbstractState
from telebot.types import \
     ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class ScheduleState(AbstractState):
    def kind_of(self, chat_id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.row(KeyboardButton('На сегодня'), KeyboardButton('На завтра'))
        keyboard.row(KeyboardButton('На конкретную дату'), KeyboardButton('На неделю'))
        bot.send_message(chat_id, 'Какое расписание Вам нужно?', reply_markup=keyboard)

    def get(self, chat_id):
        user = User.get(User.id == chat_id)
        r = ElJurRequest('/getschedule?auth_token=' + user.token + '&days=' + user.date)
        if not r.is_valid:
            bot.send_message(chat_id, r.query)
            return None
        if not r.query:
            keyboard = ReplyKeyboardRemove()
            bot.send_message(chat_id, 'Занятий в этот день нет! Ну, или же Вы указали некорректную дату', reply_markup=keyboard)
            return None
        schedule = r.query.get('students', {})
        key = list(schedule.keys())[0]
        schedule = schedule[key].get('days', {})
        return schedule

    def send(self, chat_id, schedule):
        day_temp = '{0} ({1}.{2}.{3})\n'
        subj_temp = '{0}. {1} ({2})\n'
        for day in sorted(schedule.keys()):
            date = schedule[day]['name'][6:], schedule[day]['name'][4:6], schedule[day]['name'][:4]
            schedule_list = day_temp.format(schedule[day]['title'], date[0], date[1], date[2])
            subjects = schedule[day].get('items', {})
            for subj in sorted(subjects.keys()):
                schedule_list += subj_temp.format(subjects[subj].get('num', ''), subjects[subj].get('name', ''), subjects[subj].get('room', ''))
            bot.send_message(chat_id, schedule_list, reply_markup=ReplyKeyboardRemove()).wait()
