import time

from threading import Lock, currentThread
from Queue import Queue, Empty

class Scheduler(object):
    """
    Allows to control the execution of multiple threads by using
    checkpoints (named critical sections) to be able to test
    concurrent behaviour.
    """
    transition_lock = Lock()
    run_lock = Lock()
    ready = Queue(maxsize=1)
    events = []

    @classmethod
    def enter_critical(cls, name):
        """Beginning of a critical section that is marked by name"""
        while True:
            time.sleep(0.1)
            cls.transition_lock.acquire()
            try:
                #Is there a job available for immediate execution?
                try:
                    current = cls.ready.get_nowait()
                except Empty:
                    #Ready queue is empty and events is empty too: fire at will
                    if not cls.events:
                        #Also, there are no events to be scheduled
                        cls.run_lock.acquire()
                        break
                    continue
                if current != "%s_%s" % (currentThread().name, name):
                    cls.ready.put(current)
                else: # we are about to run this critical section, make sure
                      # no other thread is in their critical section
                    cls.run_lock.acquire()
                    break
            finally:
                cls.transition_lock.release()


    @classmethod
    def leave_critical(cls):
        """Leaving the critical section, others may run now"""
        cls.run_lock.release()

    @classmethod
    def schedule(cls):
        """Take control of execution by pushing new jobs into
        an empty to_run queue"""
        while cls.events:
            cls.transition_lock.acquire()
            if cls.ready.empty():
                cls.ready.put(cls.events.pop(0))
            cls.transition_lock.release()

def critical_section(func, name):
    """A decorator to for class Scheduler
    that automates the critical section behaviour"""
    def _inner(*args, **kwargs):
        Scheduler.enter_critical(name)
        try:
            return func(*args, **kwargs)
        finally:
            Scheduler.leave_critical()
    _inner.func_name = name
    return _inner