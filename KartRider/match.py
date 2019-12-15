from .basedata import BaseData


class _MatchResponse(BaseData):
    def __init__(self, api, nickname, matches):
        super(_MatchResponse, self).__init__(api)
        self.nickname = nickname
        self.matches = matches

    def __len__(self):
        return len(self.matches)


class _Match(BaseData):
    def __init__(self, api, matchtypeid: str, matches: list):
        super(_Match, self).__init__(api)
        self.matchtypeid = matchtypeid
        self.matches = matches

    @property
    def matchtype(self) -> str:
        raise NotImplementedError  # TODO : Metadata에서 매치 이름 찾아서 반환


class _MatchInfo(BaseData):
    def __init__(self, api, **kwargs):
        intattrs = ['playTime', 'playerCount']
        ignoreattrs = ['startTime', 'endTime', 'player']
        changeattrs = {'matchtype': 'matchtypeid',
                       'character': 'characterid',
                       'playtime': '_playtimesec'}

        super(_MatchInfo, self).__init__(api, intattrs,
                                         ignoreattrs, changeattrs, **kwargs)

        _ = {k: v for k, v in kwargs if k in ignoreattrs}

        # TODO : ignoreattrs 처리
