from .basedata import BaseData


class User(BaseData):
    """사용자 정보 클래스
    User(api, name) -> 닉네임과 api로 User 클래스를 만듭니다.
    User(api, accessid) -> Accessid로 User 클래스를 만듭니다.
    User(name, accessid) -> 유효성 검사를 하지 않습니다.
    name과 accessid가 확실하게 일치할때만 사용하세요.
    아니라면 대신 Api.user(nickname) 혹은 Api.user(accessid)를 사용하세요.

    api가 None 이고 name, accessid 중 하나만 입력했다면
    나머지 하나를 호출할때 ValueError가 던져집니다.
    api가 None 이 아니라면 나머지 하나를 호출할때
    api를 사용합니다.

    :raises ValueError: name 과 accessid 모두 입력하지 않음
    :param api: Api 클래스
    :param name: 카트라이더 닉네임 문자열
    :param accessid: 카트라이더 내부 유저 id 문자열(계정 id가 아님)
    """

    def __init__(self, api=None,
                 name: str = None, accessid: str = None):
        if name is None and accessid is None:
            raise ValueError

        super(User, self).__init__(api)

        self._name = name
        self._accessid = accessid

    @property
    def name(self) -> str:
        if self._name is None:
            if self._api is None:
                raise ValueError
            self._name = self._api._getNicknamebyID(self._accessid)
        return self._name

    @property
    def accessid(self) -> str:
        if self._api is None:
            raise ValueError
        self._accessid = self._api._getIDbyNickname(self._name)
        return self._accessid


class _Player(BaseData):
    def __init__(self, api, **kwargs):
        changeattrs = {'kart': 'kartid',
                       'pet': 'petid', 'flyingPet': 'flyingPetid'}
        ignoreattrs = ['matchRank', 'matchWin', 'matchRetired']
        super(_Player, self).__init__(
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
