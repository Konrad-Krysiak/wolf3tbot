import re as RE
import socket as SO
import random

class Connection(object):
    PREFIX_LENGTH = 4
    PACKET_PREFIX = "\xff" * PREFIX_LENGTH

    def __init__(self, host, port, size=8192, timeout=1.0, retries=5):
        assert 0.1 <= timeout <= 4.0
        assert 4096 <= size <= 65536
        assert 1 <= retries <= 10
        self.socket = SO.socket(SO.AF_INET, SO.SOCK_DGRAM)
        self.socket.connect((host, port))
        self.socket.settimeout(timeout)
        self.host = host
        self.port = port
        self.size = size
        self.timeout = timeout
        self.retries = retries

    def send(self, data):
        self.socket.send("%s%s\n" % (Connection.PACKET_PREFIX, data))

    def receive(self):
        packet = self.socket.recv(self.size)
        if packet.find(Connection.PACKET_PREFIX) != 0:
            raise ConnectionError("Malformed packet")
        first_line_length = packet.find("\n")
        if first_line_length == -1:
            raise ConnectionError("Malformed packet")
        response_type = packet[Connection.PREFIX_LENGTH:first_line_length]
        response_data = packet[first_line_length+1:]
        return (response_type, response_data)

    def receive_all(self):
        packets = []
        try:
            while True:
                packet = self.receive()
                packets.append(packet)
        except SO.timeout:
            pass
        assert len(packets) > 0
        status, data = packets[0]
        for packet in packets[1:]:
            assert status == packet[0]
            data += packet[1]
        return (status, data)

    def command(self, cmd):
        retries = self.retries
        response = None
        while retries > 0:
            self.send(cmd)
            try:
                response = self.receive_all()
            except Exception:
                retries -= 1
            else:
                return response
        raise ConnectionError("No response after %d attempts." % self.retries)

    def close(self):
        """Close connection."""
        self.socket.close()

def filter_name(name):
	result = ""
	i = 0
	while i < len(name):
	    if name[i] == "^":
	        i += 2
	    else:
	        result += name[i]
	        i += 1
	return result

def connect_to_server():
    c = Connection("176.57.142.251", 27960) #nd
    #c = Connection("62.67.42.200", 27960) #os
    #c = Connection("vietnam.twcclan.org", 27960) #vietnam
    #c = Connection("193.192.59.195", 27960) #tj
    #c = Connection("193.192.59.165", 27960) #bg
    #c = Connection("176.57.129.78", 27960) #pw
    #c = Connection("193.192.59.195", 27960) #hs
    #c = Connection("vietnam.twcclan.org", 27960)
    #c = Connection("sniper.twcclan.org", 27960)
    #c = Connection("etpro.twcclan.org", 27960) #twc.etpro
    status = c.command("getstatus")
    assert len(status) > 0
    return status
    c.close()

def get_color_names():
	data = connect_to_server()
	statusResponse, data = data
	nickList = RE.findall(r'"(.*?)"', data)
	return nickList

def get_names():
    data = get_color_names()
    nickList = list()    
    for nick in data:
        nickList.append(filter_name(nick))
    return nickList
# while True:
#     try:
#         print connect_to_server()
#         easygui.msgbox("SERVER ON", title="Server Status")
#         break
#     except:
#         print "Server is down at " + time.strftime("%Y-%m-%d %H:%M:%S.", time.gmtime())
#     time.sleep(10)
