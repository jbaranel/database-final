from random import randrange
from datetime import timedelta, datetime

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def get_dates():
    d1 = datetime.strptime('1/1/2021 00:00', '%m/%d/%Y %H:%M')
    d2 = datetime.strptime('12/1/2021 00:00', '%m/%d/%Y %H:%M')

    for i in range(100):
        print(random_date(d1, d2))