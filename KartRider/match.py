from typing import List
from datetime import datetime
from .basedata import BaseData, AliasDict
from .user import _Player
from . import utils
from .metadata import _getname, _safe_check


class _MatchResponse(BaseData):
    def __init__(self, api, nickname: str, matcheslist):
        super(_MatchResponse, self).__init__(api)
        self.nickname = nickname
        self.matches: AliasDict[str, '_MatchInfo'] = AliasDict()

        meta = _safe_check('gameType.json')

        for match in matcheslist:
            matchinforaw = match['matches']
            matchtypeid = match['matchType']
            matchinfo = [None] * len(matchinforaw)

            for i, m in enumerate(matchinforaw):
                matchinfo[i] = _MatchInfo(api, **m)
            self.matches[matchtypeid] = matchinfo

            if meta:
                self.matches.add_aliases(
                    matchtypeid, _getname('gameType', matchtypeid))

    def __getitem__(self, key: str) -> List['_MatchInfo']:
        if type(key) is not str:
            raise TypeError((
                f'_AllMatches 의 key는 str 이어야 합니다. '
                f'{type(key)}가 아닙니다.'))
        if key in self.matches:
            return self.matches[key]
        else:
            raise KeyError(f'{key} -> 키를 찾을 수 없습니다.')

    def __len__(self) -> int:
        return len(self.matches)


class _MatchInfo(BaseData):
    accountNo: str
    channelName: str
    characterId: str
    matchResult: str
    matchTypeId: str
    playerCount: int
    teamId: str
    trackId: str

    def __init__(self, api, **kwargs):
        intattrs = ['playerCount']
        ignoreattrs = ['startTime', 'endTime', 'player', 'matchId']
        changeattrs = {'matchType': 'matchTypeId',
                       'character': 'characterId'}

        super(_MatchInfo, self).__init__(api, intattrs,
                                         ignoreattrs, changeattrs, **kwargs)

        self.startTime = utils._change_str_todt(kwargs['startTime'])
        self.endTime = utils._change_str_todt(kwargs['endTime'])

        self.player = _Player(api, **kwargs['player'])
        self.detail = _MatchDetail(api, kwargs['matchId'])

    @property
    def character(self) -> str:
        return _getname('character', self.characterId)

    @property
    def track(self) -> str:
        return _getname('track', self.trackId)

    @property
    def matchType(self) -> str:
        return _getname('gameType', self.matchTypeId)


class _AllMatches(BaseData):
    def __init__(self, api, **kwargs):
        matches = kwargs['matches']
        super(_AllMatches, self).__init__(api)
        self.matches: AliasDict[str, List['_MatchDetail']] = AliasDict()

        meta = _safe_check('gameType.json')

        for item in matches:
            mt = item['matchType']
            prematchlist = item['matches']

            self.matches[mt] = [None] * len(prematchlist)

            for i, match in enumerate(prematchlist):
                detail = _MatchDetail(self._api, match)
                self.matches[mt][i] = detail
                if meta:
                    name = _getname('gameType', mt)
                    self.matches.add_aliases(mt, name)

    def __getitem__(self, key: str) -> List['_MatchDetail']:
        if type(key) is not str:
            raise TypeError((
                f'_AllMatches 의 key는 str 이어야 합니다. '
                f'{type(key)}가 아닙니다.'))
        if key in self.matches:
            return self.matches[key]
        else:
            raise KeyError(f'{key} -> 키를 찾을 수 없습니다.')

    def __len__(self) -> int:
        return len(self.matches)


class _MatchDetail(BaseData):
    channelName: str
    endTime: datetime
    gameSpeed: int
    matchResult: str
    matchTypeId: str
    playTime: int
    startTime: datetime
    trackId: str

    def __init__(self, api, matchid):
        self.matchId = matchid
        super(_MatchDetail, self).__init__(api)
        self._cachedetail = False

    def _getdetail(self):
        if self._cachedetail:
            raise Exception
        raw = self._api._getMatchDetails(self.matchId)

        changeattrs = {'matchType': 'matchTypeId'}

        for k, v in raw.items():
            if k == 'teams':  #
                self.teams: List['_Team'] = [None] * len(v)

                for i, team in enumerate(v):
                    self.teams[i] = _Team(
                        self._api, team['teamId'], team['players'])

            elif k == 'players':
                self.players: List[_Player] = [None] * len(v)

                for i, player in enumerate(v):
                    self.players[i] = _Player(self._api, **player)

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
        raise AttributeError

    @property
    def matchType(self) -> str:
        return _getname('gameType', self.matchTypeId)

    @property
    def track(self) -> str:
        return _getname('track', self.trackId)


class _Team(object):
    def __init__(self, api, teamId: int, players):
        self.teamId = teamId
        self.players: List[_Player] = [None] * len(players)

        for i, player in enumerate(players):
            self.players[i] = _Player(api, **player)
