"""Network Msg."""
import json


class NetworkMsg(object):
    """Network Msg."""

    def __init__(self, sid, cid):
        """Contain sid, cid, and data."""
        self.dict = {}
        self.dict['SID'] = sid
        self.dict['CID'] = cid

    def to_json(self):
        """Turn NetworkMsg to json string."""
        return json.dumps(self.dict)


class LocalAuthMsg(NetworkMsg):
    """Local Auth msg."""
    """
    Return -1 when login failed or
    register failed.
    """
    def __init__(self, uid):
        self.dict['UserID'] = uid