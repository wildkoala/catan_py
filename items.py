#========================================================
# FILE PURPOSE:
#   - This file contains all functions necessary to create a new "physical" item in catan
#========================================================

#========================================================
# BUGS: some functions only have n set as a node id instead of a node object.
#========================================================

# POSSIBLE RESOURCES: Ore, Wheat, Brick, Lumber, Sheep

#========================================================
# Requirements and Exports
#========================================================
import catan_classes
import config

#========================================================
# FUNCTION DEFINITIONS
#========================================================

def is_valid_location(alias):
    if alias[0] < 1 or alias[0] > 19:
        return False
    elif alias[1] < 1 or alias[1] > 6:
        return False
    else:
        return True

#this function works, takes a node list and alias as a tuple ex. (1,6)
def get_node_by_alias(g_alias):
    for n in config.node_list:
        if g_alias in n.alias:
            return n

def get_node_by_id(n):
    for a in config.node_list:
        if a.id == n:
            return a

#this function works, takes a node list and alias as a tuple ex. (1,6)
def get_road_with_aliases(alias1, alias2):
    n1 = get_node_by_alias(config.node_list, alias1)
    n2 = get_node_by_alias(config.node_list, alias2)
    for r in config.road_list:
        if r.start_n == n1.id and r.end_n == n2.id:
            return r
        else:
            if r.start_n == n2.id and r.end_n == n1.id:
                return r
    print("COULDN'T FIND ROAD")

def get_road_with_nodes(node1, node2):
    #print("Here to debug 1")
    for r in config.road_list:
        #print("Here to debug 2")
        if r.start_n == node1.id and r.end_n == node2.id:
            return r
        else:
            if r.start_n == node2.id and r.end_n == node1.id:
                return r
    #print("COULDN'T FIND ROAD")

def connected_roads(node):
    roads = [] # a list of connected roads.
    for adj in node.adj_nodes:
        roads.append(get_road_with_nodes(node, config.node_list[adj-1]))
    return roads

# NEEDS TESTING FOR ADJACENT ROADS
def road_is_connected(player_color, n1, n2):
    print("IN ROAD IS CONNECTED FUNCTION")
    if n1.owns_node.lower() == player_color: # lower makes sure that a city counts too.
        return True
    else: # this is the part of the code that needs to check for an adj road.
        for r in connected_roads(n1):
            if r.owns_road == player_color:
                return True
        for r in connected_roads(n2):
            if r.owns_road == player_color:
                return True
        return False
'''
how to determine if a road is connected:

get the desired road.
    from the start_node of desired road, get all the roads coming off of it
    if any of those roads are owned by the player, it IS connected.

    now check the end_node:
        get all of the roads that come off of it.
            if any of them are owned by the player, it's connected.

'''


# Whats the point of this function?? Just use is_valid_location.
def valid_road_location(n):
    n = convert_input_to_format(n)
    if isinstance(n, int):
        return -4
    if not is_valid_location(n):
        return False
    return True


