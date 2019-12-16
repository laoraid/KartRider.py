import datetime


def _change_dt_tostr(dt: datetime.datetime):
    format = '%Y-%m-%d %H:%M:%S'
    return dt.strftime(format)


def _change_str_todt(date: str):
    format = '%Y-%m-%dT%H:%M:%S'
    return datetime.datetime.strptime(date, format)
