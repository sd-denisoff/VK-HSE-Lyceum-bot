class AbstractState(object):
    def kind_of(self, chat_id):
        raise NotImplementedError()

    def get(self, chat_id):
        raise NotImplementedError()

    def send(self, chat_id, content):
        raise NotImplementedError()
