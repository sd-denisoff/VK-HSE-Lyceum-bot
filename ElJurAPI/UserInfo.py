from models import *
from ElJurAPI.ElJurRequest import ElJurRequest
from ElJurAPI.AbstractState import AbstractState


class UserInfoState(AbstractState):
    def get(self, id):
        user = User.get(User.id == id)
        r = ElJurRequest('/getrules?auth_token=' + user.token)
        if not r.is_valid or not r.query:
            return None
        return r.query

    def send(self, id, user_info):
        user = User.get(User.id == id)
        user.eljur_id = user_info.get('name')
        group_info = user_info.get('relations', {}).get('groups', {})
        if isinstance(group_info, dict):
            user.group = list(group_info.keys())[0]
        user.save()
