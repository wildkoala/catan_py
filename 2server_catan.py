
#========================================================
#FILE PURPOSE:
#  - The functions contained in this file will directly pertain to the game loop.
#========================================================


#========================================================
#BUG SECTION:
# Not getting resources from second settlement placed in setup phase. (Not at the beginning, and not during gameplay.)
# Not getting resouces from tiles other than tile 1
#========================================================

#========================================================
# Requirements and Exports
#========================================================
import random
import catan_classes
import items
import config
import math
import socket
from _thread import *

#========================================================
# FUNCTION DECLARATIONS
#========================================================
def catan_print(conn, given_str):
    conn.send(given_str.encode('ascii'))
    return

def catan_read(conn, size=1024):
    s = conn.recv(size).decode('ascii').strip()
    return s

def handle_errors(conn, result):
    if result == -1:
        catan_print(conn, "That's an invalid location\n")
    elif result == -2:
        catan_print(conn, "Someone is already on that space!!\n")
    elif result == -3:
        catan_print(conn, "Someone is on an adjacent space!!\n")
    elif result == -4:
        catan_print(conn, "The correct format is tile,corner\n")
        catan_print(conn, "EXAMPLE: 1,2\n")
    elif result == -5:
        catan_print(conn, "Your road must be connected to one of your settlements\n")
    elif result == -6:
        catan_print(conn,"Not enough resources!!\n")
    elif result == 99:
        catan_print(conn, "Invalid input... Please try again.\n")
    else:
        catan_print(conn, "That caused some unknown error, please try to not do that again :)\n")

def catan_client(conn):
    msg = display_main_menu() # returns string
    catan_print(conn, msg)

    # THIS WORKS
    selection = catan_read(conn) # I think this is a string now.
    selection = int(selection)
    print("Client selected: " + str(selection))

    while selection != 1:
        if selection == 2:
            # this will cause an infinite loop for now.
            explain_rules(conn)
        elif selection == 3:
            display_credits(conn)
        else:
            catan_print(conn, "Please enter an appropriate value")

    # ask players for their name and color choice
    result = get_player_info(conn)
    while result == None:
        result = get_player_info(conn)

    # establish points to win
    points_to_win = declare_pts_to_win(conn)
    while points_to_win == None:
        points_to_win = declare_pts_to_win(conn)

    catan_print(conn, config.show_board()) # show_board returns the board as a string

    curr_player_turn = 0

    place_initial(conn)

    catan_print(conn, items.give_resources(0, True))



    winner = False
    while winner != True:
        #Declare whos turn it is in the game
        winner = player_turn(conn, config.player_list[curr_player_turn], points_to_win)
        if winner:
            break
        curr_player_turn = increment_player_turn(curr_player_turn, len(config.player_list))

    # send winner
    catan_print(conn, "WINNER: " + config.player_list[curr_player_turn].p_name)

    conn.close()
    print("Gracefully closed connection to client")




def move_robber(conn):
    knight_placed = False
    while knight_placed == False:
        catan_print(conn, "Which tile will you place the robber on?\n> ")
        t = int(catan_read(conn))
        if t == config.robber.on_tile: # can i get the board this way or does it have to be an argument? Maybe just put it in config?
            catan_print(conn, "You must put the robber on a new tile.")
            continue
        else:
            # maybe the tile that the robber is on should be an attribute of the robber, because im going to have to iterate over all the times to "undo" the old robber.
            config.robber.on_tile = t
            knight_placed = True


