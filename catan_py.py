
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

def player_choose_color(color_options):
        print("Which color will you be?")
        i = 1
        for c in color_options:
            print("\t" + str(i) + ". " + c)
            i += 1
        choice = int(input("Chose the number of the color you'd like?\n"))
        return choice

def robber():
    print("ROBBER HAS BEEN ROLLED")

    # Loop checks to see if any players have 7 or more cards
    for i in player_list:
        if len(i.p_hand) >= 7:
            discard = ""
            has_cards = False
            while (len(discard) != math.ceil(len(i.p_hand)/2)) or (has_cards == False):
                print(i.p_name + " this is your current hand: ")
                i.show_hand()
                discard = input(i.p_name + " Please discard half your cards (rounding up)")
                if len(discard) > math.ceil(len(i.p_hand)/2):
                    print("You have discarded more cards than necessary.")
                elif len(discard) < math.ceil(len(i.p_hand)/2):
                    print("You must discard half your cards (ROUNDING UP)")
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

def player_turn(player, points_to_win, game_board, game_players):
    print(player.p_name + " it is your turn")

    user_input = input("Press Enter to Roll Die")

    roll = catan_classes.roll_dice()
    print(str(roll) + " has been rolled")
    items.give_resources(roll, game_board, game_players)

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
            b.show_board()

        if (player.show_victory_pts() >= points_to_win):
            return True
    return False

#========================================================
# START OF GAME
#========================================================

def place_initial(player_list):
    for i in player_list:
        print(i.p_name + " is placing their first settlement")
        items.build_settlement(i, True)
        print(i.p_name + " is placing their first road")
        items.build_road(i, True)
    for i in reversed(player_list):
        print(i.p_name + " is placing their second settlement")
        items.build_settlement(i, True)
        print(i.p_name + " is placing their second road")
        items.build_road(i, True)


def setup():

    print('''
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
''')

    num_players = int(input("Please enter the number of players\n"))

    player_list = [] # this will be a list of Player objects
    i = 0
    color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]

    while i < num_players:
        name = input("Please Enter Player " + str((i + 1)) + "'s Name\n")
        # give player a list of color options

        p_color =  color_options.pop(player_choose_color(color_options)-1)
        print("You selected: " + p_color)
        color = p_color[0].lower()
        player_list.append(catan_classes.Player(name,color))
        i+=1

# most of this should be wrapped up in a "setup" function
    points_to_win = int(input("Enter the Amount of Points Required to Win\n"))

    b.create_board()

    print("Here is the Board:")
    b.show_board()

    return (player_list, points_to_win)


if __name__ == "__main__":

    # Display CATAN name
    # main menu
    # 1. Play Catan
    # 2. Explain Rules
    # 3. Credits
    #
    # Players Connected: _#_

    # assume they chose 1.

    #Setup the game and return player_list and amount of points to win
    b = catan_classes.Board()

    # need node list accessible across all modules
    # config.node_list

    # need road list


    # need player list accessible across all modules
    # ask players for their name and color choice
    game_specifications = setup()


    #catan_classes.create_nodes()


    # establish points to win

    # Everyone rolls for who goes first
        # highest goes first
            # place settlement
            # get resources
            # place roads
        # once through list, go in reverse order placing second settlement


    # once every player has their settlements down

    # GAME LOOP

    #Store player_list and points to win in variables
    player_list = game_specifications[0]
    points_to_win = game_specifications[1]
    curr_player_turn = 0

    place_initial(player_list)

    #Give players their initial resources
    items.give_resources(0, b, player_list, True)

    winner = False
    while winner != True:

        #Declare whos turn it is in the game
        winner = player_turn(player_list[curr_player_turn], points_to_win, b, player_list)
        curr_player_turn = increment_player_turn(curr_player_turn, len(player_list))


  # accept connections
  # first menu
  # set options
  # create board
  # create players

  # while winner != 1:
    #player_turn
    #check_win
