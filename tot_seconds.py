import datetime
import time
import sys


def secs(s):
    x = time.strptime("00:"+s,'%H:%M:%S')
    return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()


def main():
    if len(sys.argv)<2:
        print(f"Usage: python3 {__file__} <time in mm:ss example 01:33 gives 93 as output>")
    print(secs(sys.argv[1]))


if __name__ == '__main__':
    main()
    
    
