from .basedata import BaseData
from .user import _Player
from . import utils
from .metadata import _getname, _check_metadatapath


class _MatchResponse(BaseData):
    def __init__(self, api, nickname, matcheslist):
        super(_MatchResponse, self).__init__(api)
        self.nickname = nickname
        self.matches = [None] * len(matcheslist)

        for i, match in enumerate(matcheslist):
            self.matches[i] = _Match(api, match['matchType'], match['matches'])

    def __len__(self):
        return len(self.matches)


class _Match(BaseData):
    def __init__(self, api, matchtypeid: str, matchesinfolist: list):
        super(_Match, self).__init__(api)
        self.matchtypeid = matchtypeid

        self.matchesinfo = [None] * len(matchesinfolist)

        for i, matchinfo in enumerate(matchesinfolist):
            self.matchesinfo[i] = _MatchInfo(api, **matchinfo)

    @property
    def matchtype(self) -> str:
        return _getname('gameType', self.matchtypeid)


class _MatchInfo(BaseData):
    def __init__(self, api, **kwargs):
        intattrs = ['playTime', 'playerCount']
        ignoreattrs = ['startTime', 'endTime', 'player', 'matchId']
        changeattrs = {'matchtype': 'matchtypeid',
                       'character': 'characterid',
                       'playtime': '_playtimesec'}

        super(_MatchInfo, self).__init__(api, intattrs,
                                         ignoreattrs, changeattrs, **kwargs)

        self.startTime = utils._change_str_todt(kwargs['startTime'])
        self.endTime = utils._change_str_todt(kwargs['endTime'])

        self.player = _Player(api, **kwargs['player'])
        self.detail = _MatchDetail(api, kwargs['matchId'])

    @property
    def character(self):
        return _getname('character', self.characterid)

    @property
    def track(self) -> str:
        return _getname('track', self.trackId)


class _AllMatches(BaseData):
    def __init__(self, api, **kwargs):
        matches = kwargs['matches']
        super(_AllMatches, self).__init__(api)
        self.matches = {}

        try:
            _check_metadatapath('gameType.json')
            meta = True
        except FileNotFoundError:
            meta = False

        for item in matches:
            mt = item['matchType']
            prematchlist = item['matches']

            self.matches[mt] = [None] * len(prematchlist)
            if meta:
                name = _getname('gameType', mt)
                self.matches[name] = [None] * len(prematchlist)

            for i, match in enumerate(prematchlist):
                detail = _MatchDetail(self._api, match)
                self.matches[mt][i] = detail
                if meta:
                    self.matches[name][i] = detail


class _MatchDetail(BaseData):
    def __init__(self, api, matchid):
        self.matchId = matchid
        super(_MatchDetail, self).__init__(api)
        self._cachedetail = False

    def _getdetail(self):
        if self._cachedetail:
            raise Exception
        raw = self._api._getMatchDetails(self.matchId)

        for k, v in raw.items():
            if k == 'teams':  #
                self.teams = [None] * len(v)

                for i, team in enumerate(v):
                    self.teams[i] = _Team(
                        self._api, team['teamId'], team['players'])

            elif k == 'players':
                self.players = [None] * len(v)

                for i, player in enumerate(v):
                    self.players[i] = _Player(self._api, **player)

            elif k == 'endTime' or k == 'startTime':
                time = utils._change_str_todt(v)
                setattr(self, k, time)
            else:
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


class _Team(object):
    def __init__(self, api, teamId, players):
        self.teamId = teamId
        self.players = [None] * len(players)

        for i, player in enumerate(players):
            self.players[i] = _Player(api, **player)
