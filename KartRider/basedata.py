
class BaseData(object):
    def __init__(self, api, intattrs=None, ignoreattrs=None, **kwargs):
        self._api = api

        if len(kwargs) != 0:
            if intattrs is None:
                intattrs = []

            for k, v in kwargs:
                if k in intattrs:
                    setattr(self, k, int(v))
                elif k in ignoreattrs:
                    continue
                else:
                    if v == "":
                        v = None
                    setattr(self, k, v)
