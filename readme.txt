Application Name
================
multicast_to_unicast


Application Version
===================
0.1


NCOS Devices Supported
======================
ALL


External Requirements
=====================
- Multicast udp stream to subscribe to
- Unicast udp destination to send to


Application Purpose
===================
This application will monitor a specified UDP multicast stream
and rebroadcast it to a specified unicast destination


Expected Output
===============
A message is generated each time a UDP datagram is received.
In production, this should probably be commented out.

