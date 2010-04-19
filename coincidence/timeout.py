import sys

from multiprocessing import Process, Queue
from Queue import Empty

class TimeoutException(Exception):
    """Exception used to notify when timeout expires"""

def runner(result, func, *args, **kwargs):
    """Runs the given function and returns the result:
        (True, <payload>) in case of a function that returned correctly
                            payload is return value
        (False, <payload>) in case of an exception
                            payload is exception
    """
    try:
        result.put((True, func(*args, **kwargs)))
    except Exception:
        result.put((False, sys.exc_info()[1]))

def timelimited(timeout, func, *args, **kwargs):
    """Forces a function to terminate after timeout seconds"""
    results = Queue(1)
    limited_process = Process(target=runner,
                              args=(results, func) + args,
                              kwargs=kwargs)
    limited_process.start()
    try:
        status, result = results.get(timeout=timeout)
    except Empty:
        limited_process.terminate()
        raise TimeoutException("The function exceeded its time limit")
    limited_process.join()
    if status:
        return result
    else:
        raise result


