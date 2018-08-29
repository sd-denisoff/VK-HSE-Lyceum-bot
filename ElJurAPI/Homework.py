from config import *
from models import *
from actions import default_keyboard
from ElJurAPI.ElJurRequest import ElJurRequest
from ElJurAPI.AbstractState import AbstractState


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
        day_temp = '{0} ({1}.{2}.{3})\n'
        subj_temp = '{0} - {1}\n'
        for day in sorted(homework.keys()):
            date = homework[day]['name'][6:], homework[day]['name'][4:6], homework[day]['name'][:4]
            homework_list = day_temp.format(homework[day]['title'], date[0], date[1], date[2])
            subjects = homework[day].get('items', {})
            for subj in sorted(subjects.keys()):
                name = subjects[subj].get('name', '')
                tasks = ''
                for hw in subjects[subj]['homework'].keys():
                    tasks += subjects[subj]['homework'][hw]['value']
                    for f in subjects[subj].get('files', []):
                        if subjects[subj]['homework'][hw]['id'] == f['toid']:
                            tasks += ' <a href="' + f['link'] + '">' + f['filename'] + '</a> '
                homework_list += subj_temp.format(name, tasks)
            vk.messages.send(user_id=id, message=homework_list, keyboard=default_keyboard)
