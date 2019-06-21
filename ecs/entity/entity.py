from worldmgr import WorldMgr


class Entity(object):
    def __init__(self):
        self.entity_id = WorldMgr.generate_entity_id()
        self.components = {}
        WorldMgr.add_entity(self)

    def destroy(self):
        WorldMgr.remove_entity(self)

    def get_component(component):
        raise NotImplementedError

    def add_component(component):
        raise NotImplementedError

    def remove_component(component):
        raise NotImplementedError

    def has_component(component):
        raise NotImplementedError
