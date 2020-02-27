import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 4044

# connection to hostname on the port.
s.connect((host, port))

def catan_print(conn, given_str):
    conn.send(given_str.encode('ascii'))
    return

def catan_read(conn, size=1024):
    s = conn.recv(size).decode('ascii')
    return s





welcome_msg = s.recv(4096)
print(welcome_msg.decode('ascii'))

#Answer "1"
response = input("> ")
s.send(response.encode('ascii'))

# number of players
server_data = catan_read(s)
print(server_data)
response = input("> ")
catan_print(s, response)

#player 1 name
server_data = catan_read(s)
print(server_data)
response = input("> ")
catan_print(s, response)

#player 1 color
server_data = catan_read(s)
print(server_data)
response = input("> ")
catan_print(s, response)


#player 2 name
server_data = catan_read(s)
print(server_data)
response = input("> ")
catan_print(s, response)

#player 2 color
server_data = catan_read(s)
print(server_data)
response = input("> ")
catan_print(s, response)








s.close()
