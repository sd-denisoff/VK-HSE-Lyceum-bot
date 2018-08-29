from config import *
from models import *
from actions import *
from flask import render_template
from web.forms import AuthForm, ReviewForm
from ElJurAPI.ElJurRequest import ElJurRequest
from ElJurAPI.ElJurCapab import *
from calendar_keyboard import create_calendar
from datetime import date


@app.route('/auth/<string:id>', methods=['GET', 'POST'])
def eljur_auth(id):
    form = AuthForm()
    if form.validate_on_submit():
        r = ElJurRequest('/auth?login=' + form.login.data + '&password=' + form.password.data)
        if r.is_valid:
            user = User.get(User.id == id)
            user.token = r.query['token']
            user.save()
            return render_template('auth_success.html')
        else:
            return render_template('auth_error.html', error=r.query)
    return render_template('auth.html', form=form, action='/auth/' + id)


@app.route('/review', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        Review.create(text=form.review.data, date=date.today().strftime('%d-%m-%Y'))
        return render_template('review_success.html')
    return render_template('review.html', form=form)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Hello from server!'


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        user_id = data['object']['from_id']
        user_recognition(data['object'], str(user_id))
    return 'ok'


def user_recognition(data, id):
    try:
        User.get(User.id == id)
    except User.DoesNotExist:
        User.create(id=id)
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(label='Да', color=VkKeyboardColor.POSITIVE, payload={'action': 'is_account'})
        keyboard.add_button(label='Нет', color=VkKeyboardColor.NEGATIVE, payload={'action': 'is_account'})
        vk.messages.send(user_id=id, message=open('greeting.txt', 'r').read())
        vk.messages.send(user_id=id, message='Есть ли у Вас аккаунт в системе ЭлЖур?', keyboard=keyboard.get_keyboard())
    else:
        text_handler(data, id)


def action_recognition(data, id, payload):
    if payload['action'] == 'capabilities':
        show_capabilities(id)
    elif payload['action'] == 'is_account':
        is_account(data, id)
    elif payload['action'] == 'auth':
        auth(data, id)
    elif payload['action'] == 'schedule':
        eljur_capab.change_state('schedule')
        eljur_capab.kind_of_content(id)
    elif payload['action'] == 'homework':
        eljur_capab.change_state('homework')
        eljur_capab.kind_of_content(id)
    elif payload['action'] == 'kind':
        kind_processing(data, id)
    elif payload['action'] == 'title':
        vk.messages.send(user_id=id, message='Необходимо выбрать дату!', keyboard=create_calendar())
    elif payload['action'] == 'calendar':
        user = User.get(User.id == id)
        user.date = payload['date']
        user.save()
        eljur_capab.get_content(id)
    elif payload['action'] == 'forget':
        forget_user(id)
    elif payload['action'] == 'review':
        leave_review(id)
    elif payload['action'] == 'about':
        about(id)


def text_handler(data, id):
    if 'payload' in data.keys():
        payload = json.loads(data['payload'])
        action_recognition(data, id, payload)
    else:
        vk.messages.send(user_id=id, message='Извините, не совсем Вас понимаю 😔', keyboard=default_keyboard)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
