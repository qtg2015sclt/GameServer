import Queue


class WorldMgr(object):
    """World Manager."""
    SYSTEM_LEVEL_FACTOR = 100
    SYSTEM_COMMON_LEVEL = 5
    entity_count = 0
    system_count = 0
    entity_id_record = 0
    system_id_record = 0
    system_dict = {}
    entity_dict = {}
    entity_add_queue = Queue.Queue()
    entity_remove_queue = Queue.Queue()
    system_entity_match_dict = {}

    def __init__(self):
        # TODO: sort system_dict
        for system in self.system_dict.itervalues():
            # print system.system_id
            self.system_entity_match_dict[system.system_id] = set()

    def update_all(self):
        # print 'WorldMgr update_all'
        self.update_entity_dict()
        for system in self.system_dict.itervalues():
            # print system.__class__
            self.do_update(system.update_entity, system.system_id)

    @classmethod
    def add_system(cls, system_id, system):
        cls.system_dict[system_id] = system

    @classmethod
    def add_entity(cls, entity):
        # print entity.__class__
        cls.entity_add_queue.put(entity)

    @classmethod
    def remove_entity(cls, entity):
        cls.entity_remove_queue.put(entity)

    @classmethod
    def generate_system_id(cls):
        cls.system_count += 1
        cls.system_id_record += 1
        return cls.system_id_record

    @classmethod
    def generate_entity_id(cls):
        cls.entity_count += 1
        cls.entity_id_record += 1
        return cls.entity_id_record

    @classmethod
    def clear_world_mgr_state(cls):
        raise NotImplementedError

# private:

    def update_entity_dict(self):
        for system in self.system_dict.itervalues():
            while not self.entity_add_queue.empty():
                entity = self.entity_add_queue.get()
                # print entity.__class__
                self.do_add_entity(entity)

            while not self.entity_remove_queue.empty():
                entity = self.entity_remove_queue.get()
                self.do_remove_entity(entity)

    @classmethod
    def do_update(cls, func, system_id):
        if cls.system_entity_match_dict.get(system_id) is None:
            # print system_id
            return
        for entity_id in cls.system_entity_match_dict[system_id]:
            func(cls.entity_dict[entity_id])

    @classmethod
    def do_add_entity(cls, entity):
        if not cls.entity_dict.get(entity.entity_id):
            # print entity.entity_id
            cls.entity_dict[entity.entity_id] = entity
            cls.do_match_entity(entity)

    @classmethod
    def do_remove_entity(cls, entity):
        if cls.entity_dict.get(entity.entity_id):
            del cls.entity_dict[entity.entity_id]
            cls.remove_entity_match()

    @classmethod
    def do_match_entity(cls, entity):
        cls.remove_entity_match(entity)
        for system in cls.system_dict.itervalues():
            if cls.match_components(entity, system.get_attached_components()):
                cls.system_entity_match_dict[system.system_id]\
                    .add(entity.entity_id)

    @classmethod
    def remove_entity_match(cls, entity):
        for system in cls.system_dict.itervalues():
            if cls.system_entity_match_dict.get(system.system_id) is None:
                # print system.system_id
                return
            cls.system_entity_match_dict[system.system_id]\
                .discard(entity.entity_id)

    @classmethod
    def match_components(cls, entity, components):
        for component in components:
            # print component
            if not entity.has_component(component):
                return False
        return True
