from config import *
from models import *


default_keyboard = VkKeyboard(one_time=False)
default_keyboard.add_button(label='Все возможности', color=VkKeyboardColor.DEFAULT, payload={'action': 'capabilities'})
default_keyboard = default_keyboard.get_keyboard()


def show_capabilities(id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label='Узнать расписание', color=VkKeyboardColor.DEFAULT, payload={'action': 'schedule'})
    keyboard.add_button(label='Узнать ДЗ', color=VkKeyboardColor.DEFAULT, payload={'action': 'homework'})
    keyboard.add_line()
    keyboard.add_button(label='Пройти авторизацию', color=VkKeyboardColor.DEFAULT, payload={'action': 'auth'})
    keyboard.add_line()
    keyboard.add_button(label='Стереть данные о себе', color=VkKeyboardColor.DEFAULT, payload={'action': 'forget'})
    keyboard.add_line()
    keyboard.add_button(label='Оставить отзыв', color=VkKeyboardColor.DEFAULT, payload={'action': 'review'})
    vk.messages.send(user_id=id, message='Возможности 👇', keyboard=keyboard.get_keyboard())


def is_account(data, id):
    if data['text'] == 'Да':
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(label='Да', color=VkKeyboardColor.POSITIVE, payload={'action': 'auth'})
        keyboard.add_button(label='Нет', color=VkKeyboardColor.NEGATIVE, payload={'action': 'auth'})
        vk.messages.send(user_id=id, message='Хотите ли Вы пройти авторизацию сейчас?', keyboard=keyboard.get_keyboard())
    else:
        vk.messages.send(user_id=id, message='Жаль, некоторые функции будут недоступны ☹\n'
                                             'Тогда Вы можете просто поговорить со мной или спросить о чём-нибудь!', keyboard=default_keyboard)


def auth(data, id):
    user = User.get(User.id == id)
    if data['text'] == 'Нет':
        vk.messages.send(user_id=id, message='Хорошо, Вы можете сделать это позже 🙃', keyboard=default_keyboard)
    elif user.token is not None:
        vk.messages.send(user_id=id, message='Вы уже авторизованы! 🙃', keyboard=default_keyboard)
    else:
        vk.messages.send(user_id=id, message='Страница авторизации в ЭлЖур 👇 \n' + APP_URL + '/auth/' + id,
                         keyboard=default_keyboard)


def forget_user(id):
    user = User.get(User.id == id)
    user.delete_instance()
    vk.messages.send(user_id=id, message='Данные удалены', keyboard=default_keyboard)


def leave_review(id):
    vk.messages.send(user_id=id, message='Форма отправки отзыва 👇 \n' + APP_URL + '/review', keyboard=default_keyboard)
