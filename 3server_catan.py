#========================================================
#FILE PURPOSE:
#  - Allows for creation of a server that supports single and multiplayer Catan
#========================================================


#========================================================
#BUG SECTION:
#========================================================

#========================================================
# Requirements and Exports
#========================================================
import catan_classes
import socket
import threading


#========================================================
# FUNCTION DECLARATIONS
#========================================================
single_player_games = []
game_lobbies = [[]] # list of lists, where each list represents a lobby that contains the connections for a particular game.

def choose_mode(conn):
    global single_player_games
    global game_lobbies

    given_str = "Welcome to Catan!\nPlay against others Online? (y/n)\n> "
    conn.send(given_str.encode('ascii'))
    result = conn.recv(1024).decode('ascii').strip()
    i = len(game_lobbies)-1
    if result == "y":
        # if there are less than 4 people in the game, put them in a lobby.
        if len(game_lobbies[i]) < 4:
            game_lobbies[i].append(conn)
            print("[+] Added a connected player to an existing lobby")
            if len(game_lobbies[i]) == 1:
                given_str = '''You're the game owner.
Please wait for other players, then press Enter to begin the game.
Number of players in the lobby: {}
'''.format(len(game_lobbies[i]))
                conn.send(given_str.encode('ascii'))
                result = conn.recv(1024).decode('ascii').strip()
                print(result)
                game_thread = threading.Thread(target=catan_client, args=(game_lobbies[i],))
                game_thread.start()
            else:
                client_msg = "You're in a lobby!! Wait on the Game Owner to start the game...\n"
                conn.send(client_msg.encode('ascii'))

                for client in game_lobbies[i]:
                    given_str = "Number of players in the lobby: {}\n".format(len(game_lobbies[i]))
                    client.send(given_str.encode('ascii'))

        # Otherwise make a new one.
        else:
            game_lobbies.append([conn])
            print("[+] Created new lobby with a player in it.")

    elif result == "n":
        conn.send("You're playing a local game!\n".encode('ascii'))
        game_thread = threading.Thread(target=catan_client, args=([conn],))
        single_player_games.append(conn)
        game_thread.start()
        return

    else:
        # Error handling, you have to put in y/n
        pass


def catan_client(conns):
    # create an instance of the game
    game = catan_classes.Game(conns) # pass a list of sockets.
    for conn in conns:
        conn.close()
    print("Gracefully closed connection to a lobby of clients")


if __name__ == "__main__":

    # Create a socket on the server
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #REMOVE THIS OPTION BEFORE DEPLOYING.
    port = 4444

    # Bind to the port
    serversocket.bind(('', port))

    # Allow connections
    serversocket.listen(5)

    # Feedback to know the server is running
    print("CATAN SERVER STARTED\nWaiting for connctions...")
    while True:

        # establish a connection
        client_conn,addr = serversocket.accept()

        # Feedback on server side of established connection
        print("Got a connection from %s" % str(addr))

        # Create a thread so you can serve multiple people.
        mode_thread = threading.Thread(target=choose_mode, args=(client_conn,))
        mode_thread.start()

    # When all is said and done, close the socket on the server-side
    serversocket.close()
