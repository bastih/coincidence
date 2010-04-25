import sys
import gc
import logging
from types import FrameType

from coincidence.timeout import timelimited

log = logging.getLogger("isolation")

def already_imported(*modules):
    return [module for module in modules if module in sys.modules]

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

    def __init__(self, *modules, **kwargs):
        """Isolate a function from specific imports

        modules list of modules that are not allowed
            to be present at the point of execution.

        spawn_process boolean optional run this function inside its
            own process, protecting the host process from import side effects
        """
        print modules
        self.modules = modules
        self.spawn_process = kwargs.get('spawn_process', True)

    def __call__(self, func=None):
        def wrapped(*args, **kwargs):
            modules = already_imported(*self.modules)
            if modules:
                raise IsolationException(
                        "Module %s was already imported" % ', '.join(modules))
            if self.spawn_process:
                return timelimited(None, func, *args, **kwargs)
            else:
                return func(*args, **kwargs)
            
        return wrapped

