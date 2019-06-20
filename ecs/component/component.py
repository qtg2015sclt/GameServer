import Queue


class component(object):
    def __init__(self):
        pass


class login_component(component):
    def __init__(self):
        self.login_result_q = Queue.Queue()
