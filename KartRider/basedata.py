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


class _AliasDict(dict, Mapping[str, T]):
    def __init__(self, *args, **kwargs):
        super(_AliasDict, self).__init__(*args, **kwargs)
        self._aliases = {}

    def __getitem__(self, key) -> T:
        return dict.__getitem__(self, self._aliases.get(key, key))

    def __setitem__(self, key, value):
        return dict.__setitem__(self, self._aliases.get(key, key), value)

    def add_aliases(self, key, alias):
        self._aliases[alias] = key

    def __contains__(self, item):
        if item in self._aliases:
            return True
        return dict.__contains__(self, item)
