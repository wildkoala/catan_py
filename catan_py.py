
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


def increment_player_turn():
  current_player_turn = (current_player_turn + 1) % num_players


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
'''
    )

def player_turn(a_player):
  user_input = input("Press Enter to Roll Die")
  roll = roll_dice()
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
      a_player.show_hand()
    
    elif selection == 2:
      build_road(a_player)
  
    elif selection == 3:
      build_settlement(a_player)
    
    elif selection == 4:
      build_city(a_player)
    
    elif selection == 5:
      build_dev_card(a_player)


#========================================================
# START OF GAME
#========================================================


def setup():
  # this should be a function
  
  num_players = int(input("Please enter the number of players\n"))
  player_list = [] # this will be a list of Player objects
  i = 0
  while i < num_players:
    name = input("Please Enter Player " + str((i + 1)) + "'s Name\n")
    player_list.append(classes.Player(name))
    i+=1

# most of this should be wrapped up in a "setup" function
  points_to_win = int(input("Press Enter the Amount of Points Required to Win\n"))

  winner = 0
  current_player_turn = 0

  my_card = classes.Card("B") # need the classes file for this to be defined
  player_list[0].add_card(my_card)
  player_list[0].add_card(my_card)
  player_list[0].add_card(my_card)

  my_card2 = classes.Card("L")
  player_list[0].add_card(my_card2)
  player_list[0].add_card(my_card2)
  player_list[0].add_card(my_card2)
  player_list[0].add_card(my_card2)

  my_card3 = classes.Card("C")
  player_list[0].add_card(my_card3)


  while(winner == 0):
    if player_list[current_player_turn].show_victory_pts() >= points_to_win:
      print(player_list[current_player_turn].present() + " wins")
      winner = 1

    # this should be part of the player_turn function
    print(player_list[current_player_turn].p_name + " it is your turn")

    player_turn(player_list[current_player_turn])
    
    #Increments to the next player
    increment_player_turn()

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

'''
if __name__ == "__main__": 
  setup()