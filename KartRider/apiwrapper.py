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
    """카트라이더 OpenAPI Wrapper 클래스

    :param accesstoken: 사용자의 API KEY 문자열
    """

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
        """
        유저의 닉네임과 ID 클래스
        Api.user(nickname) -> nickname 으로 User 클래스 생성
        Api.user(accessid) -> accessid 로 User 클래스 생성
        Api.user(nickname, accessid) -> nickname 과 accessid 일치 여부 확인 후
        User 클래스 생성

        :param nickname: 검색할 닉네임
        :param accessid: 검색할 accessid
        :raises ValueError: nickname 과 accessid 모두 입력하지 않음
        :raises ValueError: nickname 과 ID가 일치하지 않음
        :raises InvalidToken: 잘못된 Token이나 파라미터 입력
        :raises ForbiddenToken: 허용되지 않은 AccessToken 사용
        :raises NotFound: 존재하지 않는 리소스
        :raises TooManyRequest: AccessToken의 요청 허용량 초과
        :raises UnknownStatusCode: 알 수 없는 오류로 API 서버와 통신이 불가능

        :return: 검색한 유저의 닉네임, ID 클래스
        :rtype: User
        """
        if nickname is None and accessid is None:
            raise ValueError

        elif nickname is not None and accessid is not None:
            vnick = self._getNicknamebyID(accessid)
            if vnick != nickname:
                raise ValueError
            else:
                return User(self, vnick, accessid)

        else:
            if nickname is None:
                nickname = self._getNicknamebyID(accessid)
            else:
                accessid = self._getIDbyNickname(nickname)
            return User(self, nickname, accessid)

    def _getIDbyNickname(self, nickname: str) -> str:
        raw = self._getresponse(_API_URL + f'users/nickname/{nickname}').json()
        return raw['accessId']

    def _getNicknamebyID(self, accessid: str) -> str:
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
