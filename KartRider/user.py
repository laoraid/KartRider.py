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


class Player(BaseData):
    def __init__(self, api, name, accessid, **kwargs):
        changeattrs = {'kart': 'kartid',
                       'pet': 'petid', 'flyingPet': 'flyingPetid'}
        ignoreattrs = ['matchRank', 'matchWin', 'matchRetired']
        super(Player, self).__init__(
            api, None, ignoreattrs, changeattrs, **kwargs)

        rank = kwargs['matchRank']

        if rank == '99' or rank == '':
            self.matchRank = -1
            self.matchRetired = True
        elif rank == '1':
            self.matchRank = 1
            self.matchRetired = False
        else:
            self.matchRank = int(rank)
            self.matchRetired = False

        if kwargs['matchWin'] == '0':
            self.matchWin = False
        else:
            self.matchWin = True

    @property
    def kart(self) -> str:
        pass  # TODO : get metadata name

    @property
    def pet(self) -> str:
        pass

    @property
    def flyingPet(self) -> str:
        pass
