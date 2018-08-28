from config import *
from actions import *


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
        keyboard.add_button(label='Да', color=VkKeyboardColor.POSITIVE, payload={'action': 'account'})
        keyboard.add_button(label='Нет', color=VkKeyboardColor.NEGATIVE, payload={'action': 'account'})
        vk.messages.send(user_id=id, message=open('greeting.txt', 'r').read())
        vk.messages.send(user_id=id, message='Есть ли у Вас аккаунт в системе ЭлЖур?', keyboard=keyboard.get_keyboard())
    else:
        text_handler(data, id)


def command_recognition(data, id, payload):
    if payload == 'account':
        account(data, id)
    elif payload == 'auth':
        pass


def text_handler(data, id):
    if 'payload' in data.keys():
        payload = json.loads(data['payload'])
        command_recognition(data, id, payload['action'])
    else:
        vk.messages.send(user_id=id, message='Извините, не совсем Вас понимаю 😔')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
