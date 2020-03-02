
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
    print(config.show_board())
    knight_placed = False
    while knight_placed == False:
        t = int(input("Which tile will you place the robber on?\n> "))
        if t == config.robber.on_tile: # can i get the board this way or does it have to be an argument? Maybe just put it in config?
            print("You must put the robber on a new tile.")
            continue
        else:
            # maybe the tile that the robber is on should be an attribute of the robber, because im going to have to iterate over all the times to "undo" the old robber.
            config.robber.on_tile = t
            knight_placed = True

def check_largest_army(a_player):
    player_has_largest_army = False
    counter = 0
    index = -1
    #First check if anybody currently has the largest army
    for i in config.player_list:
        if i.has_largest_army == True:
            player_has_largest_army = True
            print(i.p_name + " has the largest army")
            index = counter
        counter += 1
    #Then if somebody has the largest army check if player has more knights
    #nobody has largest army check if player has 3 knights now
    if player_has_largest_army:
        if a_player.count_knights() > config.player_list[index].count_knights():
            a_player.has_largest_army = True
            a_player.p_victory_pts += 2
            config.player_list[index].has_largest_army = False
            config.player_list[index].p_victory_pts -= 2
            print(a_player.p_name + " has taken the largest army")
    else:
        if a_player.count_knights() >= 3:
            a_player.has_largest_army = True
            a_player.p_victory_pts += 2
            print(a_player.p_name + " is the first to get the largest army")

def check_longest_road(a_player):
    player_has_longest_road = False
    counter = 0
    index = -1
    #First check if anybody currently has the largest army
    for i in config.player_list:
        if i.has_longest_road == True and i.count_road() >= 5:
            player_has_longest_road = True
            print(i.p_name + " has gotten the longest road")
            index = counter
        elif i.has_longest_road == True and i.count_road() < 5:
            i.has_longest_road = False
            i.p_victory_pts -= 2
            print(i.p_name + " has lost the longest road")
        counter += 1

    if player_has_longest_road:
        if a_player.count_road() > config.player_list[index].count_road():
            a_player.has_longest_road = True
            a_player.p_victory_pts += 2
            config.player_list[index].has_largest_army = False
            config.player_list[index].p_victory_pts -= 2
            print(a_player.p_name + " has taken the longest road")
    else:
        if a_player.count_road() >= 5:
            a_player.has_largest_army = True
            a_player.p_victory_pts += 2
            print(a_player.p_name + " is the first to get the largest road")

def play_dev_card(a_player, dev_card):
    # Partially Implemented
    if dev_card.card_type == "Knight":
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)
        move_robber()
        a_player.p_played_dev_cards.append(dev_card)
        a_player.p_dev_cards.remove(dev_card)
        check_largest_army(a_player)
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
        while roads_placed < 2:
            road = items.build_road(a_player)
            # have to check they built a valid road. function can return None.
            if road == None:
                continue
            else:
                roads_placed += 1

        a_player.p_played_dev_cards.append(dev_card)
        a_player.p_dev_cards.remove(dev_card)

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

        a_player.p_played_dev_cards.append(dev_card)
        a_player.p_dev_cards.remove(dev_card)

    #DONE
    elif dev_card.card_type == "Monopoly":
        print(a_player.p_name + " played a development card: ", end='')
        print(dev_card)
        got_resources = False
        while got_resources == False:
            wanted_card = input("What resource would you like to steal from all other players? ")
            if wanted_card.upper() in "BLSWO":

                num_taken = 0
                for p in config.player_list: # wait, this actually takes cards from the player using it too, since they're in player list. I guess that's okay if i add them back?
                    for resource in p.p_hand:
                        if resource == wanted_card.upper():
                            p.p_hand.remove(resource)
                            num_taken += 1

                for num in range(0, num_taken):
                    a_player.p_hand.append(wanted_card.upper())

                print(a_player.p_name + " took everyone's " + wanted_card.upper())
                got_resources = True

            else:
                print(wanted_card + " is not a valid resource")

        a_player.p_played_dev_cards.append(dev_card)
        a_player.p_dev_cards.remove(dev_card)


    #DONE
    elif dev_card.card_type == "Victory Point":
        a_player.p_victory_pts += 1 # I don't want to tell anyone else that this was played.
        a_player.p_played_dev_cards.append(dev_card)
        a_player.p_dev_cards.remove(dev_card)
        return False

    else:
        print("Not a known development card type")

    return True