def play_dev_card(conn, a_player, dev_card):
    # Partially Implemented
    if dev_card.card_type == "Knight":
        catan_print(conn, a_player.p_name + " played a development card: ")
        catan_print(conn, dev_card.card_type) # this might break, need to pass a string
        move_robber(conn)
        # steal a card from a player.

    #DONE
    elif dev_card.card_type == "Road Building":
        catan_print(conn, a_player.p_name + " played a development card: ")
        catan_print(conn, dev_card.card_type)
        a_player.p_hand.append("B")
        a_player.p_hand.append("L")
        a_player.p_hand.append("B")
        a_player.p_hand.append("L")

        # this should force the player to build two roads
        roads_placed = 0
        while roads_placed != 2:
            # have to check they built a valid road. function can return None.
            if build_road(a_player) == None:
                continue
            else:
                roads_placed += 1

    #DONE
    elif dev_card.card_type == "Year of Plenty":
        catan_print(conn, a_player.p_name + " played a development card: ", end='')
        catan_print(conn, dev_card.card_type)

        added_cards = 0
        while added_cards != 2: # even if this loo
            catan_print(conn, "What resource would you like? Resource (" + str(added_cards+1) + "/2)")
            wanted_card = catan_read(conn)
            if wanted_card.upper() in "BLSWO":
                    a_player.p_hand.append(wanted_card.upper())
                    added_cards += 1
            else:
                catan_print(conn, wanted_card + " is not a valid resource")

    #DONE
    elif dev_card.card_type == "Monopoly":
        catan_print(conn, a_player.p_name + " played a development card: ")
        catan_print(conn, dev_card.card_type)
        got_resources = False
        while got_resources == False:
            catan_print(conn, "What resource would you like? Resource (" + str(added_cards+1) + "/2)")
            wanted_card = catan_read(conn)
            if wanted_card.upper() in "BLSWO":
                num_taken = 0
                for p in config.player_list: # wait, this actually takes cards from the player using it too, since they're in player list. I guess that's okay if i add them back?
                    for resource in p.p_hand:
                        if resource == wanted_card.upper():
                            p.p_hand.remove(resource)
                            num_taken += 1

                for num in range(0, num_taken):
                    a_player.p_hand.append(wanted_card.upper())

                catan_print(conn, a_player.p_name + " took all everyone's " + wanted_card.upper())
                got_resources = True

            else:
                catan_print(conn, wanted_card + " is not a valid resource")


    #DONE
    elif dev_card.card_type == "Victory Point":
        a_player.p_victory_pts += 1 # I don't want to tell anyone else that this was played.

    else:
        catan_print(conn, "Not a known development card type")



def player_choose_color(conn, color_options):
        catan_print(conn, "Which color will you be?\n")
        i = 1
        for c in color_options:
            color_format = "\t" + str(i) + ". " + c + "\n"
            catan_print(conn, color_format)
            i += 1
        try:
            catan_print(conn, "Chose the number of the color you'd like.\n> ")
            choice = int(catan_read(conn))
            return choice

        except ValueError:
            catan_print(conn, "You must enter an integer.") # this exception handling might not work...
            choice = player_choose_color(conn, color_options) # I don't want to call this recursively, but im hacking it together.
            return choice

#def valid_discard(a_string, player_hand):

def robber(conn):
    catan_print(conn, "ROBBER HAS BEEN ROLLED\n")

    # Loop checks to see if any players have 7 or more cards
    for i in config.player_list:
        if len(i.p_hand) >= 7:
            num_to_discard = math.ceil(len(i.p_hand)/2)
            discard = ""
            has_cards = False
            while len(discard) != num_to_discard or has_cards == False:
                catan_print(conn, i.p_name + " this is your current hand: ")
                i.show_hand()
                catan_print(conn, i.p_name + " Please discard " + str(num_to_discard) + " cards\n> ")
                discard = catan_read(conn)
                if len(discard) > num_to_discard:
                    catan_print(conn, "You have discarded more cards than necessary.")

                elif len(discard) < num_to_discard:
                    catan_print(conn, "You didn't discard enough cards... try again.")

                if i.p_hand.count("O") >= list(discard).count("O") and i.p_hand.count("B") >= list(discard).count("B") and i.p_hand.count("S") >= list(discard).count("S") and i.p_hand.count("W") >= list(discard).count("W") and i.p_hand.count("L") >= list(discard).count("L"):
                    has_cards = True
                    catan_print(conn, "You have those cards")
                else:
                    has_cards = False
                    catan_print(conn, "You do not have those cards")
            for card in discard:
                i.p_hand.remove(card)
            catan_print(conn, i.p_name + " this is your new hand: ")
            i.show_hand()

    move_robber(conn)

