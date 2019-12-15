from .basedata import BaseData


class MatchResponse(BaseData):
    def __init__(self, api, nickname, matches):
        super(MatchResponse, self).__init__(api)
        self.nickname = nickname
        self.matches = matches

    def __len__(self):
        return len(self.matches)


class Match(BaseData):
    def __init__(self, api, matchtypeid: str, matches: list):
        super(Match, self).__init__(api)
        self.matchtypeid = matchtypeid
        self.matches = matches

    @property
    def matchtype(self) -> str:
        raise NotImplementedError  # TODO : Metadata에서 매치 이름 찾아서 반환


class MatchInfo(BaseData):
    def __init__(self, api, **kwargs):
        intattrs = ['playTime', 'playerCount']
        ignoreattrs = ['startTime', 'endTime', 'player']
        changenameattrs = {'matchtype': 'matchtypeid',
                           'character': 'characterid',
                           'playtime': '_playtimesec'}

        super(MatchInfo, self).__init__(api, intattrs,
                                        ignoreattrs, changenameattrs, **kwargs)

        _ = {k: v for k, v in kwargs if k in ignoreattrs}

        # TODO : ignoreattrs 처리
