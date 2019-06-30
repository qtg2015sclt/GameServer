"""Login Component."""
import Queue
from common.singleton import singleton


class Component(object):
    """Component base."""

    def __init__(self, component_type='Component'):
        """Init Component."""
        self.component_type = component_type
        print 'Component __init__'


@singleton
class LoginComponent(Component):
    """Login Component."""

    def __init__(self):
        """Init Login Component."""
        Component.__init__(self, 'LoginComponent')
        print 'LoginComponent __init__', self
        # print self.component_type
        self.login_result_q = Queue.Queue()
