import requests
from .user import User
_API_URL = 'https://api.nexon.co.kr/kart/v1.0/'


class TooManyRequest(Exception):
    pass


class ForbiddenToken(Exception):
    pass


class InvalidToken(Exception):
    pass


class NotFound(Exception):
    pass


class UnknownStatusCode(Exception):
    pass


class Api(object):
    def __init__(self, accesstoken: str):
        self.accesstoken = accesstoken

    def _makeapiheader(self):
        return {'Authorization': self.accesstoken}

    def _getresponse(self, url):
        res = requests.get(url, headers=self._makeapiheader())

        self._errorstatuscode(res.status_code)
        return res

    def _errorstatuscode(self, code):
        if code == 200:
            return None
        elif code == 400:
            raise InvalidToken
        elif code == 403:
            raise ForbiddenToken
        elif code == 404:
            raise NotFound
        elif code == 429:
            raise TooManyRequest
        else:
            raise UnknownStatusCode(code)

    def user(self, nickname=None, accessid=None):
        if nickname is None and accessid is None:
            raise ValueError

        elif nickname is not None and accessid is not None:
            vnick = self.getIDfromNickname(accessid)
            if vnick != nickname:
                raise ValueError
            else:
                return User(self, vnick, accessid)

        else:
            if nickname is None:
                nickname = self.getNicknamefromID(accessid)
            else:
                accessid = self.getIDfromNickname(nickname)
            return User(self, nickname, accessid)

    def getIDfromNickname(self, nickname):
        raw = self._getresponse(_API_URL + f'users/nickname/{nickname}').json()
        return raw['accessId']

    def getNicknamefromID(self, accessid):
        raw = self._getresponse(_API_URL + f'users/{accessid}').json()
        return raw['name']
