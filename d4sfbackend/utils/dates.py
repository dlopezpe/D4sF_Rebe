from datetime import datetime
import datetime as dt

def get_current_date():
    return datetime.now()

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_current_date_es():
    pass

def get_current_date_eng():
    pass

def get_only_date(date_to_format=None):
    if date_to_format:
        return date_to_format[0:10]
    return datetime.now().strftime("%Y-%m-%d")

def convert_time_to_seconds(time_format):
    return int(str(time_format).split(':')[0]) * 3600 + int(str(time_format).split(':')[1]) * 60 + int(str(time_format).split(':')[2])


