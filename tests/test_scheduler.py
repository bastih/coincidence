import unittest2
from Queue import Queue
from threading import Thread, currentThread

from coincidence.scheduler import Scheduler
from coincidence.timeout import timelimited
from coincidence.utils import intermerge

def threaded(queue):
    Scheduler.enter_critical("a")
    queue.put("%s_%s" % (currentThread().name, "a"))
    Scheduler.leave_critical()

    Scheduler.enter_critical("b")
    queue.put("%s_%s" % (currentThread().name, "b"))
    Scheduler.leave_critical()

class SchedulerTestCase(unittest2.TestCase):

    def scheduler_basic(self, procs=2, events=None):
        threads = []
        q = Queue()
        for num in range(procs):
            thread = Thread(target=threaded, args=(q,))
            thread.name = num
            threads.append(thread)

        Scheduler.events = list(events)
        [t.start() for t in threads]
        Scheduler.schedule()
        [t.join() for t in threads]

        result = []
        while not q.empty():
            result.append(q.get())

        return result

    def test_scheduler_example(self):
        procs = 2
        streams = [["%s_a" % n, "%s_b" % n] for n in range(procs)]
        for events in intermerge(*streams):
            result = timelimited(2, self.scheduler_basic, procs, events)
            self.assertEqual(events, result)

    def test_scheduler_early_exhaustion(self):
        procs = 2
        streams = [["%s_a" % n, "%s_b" % n] for n in range(procs)]
        for events in intermerge(*streams):
            result = timelimited(2, self.scheduler_basic, procs, events[:len(events)/2])
            self.assertEqual(events[:len(events)/2], result[:len(events)/2])
            self.assertEqual(sorted(events), sorted(result))
