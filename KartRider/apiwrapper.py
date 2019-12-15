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

    def _getresponse(self, url: str) -> requests.Response:
        res = requests.get(url, headers=self._makeapiheader())

        self._errorstatuscode(res.status_code)
        return res

    def _errorstatuscode(self, code: int):
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

    def user(self, nickname: str = None, accessid: str = None) -> User:
        if nickname is None and accessid is None:
            raise ValueError

        elif nickname is not None and accessid is not None:
            vnick = self.getNicknamebyID(accessid)
            if vnick != nickname:
                raise ValueError
            else:
                return User(self, vnick, accessid)

        else:
            if nickname is None:
                nickname = self.getNicknamebyID(accessid)
            else:
                accessid = self.getIDbyNickname(nickname)
            return User(self, nickname, accessid)

    def getIDbyNickname(self, nickname: str) -> str:
        raw = self._getresponse(_API_URL + f'users/nickname/{nickname}').json()
        return raw['accessId']

    def getNicknamebyID(self, accessid: str) -> str:
        raw = self._getresponse(_API_URL + f'users/{accessid}').json()
        return raw['name']

    def _getMatchlist(self, accessid: str, start_date: str = "",
                      end_date: str = "", offset: int = 0, limit: int = 10,
                      match_types: str = "") -> dict:
        url = _API_URL + (
            f'users/{accessid}/matches?'
            f'start_date={start_date}&end_date={end_date}'
            f'&offset={offset}&limit={limit}&match_types={match_types}')

        raw = self._getresponse(url).json()
        return raw

    def _getAllmatchlist(self, start_date: str = "", end_date: str = "",
                         offset: int = 0, limit: int = 10,
                         match_types: str = "") -> dict:
        url = _API_URL + (
            f'matches/all?start_date={start_date}'
            f'&end_date={end_date}&offset={offset}'
            f'&limit={limit}&match_types={match_types}'
        )

        raw = self._getresponse(url).json()
        return raw

    def _getMatchdetails(self, match_id: str) -> dict:
        url = _API_URL + f'matches/{match_id}'
        raw = self._getresponse(url).json()
        return raw
