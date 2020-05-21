from typing import List
from datetime import datetime
from .basedata import _BaseData, MergeAbleDict
from . import utils
from .metadata import (_safe_check, getTrackName, getGameTypeName,
                       getCharacterName)
from . import user


class MatchResponse(_BaseData, MergeAbleDict[List['MatchInfo']]):
    """매치 응답 정보를 담고 있는 클래스입니다.

    매치 타입 ID 또는 이름(메타데이터 경로가 지정됐을때)을 키로,
    :class:`.MatchInfo` 의 리스트를 값으로 가지는 dict와 같습니다.

    사용법:
        >>> mr = api.user('닉네임').getMatches()
        >>> mr['아이템 팀전'][0].playerCount
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
                matchtype = getGameTypeName(matchtypeid)
            else:
                matchtype = matchtypeid
            self[matchtype] = matchinfo


class MatchInfo(_BaseData):
    """매치 정보를 담고 있는 클래스입니다.

    사용법:
        >>> mr = api.user('닉네임').getMatches()
        >>> mi = mr['아이템 팀전'][0]
        >>> mi.character
        황금망토 배찌
    """
    accountNo: str  #: 계정 고유 식별자(str)
    channelName: str  #: 채널 이름(str)
    characterId: str  #: 캐릭터 ID(str)
    matchResult: str  # :(str)
    matchTypeId: str  #: 매치 종류 ID(str)
    playerCount: int  #: 참여 유저 수(int)
    teamId: str  #: 팀 ID(str)
    trackId: str  #: 트랙 ID(str)

    def __init__(self, api, **kwargs):
        intattrs = ['playerCount']
        ignoreattrs = ['startTime', 'endTime', 'player', 'matchId']
        changeattrs = {'matchType': 'matchTypeId',
                       'character': 'characterId'}

        super(MatchInfo, self).__init__(api, intattrs,
                                        ignoreattrs, changeattrs, **kwargs)

        #: 게임 시작 시간(UTC)(datetime)
        self.startTime = utils._change_str_todt(kwargs['startTime'])

        #: 게임 종료 시간(UTC)(datetime)
        self.endTime = utils._change_str_todt(kwargs['endTime'])

        #: 참여 유저 정보 (:class:`KartRider.user.Player`)
        self.player = user.Player(api, **kwargs['player'])

        #: 매치 상세 정보 (:class:`.MatchDetail`)
        self.detail = MatchDetail(api, kwargs['matchId'])

    @property
    def character(self) -> str:
        """캐릭터 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getCharacterName(self.characterId)

    @property
    def track(self) -> str:
        """트랙 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getTrackName(self.trackId)

    @property
    def matchType(self) -> str:
        """매치 종류 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getGameTypeName(self.matchTypeId)


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
                mt = getGameTypeName(mt)

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
    channelName: str  #: 채널 명(str)
    endTime: datetime  #: 게임 종료 시간(datetime)
    gameSpeed: int  #: 게임 스피드 모드(int)
    matchResult: str  #: 매치 결과(str)
    matchTypeId: str  #: 매치 종류 ID(str)
    playTime: int  #: 게임 진행 시간(int)
    startTime: datetime  #: 게임 시작 시간(datetime)
    trackId: str  #: 트랙 ID(str)
    players: None  #: 참여 플레이어 정보 (list(:class:`KartRider.user.Player`))
    teams: None  #: 팀 정보 (list(:class:`KartRider.match.Team`))
    isTeamGame: bool  #: 팀 게임 여부(bool)

    def __init__(self, api, matchid):
        self.matchId = matchid  #: 매치 ID(str)
        super(MatchDetail, self).__init__(api)
        self._cachedetail = False

    def _getdetail(self):
        if self._cachedetail:
            raise Exception('알 수 없는 에러')
        raw = self._api._getMatchDetails(self.matchId)

        changeattrs = {'matchType': 'matchTypeId'}

        for k, v in raw.items():
            if k == 'teams':
                self.teams: List['Team'] = [None] * len(v)

                for i, team in enumerate(v):
                    self.teams[i] = Team(
                        self._api, team['teamId'], team['players'])

            elif k == 'players':
                self.players: List[user.Player] = [None] * len(v)

                for i, player in enumerate(v):
                    self.players[i] = user.Player(self._api, **player)

            elif k == 'endTime' or k == 'startTime':
                time = utils._change_str_todt(v)
                setattr(self, k, time)
            else:
                if k in changeattrs:
                    k = changeattrs[k]
                if v == '':
                    v = None
                setattr(self, k, v)

        if 'teams' in self.__dict__:
            self.isTeamGame = True
        else:
            self.isTeamGame = False
        self._cachedetail = True

    def __getattr__(self, attr):
        lazyattrs = ['channelName', 'endTime', 'gameSpeed', 'matchId',
                     'matchResult', 'matchType', 'playTime', 'startTime',
                     'trackId', 'teams', 'players']

        if attr in lazyattrs:
            if self._cachedetail:
                raise AttributeError
            self._getdetail()
            return getattr(self, attr)
        raise AttributeError(f'없는 속성 {attr}을 호출하려 했습니다.')

    @property
    def matchType(self) -> str:
        """매치 종류 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getGameTypeName(self.matchTypeId)

    @property
    def track(self) -> str:
        """트랙 이름

        :raises FileNotFoundError: 메타데이터 경로가 설정되지 않았을때
        :rtype: str
        """
        return getTrackName(self.trackId)


class Team(List['user.Player'], list):
    """:class:`KartRider.user.Player` 의 List입니다.
    """

    def __init__(self, api, teamId: int, players):
        self.teamId = teamId  #: 팀 ID(str)

        for player in players:
            self.append(user.Player(api, **player))
