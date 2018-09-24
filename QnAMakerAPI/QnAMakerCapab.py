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


def update_base(question, answer):
    payload = {
        'add': {
            'qnaPairs': [
                {
                    'answer': answer,
                    'question': question
                }
            ]
        }
    }
    QnAMakerRequest('update', payload=payload)
    publish_base()


def publish_base():
    QnAMakerRequest('publish')
