from csclient import EventingCSClient
import socket
import struct

cp = EventingCSClient('multicast_to_unicast')

'''
MODIFY THESE VARIABLES TO MATCH YOUR ENVIRONMENT
'''

MCAST_GRP = '224.1.1.1' # Multicast group to listen on
MCAST_PORT = 5001 # Multicast port to listen on
MCAST_LISTEN_IP = '192.168.0.1' # Cradlepoint interface IP address to listen on

UCAST_DST_IP = '192.168.0.125' #Unicast destination to
UCAST_DST_PORT = 5002

'''
DO NOT CHANGE ANYTHING BELOW
'''

cp.log("APP STARTED")

s = socket.socket(type=socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError:
    pass
s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

s.bind(('',MCAST_PORT))

intf = MCAST_LISTEN_IP
s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton(intf))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

s2 = socket.socket(type=socket.SOCK_DGRAM)

while True:
    data, addr = s.recvfrom(10240)
    # cp.log(data)
    cp.log('Packet received from {}. Forwarding to: {}'.format(addr, UCAST_DST_IP))
    s2.sendto(data, (UCAST_DST_IP, UCAST_DST_PORT))
