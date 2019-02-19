import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(s)
s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])
s.close()
print(socket.gethostname())
print(socket.gethostbyaddr('172.30.20.299'))
