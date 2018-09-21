from models import *
from QnAMakerAPI.QnAMakerRequest import QnAMakerRequest


def generate_answer(text):
    payload = {'question': text}
    r = QnAMakerRequest('/generateAnswer', payload)
    if r.isValid:
        if r.query['score'] > 80:
            return True, r.query['answer']
        else:
            return False, r.query['answer']
    else:
        return False, r.query['message']


# def update_base(msg, bot):
#     user = User.get(User.id == msg.chat.id)
#     payload = {
#         'add': {
#             'qnaPairs': [
#                 {
#                     'answer': msg.text,
#                     'question': user.lastQ
#                 }
#             ]
#         }
#     }
#     QnAMakerRequest('update', payload=payload)
#     publish_base()
#     bot.send_message(msg.chat.id, "Ответ записан!")
#     user.act = None
#     user.save()


# def publish_base():
#     QnAMakerRequest('publish')
