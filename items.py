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

# need globally accessible list of nodes
# need globally accessible list of roads
#node_list = catan_classes.init_nodes() # this doesnt work?
#road_list = catan_classes.create_roads(node_list) # this doesnt work?

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
    for r in config.road_list:
        if r.start_n == node1.id and r.end_n == node2.id:
            return r
        else:
            if r.start_n == node2.id and r.end_n == node1.id:
                return r
    print("COULDN'T FIND ROAD")

# player.id this will have to be added to player. it's their icon on the map
def road_is_connected(player_color, n1, n2):
    if n1.owns_node.lower() == player_color: # lower makes sure that a city counts too.
        return True
    else:
        for adj in n1.adj_nodes:
            if get_road_by_nodes(n1,n2).owns_road == player_color:
                return True
        return False

# maybe have is_init set to False by default (a keyword argument)
def build_road(a_player, initializing = False):

    if initializing:
        placed = False
        while not placed:
            n1 = input("Where do you want to start your road?")#1,6 for example
            n1 = n1.split(",")
            n1 = [ int(x) for x in n1]
            n1 = tuple(n1)

            n1 = get_node_by_alias(n1)


            n2 = input("Where do you want to end your road?") #1,6 for example
            n2 = n2.split(",")
            n2 = [ int(x) for x in n2]
            n2 = tuple(n2)
            n2 = get_node_by_alias(n2)

            if n1.owns_node == a_player.p_color or n2.owns_node == a_player.p_color:

                wanted_road = get_road_with_nodes(n1, n2)
                if wanted_road.owns_road != "":
                    print(wanted_road.owns_road + " is already on that space!!")
                    continue
                else:
                    wanted_road.owns_road = a_player.p_color
                    print(a_player.p_name + " has placed a road!!")
                    placed = True

            else:
                print("Your road must be connected to one of your settlements")

    else:
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
# is build settlement only getting a copy of the list? maybe return node_list, and replace the global one in main file?
def build_settlement(a_player, initializing = False):

    if initializing:
        settled = False
        while not settled:
            adj_player = False
            n1 = input("Where do you want to place your settlement?") #1,6 for example
            n1 = n1.split(",")
            n1 = [ int(x) for x in n1]
            n1 = tuple(n1)

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
                settled = True



    else:
        have_resources = has_needed_resources("settlement", a_player)
        if have_resources:
            # check if that settlement is open
            n1 = input("Where do you want to place your settlement?") #1,6 for example
            n1 = n1.split(",")
            n1 = tuple(n1)
            wanted_node = get_node_by_alias(n1)

            if wanted_node.owns_node != "":
                print(wanted_node.owns_node + " is already on that space!!")
                return #this is a NoneType

            for n in wanted_node.adj_nodes:
                if n.owns_node != "":
                    print("There's a player on an adjacent space!!")
                    return #this is a NoneType

            wanted_node.owns_node = a_player.color
            print(a_player.p_name + "has placed down a road!")
            a_player.p_hand.remove("B")
            a_player.p_hand.remove("L")
            a_player.p_hand.remove("S")
            a_player.p_hand.remove("W")

        else:
            print("Not enough resources to build a settlement!!")

# partially implemented
def build_city(a_player):
    have_resources = has_needed_resources("city", a_player)
    if have_resources:
        print("building a city")
        # check that a player has a settlement at that location
        n1 = input("Where do you want to place your city?") #1,6 for example
        n1 = n1.split(",")
        n1 = tuple(n1)
        wanted_node = get_node_by_alias(n1)

        # needs to specifically be a lower case letter.
        if wanted_node.owns_node == a_player.color:
            print("building a city")
            print(a_player.p_name + "has placed down a city!")
            wanted_node.owns_node = a_player.color.upper()
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("O")
            a_player.p_hand.remove("W")
            a_player.p_hand.remove("W")

        elif wanted_node.owns_node == a_player.color.upper():
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

        print("here's a dev card")
        print(a_player.p_name + " bought a development card!")
        a_player.p_hand.remove("O")
        a_player.p_hand.remove("S")
        a_player.p_hand.remove("W")
        # give player a dev card... I need to have dev cards (and shuffled)

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

    elif item == "settlement":
        # Check that they have 1 sheep, wheat, brick, and lumber
        hand = a_player.p_hand
        if (hand.count("S") > 0 and hand.count("L") > 0 and hand.count("W") > 0 and hand.count("B") > 0):
            return True
        else:
            return False

    elif item == "city":
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



# Need  a function for distributing resources
def give_resources(roll_num, a_board, game_players):
    for t in a_board.tiles:
        if t.number == roll_num:
            if t.has_robber:
                print("The robber stole your " + t.resource + "!!")
            else:
                # Check every node for a player
                corners = []
                corners.append(get_node_by_alias((t.id, 1)))
                corners.append(get_node_by_alias((t.id, 2)))
                corners.append(get_node_by_alias((t.id, 3)))
                corners.append(get_node_by_alias((t.id, 4)))
                corners.append(get_node_by_alias((t.id, 5)))
                corners.append(get_node_by_alias((t.id, 6)))

                for n in corners:
                    if not n.is_empty:
                        if n.is_settlement:
                            # need game_players to be accessible
                            # go through players to find out who has
                            for p in game_players:
                                if n.owns_node == p.color:
                                    p.p_hand.append(t.resource)
                                    print(p.p_name + " got a " + t.resource)
                        else:
                            p.p_hand.append(t.resource)
                            p.p_hand.append(t.resource)
                            print(p.p_name + " got 2 " + t.resource)


                # if it's a settlement, give that player 1 of t.resource
                # if it's a city, give that player 2 of t.resource
