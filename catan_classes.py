#
#FILE PURPOSE:
#  1. This file contains all class definitions and functions that instantiate one of
#  the created classes.

#BUG SECTION:
#  1. showing a tile needs to have a point at the top, not an edge
# */

#/* Requirements and Exports */

# need to give players an id, use first letter of not conflicting colors (NOT BLWSO)
# Red, Yellow, Purple, Green, Cyan, Tan
class Player:
    def __init__(self, name, color):
        self.p_name = name
        self.p_hand = [] # should be a list of characters
        self.p_color = color # Red, Yellow, Purple, Green, Cyan, Tan
        self.p_victory_pts = 0
        self.p_dev_cards = []

    def present(self):
        print(self.p_name)

    def show_hand(self):
        if len(self.p_hand) == 0:
            print("You have no cards")
        else:
            print(''.join(self.p_hand))

    def show_dev_cards(self):
        if len(self.p_dev_cards) == 0:
            print("You have no development cards")
        else:
            counter = 1
            for i in self.p_dev_cards:
                print("\t" + str(counter) + i) # idk if i is gonna work like That
                counter += 1

    #def add_card(self, new_card):
    #    self.p_hand += new_card

    #returns how many victory points a player has
    def show_victory_pts(self):
        return self.p_victory_pts

    def calculate_victory_pts(self):
        pass # needs to be implemented
#Partial implementation

class Board:
    def __init__(self):
        self.tiles = [] #Is a list of tiles

class Tile:

    def __init__(self, resource, number, id):
        self.resource = resource
        self.number = number
        self.id = id

class Robber:

    def __init__(self, first_tile):
        self.on_tile = first_tile

    def is_on_tile(self, tile_num):
        if self.on_tile == tile_num:
            return "!"
        else:
            return " "

class Node:
    def __init__(self, id): # Just gonna have every node have an id.
        self.id = id
        self.owns_node = "" # color of player with a settlement or city on this node
        self.alias = [] # this is a list of tuples, where the first vvalue is the tile it's on, and the second is the corner that it is.
        self.can_place = False # basically, this is only true in limited circumstances
        self.adj_nodes = [] # list of id's for connected nodes

    def is_empty(self):
        if self.owns_node == "":
            return True
        else:
            return False

    def add_adj(self, id):
        self.adj_nodes.append(id)

    def status(self):
        if self.owns_node == "":
            return "."
        else:
            return self.owns_node

    def is_settlement(self):
        if self.owns_node.islower():
            return True
        else:
            return False

    def is_city(self):
        if self.owns_node.isupper():
            return True
        else:
            return False

    def connected_roads(self):
        roads = [] # a list of connected roads.
        for adj in self.adj_nodes:
            roads.append(get_road_with_nodes(self.id, adj))
        return roads

    def __str__(self):
        return "Node: " + str(self.id)


class Dev_Card:
    def __init__(self, card_type):
        self.card_type = card_type            # options are Knight (14), Road Building(2), Year of Plenty(2), Monopoly(2), Victory Point (5)

    def __str__(self):
        return self.card_type

class Road:
    def __init__(self, start_n, end_n):
        self.owns_road = ""
        self.start_n = start_n # id of starting node
        self.end_n = end_n # id of ending node

    def is_owned(self):
        if self.owns_node == "":
            return False
        else:
            return True

    def __str__(self):
        return "Road: " + str(str(self.start_n) + " " +  str(self.end_n))
