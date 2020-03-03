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
import itertools

#========================================================
# FUNCTION DEFINITIONS
#========================================================

def is_valid_location(alias):
    try:
        if alias[0] < 1 or alias[0] > 19:
            return False
        elif alias[1] < 1 or alias[1] > 6:
            return False
        else:
            return True
    except:
        print("User inputted an int and broke the is_valid_location function")
#this function works, takes a node list and alias as a tuple ex. (1,6)
def get_node_by_alias(g_alias, node_list):
    for n in node_list:
        if g_alias in n.alias:
            return n
    print("NO MATCH FOUND")

def get_node_by_id(n, node_list):
    for a in node_list:
        if a.id == n:
            return a

#this function works, takes a node list and alias as a tuple ex. (1,6)
def get_road_with_aliases(alias1, alias2, node_list, road_list):
    n1 = get_node_by_alias(alias1,node_list)
    n2 = get_node_by_alias(alias2, node_list)
    for r in road_list:
        if r.start_n == n1.id and r.end_n == n2.id:
            return r
        else:
            if r.start_n == n2.id and r.end_n == n1.id:
                return r
    print("COULDN'T FIND ROAD")

def get_road_with_nodes(node1, node2, road_list):
    #print("Here to debug 1")
    for r in road_list:
        #print("Here to debug 2")
        if r.start_n == node1.id and r.end_n == node2.id:
            return r
        else:
            if r.start_n == node2.id and r.end_n == node1.id:
                return r
    #print("COULDN'T FIND ROAD")

def get_road_by_id(id):
    for r in config.road_list:
        if id == r.id:
            return r

def get_nodes_by_road(road):
    n1 = config.node_list[road.start_n - 1]
    n2 = config.node_list[road.end_n - 1]
    return [n1,n2]

#I need to somehow check to see if a player branches a road rather than extends it
#Currently any roads attached and not broken will be merged so length of 2 roads
#will be considered as 3 sometimes etc.

#This returns true if I need to branch a players roads
#Now i need to create 3 lists that are unmergable
def does_road_branch(a_player, placed_road):
    nodes = get_nodes_by_road(placed_road)
    for placed_node in nodes:
        counter = 0
        for adj_nodes in placed_node.adj_nodes:
            tested_road = get_road_with_nodes(placed_node, config.node_list[adj_nodes-1])
            if a_player.p_color == tested_road.owns_road:
                counter += 1
        if counter == 3:
            print("I need to branch the player road list here")
            print(str(placed_node.id) + " is the node where i must branch")
            return get_node_by_alias(placed_node.id)
    return None

#Calculates a players road chains based on breaks in roads and placement of roads
def merge_chain(a_player):
    if len(a_player.road_chains) >= 2:
        for i in range(0,(len(a_player.road_chains)-1)):
            complist = a_player.road_chains[i]
            for j in range(i+1,len(a_player.road_chains)):
                complist2 = a_player.road_chains[j]
                if are_connected_roads(a_player, complist, complist2):
                    a_player.road_chains.append(a_player.road_chains[i] + a_player.road_chains[j])
                    a_player.road_chains.remove(complist)
                    a_player.road_chains.remove(complist2)
                    return True
    print(a_player.road_chains)
    return False

#This function will split a player's road
def split_road(a_player, node):
    new_list = []
    for i in a_player.road_chains:
        for roads in i:
            new_list.append([roads])
    a_player.road_chains = new_list
    keep_merging = True
    while keep_merging:
        keep_merging = merge_chain(a_player)


#Called when a player places a road. gets the end node of the road placed
#and finds other two roads associated with that node. if both roads are owned by
#a particular player. we know that his road has been split
def does_split_road(a_player, placed_road):
    nodes = get_nodes_by_road(placed_road)
    for placed_node in nodes:
        player = ""
        counter = 0
        for adj_nodes in placed_node.adj_nodes:
            tested_road = get_road_with_nodes(placed_node, config.node_list[adj_nodes-1])
            if player != "":
                    counter += 1
            else:
                if tested_road.owns_road != a_player.p_color and tested_road.owns_road != "":
                    player = tested_road.owns_road
                    counter += 1
        if counter == 2:
            for i in config.player_list:
                if i.p_color == player:
                    i.split_roads.append(placed_node.id)
                    split_road(i, placed_node)
    pass
    #

#Currently very messy but it works fine.  the 4 for loops hurt me spiritually
def are_connected_roads(a_player, list1, list2):
    for r1 in list1:
        for r2 in list2:
            n1 = get_nodes_by_road(get_road_by_id(r1))
            n2 = get_nodes_by_road(get_road_by_id(r2))
            for node1 in n1:
                for node2 in n2:
                    if node1.id in a_player.split_roads and node1.id == node2.id:
                        return False
                    if node1.id == node2.id:
                        return True
    return False