def increment_player_turn(current_player_turn, num_players):
    return (current_player_turn + 1) % num_players


def player_menu(conn):
    catan_print(conn,
'''
        1. View your hand
        2. Buy a road
        3. Buy a settlement
        4. Upgrade a settlement to a city
        5. Buy a development card
        6. Trade with a player
        7. Trade with the bank (4 for 1)
        8. Trade using a port
        9. Display Board
        10. View Development cards
        11. Play Development Card
        0. End Turn
'''
    )

def trade_resources(player, trade_to, want, offer):
    for r in offer:
        player.p_hand.remove(r)
        trade_to.p_hand.append(r)

    for r in want:
        player.p_hand.append(r)
        trade_to.p_hand.remove(r)

def trade_accepted(conn, player, trade_to, want, offer):
    catan_print(conn, trade_to.p_name + ", " + player.p_name + " has offered you: " )
    catan_print(conn, offer + "\n")
    catan_print(conn, "In exchange for: ")
    catan_print(conn, want + "\n")
    choice = ""
    while choice == "":
        catan_print(conn, "Do you want to accept this trade? (y/n)\n> ")
        choice = catan_read(conn)
        if choice not in "yn":
            catan_print(conn, "You must enter 'y' or 'n'")
            choice = ""
            continue

    if choice == "y":
        return True
    elif choice == "n":
        return False

def player_turn(conn, player, points_to_win):
    catan_print(conn, "\n" + player.p_name + " it is your turn\n")

    catan_print(conn, "Press Enter to Roll Die")
    user_input = catan_read(conn)

    roll = config.roll_dice()
    catan_print(conn, "\n" + str(roll) + " has been rolled\n")
    catan_print(conn, items.give_resources(roll))


    #Check to see if robber() should be called
    if roll == 7:
        robber(conn)

  #Player Selects an Option
    selection = -1
    while selection != 0:
        player_menu(conn)
        try:
            catan_print(conn, "Please Select One\n"+ player.p_name + "> ")
            selection = int(catan_read(conn))
        except ValueError:
            catan_print(conn, "You must enter a number corresponding to an option")
            selection = -1

        if selection == 1:
            catan_print(conn, player.show_hand())

        elif selection == 2:
            server_build_item(conn, player, "road")


        elif selection == 3:
            server_build_item(conn, player, "settlement")

        elif selection == 4:
            server_build_item(conn, player, "city")

        elif selection == 5:
            result = items.build_dev_card(player)
            if isinstance(result, str):
                catan_print(conn, result)
            elif isinstance(result, int):
                handle_errors(conn, result)

        # Partially implemented
        elif selection == 6:
            catan_print(conn, "Players:\n")
            counter  = 1
            for p in config.player_list:
                catan_print(conn, "\t" + str(counter) + ". " + p.p_name + "\n")
                counter += 1
            catan_print(conn, "\t" + str(counter) + ". Offer trade to everyone\n")
            catan_print(conn, "Who do you want to trade with?\n> ")

            option = int(catan_read(conn)) # gonna have to do error checking on this too...
            trade_to = config.player_list[option-1]
            catan_print(conn, "What resource(s) do you want?")
            want = catan_read(conn)
            catan_print(conn, "What resource(s) are you offering in exchange?\n> ")
            offer = catan_read(conn)


            if option <= len(config.player_list):
                if player.has_resources(offer):
                    want_to_trade = trade_accepted(conn, player, trade_to, want, offer)
                    they_have_resources = trade_to.has_resources(want)
                    if want_to_trade and they_have_resources:
                        trade_resources(player, trade_to, want, offer)
                else:
                    catan_print(conn, "You don't have those resources to offer...")
            elif trade_to == len(player_list) + 1:
                catan_print(conn, "Trade to all players is coming soon")
            else:
                catan_print(conn, "Invalid option")





        elif selection == 7:
            catan_print(conn, "What resource would you like?\n> ")
            want = catan_read(conn)
            catan_print(conn, "What resource will you be trading 4 of?\n> ")
            give = catan_read(conn)
            if player.has_resources(give*4):
                player.p_hand.remove(give)
                player.p_hand.remove(give)
                player.p_hand.remove(give)
                player.p_hand.remove(give)
                player.p_hand.append(want)
                catan_print(conn, "You traded with the bank!")

                '''
                for p in config.player_list: # for some reason
                    print("global p_name: " + p.p_name + " local player: " + player.p_name)

                    if p.p_name == player.p_name:

                        p.p_hand.remove(give)
                        p.p_hand.remove(give)
                        p.p_hand.remove(give)
                        p.p_hand.remove(give)
                        p.p_hand.append(want)
                        print("You traded with the bank!")
                    else:
                        print("p_names didn't match?")
                '''
            else:
                catan_print(conn, "You don't have enough of that resource to trade...")

        elif selection == 8:
            catan_print(conn, "Trade using a port")

        elif selection == 9:
            catan_print(conn, config.show_board())

        elif selection == 10:
            catan_print(conn, player.show_dev_cards())


        elif selection == 11:
            if player.p_dev_cards == []:
                catan_print(conn, "You have no development cards!!")
                continue
            catan_print(conn, "Please select a dev_card: ")
            player.show_dev_cards(conn)
            num = catan_read(conn)
            play_dev_card(conn, player, player.p_dev_cards[num-1])

        elif selection == 0:
            pass


        # I don't know if this check actually works.

        if (player.show_victory_pts() >= points_to_win):
            return True



    return False

