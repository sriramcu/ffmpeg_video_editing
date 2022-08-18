import sys
from tot_seconds import secs
import re

def arguments_converter(arguments):
    result = []
    dash_re = re.compile(r'(.*)-(.*)')
    for arg in arguments:
        mo = dash_re.search(arg)
        ts1 = mo.group(1)
        ts2 = mo.group(2)
        result.append(str(int(secs(ts1))) + "-" + str(int(secs(ts2))))

    return result

   
def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {__file__} 10:20-11:30 11:55-32:22 ...")
    print(" ".join(arguments_converter(sys.argv[1:])))


if __name__ == '__main__':
    main()