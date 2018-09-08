from config import *
from models import *
from telebot.types import \
     ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from textParsing.brain import brain
from ElJurAPI.ElJurCapab import *
from MainActFunctions import default, is_account, auth, input_login, input_password, save_review
from InlineCalendar import create_calendar
from datetime import datetime, date
import time

b = brain()
b.get('null', 'init')


# WEBHOOK ROUTES

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Hello, world!'


@app.route('/' + token + '/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# MESSAGE HANDLERS

@bot.message_handler(commands=['start'])
def start(msg):
    try:
        User.get(User.id == msg.chat.id)
    except User.DoesNotExist:
        User.create(id=msg.chat.id, act='is_account')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton('Да'), KeyboardButton('Нет'))
        bot.send_message(msg.chat.id, 'Приветствую, ' + msg.chat.first_name + '! \n' + open('greeting.txt', 'r').read()).wait()
        bot.send_message(msg.chat.id, 'Есть ли у Вас аккаунт в системе ЭлЖур?', reply_markup=keyboard).wait()
    else:
        default(msg)


@bot.message_handler(commands=['auth'])
def authorization(msg):
    auth(msg)


@bot.message_handler(commands=['schedule'])
def schedule(msg):
    eljur_capab.change_state('schedule')
    eljur_capab.kind_of_content(msg.chat.id)


@bot.message_handler(commands=['homework'])
def homework(msg):
    eljur_capab.change_state('homework')
    eljur_capab.kind_of_content(msg.chat.id)


@bot.message_handler(commands=['commands'])
def commands(msg):
    bot.send_message(msg.chat.id, '/auth - пройти авторизацию\n'
                                  '/schedule - расписание\n'
                                  '/homework - домашнее задание\n'
                                  '/commands - список команд (рекурсия :D)\n'
                                  '/cancel - отменить текущее действие\n'
                                  '/forget_me - забыть данные\n'
                                  '/review - написать отзыв\n'
                                  '/about - о проекте\n'
                                  '/help - помощь')


@bot.message_handler(commands=['cancel'])
def cancel(msg):
    user = User.get(User.id == msg.chat.id)
    user.act = None
    user.save()
    keyboard = ReplyKeyboardRemove()
    bot.send_message(msg.chat.id, 'Действие отменено', reply_markup=keyboard)


@bot.message_handler(commands=['forget_me'])
def forget_user(msg):
    user = User.get(User.id == msg.chat.id)
    user.token = None
    user.login = None
    user.password = None
    user.date = ''
    user.act = None
    user.save()
    keyboard = ReplyKeyboardRemove()
    bot.send_message(msg.chat.id, 'Данные удалены', reply_markup=keyboard)


@bot.message_handler(commands=['review'])
def review(msg):
    user = User.get(User.id == msg.chat.id)
    user.act = 'save_review'
    user.save()
    bot.send_message(msg.chat.id, 'Напишите Ваш отзыв')


@bot.message_handler(commands=['about'])
def about(msg):
    bot.send_message(msg.chat.id, 'Официальный бот Лицея НИУ ВШЭ \n'
                                  'Проект разработан лицеистами с направлений МатИнфо, гум. науки, дизайн и юриспруденция')


@bot.message_handler(commands=['help'])
def help(msg):
    bot.send_message(msg.chat.id, 'Для вопросов, предложений и сообщений об ошибках - sd.denisoff@gmail.com')


@bot.message_handler(commands=['statistics'])
def statistics(msg):
    reg = User.select().count()
    auth = User.select().where(User.token != None).count()
    bot.send_message(msg.chat.id, 'Количество зарегистрированных пользователей - ' + str(reg) + '\n'
                                  'Количество авторизованных пользоваталей - ' + str(auth) + '\n')

@bot.message_handler(commands=['get_reviews'])
def get_reviews(msg):
    reviews = ''
    number = 1
    for r in Review.select():
        reviews += str(number) + '. ' + r.author + ': ' + r.text + '\n\n'
        number += 1
    bot.send_message(msg.chat.id, reviews)


# CALLBACK HANDLERS

@bot.callback_query_handler(func=lambda call: call.data[:4] == 'day-')
def get_day(call):
    user = User.get(User.id == call.from_user.id)
    day = call.data[4:]
    if len(day) == 1:
        day = '0' + day
    user.date += day
    user.save()
    date_for_ans = user.date[6:] + '-' + user.date[4:6] + '-' + user.date[:4]
    bot.answer_callback_query(call.id, text=date_for_ans)
    eljur_capab.get_content(call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    user = User.get(User.id == call.from_user.id)
    year = int(user.date[:4])
    month = int(user.date[4:])
    month += 1
    if month > 12:
        month = 1
        year += 1
    user.date = ''.join(str(date(year, month, 1)).split('-'))[:6]
    user.save()
    keyboard = create_calendar(year, month)
    bot.edit_message_text('Просто нажмите на нужный день в календаре!', call.from_user.id, call.message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    user = User.get(User.id == call.from_user.id)
    year = int(user.date[:4])
    month = int(user.date[4:6])
    month -= 1
    if month < 1:
        month = 12
        year -= 1
    user.date = ''.join(str(date(year, month, 1)).split('-'))[:6]
    user.save()
    keyboard = create_calendar(year, month)
    bot.edit_message_text('Просто нажмите на нужный день в календаре!', call.from_user.id, call.message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text='Кнопка не кликабельна')


@bot.message_handler(content_types=['text'])
def text_handler(msg):
    try:
        user = User.get(User.id == msg.chat.id)
    except User.DoesNotExist:
        start(msg)
    else:
        if user.act is not None:
            eval(user.act + '(msg)')
        else:
            responses = b.get(user.id, msg.text)
            print(responses)
            for r in responses:
                if r['answered']:
                    keyboard = ReplyKeyboardRemove()
                    if r.get('quickAnswers') is not None:
                        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                        for button in r['quickAnswers']:
                            keyboard.add(KeyboardButton(button))
                    bot.send_message(msg.chat.id, r.get('generatedText'), reply_markup=keyboard)
                else:
                    if r['class'] == 'commands':
                        commands(msg)
                    elif user.token is not None:
                        eljur_capab.change_state(r['class'])
                        user.date = r['date']
                        user.save()
                        eljur_capab.get_content(msg.chat.id)


if __name__ == '__main__':
    while True:
        try:
            # bot.polling(none_stop=True)
            app.run(host=WEBHOOK_LISTEN,
                    port=WEBHOOK_PORT,
                    ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV))
        except Exception as e:
            f = open('errors.txt', 'a', encoding='utf-8')
            f.write(str(e) + ' ### ' + str(datetime.now()) + '\n')
            f.close()
            time.sleep(5)
