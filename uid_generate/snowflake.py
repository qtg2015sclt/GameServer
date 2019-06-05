import time


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
        cur_t = time.time()
        timestamp = int(round(cur_t * 1000))
        # Generate id
        new_id = (timestamp & self.time_mask) << 22\
            | (self.nodeid & self.nodeid_mask) << 12\
            | self.seq
        self.seq = (self.seq + 1) & self.sequence_mask
        return new_id

    # def parse(self, id_need_parse):
    #     timestamp = (id_need_parse >> 22)
    #     nodeid = (id_need_parse >> 12) & self.nodeid_mask
    #     seq = id_need_parse & self.sequence_mask
    #     return (timestamp, nodeid, seq)


# For test:
if __name__ == '__main__':
    start_time = time.time()
    snowflake = SnowFlake()
    for i in xrange(10):
        uid = snowflake.next_id()
        print i, uid
    end_time = time.time()
    last_time = end_time - start_time
    print 'Generate 1000 uid cost ', last_time, 's'
