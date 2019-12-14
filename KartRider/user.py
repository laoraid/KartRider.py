class User(object):
    def __init__(self, name=None, accessid=None):
        if name or accessid is None:
            raise ValueError

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

    @property
    def matches(self):
        pass  # TODO : get matches class
