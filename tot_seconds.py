import datetime
import time
import sys
def secs(s):
    x = time.strptime("00:"+s,'%H:%M:%S')
    return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()


if __name__ == '__main__':
    print(secs(sys.argv[1]))
