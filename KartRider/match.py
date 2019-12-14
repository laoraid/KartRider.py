from .basedata import BaseData


class MatchResponse(BaseData):
    def __init__(self, api, nickname, matches):
        super(MatchResponse, self).__init__(api)
        self.nickname = nickname
        self.matches = matches

    def __len__(self):
        return len(self.matches)


class MatchInfo(BaseData):
    def __init__(self, api, **kwargs):
        intattrs = ['playTime', 'playerCount']
        ignoreattrs = ['startTime', 'endTime', 'player']

        super(MatchInfo, self).__init__(api, intattrs, ignoreattrs, **kwargs)

        _ = {k: v for k, v in kwargs if k in ignoreattrs}

        # TODO : ignoreattrs 처리
