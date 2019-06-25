from worldmgr import WorldMgr


class Entity(object):
    def __init__(self):
        self.entity_id = WorldMgr.generate_entity_id()
        self.components = []
        WorldMgr.add_entity(self)

    def destroy(self):
        WorldMgr.remove_entity(self)

    def get_component(self, component_type):
        for component in self.components:
            if component.__class__ == component_type:
                return component
        print 'Error: No such component in the entity.'

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        self.components.remove(component)

    def has_component(self, component_type):
        return component_type in\
            [component.__class__ for component in self.components]