#========================================================
# START OF GAME
#========================================================




def server_build_item(conn, a_player, item, init = False):

    # There's a way to get this down into one thing. More DRY, but i can't figure it out rn.
    # PARTIALLY IMPLEMENTED
    if item == "settlement":
        if init:
            settled = False
            while settled == False:
                catan_print(conn, "Where do you want to place your settlement?\n" + a_player.p_name.strip() + "> ")
                location = catan_read(conn)
                result = items.build_settlement(a_player, location, True)
                if isinstance(result, int):
                    handle_errors(conn, result)
                elif isinstance(result, str):
                    catan_print(conn, result)
                    settled = True

                '''
                if result < 0:
                    handle_errors(conn, result)
                    continue
                else:
                    catan_print(conn, a_player.p_name + " has placed a settlement!!\n")
                    return
                '''
        else:
            catan_print(conn, "Where do you want to place your settlement?\n> ")
            location = catan_read(conn)
            result = items.build_settlement(a_player, location)
            if isinstance(result, int):
                handle_errors(conn, result)
            elif isinstance(result, str):
                catan_print(conn, result)

    elif item == "road": # not yet written for anything other than initial setup
        if init:
            first_road = False
            while first_road == False:
                catan_print(conn, "Where do you want to start your road?\n> ")
                n1 = catan_read(conn)
                catan_print(conn, "Where do you want to end your road?\n> ")
                n2 = catan_read(conn)
                result = items.build_road(a_player, n1, n2, True)
                if isinstance(result, int):
                    handle_errors(conn, result)
                elif isinstance(result, str):
                    catan_print(conn, result)
                    first_road = True
        else:
            catan_print(conn, "Where do you want to start your road?\n> ")
            n1 = catan_read(conn)
            catan_print(conn, "Where do you want to end your road?\n> ")
            n2 = catan_read(conn)
            result = items.build_road(a_player, n1, n2)
            if isinstance(result, int):
                handle_errors(conn, result)
            elif isinstance(result, str):
                catan_print(conn, result)

    elif item == "dev card":
        catan_print(conn, "Where do you want to start your road?\n> ")
        n1 = catan_read(conn)
        catan_print(conn, "Where do you want to end your road?\n> ")
        n2 = catan_read(conn)
        result = items.build_dev_card(a_player)
        if isinstance(result, int):
            handle_errors(conn, result)
        elif isinstance(result, str):
            catan_print(conn, result)


