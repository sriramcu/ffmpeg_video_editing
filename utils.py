import sys
import time
import datetime

import re

def time_intervals_converter(time_intervals) -> list:
    """
    Parameters:
    -----------
    arguments: list
        List of time intervals in the format ["10:20-11:30", "715-32:22", ...]
    Returns:
        List of time intervals in the format ["620-690", "1350-1942", ...]
    """
    result = []
    dash_re = re.compile(r'(.*)-(.*)')
    for arg in time_intervals:
        mo = dash_re.search(arg)
        start_timestamp = mo.group(1)
        end_timestamp = mo.group(2)
        result.append(str(int(full_time_string_to_seconds(start_timestamp))) + "-" + str(int(full_time_string_to_seconds(end_timestamp))))

    return result


def parse_time(time_str):
    # Try parsing with '%H:%M:%S'
    try:
        return time.strptime(time_str, '%H:%M:%S')
    except ValueError:
        pass
    # If the first format fails, try '%M:%S'
    try:
        return time.strptime(time_str, '%M:%S')
    except ValueError:
        raise ValueError(f"Time format for '{time_str}' is not supported.")


def full_time_string_to_seconds(time_str: str):
    """
    Parameters:
    A time string in the format HH:MM:SS or MM:SS
    Returns:
    The time in seconds
    """
    time_obj = parse_time(time_str)
    try:
        seconds = datetime.timedelta(hours=time_obj.tm_hour,minutes=time_obj.tm_min,seconds=time_obj.tm_sec).total_seconds()
    except AttributeError:
        seconds = datetime.timedelta(minutes=time_obj.tm_min,seconds=time_obj.tm_sec).total_seconds()
    return seconds


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {__file__} 10:20-11:30 11:55-32:22 ...")
        return
    print(" ".join(time_intervals_converter(sys.argv[1:])))


if __name__ == '__main__':
    main()