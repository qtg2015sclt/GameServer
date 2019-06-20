from worldmgr import WorldMgr


class Entity(object):
	def __init__(self):
		self.entity_id = WorldMgr.generate_entity_id()
		WorldMgr.add_entity(self)
		
	def destroy(self):
		WorldMgr.remove_entity(self)