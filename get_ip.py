import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(s)
s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])
s.close()
