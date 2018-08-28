from config import *
from models import *


def account(data, id):
    if data['text'] == 'Да':
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(label='Да', color=VkKeyboardColor.POSITIVE, payload=['auth'])
        keyboard.add_button(label='Нет', color=VkKeyboardColor.NEGATIVE, payload=['auth'])
        vk.messages.send(user_id=id, message='Хотите ли Вы пройти авторизацию сейчас?', keyboard=keyboard.get_keyboard())
    else:
        vk.messages.send(user_id=id, message='Жаль, некоторые функции будут недоступны ☹\n'
                                             'Тогда Вы можете просто поговорить со мной или спросить о чём-нибудь!', keyboard=VkKeyboard.get_empty_keyboard())
