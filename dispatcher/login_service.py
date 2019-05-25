"""Login Service."""
import sys
import pymongo
from dispatcher import Service
sys.path.append('./network/')
from network_msg import LocalAuthMsg


class LoginService(Service):
    """Handle login."""

    SID = 1000
    HandleLoginCmdID = 1001
    HandleRegisterCmdID = 1002

    def __init__(self):
        """Register all handle functions."""
        super(LoginService, self).__init__(self.SID)
        command_dict = {
            self.HandleLoginCmdID: self.handle_login,
            self.HandleRegisterCmdID: self.handle_register,
        }
        self.registers(command_dict)

    def handle_login(self, msg, who):
        """Handle login."""
        username = msg["UserName"]
        password = msg["Password"]
        # print 'Login data: username = ', username, ", password = ", password
        # db host and port for test
        userid_query = {"username": username, "password": password}
        # res = self.query_db(userid_query)
        # if res:
        #     userid = res["userid"]
        #     print "userid = ", userid
        #     msg = LocalAuthMsg(self.SID, self.HandleLoginCmdID, userid)
        #     who.store_to_send_buffer(msg.to_json)
        # else:
        #     print "No such user."

        # For test:
        userid = 1
        msg = LocalAuthMsg(self.SID, self.HandleLoginCmdID, userid)
        who.store_to_send_buffer(msg.to_json())

    def handle_register(self, msg, who):
        """Handle new account register."""
        username = msg["UserName"]
        password = msg["Password"]
        username_query = {"username": username}
        res = self.query_db(username_query)
        if res:  # user name exist when there is a result
            print "UserName has been used."
            return
        # insert new dict:
        # TODO: generate userid
        userid = None
        user_dict = {
            "username": username,
            "password": password,
            "userid": userid
        }
        res = self.insert_new_user_dict(user_dict)
        if res:
            print "Register new account."
        else:
            print "Register failed."

    def insert_new_user_dict(self, new_dict):
        """Insert new account dict."""
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["tpsdemo"]
        col = db["LocalAuth"]
        try:
            res = col.insert_one(new_dict)
        except:
            print "Insert new user failed."
            res = None
        return res

    def query_db(self, query):
        """Query db."""
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["tpsdemo"]
        col = db["LocalAuth"]
        try:
            res = col.find(query).limit(1)[0]
        except:
            print "Query failed."
            res = None
        return res
