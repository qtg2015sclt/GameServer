"""Network Msg."""
import json


class NetworkMsg(object):
    """Network Msg."""

    def __init__(self, sid=None, cid=None, data=None):
        """Contain sid, cid, and data."""
        self.sid = sid
        self.cid = cid
        self.data = data

    def dict2networkmsg(self, d):
        """Turn dict to NetworkMsg."""
        return NetworkMsg(d.get('SID'), d.get('CID'), d.get('Data'))

    def networkmsg2dict(self):
        """Turn NetworkMsg to dict."""
        return {
            'SID': self.sid,
            'CID': self.cid,
            'Data': self.data
        }

    def json_string(self):
        """Turn NetworkMsg to json string."""
        return json.dumps(self.networkmsg2dict())
