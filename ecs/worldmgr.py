import Queue
from system.login_system import LoginSystem


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


def init():
    login_system = LoginSystem()
    system_dict[login_system.system_id] = login_system
    # TODO: sort system_dict
    for system in system_dict.itervalues():
        system_entity_match_dict[system.system_id] = set()


def update_all():
    update_entity_dict()
    for system in system_dict.itervalues():
        do_update(system.update_entity, system.system_id)


def add_entity(entity):
    entity_add_queue.put(entity)


def remove_entity(entity):
    entity_remove_queue.put(entity)


def update_entity_dict():
    for system in system_dict.itervalues():
        while not entity_add_queue.empty():
            entity = entity_add_queue.get()
            do_add_entity(entity)

        while not entity_remove_queue.empty():
            entity = entity_remove_queue.get()
            do_remove_entity(entity)


def do_add_entity(entity):
    if not entity_dict.get(entity.entity_id):
        entity_dict[entity.entity_id] = entity


def do_remove_entity(entity):

def generate_system_id():
    global system_count
    global system_id_record
    system_count += 1
    system_id_record += 1
    return system_id_record


def generate_entity_id():
    global entity_count
    global entity_id_record
    entity_count += 1
    entity_id_record += 1
    return entity_id_record


def clear_world_mgr_state():
    pass


def do_update(func, system_id):
    if system_entity_match_dict.get(system_id) is None:
        return
    for entity_id in system_entity_match_dict[system_id]:
        func(entity_dict[entity_id])
