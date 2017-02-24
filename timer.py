import time
from functools import wraps


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total_time = '{}'.format(end - start)
        result["time_to_complete"] = total_time
        print("{} data retrieval time: {}".format(result["site_name"], total_time))
        return result
    return wrapper


def timeprogram(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total_time = '{}'.format(end - start)
        result["time_to_complete"] = total_time
        print("{} data retrieval time: {}".format(result["site_name"], total_time))
        return result
    return wrapper
