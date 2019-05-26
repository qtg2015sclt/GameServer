"""Database Implementation Interface and Concrete Implementation."""
import pymongo


class DBImplInterface(object):
    """Database Implmentation Interface."""

    def __init__(self, db_impl):
        """Init."""
        super(DBImplInterface, self).__init__()
        self.db_impl = db_impl

    def query_db(self, query):
        """Query database."""
        self.db_impl.query_db(query)

    def insert_db(self, content):
        """Insert database."""
        self.db_impl.insert_db(content)

    def connect_db(self):
        """Connect to database."""
        self.db_impl.connect_db()

    def disconnect_db(self):
        """Disconnect to database."""
        self.db_impl.disconnect_db()


class MongoDBImpl(object):
    """Database Implementation of MongoDB."""

    def query_db(self, query):
        """Query MongoDB."""
        col = self.connect_db()
        try:
            res = col.find(query).limit(1)[0]
        except:
            print "Query failed."
            res = None
        return res

    def insert_db(self, new_dict):
        """Insert new dict to MongoDB."""
        col = self.connect_db()
        try:
            res = col.insert_one(new_dict)
        except:
            print "Insert new user failed."
            res = None
        return res

    def connect_db(self):
        """Connect MongoDB."""
        # db host and port for test
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["tpsdemo"]
        collection = db["LocalAuth"]
        return collection

    def disconnect_db(self):
        """Disconnect DB."""
        raise NotImplementedError
