from datetime import datetime
from typing import Union, List
from .basedata import _BaseData
from .metadata import _getname
from .match import MatchResponse

dtstr = Union[datetime, str]
mr = MatchResponse


class User(_BaseData):
    """사용자 정보 클래스입니다.


    >>> User(api, name)
    # 닉네임과 api로 User 클래스를 만듭니다.


    >>> User(api, accessid)
    # Accessid로 User 클래스를 만듭니다.


    >>> User(name, accessid)
    # 유효성 검사를 하지 않습니다.
    name과 accessid가 확실하게 일치할때만 사용하세요.
    아니라면 대신 Api.user(nickname) 혹은 Api.user(accessid)를 사용하세요.


    .. note:: api가 None 이고 name, accessid 중 하나만 입력했다면
        나머지 하나를 호출할때 ValueError가 던져집니다.
        api가 None 이 아니라면 나머지 하나를 호출할때
        api를 사용합니다.


    :raises ValueError: name 과 accessid 모두 입력하지 않음
    :param api: Api 클래스
    :type api: KartRider.apiwrapper.Api
    :param name: 카트라이더 닉네임 문자열
    :param accessid: 카트라이더 내부 유저 id 문자열(계정 id가 아님)
    """

    def __init__(self, api=None,
                 name: str = None, accessid: str = None):
        if name is None and accessid is None:
            raise ValueError('파라미터를 입력하지 않았습니다.')

        super(User, self).__init__(api)

        self._name = name
        self._accessid = accessid

    @property
    def name(self) -> str:
        """플레이어 닉네임

        :raises ValueError: api가 None인데 호출함
        """
        if self._name is None:
            if self._api is None:
                raise ValueError('api 가 None 이지만 호출하려 했습니다.')
            self._name = self._api._getNicknamebyID(self._accessid)
        return self._name

    @property
    def accessid(self) -> str:
        """플레이어 고유 ID

        :raises ValueError: api가 None인데 호출함
        """
        if self._accessid is None:
            if self._api is None:
                raise ValueError('api 가 None 이지만 호출하려 했습니다.')
            self._accessid = self._api._getIDbyNickname(self._name)
        return self._accessid

    def getMatches(self, start_date: dtstr = "",
                   end_date: dtstr = "", offset: int = 0,
                   limit: int = 10,
                   match_types: Union[List[str], str] = "") -> mr:
        """유저의 매치 데이터를 받아옵니다.

        :param start_date: 조회 시작 날짜(UTC)
        :param end_date: 조회 끝 날짜(UTC)
        :param offset: 조회 오프셋
        :param limit: 조회 수 (최대 500건)
        :param match_types: 매치 타입 이름이나 ID (리스트 또는 단일 문자열)

        :raises ValueError: api가 None인데 호출함
        :raises InvalidToken: 잘못된 Token이나 파라미터 입력
        :raises ForbiddenToken: 허용되지 않은 AccessToken 사용
        :raises NotFound: 존재하지 않는 리소스
        :raises TooManyRequest: AccessToken의 요청 허용량 초과
        :raises UnknownStatusCode: 알 수 없는 오류

        :rtype: MatchResponse
        """
        if self._api is None:
            raise ValueError('api 가 None 이지만 호출하려 했습니다.')

        return self._api.getUserMatches(self.accessid, start_date, end_date,
                                        offset, limit, match_types)


class Player(_BaseData):
    """매치 플레이어의 정보를 담고 있는 클래스입니다.

    사용법:
        >>> all = api.getAllMatches()
        >>> teamgame = all['스피드 팀전']
        >>> detail = teamgame[0]
        >>> player = detail.teams[0][1]
        >>> player.kart
        루루 X
        """
    accountNo: str  #: 유저 ID(str)
    characterName: str  #: 유저 닉네임(str)
    characterId: str  #: 캐릭터 ID(str)
    flyingPetId: str  #: 플라잉펫 ID(str)
    kartId: str  #: 카트 ID(str)
    license: str  #: 구 라이선스(str)
    matchTime: int  #: 매치 진행 시간(int)
    partsEngine: str  #:(str)
    partsHandle: str  #:(str)
    partsKit: str  #:(str)
    partsWheel: str  #:(str)
    petId: str  #: 펫 ID(str)
    rankinggrade2: str  #: 리뉴얼 라이선스(str)

    def __init__(self, api, **kwargs):
        changeattrs = {'kart': 'kartId', 'character': 'characterId',
                       'pet': 'petId', 'flyingPet': 'flyingPetId'}
        ignoreattrs = ['matchRank', 'matchWin', 'matchRetired']
        intattrs = ['matchTime']
        super(Player, self).__init__(
            api, intattrs, ignoreattrs, changeattrs, **kwargs)

        rank = kwargs['matchRank']

        if rank == '99' or rank == '':
            self.matchRank = -1  #: 순위, 리타이어는 -1
            self.matchRetired = True  #: 리타이어 여부
        elif rank == '1':
            self.matchRank = 1
            self.matchRetired = False
        else:
            self.matchRank = int(rank)
            self.matchRetired = False

        if kwargs['matchWin'] == '0':
            self.matchWin = False  #: 매치 승리 여부
        else:
            self.matchWin = True

    @property
    def kart(self) -> str:
        """카트 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('kart', self.kartId)

    @property
    def pet(self) -> str:
        """펫 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('pet', self.petId)

    @property
    def flyingPet(self) -> str:
        """플라잉펫 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('flyingPet', self.flyingPetId)

    @property
    def character(self) -> str:
        """캐릭터 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('character', self.characterId)
