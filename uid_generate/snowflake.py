class SnowFlake(object):
    """SnowFlake: id generator."""
    def __init__(self):
        self.time_mask = 0x1ffffffffff  # 2199023255551
        self.nodeid_mask = 0x3ff  # 1023
        self.sequence_mask = 0xfff  # 4095

        # TODO: do not hardcode nodeid(machine id)?
        self.nodeid = 0
        self.seq = 0

    def next_id(self):
        """Generate next id."""
        # Get current time(ms)
        # Generate id
        raise NotImplementedError
