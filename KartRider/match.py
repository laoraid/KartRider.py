from datetime import datetime
from typing import List

from . import utils
from .basedata import MergeAbleDict, _BaseData
from .metadata import (_getname, _safe_check, getcharactername,
                       getgametypename, gettrackname)


class MatchResponse(_BaseData, MergeAbleDict[List['MatchInfo']]):
    """매치 응답 정보를 담고 있는 클래스입니다.

    매치 타입 ID 또는 이름(메타데이터 경로가 지정됐을때)을 키로,
    :class:`.MatchInfo` 의 리스트를 값으로 가지는 dict와 같습니다.

    사용법:
        >>> mr = api.user('닉네임').getMatches()
        >>> mr['아이템 팀전'][0].playerCount # 검색된 매치 중 아이템 팀전의 0번째 매치 정보의 플레이어 카운트
        6
    """

    def __init__(self, api, nickname: str, matcheslist):
        _BaseData.__init__(self, api)
        MergeAbleDict.__init__(self)

        self.nickname = nickname  #: 매치 정보를 호출한 유저의 닉네임

        meta = _safe_check('gameType.json')

        for match in matcheslist:
            matchinforaw = match['matches']
            matchtypeid = match['matchType']
            matchinfo = [None] * len(matchinforaw)

            for i, m in enumerate(matchinforaw):
                matchinfo[i] = MatchInfo(api, **m)

            if meta:
                matchtype = getgametypename(matchtypeid)
            else:
                matchtype = matchtypeid
            self[matchtype] = matchinfo


