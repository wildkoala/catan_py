#========================================================
# FILE PURPOSE: 
#   - This file contains all functions necessary to create a new "physical" item in catan
#========================================================

# POSSIBLE RESOURCES: Ore, Wheat, Brick, Lumber, Sheep

#========================================================
# Requirements and Exports
#========================================================
import catan_classes

#========================================================
# FUNCTION DEFINITIONS
#========================================================

# need globally accessible list of nodes
# need globally accessible list of roads
node_list = catan_classes.init_nodes() # this doesnt work?
road_list = catan_classes.create_roads(node_list) # this doesnt work?

#this function works, but it needs a node list and alias as a tuple ex. (1,6)
def get_node_by_alias(node_list, g_alias):
	for n in node_list:
		if g_alias in n.alias:
			return n.id

#this function works, but it needs the node list, road list and the aliases as tuples (tile,corner)
def get_road_by_nodes(node_list, road_list, alias1, alias2):
	n1 = get_node_by_alias(node_list, alias1)
	n2 = get_node_by_alias(node_list, alias2)
	if n1 < n2:
		for r in road_list:
			if r.start_n == n1 and r.end_n == n2:
				return r
	else:
		for r in road_list:
			if r.start_n == n2 and r.end_n == n1:
				return r


# player.id this will have to be added to player. it's their icon on the map
def road_is_connected(player_color, n1, n2):
	if n1.owns_node.lower() == player_color: # lower makes sure that a city counts too.
		return True
	else:
		for adj in n1.adj_nodes:
			if get_road_by_nodes(n1,n2).owns_road == player_color:
				return True
		return False

def build_road(a_player):
	have_resources = has_needed_resources("road", a_player)
	if have_resources:
		# ask for the two nodes they want to build a road between
		n1 = input("Give the location of the start of the road") #"1,6"
		n2 = input("Give the location of the end of the road") #"1,5"
		
		n1 = n1.split(",")
		n1 = tuple(n1)

		n2 = n2.split(",")
		n2 = tuple(n2)
		
		r = get_road_by_nodes(n1, n2)
		is_open = not r.is_owned # i think this is valid, but not sure
		is_connected = road_is_connected(a_player.player_color, n1, n2)

		if is_open and is_connected:
			r.owns_node = a_player.id
			print(a_player.p_name + "has placed down a road!")
			#remove the cards that the player spent
			a_player.p_hand.remove("B")
			a_player.p_hand.remove("L")

		else:
			print("That space is already taken, or you're not connected to that road")
		
	else:
		print("Not enough resources to build a road!!")


# partially implemented
# the intial setup will probably not work with this function.
def build_settlement(a_player):
	have_resources = has_needed_resources("settlement", a_player)
	if (have_resources):
		# check if that settlement is open
		n1 = int(input("Where do you want to place your settlement?")) #1

		#ensure that the adjacent nodes don't have a settlement or city


	else:
		print("Not enough resources to build a settlement!!")

	# Space is open
	# no one is on an adjacent territory


# partially implemented
def build_city(a_player):
	have_resources = has_needed_resources("city", a_player)
	if have_resources:
		print("building a city")
	else:
    	print("Not enough resources to upgrade into a city!!") 
# Have a settlement
# It is a settlement, and not anything else


# partially implemented
def build_dev_card(a_player):
	have_resources = has_needed_resources("dev_card", a_player)
	if have_resources:
		print("here's a dev card")
	else:
		print("Not enough resources to get dev card!!")
  


# CHECK FOR RESOURCES TO GET ITEMS
def has_needed_resources(item, a_player):
	if item == "road":
		# Check that they have 1 brick and lumber
		hand = a_player.p_hand
		if (hand.count("B") > 0 and hand.count("L") > 0):
			return True
		else:
			return False
  
	elif (item == "settlement"):
	# Check that they have 1 sheep, wheat, brick, and lumber
      	hand = a_player.p_hand
		if (hand.count("S") > 0 and hand.count("L") > 0 and hand.count("W") > 0 and hand.count("B") > 0):
			return True
		else:
			return False


	elif (item == "city"):
	# Check that they have 2 wheat, 3 ore
		hand = a_player.p_hand
		if (hand.count("O") > 2 and hand.count("W") > 1):
			return True
		else:
			return False

	elif (item == "dev_card"):
	# Check they have 1 sheep, ore and wheat
		hand = a_player.p_hand
		if (hand.count("O") > 0 and hand.count("W") > 0 and hand.count("S") > 0):
			return True
		else:
			return False



