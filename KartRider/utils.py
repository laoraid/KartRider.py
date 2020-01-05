from datetime import datetime
from . import metadata as md


def _change_dt_tostr(dt: datetime):
    format = '%Y-%m-%d %H:%M:%S'
    return dt.strftime(format)


def _change_str_todt(date: str):
    format = '%Y-%m-%dT%H:%M:%S'
    try:
        dt = datetime.strptime(date, format)
    except ValueError:
        format = '%Y-%m-%dT%H:%M:%S.%f'
        dt = datetime.strptime(date, format)

    return dt


def _convMt(mt):
    if mt != '':
        if type(mt) is str:
            mt = [mt]

        match_type_ids = [None] * len(mt)

        for i, id in enumerate(mt):
            if _isId(id):
                match_type_ids[i] = id
            else:
                match_type_ids[i] = md._getid('gameType', id)

        return ','.join(match_type_ids)
    else:
        return ''


def _isId(string):
    if ' ' in string:
        return False

    if len(string) >= 64:
        return True

    return False


def _convStEt(st, et):
    if st != '' and type(st) is datetime:
        st = _change_dt_tostr(st)

    if et != '' and type(et) is datetime:
        et = _change_dt_tostr(et)
    return st, et
