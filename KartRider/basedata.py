from typing import TypeVar, Mapping


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

    def mergeValues(self) -> list:
        """dict의 리스트 밸류들을 모두 하나로 합칩니다.

        게임타입을 key로, 게임 정보의 리스트를 value 로 가지는 dict에서
        게임타입을 무시하고게임 정보의 리스트를 합쳐 1차원 리스트로 반환합니다.


        :return: 게임 정보의 리스트
        :rtype: list
        """
        length = sum(len(x) for x in self.values())
        li = [None] * length

        i = 0

        for v in self.values():
            for rr in v:
                li[i] = rr
                i += 1

        return li
