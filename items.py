#========================================================
# FILE PURPOSE: 
#   - This file contains all functions necessary to create a new "physical" item in catan
#========================================================

# POSSIBLE RESOURCES: Ore, Wheat, Brick, Lumber, Sheep

#========================================================
# Requirements and Exports
#========================================================
from catan_classes import *
#========================================================
# FUNCTION DEFINITIONS
#========================================================

# need globally accessible list of nodes
# need globally accessible list of roads
#node_list = create_nodes() # this doesnt work?
#road_list = create_roads(node_list) # this doesnt work?

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
def road_is_connected(player_id, n1, n2):
	if n1.owns_node == player_id: 
		return True
	else:
		for adj in n1.adj_nodes:
			if get_road_by_nodes(n1,n2).owns_road == player_id:
				return True
		return False


# partially implemented
# need get_road_by_nodes(alias, alias)
# need road_is_valid(Player, Node.alias, Node.alias)
def build_road(a_player):
	have_resources = has_needed_resources("road", a_player)
	if have_resources:
		# ask for the two nodes they want to build a road between
		n1 = input("Give the location of the start of the road")
		n2 = input("Give the location of the end of the road")

		# node1 = # take an alias and get back the id
		# node2 = # take an alias and get back the id

		# i need all the roads to be initialized in between all the nodes.
		r = get_road_by_nodes(n1, n2)
		is_open = not r.is_owned # i think this is valid, but not sure
		is_connected = road_is_connected(a_player, n1, n2)

		if is_open and is_connected:
			r.owns_node = a_player.id

		
	else:
		console.log("Not enough resources to build a road!!")
  
  # Space is open
  # It's connected to another road or settlement

# partially implemented
# the intial setup will probably not work with this function.

def build_settlement(a_player):
  have_resources = has_needed_resources("settlement", a_player)
  if (have_resources):
    print("building a settlement")
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
    b = 0
    l = 0
    for card in a_player.p_hand:
      if card.resource == "B":
        b+=1
      if card.resource == "L":
        l+=1
      
    if (b > 0 and l > 0):
      return True
    else:
      return False
    
  
  elif (item == "settlement"):
    # Check that they have 1 sheep, wheat, brick, and lumber
    b = 0
    l = 0
    s = 0
    w = 0

    for card in a_player.p_hand:
      if card.resource == "B":
        b+=1
      if card.resource == "L":
        l+=1
      if card.resource == "W":
        w+=1
      if card.resource == "S":
        s+=1
      
    
    if (b > 0 and l > 0 and w > 0 and s > 0):
      return True
    
    else:
      return False


  elif (item == "city"):
    # Check that they have 2 wheat, 3 ore
    o = 0
    w = 0
    for card in a_player.p_hand:
      if card.resource == "O":
        o+=1 
      elif card.resource == "W":
        w+=1    
      
    
    if (o > 2 and w > 1):
      return True
    else:
      return False

  elif (item == "dev_card"):
    # Check they have 1 sheep, ore and wheat
    o = 0
    w = 0
    s = 0
    counter = 0

    for card in a_player.p_hand:
      if card.resource == "O":
        o+=1
      elif card.resource == "W":
        w+=1
      elif card.resource == "S":
        s+=1

    if (o > 0 and w > 0 and s > 0):
      return True
    else:
      return False



