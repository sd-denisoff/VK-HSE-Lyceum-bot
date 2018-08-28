from config import *
from datetime import datetime
import time


@app.route('/', methods=['GET'])
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
        vk.messages.send(user_id=str(user_id), message=open('greeting.txt', 'r').read())
    return 'ok'


if __name__ == '__main__':
    while True:
        try:
            app.run(host='0.0.0.0', port=8080)
        except Exception as e:
            f = open('errors.txt', 'a', encoding='utf-8')
            f.write(str(e) + ' ### ' + str(datetime.now()) + '\n')
            f.close()
            time.sleep(5)
