
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
import classes
import items


#========================================================
# FUNCTION DECLARATIONS
#========================================================

def robber(player_list):
  print("Robber has been called")

  # Loop checks to see if any players have 7 or more cards
  for i in player_list.length:
    if player_list[i].p_hand.length >= 7: 
      print(player_list[i].p_name + " Please discard half your cards")

def roll_dice():
    x = random.randint(1, 6) 
    y = random.randint(1, 6) 
    return x + y


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
      0. End turn
'''
    )

def player_turn(player, points_to_win):
  user_input = input("Press Enter to Roll Die\n")
  roll = roll_dice()
  print(str(roll) + " has been rolled")

  #Check to see if robber() should be called
  #if roll == 7:
    #robber()

  #Player Selects an Option
  selection = -1

  while selection != 0:
    player_menu()
    selection = int(input("Please Select One"))

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

    if (player.show_victory_pts() >= points_to_win):
      print(player.present() + " wins")
      return True
    
  return False

      


#========================================================
# START OF GAME
#========================================================


def setup():
  # this should be a function
  print("catan_py invoked directly!!")
  num_players = int(input("Press Enter the number of players\n"))
  player_list = [] # this will be a list of Player objects
  i = 0
  while i < num_players:
    name = input("Please Enter Player " + str((i + 1)) + "'s Name\n")
    player_list.append(classes.Player(name))
    i+=1

# most of this should be wrapped up in a "setup" function
  points_to_win = int(input("Press Enter the Amount of Points Required to Win\n"))

  game_requirements = (player_list, points_to_win)
  return game_requirements
  #Debug Purpose
  #console.log(selection + "\n");

def next_turn(player_list, current_player_turn):

  curr_player = player_list[current_player_turn]

  print(str(curr_player.present()) + " it is your turn\n");

  return curr_player

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

'''

if __name__ == "__main__": 
  #Run Setup of the Game
  game_specs = setup()

  current_player_turn = 0

  points_to_win = game_specs[1]

  #Save the player list in player_list array for future reference in main
  player_list = game_specs[0]

  win = False

  #Loop until somebody wins
  while(win == False):
    #specify who has the next turn in the game and return a player
    player = next_turn(player_list, current_player_turn)

    #After next turn is declared have that player perform their turn and check to see if they won at the end of their turn
    win = player_turn(player, points_to_win)

    #Increment player if nobody has won
    current_player_turn = increment_player_turn(current_player_turn, len(player_list));
    
