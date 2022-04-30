import datetime


def get_date_and_time_as_string(_datetime: datetime.datetime):
    return _datetime.strftime("%Y%m%d_%H%M%S")
