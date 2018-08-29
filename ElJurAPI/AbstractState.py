class AbstractState(object):
    def kind_of(self, id):
        raise NotImplementedError()

    def get(self, id):
        raise NotImplementedError()

    def send(self, id, content):
        raise NotImplementedError()
