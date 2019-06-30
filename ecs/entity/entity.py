"""Entity."""
from ..worldmgr import WorldMgr
from ..component.login_component import LoginComponent


class Entity(object):
    """Entity base."""

    def __init__(self):
        """Contain entity_id, components. Add self to WorldMgr."""
        self.entity_id = WorldMgr.generate_entity_id()
        self.components = []
        WorldMgr.add_entity(self)

    def destroy(self):
        """Destroy a entity should remove it from WorldMgr."""
        WorldMgr.remove_entity(self)

    def get_component(self, component_type):
        for component in self.components:
            if component.component_type == component_type:
                return component
        print 'Error: No such component in the entity.'

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        self.components.remove(component)

    def has_component(self, component_type):
        return component_type in\
            [component.component_type for component in self.components]


class SingletonMgrEntity(Entity):
    def __init__(self):
        super(SingletonMgrEntity, self).__init__()
        self.components.append(LoginComponent())
