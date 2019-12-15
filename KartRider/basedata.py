
class BaseData(object):
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

            for k, v in kwargs:
                if k in ignoreattrs:
                    continue
                elif k in intattrs:
                    setattr(self, k, int(v))
                elif k in changenameattrs:
                    setattr(self, changenameattrs[k], v)
                else:
                    if v.strip() == "":
                        v = None
                    setattr(self, k, v)
