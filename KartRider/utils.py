import datetime
from .metadata import _safe_check, _getid


def _change_dt_tostr(dt: datetime.datetime):
    format = '%Y-%m-%d %H:%M:%S'
    return dt.strftime(format)


def _change_str_todt(date: str):
    format = '%Y-%m-%dT%H:%M:%S'
    try:
        dt = datetime.datetime.strptime(date, format)
    except ValueError:
        format = '%Y-%m-%dT%H:%M:%S.%f'
        dt = datetime.datetime.strptime(date, format)

    return dt


def _convMt(mt):
    if mt != '':
        if type(mt) is str:
            mt = [mt]

        match_type_ids = [None] * len(mt)

        if _safe_check('gameType.json'):
            for i, name in enumerate(mt):
                match_type_ids[i] = _getid('gameType', name)

            match_type_ids = list(match_type_ids)
            match_type_ids = ','.join(match_type_ids)
        else:
            match_type_ids = ','.join(mt)
    else:
        match_type_ids = ''

    return match_type_ids


def _convStEt(st: datetime, et: datetime):
    if st != '' and type(st) is datetime:
        st = _change_dt_tostr(st)

    if et != '' and type(et) is datetime:
        et = _change_dt_tostr(et)
    return st, et
