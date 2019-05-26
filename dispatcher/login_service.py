"""Login Service."""
import sys
from dispatcher import Service
sys.path.append('./network/')
from network_msg import LocalAuthMsg
sys.path.append('./dbmgr/')
from dbmgr import DBMgr


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
        # TODO: should not make concrete query here
        userid_query = {"username": username, "password": password}
        # dbmgr = DBMgr()
        # res = dbmgr.query_db(userid_query)
        # if res:
        #     userid = res["userid"]
        #     print "userid = ", userid
        #     msg = LocalAuthMsg(self.SID, self.HandleLoginCmdID, userid)
        #     who.store_to_send_buffer(msg.to_json)
        # else:
        #     print "No such user."

        # For test:
        # userid > 0 => valid username and password
        # userid == -1 => invalid username and password
        userid = -1
        msg = LocalAuthMsg(self.SID, self.HandleLoginCmdID, userid)
        who.store_to_send_buffer(msg.to_json())

    def handle_register(self, msg, who):
        """Handle new account register."""
        username = msg["UserName"]
        password = msg["Password"]
        # TODO: should not make concrete query here
        username_query = {"username": username}
        # dbmgr = DBMgr()
        # res = dbmgr.query_db(username_query)
        # if res:  # user name exist when there is a result
        #     print "UserName has been used."
        #     return
        # # insert new dict:
        # # TODO: generate userid
        # userid = None
        # user_dict = {
        #     "username": username,
        #     "password": password,
        #     "userid": userid
        # }
        # res = dbmgr.insert_db(user_dict)
        # if res:
        #     print "Register new account."
        # else:
        #     print "Register failed."
        # For test
        # userid > 0 => valid username and password
        # userid == 0 => username exist
        # userid == -1 => register failed
        userid = 1
        msg = LocalAuthMsg(self.SID, self.HandleRegisterCmdID, userid)
        who.store_to_send_buffer(msg.to_json())
