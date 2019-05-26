"""Database Manager."""
from db_impl_interface import DBImplInterface, MongoDBImpl


def singleton(cls, *arg, **kw):
    """A singleton decorator."""
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*arg, **kw)
        return instances[cls]
    return _singleton


@singleton
class DBMgr(object):
    """Database Manager."""

    def __init__(self):
        """Init."""
        super(DBMgr, self).__init__()

    def query_db(self, query):
        """Query DB."""
        db = DBImplInterface(MongoDBImpl())
        res = db.query_db(query)
        return res

    def insert_db(self, new_dict):
        """Insert new dict to db."""
        db = DBImplInterface(MongoDBImpl())
        res = db.insert_db(new_dict)
        return res
