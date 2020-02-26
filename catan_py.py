
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

def play_dev_card(a_player, dev_card):
    # Partially implemented
    if dev_card.card_type == "Knight":
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)
        knight_placed = False
        t = int(input("Which tile will you place the robber on?"))
        # if the tile has the robber already
            # print
    
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

             

    elif dev_card.card_type == "Victory Point":
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)

    else:
        print("Not a known development card type")

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
    return player_list


def declare_pts_to_win():
    # most of this should be wrapped up in a "setup" function
    points_to_win = int(input("Enter the Amount of Points Required to Win\n"))

    return points_to_win


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
    b = catan_classes.Board()

    # need player list accessible across all modules
    # ask players for their name and color choice
    player_list = get_player_info()

    # establish points to win
    points_to_win = declare_pts_to_win()

    b.create_board()

    print("Here is the Board:")
    b.show_board()

    #Store player_list and points to win in variables
    curr_player_turn = 0


    # Everyone rolls for who goes first
        # highest goes first (still need to incorporate this)
            # place settlement
            # get resources
            # place roads
        # once through list, go in reverse order placing second settlement
    place_initial(player_list)


    # once every player has their settlements down

    # GAME LOOP

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
