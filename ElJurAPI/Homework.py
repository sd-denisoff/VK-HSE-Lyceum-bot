from config import *
from models import *
from actions import default_keyboard
from ElJurAPI.ElJurRequest import ElJurRequest
from ElJurAPI.AbstractState import AbstractState
import requests
from pytils import translit
import os


class HomeworkState(AbstractState):
    def kind_of(self, id):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(label='Сегодня', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        keyboard.add_button(label='Завтра', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        keyboard.add_line()
        keyboard.add_button(label='Дата', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        keyboard.add_button(label='Всё актуальное', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        vk.messages.send(user_id=id, message='Какое домашнее задание Вам нужно?', keyboard=keyboard.get_keyboard())

    def get(self, id):
        user = User.get(User.id == id)
        r = ElJurRequest('/gethomework?auth_token=' + user.token + '&days=' + user.date)
        if not r.is_valid:
            vk.messages.send(user_id=id, message=r.query, keyboard=default_keyboard)
            return None
        if not r.query:
            vk.messages.send(user_id=id, message='Хм, ничего не задано! Ну, или же Вы указали некорректную дату',
                             keyboard=default_keyboard)
            return None
        homework = r.query.get('students', {})
        key = list(homework.keys())[0]
        homework = homework[key].get('days', {})
        return homework

    def send(self, id, homework):
        day_temp = '{title} ({date})\n\n'
        subj_temp = '{num}. {name}\n{tasks}\n\n'
        for day in sorted(homework.keys(), key=lambda d: len(d)):
            date = '.'.join([day[6:], day[4:6], day[:4]])
            response = day_temp.format(title=homework[day]['title'].upper(), date=date)
            subjects = homework[day].get('items', {})
            list_of_attachs = list()
            num = 1
            for subj in sorted(subjects.keys(), key=lambda s: len(s)):
                name = subjects[subj].get('name', '')
                tasks = ''
                hw = subjects[subj]
                for t in hw['homework'].keys():
                    tasks += hw['homework'][t]['value'] + '\n'
                    for f in hw.get('files', []):
                        r = requests.get(url=f['link'], headers={'User-Agent': 'Mozilla/5.0'})
                        filename = translit.translify(f['filename'])
                        with open('ElJurAPI/DocsBuff/' + filename, 'wb') as doc:
                            doc.write(r.content)
                        url = vk.docs.getMessagesUploadServer(peer_id=id)['upload_url']
                        r = requests.post(url=url, files={'file': open('ElJurAPI/DocsBuff/' + filename, 'rb')}).json()
                        attach = vk.docs.save(file=r['file'])[0]
                        list_of_attachs.append('doc' + str(attach['owner_id']) + '_' + str(attach['id']))
                        os.remove('ElJurAPI/DocsBuff/' + filename)
                response += subj_temp.format(num=num, name=name, tasks=tasks)
                num += 1
            vk.messages.send(user_id=id, message=response, attachment=list_of_attachs, keyboard=default_keyboard)
