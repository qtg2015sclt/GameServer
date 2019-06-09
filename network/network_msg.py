"""Network Msg."""
import json


class NetworkMsg(object):
    """Network Msg."""

    def __init__(self, sid, cid):
        """Network Msg base."""
        super(NetworkMsg, self).__init__()
        self.dict = {}
        self.dict['SID'] = sid
        self.dict['CID'] = cid

    def to_json(self):
        """Turn NetworkMsg to json string."""
        return json.dumps(self.dict)


class LocalAuthMsg(NetworkMsg):
    """Local Auth Msg."""

    """
    Return -1 when login failed or
    register failed.
    """
    def __init__(self, sid, cid, uid, username=None, password=None):
        """Contain userid."""
        super(LocalAuthMsg, self).__init__(sid, cid)
        # key(such as 'UserID') should match the client LocalAuthMsg.
        self.dict['UserID'] = uid
        self.dict['UserName'] = username
        self.dict['Password'] = password
