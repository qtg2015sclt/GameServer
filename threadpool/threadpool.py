"""Thread Pool."""
import Queue
import time
import threading


class ThreadPool(object):
    """Thread Pool."""
    def __init__(self, maxsize=10):
        super(ThreadPool, self).__init__()
        self.maxsize = maxsize
        self._pool = Queue.Queue(maxsize)
        for _ in xrange(maxsize):
            self._pool.put(threading.Thread)

    def get_thread(self):
        return self._pool.get()

    def add_thread(self):
        self._pool.put(threading.Thread)


def run(i, pool):
    print('run ', i)
    time.sleep(1)
    pool.add_thread()


if __name__ == '__main__':
    pool = ThreadPool(5)

    for i in xrange(20):
        t = pool.get_thread()
        obj = t(target=run, args=(i, pool))
        obj.start()

    print 'active thread num: ', threading.active_count() - 1
