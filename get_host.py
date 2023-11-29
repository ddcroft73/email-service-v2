'''
This module is used to get the host IP so I know what to connect to from my other computer on the 
network.
'''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])

s.close()