def place_initial(conn):
    for p in config.player_list:
        catan_print(conn, "\n" + p.p_name.strip() + " is placing their first settlement\n")

        # FIRST SETTLEMENT
        server_build_item(conn, p, "settlement", True)
        catan_print(conn, config.show_board())
        p.p_victory_pts += 1


        # FIRST ROAD
        catan_print(conn, "\n" + p.p_name.strip() + " is placing their first road\n")
        server_build_item(conn, p, "road", True)
        catan_print(conn, config.show_board())


    for p in reversed(config.player_list):

        # SECOND SETTLEMENT
        catan_print(conn, "\n" + p.p_name + " is placing their second settlement\n")
        server_build_item(conn, p, "settlement", True)
        catan_print(conn, config.show_board())
        p.p_victory_pts += 1

        # SECOND ROAD
        catan_print(conn, "\n" + p.p_name.strip() + " is placing their second road\n")
        server_build_item(conn, p, "road", True)
        catan_print(conn, config.show_board())



def display_main_menu():
    template = '''
        CCCCCCCCCCCCC               AAA         TTTTTTTTTTTTTTTTTTTTTTT         AAA               NNNNNNNN        NNNNNNNN
     CCC::::::::::::C              A:::A        T:::::::::::::::::::::T        A:::A              N:::::::N       N::::::N
   CC:::::::::::::::C             A:::::A       T:::::::::::::::::::::T       A:::::A             N::::::::N      N::::::N
  C:::::CCCCCCCC::::C            A:::::::A      T:::::TT:::::::TT:::::T      A:::::::A            N:::::::::N     N::::::N
 C:::::C       CCCCCC           A:::::::::A     TTTTTT  T:::::T  TTTTTT     A:::::::::A           N::::::::::N    N::::::N
C:::::C                        A:::::A:::::A            T:::::T            A:::::A:::::A          N:::::::::::N   N::::::N
C:::::C                       A:::::A A:::::A           T:::::T           A:::::A A:::::A         N:::::::N::::N  N::::::N
C:::::C                      A:::::A   A:::::A          T:::::T          A:::::A   A:::::A        N::::::N N::::N N::::::N
C:::::C                     A:::::A     A:::::A         T:::::T         A:::::A     A:::::A       N::::::N  N::::N:::::::N
C:::::C                    A:::::AAAAAAAAA:::::A        T:::::T        A:::::AAAAAAAAA:::::A      N::::::N   N:::::::::::N
C:::::C                   A:::::::::::::::::::::A       T:::::T       A:::::::::::::::::::::A     N::::::N    N::::::::::N
 C:::::C       CCCCCC    A:::::AAAAAAAAAAAAA:::::A      T:::::T      A:::::AAAAAAAAAAAAA:::::A    N::::::N     N:::::::::N
  C:::::CCCCCCCC::::C   A:::::A             A:::::A   TT:::::::TT   A:::::A             A:::::A   N::::::N      N::::::::N
   CC:::::::::::::::C  A:::::A               A:::::A  T:::::::::T  A:::::A               A:::::A  N::::::N       N:::::::N
     CCC::::::::::::C A:::::A                 A:::::A T:::::::::T A:::::A                 A:::::A N::::::N        N::::::N
        CCCCCCCCCCCCCAAAAAAA                   AAAAAAATTTTTTTTTTTAAAAAAA                   AAAAAAANNNNNNNN         NNNNNNN


            MAIN MENU: Please Select and Option

        1. Play Catan
        2. Explain Rules
        3. Credits
> '''
    return template

