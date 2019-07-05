"""Database Implementation Interface and Concrete Implementation."""
# mport sys
# sys.path.append('../common/')
from pymongo import MongoClient
from pymongo import errors
from common.singleton import singleton


@singleton
class DBImplInterface(object):
    """Database Implmentation Interface."""

    def __init__(self, db_impl):
        """Init."""
        self.db_impl = db_impl

    def query_db(self, query):
        """Query database."""
        return self.db_impl.query_db(query)

    def insert_db(self, content):
        """Insert database."""
        return self.db_impl.insert_db(content)

    def connect_db(self):
        """Connect to database."""
        self.db_impl.connect_db()

    def disconnect_db(self):
        """Disconnect to database."""
        self.db_impl.disconnect_db()


@singleton
class MongoDBImpl(object):
    """Database Implementation of MongoDB."""
    def __init__(self):
        """Create a connection."""
        self.client = self.connect_db()

    def query_db(self, query):
        """Query MongoDB."""
        # db = self.client["tpsdemo"]
        db = self.client["tututu"]
        col = db["LocalAuth"]
        try:
            res = col.find(query).limit(1)[0]
            # print res
        except Exception as e:
            print "Query failed. ", e
            res = None
        # print 'mongodb', res
        return res

    def insert_db(self, new_dict):
        """Insert new dict to MongoDB."""
        db = self.client["tpsdemo"]
        col = db["LocalAuth"]
        try:
            res = col.insert_one(new_dict)
        except errors.DuplicateKeyError:
            print "Duplicate username."
            res = 0
        except Exception as e:
            print "Insert new user failed. ", e
            res = -1
        return res

    def connect_db(self):
        """Connect MongoDB."""
        # db host and port for test
        host = 'localhost'
        port = 27017
        client = MongoClient(host, port, maxPoolSize=100)
        return client

    def disconnect_db(self):
        """Disconnect DB."""
        raise NotImplementedError
