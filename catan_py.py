
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


#========================================================
# FUNCTION DECLARATIONS
#========================================================

def robber():
    print("Robber has been called")

    # Loop checks to see if any players have 7 or more cards
    for i in player_list:
        if len(i.p_hand) >= 7:
            print(i.p_name + " Please discard half your cards")



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
        0. End Turn
'''
    )

def player_turn(player, points_to_win):
    print(player.p_name + " it is your turn")

    user_input = input("Press Enter to Roll Die")

    roll = catan_classes.roll_dice()

    print(str(roll) + " has been rolled")

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
            build_road(player)

        elif selection == 3:
            build_settlement(player)

        elif selection == 4:
            build_city(player)

        elif selection == 5:
            build_dev_card(player)

        elif selection == 6:
            print("Trade with Player")

        elif selection == 7:
            print("Trade with bank")

        elif selection == 8:
            print("Trade using a port")

        if (player.show_victory_pts() >= points_to_win):
            return True
    return False

#========================================================
# START OF GAME
#========================================================


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

    while i < num_players:
        name = input("Please Enter Player " + str((i + 1)) + "'s Name\n")
        # give player a list of color options
        color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]
        color = input("What color will you be?\n") 
        color = color[0].lower()
        player_list.append(catan_classes.Player(name,color))
        i+=1

# most of this should be wrapped up in a "setup" function
    points_to_win = int(input("Enter the Amount of Points Required to Win\n"))

    return (player_list, points_to_win)

  #Debug Purpose
  #console.log(selection + "\n");





#If 7 is rolled then robber effects players with more than 7 cards and blocked tile

# PSEUDO CODE
'''
//my_tile = new Tile("W", 5);
//console.log(my_tile.present());
// their methods can be accessed like this.
//card.present();

/*
console.log(
`   _____
  /     \\
 /       \\
(    ` + "W" + `    )
 \\       /
  \\_____/`);
/*
function main(){
    main_menu(num_players, points_to_win)
    create_board(size) // Create the board itself, with tiles that have a letter for the resource and number for the probability
    display_board(board) // Draw the board on screen
    setup_board() // players pick their initial locations and get their resources
    int winner = 0;
    while (winner != 1){
        player_turn()
        winner = check_win()
    }
    print("Player %s is the winner", player)
}
function player_turn(){
    print("press r and hit enter to roll.")
    int rolled;
    rolled = roll_dice();
    if rolled == 7{
        robber()
    }
    else{
        give_out_resources() // give everyone their cards
    }
    int user_response;
    user_response = player_menu(); // show them their options now.
    if user_response == 0{
        show_hand(player)
    }
}
function player_menu(){
    print:
        1. View your hand
        2. Buy a road
        3. Buy a settlement
        4. Upgrade a settlement to a city
        5. Buy a development card
        6. Trade with a player
        7. Trade with the bank (4 for 1)
        8. Trade using a port
}
show_hand(player)
robber()

We need to figure out how we're going to describe where people want to place their roads and where they want to place their settlements
I think we should specify which corners of a tile are open with "O" for open.
I think we need some colors in this game, even though its a terminal... can we do that?
How else will we specify who has a corner? Is the first letter of the player name okay? What if there are two players with the same name?
Wouldn't that be confusing with the resources?

What will clients send?

How do i draw multiple tiles? I think I might just have 2 defined board sizes, and just populate the board randomly at the start of the game.

How am i going to determine if a road is valid?
if a player has a settlement at the starting node of the road
    - if n1.owned_by == Player setting road:
        return True
or
if the player has a road that touches the start node
    - iterate over the adjacencies and see if there's a road that has the player's id on it
        if any other road.owned_by == Player setting road
        return True
'''
if __name__ == "__main__":
    #Setup the game and return player_list and amount of points to win
    game_specifications = setup()

    #Store player_list and points to win in variables
    player_list = game_specifications[0]
    points_to_win = game_specifications[1]
    curr_player_turn = 0

    winner = False

    while winner == False:

        #Declare whos turn it is in the game
        winner = player_turn(player_list[curr_player_turn], points_to_win)

        curr_player_turn = increment_player_turn(curr_player_turn, len(player_list))


  # accept connections
  # first menu
  # set options
  # create board
  # create players

  # while winner != 1:
    #player_turn
    #check_win
