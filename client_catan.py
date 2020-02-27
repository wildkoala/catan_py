import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 4042

# connection to hostname on the port.
s.connect((host, port))

# Receive no more than 1024 bytes
msg = s.recv(4096)
print(msg.decode('ascii'))
response = input("\n> ")
s.send(response.encode('ascii'))

s.close()
