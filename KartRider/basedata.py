from typing import Iterator, Mapping, TypeVar


class _BaseData(object):
    def __init__(self, api, intattrs=None, ignoreattrs=None,
                 changenameattrs=None, **kwargs):
        self._api = api

        if len(kwargs) != 0:

            if intattrs is None:
                intattrs = []
            if ignoreattrs is None:
                ignoreattrs = []
            if changenameattrs is None:
                changenameattrs = {}

            for k, v in kwargs.items():
                k = k.lower()
                if k in ignoreattrs:
                    continue
                elif k in intattrs:
                    if v == '':
                        v = 0
                    setattr(self, k, int(v))
                elif k in changenameattrs:
                    setattr(self, changenameattrs[k], v)
                else:
                    if v.strip() == "":
                        v = None
                    setattr(self, k, v)


T = TypeVar('T')


class MergeAbleDict(dict, Mapping[str, T]):
    def __init__(self, *args, **kwargs):
        super(MergeAbleDict, self).__init__(*args, **kwargs)

    def mergevalues(self) -> Iterator[T]:
        """dict의 리스트 밸류들을 순회하는 제너레이터입니다.

        게임타입을 key로, 게임 정보의 리스트를 value 로 가지는 dict에서
        게임타입을 무시하고 게임 정보의 리스트를 합쳐 순회합니다.

        :yield: :class:`KartRider.match.MatchDetail` 또는
            :class:`KartRider.match.MatchInfo`
        :rtype: Iterator[T]
        """
        for v in self.values():
            yield from v
