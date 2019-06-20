from component import login_component


class system(object):
    def __init__(self):
        self.components = []
        self.system_id = -1
        self.system_level = -1

    def update_entity(self):
        pass


class login_system(system):
    def __init__(self):
        self.components.append(login_component)

    def update_entity(self):
        pass