# maybe have is_init set to False by default (a keyword argument)
# need to always return an int on the build_ functions because of the error handling after.
def build_road(a_player, n1, n2, initializing = False): # this is not working for having a road connected to another road, makes you have a connected settlement rn.
    if initializing:

        alias1 = convert_input_to_format(n1) # n1 and n2 are strings
        alias2 = convert_input_to_format(n2)

        if isinstance(alias1, int) or isinstance(alias2, int):
            return -1

        if is_valid_location(alias1) == False:
            return -1
        n1 = get_node_by_alias(alias1)

        if is_valid_location(alias2) == False:
            return -1
        n2 = get_node_by_alias(alias2)

        if n1.owns_node == a_player.p_color or n2.owns_node == a_player.p_color:
            wanted_road = get_road_with_nodes(n1, n2)
            if wanted_road is None:
                return -1
            elif wanted_road.owns_road != "":
                return -2

            else:
                wanted_road.owns_road = a_player.p_color
                return 0

        else:
            return -5

    else:
        have_resources = has_needed_resources("road", a_player)
        if have_resources:
            # ask for the two nodes they want to build a road between
            n1 = input("Give the location of the start of the road\n> ") #"1,6"
            n1 = valid_road_location(n1)
            if (n1 == False):
                return

            n2 = input("Give the location of the end of the road\n> ") #"1,5"
            n2 = valid_road_location(n2)
            if (n2 == False):
                return

            is_connected = road_is_connected(a_player.p_color, n1, n2)
            wanted_road = get_road_with_nodes(n1, n2)
            if n1.owns_node == a_player.p_color or n2.owns_node == a_player.p_color or is_connected:

                if wanted_road is None:
                    #print("That's not a valid road segment... Try again.")
                    return -1
                elif wanted_road.owns_road != "":
                    #print(wanted_road.owns_road + " is already on that space!!")
                    return -2
                else:
                    wanted_road.owns_road = a_player.p_color
                    print(a_player.p_name + " has placed a road!!")
                    a_player.p_hand.remove("B")
                    a_player.p_hand.remove("L")
                    placed = True

            else:
                print("Your road must be connected to one of your settlements or roads")
        else:
            print("Not enough resources to build a road!!")
            return


def convert_input_to_format(given_input): # takes string, returns tuple of ints
    try:
        output = given_input.split(",")
        output = [ int(x) for x in output]
        output = tuple(output)
        return output
    except ValueError:
        return -4


# partially implemented
# needs to always return an int so that error handling doesn't get thrown of trying to compare a Nonetype
def build_settlement(a_player, location, initializing = False):

    if initializing:
        try:
            # Is that a legit location on the map?
            n1 = convert_input_to_format(location)
            if isinstance(n1, int):
                return n1
            if not is_valid_location(n1):
                return -1

            wanted_node = get_node_by_alias(n1)
            i = config.node_list.index(wanted_node)

            # Is this already taken?
            if config.node_list[i].owns_node != "":
                return -2

            # Are there any settlements adjacent to this?
            for n in config.node_list[i].adj_nodes: #list of id's
                neighbor = get_node_by_id(n)
                neighbor_i = config.node_list.index(neighbor)
                if config.node_list[neighbor_i].owns_node != "":
                    return -3

            # Okay, you're able to put down a settlement.
            config.node_list[i].owns_node = a_player.p_color
            a_player.p_victory_pts += 1
            return 0

        except ValueError:
            return -4


    else:
        have_resources = has_needed_resources("settlement", a_player)
        if have_resources:
            # check if that settlement is open
            n1 = input("Where do you want to place your settlement?\n> ") #1,6 for example
            n1 = n1.split(",")
            n1 = [ int(x) for x in n1]
            n1 = tuple(n1)
            if not is_valid_location(n1):
                return # Since this is in the game loop, just kick them back out to the options menu
            wanted_node = get_node_by_alias(n1)

            if wanted_node.owns_node != "":
                print(wanted_node.owns_node + " is already on that space!!")
                return #this is a NoneType

            for n in wanted_node.adj_nodes:
                if config.node_list[n-1].owns_node != "":
                    print("There's a player on an adjacent space!!")
                    return #this is a NoneType

            wanted_node.owns_node = a_player.p_color
            print(a_player.p_name + "has placed down a Settlement!")
            a_player.p_hand.remove("B")
            a_player.p_hand.remove("L")
            a_player.p_hand.remove("S")
            a_player.p_hand.remove("W")
            a_player.p_victory_pts += 1

        else:
            print("Not enough resources to build a settlement!!")

