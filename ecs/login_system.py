from component.login_component import LoginComponent
import worldmgr


class System(object):
    def __init__(self):
        self.components = []
        self.system_id = -1
        self.system_level = -1

    def get_attached_components(self):
        return self.components

    def get_system_id(self):
        return self.system_id

    def update_entity(self):
        print 'System update_entity'


class LoginSystem(System):
    def __init__(self):
        self.components = [LoginComponent.__class__]
        self.system_level = worldmgr.SYSTEM_COMMON_LEVEL - 3
        self.system_id = self.system_level * worldmgr.SYSTEM_LEVEL_FACTOR
        + worldmgr.generate_system_id()

    def update_entity(self, entity):
        print 'LoginSystem update_entity'
        login_component = entity.get_component(LoginComponent.__class__)
        while not login_component.login_result_q.empty():
            who, msg_json = login_component.login_result_q.get()
            print msg_json
            who.store_to_send_buffer(msg_json)