def connected_roads(node):
    roads = [] # a list of connected roads.
    for adj in node.adj_nodes:
        roads.append(get_road_with_nodes(node, node_list[adj-1], road_list))
    return roads

# NEEDS TESTING FOR ADJACENT ROADS
# takes player_color and the nodes on either side of the desired road.
def road_is_connected(player_color, n1, n2, node_list, road_list):
    print("IN ROAD IS CONNECTED FUNCTION")
    if n1.owns_node.lower() == player_color: # lower makes sure that a city counts too.
        return True
    else: # this is the part of the code that needs to check for an adj road.
        for r in connected_roads(n1, node_list, road_list):
            if r.owns_road == player_color:
                return True
        for r in connected_roads(n2, node_list, road_list):
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
# return a string if it works properly, return int if there's an error.
def build_road(a_player, n1, n2, node_list, road_list, initializing = False): # this is not working for having a road connected to another road, makes you have a connected settlement rn.
    if initializing:

        alias1 = convert_input_to_format(n1) # n1 and n2 are strings
        alias2 = convert_input_to_format(n2)

        if isinstance(alias1, int) or isinstance(alias2, int):
            return -1

        if is_valid_location(alias1) == False:
            return -1
        n1 = get_node_by_alias(alias1, node_list)

        if n1.owns_node == a_player.p_color or n2.owns_node == a_player.p_color:
            wanted_road = get_road_with_nodes(n1, n2, road_list)
            if wanted_road is None:
                return -1
            elif wanted_road.owns_road != "":
                return -2

            else:
                wanted_road.owns_road = a_player.p_color
                return "Road added!!!"

                a_player.road_chains.append([wanted_road.id])
                val = merge_chain(a_player)
                if val:
                    val = merge_chain(a_player)
                does_split_road(a_player, wanted_road)
                if does_road_branch(a_player, wanted_road):
                    print("You idiot branch here")

        else:
            return -5

    else:
        have_resources = has_needed_resources("road", a_player)
        if have_resources:
            # ask for the two nodes they want to build a road between
            alias1 = convert_input_to_format(n1) # n1 and n2 are strings
            alias2 = convert_input_to_format(n2)

            if isinstance(alias1, int) or isinstance(alias2, int):
                return -1

            if is_valid_location(alias1) == False:
                return -1
            n1 = get_node_by_alias(alias1, node_list)

            if is_valid_location(alias2) == False:
                return -1
            n2 = get_node_by_alias(alias2, node_list)

            #Checking to see if it's connected to one of your settlements or a road that the player has
            #road_is_connected checks for both.
            if road_is_connected(a_player.p_color, n1, n2, node_list, road_list):
                wanted_road = get_road_with_nodes(n1, n2, road_list)
                if wanted_road is None:
                    return -1
                elif wanted_road.owns_road != "":
                    return -2

                else:
                    wanted_road.owns_road = a_player.p_color
                    a_player.p_hand.remove("B")
                    a_player.p_hand.remove("L")
                    return "Road added!!!"
                    does_split_road(a_player, wanted_road)

                    branch_this_road = does_road_branch(a_player, wanted_road)
                    if branch_this_road != None:
                        print("You idiot branch here")

            else:
                return -5
        else:
            return -6


def convert_input_to_format(given_input): # takes string, returns tuple of ints
    try:
        output = given_input.split(",")
        output = [ int(x) for x in output]
        output = tuple(output)
        return output
    except ValueError:
        return -4


