from .basedata import BaseData


class User(BaseData):
    def __init__(self, api, name=None, accessid=None):
        if name is None and accessid is None:
            raise ValueError

        super(User, self).__init__(api)

        self._name = name
        self._accessid = accessid

    @property
    def name(self):
        if self._name is None:
            pass  # TODO : use api get name
        return self._name

    @property
    def accessid(self):
        if self._accessid is None:
            pass  # TODO : use api get accessid
        return self._accessid


class MatchUser(User):
    def __init__(self, api, name, accessid, **kwargs):
        super(MatchUser, self).__init__(
            api, name, accessid)  # TODO : kwargs 처리
