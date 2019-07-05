"""Login System."""
# from ..component.login_component import LoginComponent
from common.singleton import singleton
from ..worldmgr import WorldMgr


class System(object):
    """System base."""

    def __init__(self):
        """Contain components, id and level."""
        self.components = []
        self.system_id = -1
        self.system_level = -1

    def get_attached_components(self):
        """Return all components attached on this system."""
        print self.components
        return self.components

    def get_system_id(self):
        """Return id of system."""
        return self.system_id

    def update_entity(self):
        """Update the entity."""
        print 'System update_entity'


@singleton
class LoginSystem(System):
    """Login System."""

    def __init__(self):
        """Init components, level and id."""
        self.components = ['LoginComponent']
        # print self.components[0]
        self.system_level = WorldMgr.SYSTEM_COMMON_LEVEL - 3
        self.system_id = self.system_level * WorldMgr.SYSTEM_LEVEL_FACTOR
        + WorldMgr.generate_system_id()
        # print 'LoginSystem init'
        WorldMgr.add_system(self.system_id, self)

    def update_entity(self, entity):
        """Update entity."""
        # print 'LoginSystem update_entity'
        login_component = entity.get_component('LoginComponent')
        while not login_component.login_result_q.empty():
            who, msg_json = login_component.login_result_q.get()
            print msg_json
            who.store_to_send_buffer(msg_json)
