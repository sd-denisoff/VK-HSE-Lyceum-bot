from config import *
from models import *
from telebot.types import \
     ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from ElJurAPI.ElJurRequest import ElJurRequest


def default(msg):
    bot.send_message(msg.chat.id, 'Чем могу быть полезен, ' + msg.chat.first_name + '?\nСписок команд - /commands')


def is_account(msg):
    user = User.get(User.id == msg.chat.id)
    if msg.text == 'Да':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton('Да'), KeyboardButton('Нет'))
        bot.send_message(msg.chat.id, 'Хотите ли Вы пройти авторизацию?', reply_markup=keyboard)
        user.act = 'auth'
    else:
        bot.send_message(msg.chat.id, 'Жаль, Вам будут недоступны некоторые функции :(\n'
                                      'Можете тогда просто поговорить со мной или спросить о чём-нибудь!', reply_markup=ReplyKeyboardRemove())
        user.act = None
    user.save()


def auth(msg):
    user = User.get(User.id == msg.chat.id)
    keyboard = ReplyKeyboardRemove()
    if msg.text == 'Да' or msg.text == '/auth':
        # по-хорошему здесь бы ccылку на страницу авторизации кидать
        bot.send_message(msg.chat.id, 'Введите логин аккаунта в ЭлЖур', reply_markup=keyboard)
        user.act = 'input_login'
    else:
        bot.send_message(msg.chat.id, 'Хорошо, но Вы можете сделать это позже (/auth)', reply_markup=ReplyKeyboardRemove())
        user.act = None
    user.save()


def input_login(msg):
    user = User.get(User.id == msg.chat.id)
    user.login = msg.text
    user.act = 'input_password'
    user.save()
    bot.send_message(msg.chat.id, 'Введите пароль аккаунта в ЭлЖур')


def input_password(msg):
    user = User.get(User.id == msg.chat.id)
    user.password = msg.text
    r = ElJurRequest('/auth?login=' + user.login + '&password=' + user.password)
    if r.is_valid:
        user.token = r.query['token']
        bot.send_message(msg.chat.id, 'Авторизация прошла успешно!')
    else:
        bot.send_message(msg.chat.id, r.query)
        user.login = None
        user.password = None
    user.act = None
    user.save()


def save_review(msg):
    user = User.get(User.id == msg.chat.id)
    user.act = None
    user.save()
    Review.create(author=msg.from_user.first_name + ' ' + msg.from_user.last_name, text=msg.text)
    bot.send_message(msg.chat.id, 'Отзыв записан, спасибо!')
