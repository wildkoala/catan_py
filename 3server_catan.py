# THIS FILE ATTEMPTS TO INTEGRATE MULTIPLAYER.
# Let's get game to be an object first. Then it will be a bit easier to manage.

#========================================================
# DESIRED FLOW
#========================================================
'''
 - Player connects to the game
    - player chooses play local or play others online
    - if local, do the current functionality.
    - if play online, put the player in a queue of players
        - If there's no one else in the queue, they are "Game owner"
        - Tell them they are the game owner
        - Every second, send them how many people are in the queue
        - when the game owner types START, create a new game
        - ask each player in order for their player info.
        - when you ask, send a message to all other clients saying "It's player (number)'s turn. You are player #. Please wait."
            - this should populate the player_list. Points to win is up to the game_owner also.

I want to create a class called "Game" that has all this stuff wrapped up in it. It'll take an optional argument of a player_connections
for online play.


# PSEUDO CODE
# player connects
single_player_games = []
game_lobbies = [[]] # list of lists, where each list represents a lobby that contains the connections for a particular game.
catan_print(conn, "Welcome to Catan!\n")
catan_print(conn, "Play Online? (y/n)")
result = catan_read(conn)
i = len(game_lobbies)-1
if result == "y":
    # if there are less than 4 people in the game, put them in a lobby.
    if len(game_lobbies[i]) < 4:
        game_lobbies[i].append(conn)

    # Otherwise make a new one.
    else:
        game_lobbies.append([conn]) # is this correct syntax?

elif result == "n":
    thread_id = start_new_thread(catan_client, (client_conn,))
    catan_print(conn, "Your playing a local game!\n")
    single_player_games.append((client_conn, addr))

else:
    # Error handling, you have to put in y/n
    pass
'''
#========================================================
#FILE PURPOSE:
#  - On connection, the user creates a new instance of the game!!!
#  - The next step is to have a lobby where people can be in the same game together over the network.
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
#this is a test

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
                # okay, if you've got something from the game master, then start the game
                # right now this will only send the game to the game master, and that's okay.
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
        return # returning here should kill the mode_thread... that's the behavior i want.

    else:
        # Error handling, you have to put in y/n
        pass


def catan_client(conns):
    # create an instance of the game
    # for right now I'm only passing one connection to Game, because I think that's all it can take rn.
    game = catan_classes.Game(conns) # pass a list of sockets.
    for conn in conns:
        conn.close()
    print("Gracefully closed connection to a lobby of clients")


if __name__ == "__main__":

    connections = []

    # Create a socket on the server
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #REMOVE THIS OPTION BEFORE DEPLOYING.
    port = 4444

    # Bind to the port
    serversocket.bind(('', port))

    # Only take 1 connection for now until multi-threading works
    serversocket.listen(1)

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

        # Keeping track of my connections.
        connections.append((client_conn, addr))

    # When all is said and done, close the socket on the server-side
    serversocket.close()
