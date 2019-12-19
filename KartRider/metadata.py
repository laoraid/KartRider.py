import json
import os

_path = ""


def set_metadatapath(path: str):
    """메타데이터의 경로를 설정합니다.

    메타데이터는 python -m KartRider -d 로 다운로드 받을 수 있습니다.
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


def _check_metadatapath(filename):
    if not os.path.isfile(os.path.join(_path, filename)):
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


def _outer(datatype):
    def inner() -> dict:
        return _gets(datatype)
    return inner


getKarts = _outer('kart')
getPets = _outer('pet')
getTracks = _outer('track')
getgameTypes = _outer('gameType')
getflyingPets = _outer('flyingPet')
getCharacters = _outer('character')
