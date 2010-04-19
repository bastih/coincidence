import sys
import gc
import logging
from types import FrameType

from coincidence.timeout import timelimited

log = logging.getLogger("isolation")

class IsolationException(Exception):
    pass

class isolate(object):
    """Decorator that only runs a function within a new process"""
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        return timelimited(None, self._func, *args, **kwargs)

class isolate_from(object):
    """Decorator to isolate the execution of a function
    by a) running it in a separate process and b) making
    sure that none of the named modules have been imported
    yet, otherwhise raise an IsolationException"""

    def __init__(self, *modules):
        self.modules = modules

    def __call__(self, func=None):
        def wrapped(*args, **kwargs):
            for module in self.modules:
                if module in sys.modules:
                    referring = [obj for obj in gc.get_referrers(sys.modules[module]) if obj != sys.modules]
                    ref_frames = filter(lambda obj: isinstance(obj, FrameType), referring)
                    log.error("Where imports have happened or references are held")
                    log.error("\n".join(["%s %s %s" % (obj.f_code.co_filename,
                                                       obj.f_lineno,
                                                       obj.f_code.co_name) for obj in ref_frames]))
                    raise IsolationException("Module %s was already imported" % module)
            return timelimited(None, func, *args, **kwargs)
        return wrapped

