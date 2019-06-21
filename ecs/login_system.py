from component.component import LoginComponent
import worldmgr


class System(object):
    def __init__(self):
        self.components = []
        self.system_id = -1
        self.system_level = -1

    def update_entity(self):
        pass


class LoginSystem(System):
    def __init__(self):
        self.components = [LoginComponent]
        self.system_level = worldmgr.SYSTEM_COMMON_LEVEL - 3
        self.system_id = self.system_level * worldmgr.SYSTEM_LEVEL_FACTOR
        + worldmgr.generate_system_id()

    def get_attached_components(self):
        return self.components

    def update_entity(self):
        pass
