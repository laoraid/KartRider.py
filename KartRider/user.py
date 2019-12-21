from datetime import datetime
from typing import Union, List
from .basedata import BaseData
from .metadata import _getname

dtstr = Union[datetime, str]


class User(BaseData):
    """사용자 정보 클래스
    >>> User(api, name) -> 닉네임과 api로 User 클래스를 만듭니다.
    >>> User(api, accessid) -> Accessid로 User 클래스를 만듭니다.
    >>> User(name, accessid) -> 유효성 검사를 하지 않습니다.
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
                raise ValueError('api 가 None 이지만 호출하려 했습니다.')
            self._name = self._api._getNicknamebyID(self._accessid)
        return self._name

    @property
    def accessid(self) -> str:
        if self._accessid is None:
            if self._api is None:
                raise ValueError('api 가 None 이지만 호출하려 했습니다.')
            self._accessid = self._api._getIDbyNickname(self._name)
        return self._accessid

    def getMatches(self, start_date: dtstr = "",
                   end_date: dtstr = "", offset: int = 0,
                   limit: int = 10, match_types: Union[List[str], str] = ""):
        """유저의 매치 데이터를 받아오는 메소드입니다.

        :param start_date: 조회 시작 날짜(UTC) datetime 혹은 str
        :param end_date: 조회 끝 날짜(UTC) datetime 혹은 str
        :param offset: 조회 오프셋
        :param limit: 조회 수 (최대 500건)
        :param match_types: 매치 타입 이름 목록 (list 또는 문자열)

        :raises ValueError: api가 None 일때 호출함

        :return: 유저 매치 데이터 클래스
        :rtype: _MatchResponse
        """
        if self._api is None:
            raise ValueError('api 가 None 이지만 호출하려 했습니다.')

        return self._api.getUserMatches(self.accessid, start_date, end_date,
                                        offset, limit, match_types)


class _Player(BaseData):
    accountNo: str
    characterName: str
    characterId: str
    flyingPetId: str
    kartId: str
    license: str
    matchTime: int
    partsEngine: str
    partsHandle: str
    partsKit: str
    partsWheel: str
    petId: str
    rankinggrade2: str

    def __init__(self, api, **kwargs):
        changeattrs = {'kart': 'kartId', 'character': 'characterId',
                       'pet': 'petId', 'flyingPet': 'flyingPetId'}
        ignoreattrs = ['matchRank', 'matchWin', 'matchRetired']
        intattrs = ['matchTime']
        super(_Player, self).__init__(
            api, intattrs, ignoreattrs, changeattrs, **kwargs)

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
        return _getname('kart', self.kartId)

    @property
    def pet(self) -> str:
        return _getname('pet', self.petId)

    @property
    def flyingPet(self) -> str:
        return _getname('flyingPet', self.flyingPetId)

    @property
    def character(self) -> str:
        return _getname('character', self.characterId)
