
#========================================================
#FILE PURPOSE:
#  - The functions contained in this file will directly pertain to the game loop.
#========================================================


#========================================================
#BUG SECTION:
#========================================================

#========================================================
# Requirements and Exports
#========================================================
import random
import catan_classes
import items
import config
import math


#========================================================
# FUNCTION DECLARATIONS
#========================================================

def move_robber():
    knight_placed = False
    while knight_placed == False:
        t = int(input("Which tile will you place the robber on?"))
        if b.tiles[t-1].has_robber: # can i get the board this way or does it have to be an argument? Maybe just put it in config?
            print("You must put the robber on a new tile.")
            continue
        else:
            # maybe the tile that the robber is on should be an attribute of the robber, because im going to have to iterate over all the times to "undo" the old robber.
            if t == config.robber.on_tile:
                print("The robber is already here... you must move it somewhere else.")
                continue
            config.b.tiles[t-1] = True
            knight_placed = True


def play_dev_card(a_player, dev_card):
    # Partially Implemented
    if dev_card.card_type == "Knight":
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)
        move_robber()
        # steal a card from a player.
        

    #DONE
    elif dev_card.card_type == "Road Building":
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)
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
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)

        added_cards = 0
        while added_cards != 2: # even if this loo
            wanted_card = input("What resource would you like? Resource (" + str(added_cards+1) + "/2)" )
            if wanted_card.upper() in "BLSWO":
                    a_player.p_hand.append(wanted_card.upper())
                    added_cards += 1
            else:
                print(wanted_card + " is not a valid resource")

    #DONE
    elif dev_card.card_type == "Monopoly":
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)
        got_resources = False
        while got_resources == False:
            wanted_card = input("What resource would you like? Resource (" + str(added_cards+1) + "/2)" )
            if wanted_card.upper() in "BLSWO":

                num_taken = 0
                for p in config.player_list: # wait, this actually takes cards from the player using it too, since they're in player list. I guess that's okay if i add them back?
                    for resource in p.p_hand:
                        if resource == wanted_card.upper():
                            p.p_hand.remove(resource)
                            num_taken += 1

                for num in range(0, num_taken):
                    a_player.p_hand.append(wanted_card.upper())

                print(a_player.p_name + " took all everyone's " + wanted_card.upper())
                got_resources = True

            else:
                print(wanted_card + " is not a valid resource")


    #DONE
    elif dev_card.card_type == "Victory Point":
        a_player.p_victory_pts += 1 # I don't want to tell anyone else that this was played.

    else:
        print("Not a known development card type")

def player_choose_color(color_options):
        print("Which color will you be?")
        i = 1
        for c in color_options:
            print("\t" + str(i) + ". " + c)
            i += 1
        try:
            choice = int(input("Chose the number of the color you'd like.\n"))
            return choice
        except ValueError:
            print("You must enter an integer.")
            choice = player_choose_color(color_options) # I don't want to call this recursively, but im hacking it together.
            return choice

#def valid_discard(a_string, player_hand):

def robber():
    print("ROBBER HAS BEEN ROLLED")

    # Loop checks to see if any players have 7 or more cards
    for i in config.player_list:
        if len(i.p_hand) >= 7:
            num_to_discard = math.ceil(len(i.p_hand)/2
            discard = ""
            has_cards = False
            while len(discard != num_to_discard) or has_cards == False:
                print(i.p_name + " this is your current hand: ")
                i.show_hand()
                discard = input(i.p_name + " Please discard " + str(num_to_discard) + " cards (rounding up)")
                if len(discard) > num_to_discard):
                    print("You have discarded more cards than necessary.")
                    
                elif len(discard) < num_to_discard):
                    print("You didn't discard enough cards... try again.")

                if i.p_hand.count("O") >= list(discard).count("O") and i.p_hand.count("B") >= list(discard).count("B") and i.p_hand.count("S") >= list(discard).count("S") and i.p_hand.count("W") >= list(discard).count("W") and i.p_hand.count("L") >= list(discard).count("L"):
                    has_cards = True
                    print("You have those cards")
                else:
                    has_cards = False
                    print("You do not have those cards")
            for card in discard:
                i.p_hand.remove(card)
            print(i.p_name + " this is your new hand: ")
            i.show_hand()

    move_robber()