def player_choose_color(color_options):
        print("Which color will you be?")
        i = 1
        for c in color_options:
            print("\t" + str(i) + ". " + c)
            i += 1
        try:
            choice = int(input("Chose the number of the color you'd like.\n> "))
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
            num_to_discard = math.ceil(len(i.p_hand)/2)
            discard = ""
            has_cards = False
            while len(discard) != num_to_discard or has_cards == False:
                print(i.p_name + " this is your current hand: ")
                i.show_hand()
                discard = input(i.p_name + " Please discard " + str(num_to_discard) + " cards\n> ")
                if len(discard) > num_to_discard:
                    print("You have discarded more cards than necessary.")

                elif len(discard) < num_to_discard:
                    print("You didn't discard enough cards... try again.")

                if i.p_hand.count("O") >= list(discard).count("O") and i.p_hand.count("B") >= list(discard).count("B") and i.p_hand.count("S") >= list(discard).count("S") and i.p_hand.count("W") >= list(discard).count("W") and i.p_hand.count("L") >= list(discard).count("L"):
                    has_cards = True
                    print("You have those cards")
                else:
                    has_cards = False
                    print("You do not have those cards")
            for card in discard:
                i.p_hand.remove(card.upper())
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

def trade_using_port(player):
    port = False
    player_ports = []
    for i in config.port_list:
        if i.is_player_on(player):
            player_ports.append(i)
            port = True
    if port:
        try:
            selection = -1
            while selection < 0 or selection > len(player_ports):
                print('''
Please select a port to trade with:
0   to go back to main menu''')
                count = 1
                for i in player_ports:
                    print(str(count) + "   " + i.type + " Port")
                    count+=1
                    selection = int(input())
                if selection == 0:
                    return

            want = input("What resource would you like?\n> ")
            if player_ports[selection-1].type == "3":
                give = input("What resource will you be trading 3 of?\n> ")
                r = give*3
                if player.has_resources(r):
                    player.p_hand.remove(give.upper())
                    player.p_hand.remove(give.upper())
                    player.p_hand.remove(give.upper())
                    player.p_hand.append(want.upper())
                else:
                    print("You do not have enough resources")
            else:
                r = player_ports[selection-1].type*2
                if player.has_resources(r):
                    player.p_hand.remove(player_ports[selection-1].type)
                    player.p_hand.remove(player_ports[selection-1].type)
                    player.p_hand.append(want.upper())
                else:
                    print("You do not have enough resources")
        except:
            print("An error has occurred please try again")
    else:
        print("You are not on any ports")



def trade_accepted(player, trade_to, want, offer):
    print(trade_to.p_name + ", " + player.p_name + " has offered you:" )
    print(offer)
    print("In exchange for:")
    print(want)
    choice = ""
    while choice == "":
        choice = input("Do you want to accept this trade? (y/n)\n> ")
        if choice not in "yn":
            print("You must enter 'y' or 'n'")
            choice = ""
            continue

    if choice == "y":
        return True
    elif choice == "n":
        return False

