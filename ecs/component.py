import Queue


class Component(object):
    def __init__(self):
        pass


class LoginComponent(Component):
    def __init__(self):
        self.login_result_q = Queue.Queue()