class MatchInfo(_BaseData):
    """매치 정보를 담고 있는 클래스입니다.

    사용법:
        >>> mr = api.user('닉네임').getMatches()
        >>> mi = mr['아이템 팀전'][0] # 검색된 매치 중 아이템 팀전의 0번째 매치 정보
        >>> mi.character
        황금망토 배찌
    """
    accountno: str  #: 계정 고유 식별자(str)
    channelname: str  #: 채널 이름(str)
    characterid: str  #: 캐릭터 ID(str)
    matchresult: str  # :(str)
    matchtypeid: str  #: 매치 종류 ID(str)
    playercount: int  #: 참여 유저 수(int)
    teamid: str  #: 팀 ID(str)
    trackid: str  #: 트랙 ID(str)

    def __init__(self, api, **kwargs):
        intattrs = ['playercount']
        ignoreattrs = ['starttime', 'endtime', 'player', 'matchid']
        changeattrs = {'matchtype': 'matchtypeid',
                       'character': 'characterid'}

        super(MatchInfo, self).__init__(api, intattrs,
                                        ignoreattrs, changeattrs, **kwargs)

        #: 게임 시작 시간(UTC)(datetime)
        self.starttime = utils._change_str_todt(kwargs['startTime'])

        #: 게임 종료 시간(UTC)(datetime)
        self.endtime = utils._change_str_todt(kwargs['endTime'])

        #: 참여 유저 정보 (:class:`Player`)
        self.player = Player(api, **kwargs['player'])

        #: 매치 상세 정보 (:class:`.MatchDetail`)
        self.detail = MatchDetail(api, kwargs['matchId'])

    @property
    def character(self) -> str:
        """캐릭터 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getcharactername(self.characterid)

    @property
    def track(self) -> str:
        """트랙 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return gettrackname(self.trackid)

    @property
    def matchtype(self) -> str:
        """매치 종류 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getgametypename(self.matchtypeid)


class AllMatches(_BaseData, MergeAbleDict['MatchDetail']):
    """전체 매치의 데이터를 담고 있는 클래스입니다.

    매치 타입 ID 또는 이름(메타데이터 경로가 지정됐을때)을 키로,
    :class:`.MatchDetail` 의 리스트를 값으로 가지는 dict와 같습니다.

    사용법:
        >>> mr = api.user('닉네임').getMatches()
        >>> mi = mr['아이템 팀전']
        >>> mi[0].character
        노네임
    """

    def __init__(self, api, **kwargs):
        matches = kwargs['matches']
        _BaseData.__init__(self, api)
        MergeAbleDict.__init__(self)

        meta = _safe_check('gameType.json')

        for item in matches:
            mt = item['matchType']
            prematchlist = item['matches']

            if meta:
                mt = getgametypename(mt)

            self[mt] = [None] * len(prematchlist)

            for i, match in enumerate(prematchlist):
                detail = MatchDetail(self._api, match)
                self[mt][i] = detail


class MatchDetail(_BaseData):
    """매치의 상세 정보를 담고 있는 클래스입니다.

    사용법:
        >>> all = api.getAllMatches()
        >>> teammatch = all['스피드 팀전']
        >>> detail = teammatch[0]
        >>> detail.matchType
        스피드 팀전

    .. note:: matchTypeId를 제외한 나머지 속성들은 호출할때 최초 1번 api를 사용합니다.\n
              isTeamGame 이 True 일시 teams를, false 일시 players 를 멤버로 갖습니다.
    """
    channelname: str  #: 채널 명(str)
    endtime: datetime  #: 게임 종료 시간(datetime)
    gamespeed: int  #: 게임 스피드 모드(int)
    matchresult: str  #: 매치 결과(str)
    matchtypeid: str  #: 매치 종류 ID(str)
    playtime: int  #: 게임 진행 시간(int)
    starttime: datetime  #: 게임 시작 시간(datetime)
    trackid: str  #: 트랙 ID(str)
    players: None  #: 참여 플레이어 정보 (list(:class:`Player`))
    teams: None  #: 팀 정보 (list(:class:`KartRider.match.Team`))
    isteamgame: bool  #: 팀 게임 여부(bool)

    def __init__(self, api, matchid):
        self.matchid = matchid  #: 매치 ID(str)
        super(MatchDetail, self).__init__(api)
        self._cachedetail = False

    def _getdetail(self):
        if self._cachedetail:
            raise Exception('알 수 없는 에러')
        raw = self._api._getMatchDetails(self.matchid)

        changeattrs = {'matchtype': 'matchtypeid'}

        for k, v in raw.items():
            k = k.lower()
            if k == 'teams':
                self.teams: List['Team'] = [None] * len(v)

                for i, team in enumerate(v):
                    self.teams[i] = Team(
                        self._api, team['teamId'], team['players'])

            elif k == 'players':
                self.players: List[Player] = [None] * len(v)

                for i, player in enumerate(v):
                    self.players[i] = Player(self._api, **player)

            elif k == 'endtime' or k == 'starttime':
                time = utils._change_str_todt(v)
                setattr(self, k, time)
            else:
                if k in changeattrs:
                    k = changeattrs[k]
                if v == '':
                    v = None
                setattr(self, k, v)

        if 'teams' in self.__dict__:
            self.isteamgame = True
        else:
            self.isteamgame = False
        self._cachedetail = True

    def __getattr__(self, attr):
        lazyattrs = ['channelname', 'endtime', 'gamespeed', 'matchid',
                     'matchresult', 'matchtype', 'playtime', 'starttime',
                     'trackid', 'teams', 'players']

        if attr in lazyattrs:
            if self._cachedetail:
                raise AttributeError
            self._getdetail()
            return getattr(self, attr)
        raise AttributeError(f'없는 속성 {attr}을 호출하려 했습니다.')

    @property
    def matchtype(self) -> str:
        """매치 종류 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getgametypename(self.matchtypeid)

    @property
    def track(self) -> str:
        """트랙 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return gettrackname(self.trackid)


class Team(List['Player'], list):
    """:class:`Player` 의 List입니다.
    """

    def __init__(self, api, teamid: int, players):
        self.teamid = teamid  #: 팀 ID(str)

        for player in players:
            self.append(Player(api, **player))


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
    accountno: str  #: 유저 ID(str)
    charactername: str  #: 유저 닉네임(str)
    characterid: str  #: 캐릭터 ID(str)
    flyingPetid: str  #: 플라잉펫 ID(str)
    kartid: str  #: 카트 ID(str)
    license: str  #: 구 라이선스(str)
    matchtime: int  #: 매치 진행 시간(int)
    partsengine: str  #: 카트바디의 엔진 파츠 (9 엔진 이하)(str)
    partshandle: str  #: 카트바디의 핸들 파츠 (9 엔진 이하)(str)
    partskit: str  #: 카트바디의 킷 파츠 (9 엔진 이하)(str)
    partswheel: str  #: 카트바디의 휠 파츠 (9 엔진 이하)(str)
    petid: str  #: 펫 ID(str)
    rankinggrade2: str  #: 리뉴얼 라이선스(str)

    def __init__(self, api, **kwargs):
        changeattrs = {'kart': 'kartid', 'character': 'characterid',
                       'pet': 'petid', 'flyingpet': 'flyingpetid'}
        ignoreattrs = ['matchrank', 'matchwin', 'matchretired']
        intattrs = ['matchtime']
        super(Player, self).__init__(
            api, intattrs, ignoreattrs, changeattrs, **kwargs)

        rank = kwargs['matchRank']

        if rank == '99' or rank == '':
            self.matchrank = -1  #: 순위, 리타이어는 -1
            self.matchretired = True  #: 리타이어 여부
        elif rank == '1':
            self.matchrank = 1
            self.matchretired = False
        else:
            self.matchrank = int(rank)
            self.matchretired = False

        if kwargs['matchWin'] == '0':
            self.matchwin = False  #: 매치 승리 여부
        else:
            self.matchwin = True

    @property
    def kart(self) -> str:
        """카트 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('kart', self.kartid)

    @property
    def pet(self) -> str:
        """펫 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('pet', self.petid)

    @property
    def flyingpet(self) -> str:
        """플라잉펫 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('flyingPet', self.flyingpetid)

    @property
    def character(self) -> str:
        """캐릭터 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return _getname('character', self.characterid)