# partially implemented
def build_city(a_player):
    have_resources = has_needed_resources("city", a_player)
    if have_resources:
        print("building a city")
        # check that a player has a settlement at that location
        n1 = input("Where do you want to place your city?\n> ") #1,6 for example
        n1 = n1.split(",")
        n1 = [ int(x) for x in n1]
        n1 = tuple(n1)
        if not is_valid_location(n1):
                return # Since this is in the game loop, just kick them back out to the options menu
        wanted_node = get_node_by_alias(n1)

        # needs to specifically be a lower case letter.
        if wanted_node.owns_node == a_player.p_color:
            print("building a city")
            print(a_player.p_name + "has placed down a city!")
            wanted_node.owns_node = a_player.p_color.upper()
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("W")
            a_player.p_hand.remove("W")
            a_player.p_victory_pts += 1

        elif wanted_node.owns_node == a_player.p_color.upper():
            print("That's already a city!")
        elif wanted_node.owns_node != "":
            print(wanted_node.owns_node + " is already on that space!!")
        else:
            print("You don't have a settlement here...")

    else:
        print("Not enough resources to upgrade into a city!!")
# Have a settlement
# It is a settlement, and not anything else


# partially implemented
def build_dev_card(a_player):
    have_resources = has_needed_resources("dev_card", a_player)
    if have_resources:
        #print("here's a dev card")
        print(a_player.p_name + " bought a development card!")
        a_player.p_hand.remove("O")
        a_player.p_hand.remove("S")
        a_player.p_hand.remove("W")
        a_player.p_dev_cards.append(config.dev_cards.pop())

    else:
        print("Not enough resources to get dev card!!")



# CHECK FOR RESOURCES TO GET ITEMS
def has_needed_resources(item, a_player):
    if item == "road":
        # Check that they have 1 brick and lumber
        hand = a_player.p_hand
        if hand.count("B") > 0 and hand.count("L") > 0:
            return True
        else:
            return False

    elif item == "settlement":
        # Check that they have 1 sheep, wheat, brick, and lumber
        hand = a_player.p_hand
        if hand.count("S") > 0 and hand.count("L") > 0 and hand.count("W") > 0 and hand.count("B") > 0:
            return True
        else:
            return False

    elif item == "city":
       # Check that they have 2 wheat, 3 ore
       hand = a_player.p_hand
       if hand.count("O") > 2 and hand.count("W") > 1:
           return True
       else:
           return False

    elif (item == "dev_card"):
        # Check they have 1 sheep, ore and wheat
        hand = a_player.p_hand
        if hand.count("O") > 0 and hand.count("W") > 0 and hand.count("S") > 0:
            return True
        else:
            return False



def get_corners(tile_id):
    corners = []
    n1 = get_node_by_alias((tile_id, 1))
    n2 = get_node_by_alias((tile_id, 2))
    n3 = get_node_by_alias((tile_id, 3))
    n4 = get_node_by_alias((tile_id, 4))
    n5 = get_node_by_alias((tile_id, 5))
    n6 = get_node_by_alias((tile_id, 6))

    corners = []
    corners.append(n1)
    corners.append(n2)
    corners.append(n3)
    corners.append(n4)
    corners.append(n5)
    corners.append(n6)
    return corners

def give_resources_to_players(corners, resource):
    for n in corners:
        if not n.is_empty():
            if n.is_settlement():
                for p in config.player_list:
                    if n.owns_node == p.p_color:
                        p.p_hand.append(resource) # need to know what tile this is.
                        print(p.p_name + " got a " + resource) # need to know what tile this is.
            else:
                p.p_hand.append(t.resource)
                p.p_hand.append(t.resource)
                print(p.p_name + " got 2 " + resource)

# Need  a function for distributing resources
def give_resources(roll_num, initial = False):
    for t in config.b.tiles:
        if initial:
            corners = get_corners(t.id)
            give_resources_to_players(corners,t.resource)

        elif t.number == roll_num:
            if t.id == config.robber.on_tile:
                print("The robber stole your " + t.resource + "!!")
            else:
                corners = get_corners(t.id)
                give_resources_to_players(corners,t.resource)
