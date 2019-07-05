"""Thread Pool."""
import Queue
# import time
import threading
import contextlib
# import sys
# sys.path.append('../common')
# from singleton import singleton
from common.singleton import singleton


StopEvent = object()

# For test:
# def callback(status, result, arg):
#     """
#     :param status: running status of action function
#     :param result: result return from action function
#     """
#     print('%s task callback' % (arg + 1))


# def action(arg):
#     """
#     Real task definition.
#     :param thread_name: name of thread that run this action
#     :param arg: argument the action need
#     """
#     time.sleep(0.1)
#     print('%s task run thread' % (arg + 1))


@singleton
class ThreadPool(object):
    """Thread Pool."""
    def __init__(self, maxsize=5, max_task_size=None):
        """
        :param maxsize: max size of threads num
        :param max_task_size: task queue length
        """
        if max_task_size:
            self.q = Queue.Queue(max_task_size)
        else:
            self.q = Queue.Queue()

        self.maxsize = maxsize
        self.cancel = False
        self.terminal = False
        self.generate_thread_list = []
        self.free_thread_list = []

    def put(self, func, args, callback=None, callback_args=None):
        """Put a task in task queue.
        :param func: task function
        :param args: arguments task need
        :param callback: callback after task success of fail
        :return: if threadpool is end return True or return None
        """
        if self.cancel:
            return
        if len(self.free_thread_list) == 0\
                and len(self.generate_thread_list) < self.maxsize:
            print 'ThreadPool put: not enough free thread, generate new one.'
            self.generate_thread()
        self.q.put((func, args, callback, callback_args))

    def generate_thread(self):
        """Generate a thread."""
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        """Get and run task function."""
        cur_thread = threading.currentThread().getName()
        self.generate_thread_list.append(cur_thread)
        event = self.q.get()
        while event != StopEvent:
            func, args, callback, callback_args = event
            try:
                result = func(*args)
                success = True
            except Exception as e:
                result = None
                success = False
            if callback is not None:
                try:
                    callback(success, result, *callback_args)
                except Exception as e:
                    print e
            with self.worker_state(self.free_thread_list, cur_thread):
                if self.terminal:
                    event = StopEvent
                else:
                    # print 'ThreadPool call: finish task, try get new one.'
                    event = self.q.get()
                    # print 'ThreadPool call: get new task.'
        else:
            self.generate_thread_list.remove(cur_thread)

    def close(self):
        """After running all tasks, stop all threads."""
        self.cancel = True
        full_size = len(self.generate_thread_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        """When running tasks, terminate threads and return."""
        self.terminal = True
        while self.generate_thread_list:
            self.q.put(StopEvent)

    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """Log free thread, or get free thread to run task"""
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)


# if __name__ == '__main__':
#     pool = ThreadPool(5)
#     for i in xrange(100):
#         pool.put(action, (i,), callback, (i,))
#     time.sleep(3)
#     print('-' * 50)
#     print('\033[before tasks cancelled, there\'s %s thread,\
#         %s free thread.\033[' % (len(pool.generate_thread_list),
#                                  len(pool.free_thread_list)))
#     pool.close()
#     print 'tasks succeeded and quit.'


# Simple version
# class SimpleThreadPool(object):
#     """Simple Thread Pool."""
#     def __init__(self, maxsize=10):
#         super(ThreadPool, self).__init__()
#         self.maxsize = maxsize
#         self._pool = Queue.Queue(maxsize)
#         for _ in xrange(maxsize):
#             self._pool.put(threading.Thread)

#     def get_thread(self):
#         return self._pool.get()

#     def add_thread(self):
#         self._pool.put(threading.Thread)


# def run(i, pool):
#     print('run ', i)
#     time.sleep(1)
#     pool.add_thread()


# if __name__ == '__main__':
#     pool = SimpleThreadPool(5)

#     for i in xrange(20):
#         t = pool.get_thread()
#         obj = t(target=run, args=(i, pool))
#         obj.start()

#     print 'active thread num: ', threading.active_count() - 1
