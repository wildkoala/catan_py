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

# need globally accessible list of nodes
# need globally accessible list of roads
#node_list = catan_classes.init_nodes() # this doesnt work?
#road_list = catan_classes.create_roads(node_list) # this doesnt work?

def is_valid_location(alias):
    if alias[0] < 1 or alias[0] > 19:
        print("You're trying to place a piece on an invalid tile.")
        print("FORMAT: tile,corner.\nEXAMPLE: 1,2")
        return False
    elif alias[1] < 1 or alias[1] > 6:
        print("You're trying to place a piece on an invalid corner.")
        print("FORMAT: tile,corner.\nEXAMPLE: 1,2")
        return False
    else:
        return True

#this function works, but it needs a node list and alias as a tuple ex. (1,6)
def get_node_by_alias(g_alias):
    for n in config.node_list:
        if g_alias in n.alias:
            return n

def get_node_by_id(n):
    for a in config.node_list:
        if a.id == n:
            return a

#this function works, but it needs the node list, road list and the aliases as tuples (tile,corner)

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
        roads.append(get_road_with_nodes(node, config.node_list[adj-1]))
    return roads

# NEEDS TESTING FOR ADJACENT ROADS
def road_is_connected(player_color, n1, n2):
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

#Checks to see if a node is a valid location for a road
#Condenses code
def valid_road_location(n):
    try:
        n = n.split(",")
        n = [ int(x) for x in n]
        n = tuple(n)
        if not is_valid_location(n):
            print("input not valid")
            return False

        n = get_node_by_alias(n)
        return n
    except:
        print("input not valid")
        return False


# maybe have is_init set to False by default (a keyword argument)
def build_road(a_player, initializing = False): # this is not working for having a road connected to another road, makes you have a connected settlement rn.

    if initializing:
        placed = False
        while not placed:
            n1 = input("Where do you want to start your road?\n> ")#1,6 for example
            n1 = valid_road_location(n1)
            if (n1 == False):
                continue

            n2 = input("Where do you want to end your road?\n> ") #1,6 for example
            n2 = valid_road_location(n2)
            if (n2 == False):
                continue

            if n1.owns_node == a_player.p_color or n2.owns_node == a_player.p_color:

                wanted_road = get_road_with_nodes(n1, n2)
                if wanted_road is None:
                    print("That's not a valid road segment... Try again.")
                    continue
                elif wanted_road.owns_road != "":
                    print(wanted_road.owns_road + " is already on that space!!")
                    continue
                else:
                    wanted_road.owns_road = a_player.p_color
                    print(a_player.p_name + " has placed a road!!")

                    a_player.road_chains.append([wanted_road.id])
                    val = merge_chain(a_player)
                    if val:
                        val = merge_chain(a_player)
                    does_split_road(a_player, wanted_road)
                    if does_road_branch(a_player, wanted_road):
                        print("You idiot branch here")

                    placed = True

            else:
                print("Your road must be connected to one of your settlements")

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
                    print("That's not a valid road segment... Try again.")
                    return
                elif wanted_road.owns_road != "":
                    print(wanted_road.owns_road + " is already on that space!!")
                    return
                else:
                    wanted_road.owns_road = a_player.p_color
                    print(a_player.p_name + " has placed a road!!")
                    a_player.p_hand.remove("B")
                    a_player.p_hand.remove("L")
                    placed = True
                    a_player.road_chains.append([wanted_road.id])
                    val = merge_chain(a_player)
                    if val:
                        val = merge_chain(a_player)
                    does_split_road(a_player, wanted_road)

                    branch_this_road = does_road_branch(a_player, wanted_road)
                    if branch_this_road != None:
                        print("You idiot branch here")

            else:
                print("Your road must be connected to one of your settlements or roads")
        else:
            print("Not enough resources to build a road!!")
            return


# partially implemented
# the intial setup will probably not work with this function.
# is build settlement only getting a copy of the list? maybe return node_list, and replace the global one in main file?
def build_settlement(a_player, initializing = False):

    if initializing:
        settled = False
        while not settled:
            try:
                adj_player = False
                n1 = input("Where do you want to place your settlement?\n> ") #1,6 for example
                n1 = n1.split(",")
                n1 = [ int(x) for x in n1]
                n1 = tuple(n1)
                if not is_valid_location(n1):
                    continue

                wanted_node = get_node_by_alias(n1)

                # my wanted node is really the node in the global "node_list". Maybe I should get it's index?
                i = config.node_list.index(wanted_node)

                if config.node_list[i].owns_node != "":
                    print(wanted_node.owns_node + " is already on that space!!")
                    continue
                for n in config.node_list[i].adj_nodes: #list of id's
                    neighbor = get_node_by_id(n)
                    neighbor_i = config.node_list.index(neighbor)
                    #print(neighbor_i)
                    #print(config.node_list[neighbor_i])
                    #print(config.node_list[neighbor_i].owns_node)
                    if config.node_list[neighbor_i].owns_node != "":
                        print("There's a player on an adjacent space!!")
                        adj_player = True
                if not adj_player:
                    config.node_list[i].owns_node = a_player.p_color
                    print(a_player.p_name + " has placed a settlement!!")
                    a_player.p_victory_pts += 1
                    #Assign player to the port if needed
                    for port in config.port_list:
                        for node in port.location:
                            if node.id == wanted_node.id:
                                port.player_on = a_player.p_color
                    settled = True

            except ValueError:
                print("The correct format is tile,corner")
                print("EXAMPLE: 1,2")



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
            for port in config.port_list:
                for node in port.location:
                    if node.id == wanted_node.id:
                        port.player_on = a_player.p_color

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
                for p in config.player_list:
                    if n.owns_node == p.p_color:
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
