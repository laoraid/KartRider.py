import json
import os
import functools
from zipfile import ZipFile
from io import BytesIO
import requests
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


def _getId(datatype: str, name: str) -> str:
    return _get(datatype, 'id', name, 'name')


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


getKartsDict = functools.partial(_gets, 'kart')
"""카트 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""


getPetsDict = functools.partial(_gets, 'pet')
"""펫 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""


getTracksDict = functools.partial(_gets, 'track')
"""트랙 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""

getgameTypesDict = functools.partial(_gets, 'gameType')
"""게임 유형 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""


getflyingPetsDict = functools.partial(_gets, 'flyingPet')
"""플라잉펫 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""

getCharactersDict = functools.partial(_gets, 'character')
"""캐릭터 id를 키로, 이름을 값으로 하는 딕셔너리를 가져옵니다.

:rtype: dict
"""


def getCharacterName(id: str) -> str:
    """캐릭터 ID를 받아 이름을 반환합니다.

    :param id: 캐릭터 ID
    :type id: str
    :return: 캐릭터 이름
    :rtype: str
    """
    return _getname('character', id)


def getFlyingPetName(id: str) -> str:
    """플라잉펫 ID를 받아 이름을 반환합니다.

    :param id: 플라잉펫 ID
    :type id: str
    :return: 플라잉펫 이름
    :rtype: str
    """
    return _getname('flyingPet', id)


def getGameTypeName(id: str) -> str:
    """게임 타입 ID를 받아 이름을 반환합니다.

    :param id: 게임 타입 ID
    :type id: str
    :return: 게임 타입 이름
    :rtype: str
    """
    return _getname('gameType', id)


def getKartName(id: str) -> str:
    """카트 ID를 받아 이름을 반환합니다.

    :param id: 카트 ID
    :type id: str
    :return: 카트 이름
    :rtype: str
    """
    return _getname('kart', id)


def getPetName(id: str) -> str:
    """펫 ID를 받아 이름을 반환합니다.

    :param id: 펫 ID
    :type id: str
    :return: 펫 이름
    :rtype: str
    """
    return _getname('pet', id)


def getTrackName(id: str) -> str:
    """트랙 ID를 받아 이름을 반환합니다.

    :param id: 트랙 ID
    :type id: str
    :return: 트랙 이름
    :rtype: str
    """
    return _getname('track', id)


def getCharacterId(name: str) -> str:
    """캐릭터 이름을 받아 ID를 반환합니다.

    :param name: 캐릭터 이름
    :type name: str
    :return: 캐릭터 ID
    :rtype: str
    """
    return _getId('character', name)


def getFlyingPetId(name: str) -> str:
    """플라잉펫 이름을 받아 ID를 반환합니다.

    :param name: 플라잉펫 이름
    :type name: str
    :return: 플라잉펫 ID
    :rtype: str
    """
    return _getId('flyingPet', name)


def getGameTypeId(name: str) -> str:
    """게임 타입 이름을 받아 ID를 반환합니다.

    :param name: 게임 타입 이름
    :type name: str
    :return: 게임 타입 ID
    :rtype: str
    """
    return _getId('gameType', name)


def getKartId(name: str) -> str:
    """카트 이름을 받아 ID를 반환합니다.

    :param name: 카트 이름
    :type name: str
    :return: 카트 ID
    :rtype: str
    """
    return _getId('kart', name)


def getPetId(name: str) -> str:
    """펫 이름을 받아 ID를 반환합니다.

    :param name: 펫 이름
    :type name: str
    :return: 펫 ID
    :rtype: str
    """
    return _getId('pet', name)


def getTrackId(name: str) -> str:
    """트랙 이름을 받아 ID를 반환합니다.

    :param name: 트랙 이름
    :type name: str
    :return: 트랙 ID
    :rtype: str
    """
    return _getId('track', name)


def download_meta(file_dir: str):
    """메타데이터를 다운로드 합니다.

    :param file_dir: 메타데이터가 들어갈 폳더 경로
    :type file_dir: str
    """
    url = 'https://static.api.nexon.co.kr/kart/latest/metadata.zip'
    res = requests.get(url)

    zipfile = ZipFile(BytesIO(res.content))

    zipfile.extractall(file_dir)
    res.close()
    zipfile.close()


def downmeta_ifnotexist(file_dir: str) -> bool:
    """메타데이터 폴더가 없으면 메타데이터를 다운로드 합니다.

    :param file_dir: 메타데이터가 들어가거나 있는 폴더
    :type file_dir: str
    :return: 다운로드 했으면 True, 하지 않았으면 False 를 반환합니다.
    :rtype: bool
    """
    filenames = ['character', 'flyingPet', 'gameType', 'kart', 'pet', 'track']
    images = ['character', 'kart', 'track']

    for filename in filenames:
        if not os.path.isfile(os.path.join(file_dir, filename + '.json')):
            download_meta(file_dir)
            return True

    for image in images:
        if not os.path.isdir(os.path.join(file_dir, image)):
            download_meta(file_dir)
            return True

    return False
