"""Login Service."""
from dispatcher import Service
# import sys
# sys.path.append('./network/')
# sys.path.append('./dbmgr/')
# from network_msg import LocalAuthMsg
# from dbmgr import DBMgr
from network.network_msg import LocalAuthMsg
from dbmgr.dbmgr import DBMgr
from threadpool.threadpool import ThreadPool


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
        dbmgr = DBMgr()
        # res = dbmgr.query_db(userid_query)
        pool = ThreadPool()
        pool.put(dbmgr.query_db,
                 (userid_query,),
                 self.handle_login_callback,
                 (who,)
                 )
        # print 'login service', res
        # if res:
        #     userid = res["userid"]
        #     print "login userid = ", userid
        # else:
        #     print "No such user."
        #     userid = 0
        # msg = LocalAuthMsg(self.SID, self.HandleLoginCmdID, userid)
        # who.store_to_send_buffer(msg.to_json())

        # For test:
        # userid > 0 => valid username and password
        # userid == 0 => invalid username and password
        # userid == -1 => login failed
        # userid = 0
        # msg = LocalAuthMsg(self.SID, self.HandleLoginCmdID, userid)
        # who.store_to_send_buffer(msg.to_json())

    def handle_login_callback(self, status, result, who):
        """Callback after database operation."""
        if status:
            if result:
                userid = result["userid"]
                print "Login userid = ", userid
            else:
                print "No such user."
                userid = 0
        else:
            print "Login failed."
            userid = -1
        msg = LocalAuthMsg(self.SID, self.HandleLoginCmdID, userid)
        who.store_to_send_buffer(msg.to_json())

    def handle_register(self, msg, who):
        """Handle new account register."""
        username = msg["UserName"]
        password = msg["Password"]
        # TODO: should not make concrete query here
        username_query = {"username": username}
        dbmgr = DBMgr()
        res = dbmgr.query_db(username_query)
        if res:  # user name exist when there is a result
            print "UserName has been used."
            userid = 0
            msg = LocalAuthMsg(self.SID, self.HandleRegisterCmdID, userid)
            who.store_to_send_buffer(msg.to_json())
            return
        # insert new dict:
        # TODO: generate userid
        userid = None
        user_dict = {
            "username": username,
            "password": password,
            "userid": userid
        }
        res = dbmgr.insert_db(user_dict)
        if res:
            print "Register new account."
        else:
            userid = -1
            print "Register failed."
        msg = LocalAuthMsg(self.SID, self.HandleRegisterCmdID, userid)
        who.store_to_send_buffer(msg.to_json())

        # For test
        # userid > 0 => valid username and password
        # userid == 0 => username exist
        # userid == -1 => register failed
        # userid = 1
        # msg = LocalAuthMsg(self.SID, self.HandleRegisterCmdID, userid)
        # who.store_to_send_buffer(msg.to_json())
