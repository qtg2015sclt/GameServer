import Queue
from common.singleton import singleton


@singleton
class Component(object):
    def __init__(self):
        print 'Component'


class LoginComponent(Component):
    def __init__(self):
        print 'LoginComponet', self
        self.login_result_q = Queue.Queue()
