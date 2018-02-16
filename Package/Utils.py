import datetime
import time


def print_data(*data):
    date = datetime.datetime.now().time()
    print(date, data)


def sleep(secs, ident):
    for x in range(secs):
        if x % 10 == 0:
            print("id:", ident, "sleeping %d/%d" % (x, secs))

        time.sleep(1)
