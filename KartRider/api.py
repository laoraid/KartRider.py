import requests

_API_URL = 'https://api.nexon.co.kr/kart/v1.0/'


class TooManyRequest(Exception):
    pass


class ForbiddenToken(Exception):
    pass


class InvalidToken(Exception):
    pass


class KartRider(object):
    def __init__(self, accesstoken: str):
        self.accesstoken = accesstoken

    def _makeapiheader(self):
        return {'Authorization': self.accesstoken}

    def _getresponse(self, url):
        res = requests.get(url, headers=self._makeapiheader())

        self._statuscode(res.status_code)
        return res

    def _statuscode(self, code):
        if code == 400:
            raise InvalidToken
        elif code == 403:
            raise ForbiddenToken
        elif code == 429:
            raise TooManyRequest

    def getid(self, nickname):
        raw = self._getresponse(_API_URL + f'users/nickname/{nickname}').json()
        return raw
