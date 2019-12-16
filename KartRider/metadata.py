import json
import os

_path = ""


def set_metadatapath(path: str):
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

    if result == "":
        return 'Unknown'

    elif result is None:
        raise KeyError(f'id {datavalue} not found.')

    return result


def _getid(datatype: str, name: str) -> str:
    return _get(datatype, 'id', name, 'name')