def welcome():
    template = '''
        CCCCCCCCCCCCC               AAA         TTTTTTTTTTTTTTTTTTTTTTT         AAA               NNNNNNNN        NNNNNNNN
     CCC::::::::::::C              A:::A        T:::::::::::::::::::::T        A:::A              N:::::::N       N::::::N
   CC:::::::::::::::C             A:::::A       T:::::::::::::::::::::T       A:::::A             N::::::::N      N::::::N
  C:::::CCCCCCCC::::C            A:::::::A      T:::::TT:::::::TT:::::T      A:::::::A            N:::::::::N     N::::::N
 C:::::C       CCCCCC           A:::::::::A     TTTTTT  T:::::T  TTTTTT     A:::::::::A           N::::::::::N    N::::::N
C:::::C                        A:::::A:::::A            T:::::T            A:::::A:::::A          N:::::::::::N   N::::::N
C:::::C                       A:::::A A:::::A           T:::::T           A:::::A A:::::A         N:::::::N::::N  N::::::N
C:::::C                      A:::::A   A:::::A          T:::::T          A:::::A   A:::::A        N::::::N N::::N N::::::N
C:::::C                     A:::::A     A:::::A         T:::::T         A:::::A     A:::::A       N::::::N  N::::N:::::::N
C:::::C                    A:::::AAAAAAAAA:::::A        T:::::T        A:::::AAAAAAAAA:::::A      N::::::N   N:::::::::::N
C:::::C                   A:::::::::::::::::::::A       T:::::T       A:::::::::::::::::::::A     N::::::N    N::::::::::N
 C:::::C       CCCCCC    A:::::AAAAAAAAAAAAA:::::A      T:::::T      A:::::AAAAAAAAAAAAA:::::A    N::::::N     N:::::::::N
  C:::::CCCCCCCC::::C   A:::::A             A:::::A   TT:::::::TT   A:::::A             A:::::A   N::::::N      N::::::::N
   CC:::::::::::::::C  A:::::A               A:::::A  T:::::::::T  A:::::A               A:::::A  N::::::N       N:::::::N
     CCC::::::::::::C A:::::A                 A:::::A T:::::::::T A:::::A                 A:::::A N::::::N        N::::::N
        CCCCCCCCCCCCCAAAAAAA                   AAAAAAATTTTTTTTTTTAAAAAAA                   AAAAAAANNNNNNNN         NNNNNNN


                                    WELCOME TO CATAN!! WAITING FOR OTHER PLAYERS...
                                      GAME WILL BEGIN WHEN THERE ARE 2 PLAYERS
'''
    return template


def explain_rules(conn):
    catan_print(conn,'''
    Here are the rules for Catan:


    Please Press any key to go back to the main menu

    ''')


def display_credits(conn):
    catan_print(conn,'''
    Game Created by:
        Grayson "Twiggy" Gordon
        Anthony Walton

    Graphics:
        Grayson "Twiggy" Gordon
        Anthony Walton

    All Rights are owned by the creators of this game
    IF YOU STEAL THIS I WILL GET HANGRY


press any key to go back to the main menu
    ''')

def get_player_info(conn):
    try:
        catan_print(conn, "Please enter the number of players\n> ")

        num_players = int(catan_read(conn))
        i = 0
        color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]

        while i < num_players:
            template = "Please Enter Player " + str((i + 1)) + "'s name\n> "
            catan_print(conn, template)
            name = catan_read(conn)
            # give player a list of color options

            p_color =  color_options.pop(player_choose_color(conn, color_options)-1)
            catan_print(conn, "You selected: " + p_color + "\n")
            color = p_color[0].lower()
            config.player_list.append(catan_classes.Player(name.strip(),color))
            i+=1

        return True # doesnt matter, as long as it's not None type

    except ValueError:
        catan_print(conn, "You must enter an integer")
        return

    except IndexError:
        catan_print(conn, "You must enter one of the provided options")
        return

def declare_pts_to_win(conn):
    # most of this should be wrapped up in a "setup" function
    try:
        catan_print(conn, "Enter the Amount of Points Required to Win\n> ")
        pts_to_win = int(catan_read(conn))
        return pts_to_win
    except ValueError:
        catan_print(conn, "You must provide an integer")


if __name__ == "__main__":
    connections = [] # list of connected clients

    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4444

    # bind to the port
    serversocket.bind(('', port))

    # Only take 1 connection for now until multi-threading works
    serversocket.listen(1)
    print("CATAN SERVER STARTED\nWaiting for connctions...")
    while True:
        # establish a connection

        client_conn,addr = serversocket.accept()

        print("Got a connection from %s" % str(addr))
        thread_id = start_new_thread(catan_client, (client_conn,))
        connections.append((client_conn, addr))

    serversocket.close()


'''
UNIVERSAL ERROR CODES:

-1 : Invalid location. Location does not exist on the map
-2: Occupied space. Another player is located here
-3: Adjacent Player. A player is on an adjacent object.
'''
