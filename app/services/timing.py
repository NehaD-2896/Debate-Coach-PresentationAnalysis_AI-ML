import time


def timed_call(fn, *args, **kwargs):
    started = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, int((time.perf_counter() - started) * 1000)
