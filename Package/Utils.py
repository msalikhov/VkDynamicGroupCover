import datetime
import time


def print_data(*data):
    date = datetime.datetime.now().time()
    print(date, data)


def sleep(secs):
    for x in range(secs):
        print('sleeping, secs: %d/%d' % (x, secs), end="\r")
        time.sleep(1)