# partially implemented
# returns string when it worked, int when ther was an error.
def build_settlement(a_player, location, node_list, initializing = False):

    if initializing:
        #try:
        # Is that a legit location on the map?
        n1 = convert_input_to_format(location)
        if isinstance(n1, int):
            return n1
        if not is_valid_location(n1):
            return -1

        wanted_node = get_node_by_alias(n1, node_list)
        i = node_list.index(wanted_node)

        # Is this already taken?
        if node_list[i].owns_node != "":
            return -2

        for n in node_list[i].adj_nodes: #list of id's
            neighbor = get_node_by_id(n, node_list)
            neighbor_i = node_list.index(neighbor)
            if node_list[neighbor_i].owns_node != "":
                return -3

        # Okay, you're able to put down a settlement.
        node_list[i].owns_node = a_player.p_color
        a_player.p_victory_pts += 1
        return "Successfully placed settlement!"

        #except ValueError:
        #    return -4


    else:
        have_resources = has_needed_resources("settlement", a_player)
        if have_resources:

            # Is that a legit location on the map?
            n1 = convert_input_to_format(location)
            if isinstance(n1, int):
                return n1
            if not is_valid_location(n1):
                return -1
            wanted_node = get_node_by_alias(n1, node_list)
            i = node_list.index(wanted_node)

            # Is this already taken?
            if node_list[i].owns_node != "":
                return -2

            # Are there any settlements adjacent to this?
            for n in node_list[i].adj_nodes: #list of id's
                neighbor = get_node_by_id(n, node_list)
                neighbor_i = node_list.index(neighbor)
                if node_list[neighbor_i].owns_node != "":
                    return -3
            # Okay, you're able to put down a settlement
            wanted_node.owns_node = a_player.p_color
            a_player.p_hand.remove("B")
            a_player.p_hand.remove("L")
            a_player.p_hand.remove("S")
            a_player.p_hand.remove("W")
            a_player.p_victory_pts += 1
            return a_player.p_name + "has placed down a settlement!"

        else:
            return -6

# partially implemented
def build_city(a_player,location,node_list):
    have_resources = has_needed_resources("city", a_player)
    if have_resources:
        #print("building a city")
        # check that a player has a settlement at that location

        alias = convert_input_to_format(location)
        if not is_valid_location(alias):
                return -1
        wanted_node = get_node_by_alias(alias, node_list)

        # needs to specifically be a lower case letter.
        if wanted_node.owns_node == a_player.p_color:
            #print("building a city")

            wanted_node.owns_node = a_player.p_color.upper()
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("W")
            a_player.p_hand.remove("W")
            a_player.p_victory_pts += 1
            return a_player.p_name + " has placed down a city!\n"

        elif wanted_node.owns_node == a_player.p_color.upper():
            return -7
        elif wanted_node.owns_node != "":
            return -8
        else:
            return -1

    else:
        return -6
# Have a settlement
# It is a settlement, and not anything else


# partially implemented
#returns string if working, int if error.
def build_dev_card(a_player, dev_cards):
    have_resources = has_needed_resources("dev_card", a_player)
    if have_resources:
        #print("here's a dev card")
        a_player.p_hand.remove("O")
        a_player.p_hand.remove("S")
        a_player.p_hand.remove("W")
        a_player.p_dev_cards.append(dev_cards.pop())
        return a_player.p_name + " bought a development card!\nDevelopment Card: " + a_player.p_dev_cards[-1].card_type

    else:
        return -6



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



def get_corners(tile_id, node_list):
    corners = []
    n1 = get_node_by_alias((tile_id, 1), node_list)
    n2 = get_node_by_alias((tile_id, 2), node_list)
    n3 = get_node_by_alias((tile_id, 3), node_list)
    n4 = get_node_by_alias((tile_id, 4), node_list)
    n5 = get_node_by_alias((tile_id, 5), node_list)
    n6 = get_node_by_alias((tile_id, 6), node_list)

    corners = []
    corners.append(n1)
    corners.append(n2)
    corners.append(n3)
    corners.append(n4)
    corners.append(n5)
    corners.append(n6)
    return corners

# Return a string to be sent to the user
def give_resources_to_players(corners, resource, player_list):
    msg_to_user = ""
    for n in corners:
        if not n.is_empty():
            if n.is_settlement():
                for p in player_list:
                    if n.owns_node == p.p_color:
                        p.p_hand.append(resource) # need to know what tile this is.
                        msg_to_user += p.p_name + " got a " + resource + "\n"# need to know what tile this is.
            else:
                msg_to_user = ""
                for p in player_list:
                    if n.owns_node == p.p_color:
                        p.p_hand.append(resource) # need to know what tile this is.
                        p.p_hand.append(resource)
                        msg_to_user += p.p_name + " got 2 " + resource + "\n"# need to know what tile this is.
    return msg_to_user


# Return a string to be sent to the user
def give_resources(roll_num, robber, b, player_list, node_list, initial = False):
    msg_to_user = "\n"
    for t in b.tiles:
        if initial:
            corners = get_corners(t.id, node_list)
            msg_to_user += give_resources_to_players(corners,t.resource, player_list)

        elif roll_num == 7:
            # when the robber gets rolled I still need to return
            return ""

        elif t.number == roll_num:
            if t.id == robber.on_tile:
                return "The robber stole your " + t.resource + "!!"
            else:
                corners = get_corners(t.id, node_list)
                msg_to_user += give_resources_to_players(corners,t.resource, player_list)

    return msg_to_user
