import datetime


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
    
