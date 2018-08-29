# from config import *
# from models import *
# from ElJurAPI.ElJurRequest import ElJurRequest
# from ElJurAPI.AbstractState import AbstractState
# from telebot.types import \
#      ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
#
#
# class HomeworkState(AbstractState):
#     def kind_of(self, chat_id):
#         keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#         keyboard.row(KeyboardButton('На сегодня'), KeyboardButton('На завтра'))
#         keyboard.row(KeyboardButton('На конкретную дату'), KeyboardButton('Всё актуальное'))
#         bot.send_message(chat_id, 'Какое домашнее задание Вам нужно?', reply_markup=keyboard)
#
#     def get(self, chat_id):
#         user = User.get(User.id == chat_id)
#         r = ElJurRequest('/gethomework?auth_token=' + user.token + '&days=' + user.date)
#         if not r.is_valid:
#             bot.send_message(chat_id, r.query)
#             return None
#         if not r.query:
#             keyboard = ReplyKeyboardRemove()
#             bot.send_message(chat_id, 'Хм, ничего не задано! Ну, или же Вы указали некорректную дату', reply_markup=keyboard)
#             return None
#         homework = r.query.get('students', {})
#         key = list(homework.keys())[0]
#         homework = homework[key].get('days', {})
#         return homework
#
#     def send(self, chat_id, homework):
#         day_temp = '{0} ({1}.{2}.{3})\n'
#         subj_temp = '{0} - {1}\n'
#         for day in sorted(homework.keys()):
#             date = homework[day]['name'][6:], homework[day]['name'][4:6], homework[day]['name'][:4]
#             homework_list = day_temp.format(homework[day]['title'], date[0], date[1], date[2])
#             subjects = homework[day].get('items', {})
#             for subj in sorted(subjects.keys()):
#                 name = subjects[subj].get('name', '')
#                 tasks = ''
#                 for hw in subjects[subj]['homework'].keys():
#                     tasks += subjects[subj]['homework'][hw]['value']
#                     for f in subjects[subj].get('files', []):
#                         if subjects[subj]['homework'][hw]['id'] == f['toid']:
#                             tasks += ' <a href="' + f['link'] + '">' + f['filename'] + '</a> '
#                 homework_list += subj_temp.format(name, tasks)
#             bot.send_message(chat_id, homework_list, parse_mode='HTML', reply_markup=ReplyKeyboardRemove()).wait()