def increment_player_turn(current_player_turn, num_players):
    return (current_player_turn + 1) % num_players


def player_menu():
    print(
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
        0. End Turn
'''
    )

def player_turn(player, points_to_win):
    print(player.p_name + " it is your turn")

    user_input = input("Press Enter to Roll Die")

    roll = config.roll_dice()
    print(str(roll) + " has been rolled")
    items.give_resources(roll)

    #Check to see if robber() should be called
    if roll == 7:
        robber()

  #Player Selects an Option
    selection = -1
    while selection != 0:
        player_menu()
        selection = int(input("Please Select One\n"))

        if selection == 1:
            player.show_hand()

        elif selection == 2:
            items.build_road(player)

        elif selection == 3:
            items.build_settlement(player)

        elif selection == 4:
            items.build_city(player)

        elif selection == 5:
            items.build_dev_card(player)

        elif selection == 6:
            print("Trade with Player")

        elif selection == 7:
            print("Trade with bank")

        elif selection == 8:
            print("Trade using a port")

        elif selection == 9:
            config.show_board()

        if (player.show_victory_pts() >= points_to_win):
            return True
    return False

#========================================================
# START OF GAME
#========================================================

def place_initial():
    for i in config.player_list:
        print(i.p_name + " is placing their first settlement")
        items.build_settlement(i, True)
        print(i.p_name + " is placing their first road")
        items.build_road(i, True)
    for i in reversed(config.player_list):
        print(i.p_name + " is placing their second settlement")
        items.build_settlement(i, True)
        print(i.p_name + " is placing their second road")
        items.build_road(i, True)

def display_main_menu():
    selection = input('''
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


        ''')
    try:
        val = int(selection)
        pass
    except ValueError:
        selection = -1
        print("Please select the corresponding number. Do not enter a word/phrase")
    return selection

def explain_rules():
    input('''
    Here are the rules for Catan:


    Please Press any key to go back to the main menu

    ''')

def display_credits():
    input('''
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

def get_player_info():
    try:
        num_players = int(input("Please enter the number of players\n"))
        i = 0
        color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]

        while i < num_players:
            name = input("Please Enter Player " + str((i + 1)) + "'s Name\n")
            # give player a list of color options

            p_color =  color_options.pop(player_choose_color(color_options)-1)
            print("You selected: " + p_color)
            color = p_color[0].lower()
            config.player_list.append(catan_classes.Player(name,color))
            i+=1
        
        return True # doesnt matter, as long as it's not None type

    except ValueError:
        print("You must enter an integer")
        return

    except IndexError:
        print("You must enter one of the provided options")
        return

def declare_pts_to_win():
    # most of this should be wrapped up in a "setup" function
    try:
        return int(input("Enter the Amount of Points Required to Win\n"))
    except ValueError:
        print("You must provide an integer")


if __name__ == "__main__":

    # Display CATAN name
    selection = -1
    while selection != 1:
        selection = int(display_main_menu())

        if selection == 2:
            explain_rules()
        elif selection == 3:
            display_credits()
        elif selection == 1:
            pass
        else:
            print("Please enter an appropriate value")

    # Players Connected: _#_

    # assume they chose 1.

    #Setup the game and return player_list and amount of points to win

    # need player list accessible across all modules
    # ask players for their name and color choice
    result = get_player_info()
    while result == None:
        get_player_info()

    # establish points to win
    points_to_win = declare_pts_to_win()
    while points_to_win == None:
        points_to_win = declare_pts_to_win()


    print("Here is the Board:")
    config.show_board()

    #Store player_list and points to win in variables
    curr_player_turn = 0


    # Everyone rolls for who goes first
        # highest goes first (still need to incorporate this)
            # place settlement
            # get resources
            # place roads
        # once through list, go in reverse order placing second settlement
    place_initial()


    # once every player has their settlements down

    # GAME LOOP

    #Give players their initial resources
    items.give_resources(0, True)

    winner = False
    while winner != True:

        #Declare whos turn it is in the game
        winner = player_turn(config.player_list[curr_player_turn], points_to_win)
        curr_player_turn = increment_player_turn(curr_player_turn, len(config.player_list))


  # accept connections
  # first menu
  # set options
  # create board
  # create players

  # while winner != 1:
    #player_turn
    #check_win
