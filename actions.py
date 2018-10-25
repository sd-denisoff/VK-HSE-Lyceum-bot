from config import *
from models import *


default_keyboard = VkKeyboard(one_time=False)
default_keyboard.add_button(label='Все возможности', color=VkKeyboardColor.DEFAULT, payload={'action': 'capabilities'})
default_keyboard = default_keyboard.get_keyboard()


def show_capabilities(id):
    user = User.get(User.id == id)

    keyboard = VkKeyboard(one_time=True)

    if user.token is None:
        keyboard.add_button(label='Пройти авторизацию', color=VkKeyboardColor.DEFAULT, payload={'action': 'auth'})
    else:
        keyboard.add_button(label='Расписание 📅', color=VkKeyboardColor.PRIMARY, payload={'action': 'schedule'})
        keyboard.add_button(label='ДЗ 📚', color=VkKeyboardColor.PRIMARY, payload={'action': 'homework'})
        keyboard.add_line()
        keyboard.add_button(label='Оценки 🏆', color=VkKeyboardColor.PRIMARY, payload={'action': 'marks'})
        keyboard.add_line()
        keyboard.add_button(label='Выйти из аккаунта ЭлЖур', color=VkKeyboardColor.DEFAULT, payload={'action': 'logout'})

    keyboard.add_line()
    keyboard.add_button(label='Оставить отзыв', color=VkKeyboardColor.DEFAULT, payload={'action': 'review'})

    if user.role == 'admin':
        keyboard.add_line()
        keyboard.add_button(label='Статистика', color=VkKeyboardColor.POSITIVE, payload={'action': 'get_statistics'})
        keyboard.add_button(label='Отзывы', color=VkKeyboardColor.POSITIVE, payload={'action': 'read_reviews', 'send_link': True})
        keyboard.add_button(label='Рассылка', color=VkKeyboardColor.POSITIVE, payload={'action': 'make_newsletter'})
        keyboard.add_line()
        keyboard.add_button(label='Вопросы-ответы', color=VkKeyboardColor.POSITIVE, payload={'action': 'get_qna'})

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
    if data['text'] == 'Нет':
        vk.messages.send(user_id=id, message='Хорошо, Вы можете сделать это позже 🙃', keyboard=default_keyboard)
    else:
        vk.messages.send(user_id=id, message='Страница авторизации в ЭлЖур 👇 \n' + APP_URL + '/auth/' + id,
                         keyboard=default_keyboard)


def logout(id):
    user = User.update(token=None).where(User.id == id)
    user.execute()
    vk.messages.send(user_id=id, message='Готово! Для последующего получения расписания/оценок/ДЗ потребуется повторная авторизация', keyboard=default_keyboard)


def review(id):
    vk.messages.send(user_id=id, message='Форма отправки отзыва 👇 \n' + APP_URL + '/review', keyboard=default_keyboard)


def get_statistics(id):
    reg = User.select().count()
    auth = User.select().where(User.token != None).count()
    vk.messages.send(user_id=id, message='Зарегистрировано - ' + str(reg) + '\n' + 'Авторизовано - ' + str(auth), keyboard=default_keyboard)


def read_reviews(id):
    review = Review.select().where(Review.was_read == False).first()
    if review is None:
        vk.messages.send(user_id=id, message='Новых отзывов нет 🙁', keyboard=default_keyboard)
        return
    else:
        review.was_read = True
        review.save()
    review_temp = '{text}\nДата: {date}'
    keyboard = VkKeyboard(one_time=True)
    all = Review.select().count()
    if review.id != all:
        keyboard.add_button(label='Следующий (' + str(review.id) + '/' + str(all) + ')', color=VkKeyboardColor.PRIMARY, payload={'action': 'read_reviews'})
        keyboard.add_button(label='Возможности', color=VkKeyboardColor.DEFAULT, payload={'action': 'capabilities'})
    else:
        keyboard.add_button(label='Всё прочитано!', color=VkKeyboardColor.PRIMARY, payload={'action': 'capabilities'})
    vk.messages.send(user_id=id, message=review_temp.format(text=review.text, date=review.date), keyboard=keyboard.get_keyboard())


def make_newsletter(id):
    vk.messages.send(user_id=id, message='Страница создания рассылки 👇 \n' + APP_URL + '/mailing', keyboard=default_keyboard)


def get_qna(id):
    vk.messages.send(user_id=id, message='Страница вопросов-ответов 👇 \n' + APP_URL + '/qna', keyboard=default_keyboard)
