from .basedata import BaseData
from .user import _Player
from . import utils
from .metadata import _getname


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
        ignoreattrs = ['startTime', 'endTime', 'player']
        changeattrs = {'matchtype': 'matchtypeid',
                       'character': 'characterid',
                       'playtime': '_playtimesec'}

        super(_MatchInfo, self).__init__(api, intattrs,
                                         ignoreattrs, changeattrs, **kwargs)

        self.startTime = utils._change_str_todt(kwargs['startTime'])
        self.endTime = utils._change_str_todt(kwargs['endTime'])

        self.player = _Player(api, **kwargs['player'])

    @property
    def character(self):
        return _getname('character', self.characterid)

    @property
    def track(self) -> str:
        return _getname('track', self.trackId)
