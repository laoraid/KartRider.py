import json
import os
import functools
from . import utils

_path = ""


def set_metadatapath(path: str):
    """메타데이터의 경로를 설정합니다.

    메타데이터는 python -m KartRider -d [경로] 로 다운로드 받을 수 있습니다.
    메타데이터 경로를 설정하지 않으면 여러 정보(카트, 트랙이름, 펫이름 등)의 실제 이름 확인이 불가능합니다.

    :param path: 메타데이터 폴더 경로 문자열
    :raises FileNotFoundError: 폴더가 존재하지 않을때
    """
    path = os.path.abspath(path)
    if os.path.isdir(path):
        global _path
        _path = path
    else:
        raise FileNotFoundError('폴더가 없습니다.')


def _safe_check(filename):
    try:
        _check_metadatapath(filename)
    except FileNotFoundError:
        return False
    return True


def _check_metadatapath(filename):
    if not os.path.isfile(os.path.join(_path, filename)):
        raise FileNotFoundError


def _check_metadatadir(dirname):
    if not os.path.isdir(os.path.join(_path, dirname)):
        raise FileNotFoundError


def _getname(datatype: str, id: str) -> str:
    return _get(datatype, 'name', id, 'id')


def _get(datatype: str, finddata: str, datavalue: str, dataname: str):
    filename = datatype + '.json'
    _check_metadatapath(filename)
    with open(os.path.join(_path, filename), encoding='utf8') as f:
        data = json.load(f)

    result = None

    for item in data:
        if datavalue == item[dataname]:
            result = item[finddata]

    if result == '' or datavalue is None or result is None:
        return 'Unknown'

    return result


def _getid(datatype: str, name: str) -> str:
    return _get(datatype, 'id', name, 'name')


def _gets(datatype):
    filename = datatype + '.json'
    _check_metadatapath(filename)

    with open(os.path.join(_path, filename), encoding='utf8') as f:
        data = json.load(f)

    r = {}

    for item in data:
        r[item['id']] = item['name']

    return r


def getImagePath(name: str, typename: str) -> str:
    """메타데이터 이미지의 경로를 가져옵니다.

    :param name: 가져올 메타데이터의 이름 또는 Id
    :param typename: 가져올 메타데이터 종류(kart, character, track)
    :return: 메타데이터의 이미지 경로
    :rtype: str
    """
    _check_metadatadir(typename)

    name = name if utils._isId(name) else _getid(typename, name)
    name = name + '.png'

    path = os.path.join(_path, typename, name)
    return path


getKarts = functools.partial(_gets, 'kart')
"""카트 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""


getPets = functools.partial(_gets, 'pet')
"""펫 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""


getTracks = functools.partial(_gets, 'track')
"""트랙 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""

getgameTypes = functools.partial(_gets, 'gameType')
"""게임 유형 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""


getflyingPets = functools.partial(_gets, 'flyingPet')
"""플라잉펫 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""

getCharacters = functools.partial(_gets, 'character')
"""캐릭터 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""