def player_turn(player, points_to_win):
    print(player.p_name + " it is your turn")

    user_input = input("Press Enter to Roll Die")

    roll = config.roll_dice()
    print(str(roll) + " has been rolled")
    items.give_resources(roll)

    #Check to see if robber() should be called
    if roll == 7:
        robber()

    has_played_dev_card = False
    for i in player.p_dev_cards:
        i.can_be_played = True

  #Player Selects an Option
    selection = -1
    while selection != 0:
        player_menu()
        try:
            selection = int(input("Please Select One\n"+ player.p_name + "> "))
        except ValueError:
            print("You must enter a number corresponding to an option")
            selection = -1

        if selection == 1:
            player.show_hand()

        elif selection == 2:
            items.build_road(player)
            check_longest_road(player)

        elif selection == 3:
            items.build_settlement(player)

        elif selection == 4:
            items.build_city(player)

        elif selection == 5:
            items.build_dev_card(player)

        # Partially implemented
        elif selection == 6:
            try:
                print("Players:")
                counter  = 1
                for p in config.player_list:
                    print("\t" + str(counter) + ". " + p.p_name)
                    counter += 1
                print("\t" + str(counter) + ". Offer trade to everyone")
                option = int(input("Who do you want to trade with?")) # gonna have to do error checking on this too...
                trade_to = config.player_list[option-1]
                want = input("What resource(s) do you want?")
                offer = input("What resource(s) are you offering in exchange?\n> ").upper()

                if option <= len(config.player_list):
                    if player.has_resources(offer):
                        want_to_trade = trade_accepted(player, trade_to, want, offer)
                        they_have_resources = trade_to.has_resources(want)
                        if want_to_trade and they_have_resources:
                            trade_resources(player, trade_to, want, offer)
                    else:
                        print("You don't have those resources to offer...")
                elif trade_to == len(player_list) + 1:
                    print("Trade to all players is coming soon")
                else:
                    print("Invalid option")
            except:
                print("Something went wrong")
        elif selection == 7:
            try:
                want = input("What resource would you like?\n> ")
                give = input("What resource will you be trading 4 of?\n> ")
                r = give*4
                if player.has_resources(r) and want.upper() in "WSLBO":
                    player.p_hand.remove(give)
                    player.p_hand.remove(give)
                    player.p_hand.remove(give)
                    player.p_hand.remove(give)
                    player.p_hand.append(want)
                    print("You traded with the bank!")

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
                    print("You don't have enough of that resource to trade...")
            except:
                print("You entered an invalid input")

        elif selection == 8:
            print("Trade using a port")
            trade_using_port(player)

        elif selection == 9:
            print(config.show_board())

        elif selection == 10:
            print("Here are your dev cards:")
            player.show_dev_cards()
            print("Here are your played dev cards:")
            player.show_played_dev_cards()

        elif selection == 11:
            try:
                if has_played_dev_card == False:
                    if player.p_dev_cards == []:
                        print("You have no development cards!!")
                        continue
                    print("Please select a dev_card: ")
                    player.show_dev_cards()
                    num = int(input("> "))
                    if player.p_dev_cards[num-1].can_be_played:
                        has_played_dev_card = play_dev_card(player, player.p_dev_cards[num-1])
                    else:
                        print("A dev card can't be placed the same turn you draw it")
                else:
                    print("You've already played a dev card this round")
            except:
                print("something went wrong")
        elif selection == 0:
            pass


        # I don't know if this check actually works.

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
        print(config.show_board())
        print(i.p_name + " is placing their first road")
        items.build_road(i, True)
        print(config.show_board())
    for i in reversed(config.player_list):
        print(i.p_name + " is placing their second settlement")
        items.build_settlement(i, True)
        print(config.show_board())
        print(i.p_name + " is placing their second road")
        items.build_road(i, True)
        print(config.show_board())

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


> ''')
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
        num_players = int(input("Please enter the number of players\n> "))
        i = 0
        color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]

        while i < num_players:
            name = input("Please Enter Player " + str((i + 1)) + "'s Name\n> ")
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
        return int(input("Enter the Amount of Points Required to Win\n> "))
    except ValueError:
        print("You must provide an integer")

def player_order():
    for player in config.player_list:
        input(player.p_name + " please roll to see order to place settlements (Press Enter)")
        player.p_order = config.roll_dice()
        print(player.p_name + ", you rolled a: " + str(player.p_order))
    config.player_list = sorted(config.player_list, key=lambda x: x.p_order, reverse = True)

    print("The order of players is:")
    for i in config.player_list:
        i.present()
    return




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


    #for i in config.road_list:
        #print(i)
    # Players Connected: _#_

    # assume they chose 1.

    #Setup the game and return player_list and amount of points to win

    # need player list accessible across all modules
    # ask players for their name and color choice
    result = get_player_info()
    while result == None:
        result = get_player_info()

    player_order()

    # establish points to win
    points_to_win = declare_pts_to_win()
    while points_to_win == None:
        points_to_win = declare_pts_to_win()


    print("Here is the Board:")
    print(config.show_board())

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
        if winner:
            break
        curr_player_turn = increment_player_turn(curr_player_turn, len(config.player_list))

    print("WINNER: " + config.player_list[curr_player_turn].p_name)


  # accept connections
  # first menu
  # set options
  # create board
  # create players

  # while winner != 1:
    #player_turn
    #check_win
