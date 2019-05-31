"""Database Manager."""
import sys
from db_impl_interface import DBImplInterface, MongoDBImpl
sys.path.append('../common')
from singleton import singleton


@singleton
class DBMgr(object):
    """Database Manager."""

    def __init__(self):
        """Init."""

    def query_db(self, query):
        """Query DB."""
        # Test:
        # for i in xrange(5):
        #     db = DBImplInterface(MongoDBImpl())
        #     print db
        db = DBImplInterface(MongoDBImpl())
        res = db.query_db(query)
        return res

    def insert_db(self, new_dict):
        """Insert new dict to db."""
        db = DBImplInterface(MongoDBImpl())
        res = db.insert_db(new_dict)
        return res


# Test:
# if __name__ == '__main__':
#     # for i in xrange(5):
#     #     dbmgr = DBMgr()
#     #     print dbmgr
#     #     new_dict = {"test": "just a test"}
#     #     dbmgr.query_db(new_dict)
#     dbmgr = DBMgr()
#     new_dict = {"test": "just a test"}
#     dbmgr.query_db(new_dict)