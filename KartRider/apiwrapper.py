from datetime import datetime
import requests
from typing import Optional, List, Union
from .user import User
from .match import MatchResponse, AllMatches
from . import utils
_API_URL = 'https://api.nexon.co.kr/kart/v1.0/'

dtstr = Union[datetime, str]


class TooManyRequest(Exception):
    """API Key 의 요청 허용량을 초과했을때(응답코드 429) 발생하는 오류입니다.
    """
    pass


class ForbiddenToken(Exception):
    """허용되지 않은 API key를 사용했을때(응답코드 403) 발생하는 오류입니다.
    """
    pass


class InvalidToken(Exception):
    """잘못된 파라미터 입력(응답코드 400)을 할때 발생하는 오류입니다.
    """
    pass


class NotFound(Exception):
    """리소스가 존재하지 않을때(응답코드 404) 발생하는 오류입니다.
    """
    pass


class UnknownStatusCode(Exception):
    """OpenAPI나 모듈의 버그로 인하여 발생하는 오류입니다.
    """
    pass


class Api(object):
    """카트라이더 OpenAPI Wrapper 클래스입니다.

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

    def user(self, nickname: Optional[str] = None,
             accessid: Optional[str] = None) -> User:
        """
        유저의 닉네임과 ID 클래스를 생성합니다.

        사용법:

        >>> api = KartRider.Api(API_KEY)
        >>> api.user(nickname) # nickname 으로 User 클래스 생성
        >>> api.user(accessid) # accessid 로 User 클래스 생성
        >>> api.user(nickname, accessid)
        # nickname 과 accessid 일치 여부 확인 후 User 클래스 생성


        :param nickname: 검색할 닉네임
        :param accessid: 검색할 accessid
        :raises ValueError: nickname 과 accessid 모두 입력하지 않음
        :raises ValueError: nickname 과 ID가 일치하지 않음
        :raises InvalidToken: 잘못된 Token이나 파라미터 입력
        :raises ForbiddenToken: 허용되지 않은 AccessToken 사용
        :raises NotFound: 존재하지 않는 리소스
        :raises TooManyRequest: AccessToken의 요청 허용량 초과
        :raises UnknownStatusCode: 알 수 없는 오류

        :rtype: User
        """
        if nickname is None and accessid is None:
            raise ValueError('파라미터를 입력하지 않았습니다.')

        elif nickname is not None and accessid is not None:
            try:
                vnick = self._getNicknamebyID(accessid)
            except NotFound:
                vnick = None

            if vnick != nickname:
                raise ValueError('닉네임과 ID가 일치하지 않습니다.')
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

    def getUserMatches(self, id: Union[str, User], start_date: dtstr = "",
                       end_date: dtstr = "", offset: int = 0,
                       limit: int = 10,
                       match_types:
                       Union[List[str], str] = "") -> MatchResponse:
        """유저의 매치 데이터를 받아옵니다.
        Api.user(...).getMatches(...) 로도 사용할 수도 있습니다.

        :param id: 유저의 accessid 혹은 User 클래스
        :param start_date: 조회 시작 날짜(UTC)
        :param end_date: 조회 끝 날짜(UTC)
        :param offset: 조회 오프셋
        :param limit: 조회 수 (최대 500건)
        :param match_types: 매치 타입 이름이나 ID (리스트 또는 단일 문자열)

        :raises InvalidToken: 잘못된 Token이나 파라미터 입력
        :raises ForbiddenToken: 허용되지 않은 AccessToken 사용
        :raises NotFound: 존재하지 않는 리소스
        :raises TooManyRequest: AccessToken의 요청 허용량 초과
        :raises UnknownStatusCode: 알 수 없는 오류

        :rtype: MatchResponse
        """
        if type(id) is User:
            id = id.accessid

        start_date, end_date = utils._convStEt(start_date, end_date)

        match_type_ids = utils._convMt(match_types)

        raw = self._getMatchlist(
            id, start_date, end_date, offset, limit, match_type_ids)

        return MatchResponse(self, raw['nickName'], raw['matches'])

    def getAllMatches(self, start_date: dtstr = "", end_date: dtstr = "",
                      offset: int = 0, limit: int = 10,
                      match_types: Union[List[str], str] = "") -> AllMatches:
        """모든 유저의 매치 데이터를 받아옵니다.

        :param start_date: 조회 시작 날짜(UTC)
        :param end_date: 조회 끝 날짜(UTC)
        :param offset: 조회 오프셋
        :param limit: 조회 수 (최대 500건)
        :param match_types: 매치 타입 이름이나 ID (리스트 또는 단일 문자열)

        :raises InvalidToken: 잘못된 Token이나 파라미터 입력
        :raises ForbiddenToken: 허용되지 않은 AccessToken 사용
        :raises NotFound: 존재하지 않는 리소스
        :raises TooManyRequest: AccessToken의 요청 허용량 초과
        :raises UnknownStatusCode: 알 수 없는 오류

        :return: 모든 매치 정보 클래스
        :rtype: AllMatches
        """
        start_date, end_date = utils._convStEt(start_date, end_date)
        match_types = utils._convMt(match_types)
        url = _API_URL + (
            f'matches/all?start_date={start_date}'
            f'&end_date={end_date}&offset={offset}'
            f'&limit={limit}&match_types={match_types}'
        )

        raw = self._getresponse(url).json()

        return AllMatches(self, **raw)

    def _getMatchDetails(self, match_id: str) -> dict:
        url = _API_URL + f'matches/{match_id}'
        raw = self._getresponse(url).json()
        return raw
