#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import random
import time
from threadpool.threadpool import ThreadPool
from network.network_msg import LocalAuthMsg
from dispatcher.login_service import LoginService


def test_for_client():
    """A function to test."""


def queryAction4Test(sock):
    i = random.randint(1, 7)
    username = 'test' + str(i)
    password = 'test'

    msg = LocalAuthMsg(
        LoginService.SID,
        LoginService.HandleLoginCmdID,
        0,
        username,
        password
    )
    print 'send: ', msg.to_json()
    sock.sendall(msg.to_json() + '\n')


def setup_network(host, port):
    # print 'setup_network start'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.setblocking(0)
    sock.settimeout(0.01)
    sock.connect((host, port))
    # print 'setup_network ', sock
    return sock


if '__main__' == __name__:
    # host = '10.251.40.248'
    host = socket.gethostname()
    port = 57890
    sock = setup_network(host, port)
    threadpool = ThreadPool()
    # print threadpool
    try:
        while True:
            for i in xrange(2):
                threadpool.put(queryAction4Test, (sock,))
                # queryAction4Test(sock)
            for _ in xrange(10):
                data = ''
                try:
                    data = sock.recv(4096)
                except:
                    pass
                if data != '':
                    print 'recieve: ', data
            time.sleep(1)
    except KeyboardInterrupt:
            sock.close()
            threadpool.close()
