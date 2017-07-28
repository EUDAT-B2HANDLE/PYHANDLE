import time

def generate_timestamp():
    '''
    This generates unix time when creating Handle values in the database.
    :return: ts: The current unix timestamp (example: 1483225200: 01/01/2017 00:00:00)
    '''

    ts = int(time.time())
    return ts

def generate_timestamp_for_date(date):
    '''
    This generates unix time when quering handles values by date.
    Date format example: 01/01/2017 00:00:00
    :param date: The date that will be converted to unix timestamp
    :return: ts: Timestampe corresponding to "date"
    '''

    #ts = int(datetime.datetime.strptime(date, "%d/%m/%Y %X").timestamp())
    ts = time.mktime(time.strptime(date, "%d/%m/%Y %X"))

    return ts



